"""Socioeconomic development experiment: validation only; excludes v1 test municipalities."""
import argparse
import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone
import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GroupKFold, RandomizedSearchCV
from sklearn.pipeline import Pipeline
from src.modeling.pipelines import preprocessing, HistoricalRateBaseline
from src.preprocessing.enrichment import development_data, read_territorial, ENRICHED_NUMERIC, ENRICHED_FEATURES
from src.preprocessing.dataset import FEATURES
from src.evaluation.interpretation import validation_importance
from src.evaluation.metrics import evaluate
from scripts.analyze_validation import capacity_options
from src.visualization.figures import importance_figure, plt, save
from src.run import verify_snapshot

ROOT = Path(__file__).resolve().parents[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--search-iterations', type=int, default=4)
    args = parser.parse_args()
    if args.search_iterations < 1:
        raise ValueError('Número de tentativas deve ser positivo.')
    snapshot = ROOT / 'data/raw/alunos_gold_modelagem.parquet'
    verify_snapshot(snapshot, ROOT / 'reports/evidence/snapshot_manifest.json')
    socioeconomic = read_territorial(ROOT, 'socioeconomic')
    data = development_data(pd.read_parquet(snapshot), socioeconomic)
    train, val = data[data.split.eq('train')], data[data.split.eq('validation')]
    reports = ROOT / 'reports/v2'
    images = ROOT / 'images/v2'
    for path in [reports, images, ROOT/'models', ROOT/'data/processed']:
        path.mkdir(parents=True, exist_ok=True)
    local = ROOT / 'data/processed/development_v2.parquet'
    data.to_parquet(local, index=False)
    (reports/'development_manifest.json').write_text(json.dumps({
        'rows':len(data), 'municipalities':int(data.id_municipio.nunique()),
        'sha256':hashlib.sha256(local.read_bytes()).hexdigest(),
        'v1_test_municipalities_excluded':True, 'features':ENRICHED_FEATURES,
    }, indent=2), encoding='utf-8')
    train[ENRICHED_FEATURES].isna().mean().to_csv(reports/'missingness_train.csv', header=['fraction_missing'])
    frozen = joblib.load(ROOT/'models/risk_v1.joblib')['model']
    options = {
        'historical_rate':(HistoricalRateBaseline().fit(train[FEATURES], train.risco),None,FEATURES),
        'frozen_v1_logistic':(frozen,None,FEATURES),
        'enriched_logistic':(Pipeline([('prepare',preprocessing(ENRICHED_NUMERIC)),
            ('model',LogisticRegression(max_iter=2000,random_state=42))]),
            {'model__C':[0.01,0.1,1.0,10.0]},ENRICHED_FEATURES),
        'enriched_random_forest':(Pipeline([('prepare',preprocessing(ENRICHED_NUMERIC)),
            ('model',RandomForestClassifier(n_estimators=150,n_jobs=1,random_state=42))]),
            {'model__max_depth':[5,10,None], 'model__min_samples_leaf':[30,100,300],
             'model__max_features':['sqrt',1.0]},ENRICHED_FEATURES),
    }
    fitted, comparisons, search_info = {}, [], {}
    for name,(model,space,features) in options.items():
        print('Validação v2:', name, flush=True)
        if space:
            search = RandomizedSearchCV(model,space,n_iter=args.search_iterations,
                scoring='average_precision',cv=GroupKFold(n_splits=3),random_state=42,n_jobs=1,error_score='raise')
            search.fit(train[features],train.risco,groups=train.id_municipio)
            model = search.best_estimator_
            search_info[name] = {'best_params':search.best_params_, 'cv_ap':float(search.best_score_)}
            pd.DataFrame(search.cv_results_).drop(columns='params').to_csv(reports/f'{name}_cv.csv',index=False)
        probability = model.predict_proba(val[features])[:,1]
        capacity = capacity_options(val.risco,probability)
        op = capacity[capacity.maximum_alert_fraction.eq(0.2)].iloc[0]
        metrics = evaluate(val.risco,probability,float(op.threshold))
        comparisons.append({'model':name, **{k:v for k,v in metrics.items() if k!='confusion_matrix'}})
        capacity.assign(model=name).to_csv(reports/f'{name}_capacity.csv',index=False)
        fitted[name] = (model,features)
    comparison = pd.DataFrame(comparisons).sort_values('average_precision',ascending=False,kind='stable')
    comparison.to_csv(reports/'validation_comparison.csv',index=False)
    name = comparison.iloc[0].model
    model, features = fitted[name]
    importance = validation_importance(model,val[features],val.risco)
    importance.to_csv(reports/'validation_importance.csv',index=False)
    importance_figure(importance, images/'validation_importance.png')
    fig,ax = plt.subplots(figsize=(8,4))
    comparison.set_index('model').average_precision.plot.barh(ax=ax,color='#0D5E7D')
    ax.set(title='v2: comparação exploratória na validação',xlabel='Average precision',ylabel='')
    save(fig,images/'validation_comparison.png')
    threshold = float(comparison.iloc[0].threshold)
    joblib.dump({'model':model,'features':features,'threshold':threshold,
        'positive_class':'nao_alfabetizado','protocol':'v2_validation_only'},ROOT/'models/risk_v2.joblib')
    result = {'completed_at_utc':datetime.now(timezone.utc).isoformat(),
        'evaluation':'validation only; no new independent test result',
        'v1_test_municipalities_excluded':True,'winner_validation':name,
        'threshold_policy':'Illustrative maximum 20% alerts in validation; ties preserved',
        'train_rows':len(train),'validation_rows':len(val),'selected_validation':comparison.iloc[0].to_dict(),
        'search':search_info,'features':features,
        'social_reference_year':2010,'economic_reference_year':2021,
        'individual_snapshot_sha256':hashlib.sha256(snapshot.read_bytes()).hexdigest(),
        'socioeconomic_sha256':hashlib.sha256((ROOT/'data/raw/socioeconomic.parquet').read_bytes()).hexdigest()}
    (reports/'experiment.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
