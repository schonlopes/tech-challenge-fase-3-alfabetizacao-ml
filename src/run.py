"""Execute the first reproducible retrospective experiment: python -m src.run."""
from __future__ import annotations
import argparse
import hashlib
import importlib.metadata
import json
import platform
from datetime import datetime, timezone
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.inspection import permutation_importance
from sklearn.model_selection import GroupKFold, RandomizedSearchCV
from src.evaluation.metrics import choose_threshold, evaluate, grouped_bootstrap, subgroup_metrics
from src.modeling.pipelines import candidates
from src.preprocessing.dataset import FEATURES, prepare
from src.visualization.figures import eda_figures, evaluation_figures

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=Path, default=ROOT / 'data/raw/alunos_gold_modelagem.parquet')
    parser.add_argument('--seed', type=int, default=42)
    parser.add_argument('--search-iterations', type=int, default=4)
    args = parser.parse_args()
    if args.search_iterations < 1:
        raise ValueError('search-iterations deve ser positivo.')
    if not args.data.exists():
        raise FileNotFoundError('Snapshot real não encontrado. Execute scripts/extract_gcp.py primeiro.')
    source = pd.read_parquet(args.data)
    data = prepare(source)
    report = ROOT / 'reports' / 'v1'
    images = ROOT / 'images' / 'v1'
    models = ROOT / 'models'
    for path in (report, images, models):
        path.mkdir(parents=True, exist_ok=True)
    split_summary = data.groupby('split').agg(rows=('risco', 'size'),
        municipalities=('id_municipio', 'nunique'), risk_prevalence=('risco', 'mean'))
    split_summary.to_csv(report / 'split_summary.csv')
    data.isna().mean().rename('fraction_missing').to_csv(report / 'missingness.csv')
    data[['risco', 'taxa_municipal_anterior', 'log_populacao_anterior']].corr().to_csv(report / 'correlations.csv')
    data.groupby('sigla_uf').agg(rows=('risco','size'), risk=('risco','mean')).to_csv(report / 'eda_uf.csv')
    eda_figures(data, images)
    train = data[data.split.eq('train')]
    validation = data[data.split.eq('validation')]
    test = data[data.split.eq('test')]
    if train.id_municipio.nunique() < 3:
        raise ValueError('GroupKFold requer ao menos três municípios no treino.')
    X_train, y_train = train[FEATURES], train.risco
    X_val, y_val = validation[FEATURES], validation.risco
    fitted, rows, searches = {}, [], {}
    for name, (estimator, space) in candidates(args.seed).items():
        print('Treinando:', name, flush=True)
        if space:
            search = RandomizedSearchCV(estimator, space, n_iter=args.search_iterations,
                scoring='average_precision', cv=GroupKFold(n_splits=3), n_jobs=1,
                random_state=args.seed, error_score='raise', refit=True)
            search.fit(X_train, y_train, groups=train.id_municipio)
            estimator = search.best_estimator_
            searches[name] = {'best_params': search.best_params_, 'cv_average_precision': float(search.best_score_)}
            pd.DataFrame(search.cv_results_).drop(columns=['params']).to_csv(report / (name + '_cv.csv'), index=False)
        else:
            estimator.fit(X_train, y_train)
        fitted[name] = estimator
        probability = estimator.predict_proba(X_val)[:, 1]
        threshold = choose_threshold(y_val, probability)
        metrics = evaluate(y_val, probability, threshold)
        rows.append({'model': name, **{k:v for k,v in metrics.items() if k != 'confusion_matrix'}})
    comparison = pd.DataFrame(rows).sort_values('average_precision', ascending=False, kind='stable')
    comparison.to_csv(report / 'validation_comparison.csv', index=False)
    winner_name = str(comparison.iloc[0]['model'])
    winner = fitted[winner_name]
    threshold = float(comparison.iloc[0]['threshold'])
    # Selection ends here. Test is now evaluated for the selected model and dummy reference only.
    probabilities = winner.predict_proba(test[FEATURES])[:, 1]
    test_metrics = evaluate(test.risco, probabilities, threshold)
    baseline_threshold = float(comparison.loc[comparison.model.eq('dummy'), 'threshold'].iloc[0])
    baseline = evaluate(test.risco, fitted['dummy'].predict_proba(test[FEATURES])[:, 1], baseline_threshold)
    uncertainty = grouped_bootstrap(test.risco, probabilities, test.id_municipio, args.seed)
    permutation = permutation_importance(winner, X_val, y_val, scoring='average_precision',
        n_repeats=5, random_state=args.seed, n_jobs=1, max_samples=min(5000, len(validation)))
    importance = pd.DataFrame({'feature': FEATURES, 'importance': permutation.importances_mean,
                               'std': permutation.importances_std})
    importance.to_csv(report / 'validation_importance.csv', index=False)
    subgroup_metrics(test, probabilities, threshold).to_csv(report / 'test_subgroups_uf.csv', index=False)
    municipality = test.assign(probability=probabilities).groupby(
        ['id_municipio', 'nome_municipio', 'sigla_uf'], dropna=False).agg(
            sampled_students=('risco','size'), observed_risk=('risco','mean'), predicted_risk=('probability','mean'))
    municipality[municipality.sampled_students.ge(30)].sort_values('predicted_risk', ascending=False).to_csv(
        report / 'test_municipalities_min30.csv')
    evaluation_figures(test.risco, probabilities, threshold, comparison, importance, images)
    joblib.dump({'model':winner, 'threshold':threshold, 'features':FEATURES,
                 'positive_class':'nao_alfabetizado', 'protocol':'v1'}, models / 'risk_v1.joblib')
    metadata = {
        'finished_at_utc':datetime.now(timezone.utc).isoformat(), 'seed':args.seed,
        'snapshot_sha256':hashlib.sha256(args.data.read_bytes()).hexdigest(),
        'winner':winner_name, 'selection':'validation average_precision; F2 threshold',
        'test':test_metrics, 'dummy_test':baseline, 'test_uncertainty':uncertainty,
        'search':searches, 'features':FEATURES, 'positive_class':'nao_alfabetizado',
        'validation_protocol':'2024 municipality holdout; not an out-of-time test',
        'python':platform.python_version(),
        'packages':{p:importlib.metadata.version(p) for p in ['numpy','pandas','scikit-learn','matplotlib','pyarrow']},
    }
    (report / 'experiment.json').write_text(json.dumps(metadata, indent=2), encoding='utf-8')
    (report / 'RESULTADOS.md').write_text(
        '# Primeiro experimento retrospectivo\n\n'
        f'Modelo selecionado na validação: **{winner_name}**.\n\n'
        f'No teste territorial: AP {test_metrics["average_precision"]:.4f}, '
        f'ROC-AUC {test_metrics["roc_auc"]:.4f}, recall {test_metrics["recall"]:.4f}, '
        f'precisão {test_metrics["precision"]:.4f}.\n\n'
        f'Prevalência de risco: {test_metrics["risk_prevalence"]:.4f}. '
        f'Fração de alunos sinalizada: {test_metrics["alert_rate"]:.4f}.\n\n'
        'O alto recall deve ser lido junto à precisão e à quantidade de alertas. '
        'Este resultado não comprova previsão de anos futuros nem efeito causal das variáveis. '
        'Os dados municipais são não ponderados, restritos à amostra e não equivalem ao indicador oficial. '
        'O modelo ainda depende de verificação da disponibilidade temporal dos dados históricos.\n', encoding='utf-8')
    print(json.dumps(metadata, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
