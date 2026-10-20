"""Validation-only diagnostics of a frozen fitted model; no refit or test access."""
from pathlib import Path
import argparse
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

import joblib
import numpy as np
import pandas as pd
from src.preprocessing.dataset import FEATURES, prepare
from src.evaluation.interpretation import validation_importance
from src.evaluation.metrics import evaluate
from src.run import verify_snapshot
from src.visualization.figures import importance_figure
from src.experiments import create_run, finish_run


def capacity_options(y, probability):
    """Choose a feasible threshold at each alert budget, keeping tied scores together."""
    records = []
    thresholds = np.r_[np.unique(probability), np.nextafter(float(np.max(probability)), np.inf)]
    for budget in [0.10, 0.20, 0.30]:
        feasible = [t for t in thresholds if np.mean(probability >= t) <= budget]
        threshold = min(feasible)
        records.append({'maximum_alert_fraction':budget, **evaluate(y, probability, threshold)})
    return pd.DataFrame(records).drop(columns='confusion_matrix')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--artifact',type=Path,default=ROOT/'models/risk_v1.joblib')
    parser.add_argument('--output-dir',type=Path)
    args = parser.parse_args()
    path = ROOT / 'data/raw/alunos_gold_modelagem.parquet'
    verify_snapshot(path, ROOT / 'reports/evidence/snapshot_manifest.json')
    frozen = joblib.load(args.artifact)
    data = prepare(pd.read_parquet(path))
    validation = data[data.split.eq('validation')]
    estimator = frozen['model']
    probability = estimator.predict_proba(validation[FEATURES])[:,1]
    importance = validation_importance(estimator, validation[FEATURES], validation.risco)
    output = create_run(ROOT,'validation-diagnostics',args.output_dir,
        inputs={'snapshot':path,'artifact':args.artifact},parameters={'evaluation':'validation_only'})
    importance.to_csv(output / 'reports/validation_importance.csv', index=False)
    importance_figure(importance, output / 'images/validation_importance.png')
    options = capacity_options(validation.risco, probability)
    options.to_csv(output / 'reports/validation_capacity_options.csv', index=False)
    finish_run(output)
    print(f'Diagnóstico preservado em: {output}')
    print(options[['maximum_alert_fraction','threshold','alert_rate','precision','recall']].to_string(index=False))


if __name__ == '__main__':
    main()
