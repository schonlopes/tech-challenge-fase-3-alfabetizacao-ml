"""Validation-only diagnostics of a frozen fitted model; no refit or test access."""
from pathlib import Path
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
    path = ROOT / 'data/raw/alunos_gold_modelagem.parquet'
    verify_snapshot(path, ROOT / 'reports/evidence/snapshot_manifest.json')
    frozen = joblib.load(ROOT / 'models/risk_v1.joblib')
    data = prepare(pd.read_parquet(path))
    validation = data[data.split.eq('validation')]
    estimator = frozen['model']
    probability = estimator.predict_proba(validation[FEATURES])[:,1]
    importance = validation_importance(estimator, validation[FEATURES], validation.risco)
    importance.to_csv(ROOT / 'reports/v1/validation_importance.csv', index=False)
    importance_figure(importance, ROOT / 'images/v1/validation_importance.png')
    options = capacity_options(validation.risco, probability)
    options.to_csv(ROOT / 'reports/v1/validation_capacity_options.csv', index=False)
    print(options[['maximum_alert_fraction','threshold','alert_rate','precision','recall']].to_string(index=False))


if __name__ == '__main__':
    main()
