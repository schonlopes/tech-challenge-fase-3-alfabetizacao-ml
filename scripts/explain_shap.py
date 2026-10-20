"""Real validation explanations; exports only global aggregates, no individual rows."""
from pathlib import Path
import hashlib
import json
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

import joblib
import numpy as np
import pandas as pd
import shap
from sklearn.linear_model import LogisticRegression
from src.evaluation.shap_summary import grouped_shap
from src.visualization.figures import plt, save


def main():
    data_path = ROOT/'data/processed/development_v2.parquet'
    manifest = json.loads((ROOT/'reports/v2/development_manifest.json').read_text())
    if hashlib.sha256(data_path.read_bytes()).hexdigest()!=manifest['sha256']:
        raise ValueError('Snapshot de desenvolvimento alterado.')
    data = pd.read_parquet(data_path)
    if data.split.eq('test').any():
        raise ValueError('SHAP v2 não pode incluir o teste v1.')
    artifact = joblib.load(ROOT/'models/risk_v2.joblib')
    pipeline, features = artifact['model'], artifact['features']
    estimator = pipeline.named_steps['model']
    if not isinstance(estimator,LogisticRegression):
        raise ValueError('Esta explicação linear requer o modelo logístico selecionado.')
    train = data[data.split.eq('train')]
    validation = data[data.split.eq('validation')]
    background = train.sample(n=min(200,len(train)),random_state=42)[features]
    explain = validation.sample(n=min(500,len(validation)),random_state=42)[features]
    preprocessing = pipeline.named_steps['prepare']
    X_background = preprocessing.transform(background)
    X_explain = preprocessing.transform(explain)
    explainer = shap.LinearExplainer(estimator,shap.maskers.Independent(X_background,max_samples=200))
    explanation = explainer(X_explain)
    scores = estimator.decision_function(X_explain)
    reconstructed = np.asarray(explanation.base_values)+np.asarray(explanation.values).sum(axis=1)
    error = float(np.max(np.abs(scores-reconstructed)))
    np.testing.assert_allclose(scores,reconstructed,atol=1e-8)
    summary = grouped_shap(preprocessing.get_feature_names_out(),explanation.values,features)
    summary.to_csv(ROOT/'reports/v2/shap_global.csv',index=False)
    fig,ax = plt.subplots(figsize=(9,4))
    ordered = summary.sort_values('mean_abs_shap_log_odds')
    ax.barh(ordered.feature,ordered.mean_abs_shap_log_odds,color='#0D5E7D')
    ax.set(title='SHAP global - modelo selecionado, amostra de validação',
        xlabel='Contribuição absoluta média em log-odds do risco',ylabel='')
    save(fig,ROOT/'images/v2/shap_global.png')
    metadata = {'shap_version':shap.__version__,'explainer':'LinearExplainer / Independent masker',
        'background':'200 training rows, seed 42','validation_rows_explained':len(explain),
        'unit':'log-odds for nao_alfabetizado; not probability percentage points',
        'maximum_additivity_error':error,'test_rows_explained':0,
        'individual_explanations_exported':False,'features':features,
        'limitation':'interventional attribution; correlated features and background choice affect allocation; not causal'}
    (ROOT/'reports/v2/shap_metadata.json').write_text(json.dumps(metadata,indent=2),encoding='utf-8')
    print(json.dumps(metadata,indent=2))


if __name__=='__main__':
    main()
