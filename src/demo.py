"""Account-free, explicitly artificial end-to-end software demonstration."""
import argparse
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from src.experiments import create_run, finish_run
from src.modeling.pipelines import candidates
from src.predict import score
from src.preprocessing.dataset import FEATURES, split_for_municipality

ROOT = Path(__file__).resolve().parents[1]


def artificial_data(seed=42):
    rng = np.random.default_rng(seed)
    municipalities = np.repeat([str(1000000+n) for n in range(100)],8)
    history = np.repeat(rng.uniform(30,90,100),8)
    data = pd.DataFrame({'id_municipio':municipalities,
        'taxa_municipal_anterior':history,
        'log_populacao_anterior':np.log1p(np.repeat(rng.integers(1000,500000,100),8)),
        'rede':'3','serie':'2','sigla_uf':'SP','regiao':'Sudeste',
        'risco':rng.binomial(1,1-history/100),
        'origem':'ARTIFICIAL_SOFTWARE_DEMO_NOT_OFFICIAL_DATA'})
    data['split'] = data.id_municipio.map(split_for_municipality)
    data.loc[data.index%17==0,'taxa_municipal_anterior'] = np.nan
    return data


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output-dir',type=Path)
    parser.add_argument('--seed',type=int,default=42)
    args = parser.parse_args()
    output = create_run(ROOT,'synthetic-demo',args.output_dir,
        parameters={'seed':args.seed,'data_kind':'artificial_software_demo_only'})
    data = artificial_data(args.seed)
    data.to_parquet(output/'data/artificial.parquet',index=False)
    train = data[data.split.eq('train')]
    new_data = data[data.split.eq('test')][FEATURES].copy()
    new_data.loc[new_data.index[0],'sigla_uf'] = 'UF_NOVA'
    estimator = candidates(args.seed)['logistic'][0].set_params(model__C=0.01)
    estimator.fit(train[FEATURES],train.risco)
    artifact = {'model':estimator,'features':FEATURES,'threshold':0.5,
        'protocol':'synthetic_demo','positive_class':'nao_alfabetizado'}
    path = output/'models/demo.joblib'
    joblib.dump(artifact,path)
    new_data.to_csv(output/'data/new_features.csv',index=False)
    expected,_ = score(new_data,artifact)
    actual,policy = score(new_data,joblib.load(path))
    np.testing.assert_allclose(expected.probability_risk,actual.probability_risk,rtol=0,atol=0)
    actual.to_csv(output/'data/predictions.csv',index=False)
    summary = {'data_kind':'artificial_software_demo_only','real_world_metrics':False,
        'train_rows':len(train),'scored_rows':len(actual),'reload_predictions_identical':True,
        'unseen_category_tested':True,'policy':policy}
    (output/'reports/demo.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    finish_run(output)
    print(f'Demonstração ARTIFICIAL concluída: {output}. Não mede desempenho educacional real.')


if __name__=='__main__':
    main()
