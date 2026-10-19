"""Artificial software checks, never educational evaluation evidence."""
import json
import subprocess
import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import pytest
from src.demo import artificial_data
from src.experiments import create_run, finish_run, sha256
from src.modeling.pipelines import candidates
from src.predict import score, decision_policy
from src.preprocessing.dataset import FEATURES

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def bundle():
    data = artificial_data()
    train = data[data.split.eq('train')]
    model = candidates()['logistic'][0].fit(train[FEATURES],train.risco)
    return {'model':model,'features':FEATURES,'threshold':0.16,
        'protocol':'v1','positive_class':'nao_alfabetizado'}


def test_score_is_default_and_reload_does_not_change_predictions(bundle,tmp_path):
    frame = artificial_data().iloc[:10].copy()
    frame['private_identifier'] = 'must never be exported'
    frame['risco'] = 999  # extra target ignored, never required
    original,_ = score(frame,bundle)
    joblib.dump(bundle,tmp_path/'trusted.joblib')
    restored,_ = score(frame,joblib.load(tmp_path/'trusted.joblib'))
    pd.testing.assert_frame_equal(original,restored)
    assert list(original)==['input_row','probability_risk']
    with pytest.warns(UserWarning):
        alerts,policy = score(frame,bundle,True)
    assert (alerts.research_alert==(original.probability_risk>=0.16)).all()
    assert policy['name']=='historical_f2'


@pytest.mark.parametrize('problem',['missing','infinity','rate','log_population','nonnumeric','empty'])
def test_invalid_inputs_fail(bundle,problem):
    frame = artificial_data().iloc[:10][FEATURES].copy()
    if problem=='missing': frame = frame.drop(columns='rede')
    elif problem=='infinity': frame.loc[0,'taxa_municipal_anterior']=np.inf
    elif problem=='rate': frame.loc[0,'taxa_municipal_anterior']=101
    elif problem=='log_population': frame.loc[0,'log_populacao_anterior']=-1
    elif problem=='nonnumeric':
        frame['taxa_municipal_anterior']=frame.taxa_municipal_anterior.astype(object)
        frame.loc[0,'taxa_municipal_anterior']='invalid'
    else: frame = frame.iloc[:0]
    with pytest.raises(ValueError): score(frame,bundle)


def test_unseen_categories_and_imputation_do_not_refit(bundle):
    frame = artificial_data().iloc[:10][FEATURES].copy()
    imputer = bundle['model'].named_steps['prepare'].named_transformers_['numeric'].named_steps['imputer']
    before = imputer.statistics_.copy()
    frame['sigla_uf']='NEW'; frame['rede']=np.nan
    assert np.isfinite(score(frame,bundle)[0].probability_risk).all()
    np.testing.assert_array_equal(before,imputer.statistics_)


def test_policy_does_not_confuse_validation_with_independent_test(bundle):
    bundle['protocol']='v2_validation_only'
    assert decision_policy(bundle)['evidence']=='validation_only'
    bundle['protocol']='unknown'
    with pytest.raises(ValueError): score(artificial_data().iloc[:3],bundle)


def test_runs_refuse_reuse_and_record_output_integrity(tmp_path):
    directory = create_run(ROOT,'fixture',tmp_path/'one',inputs={'requirements':ROOT/'requirements-lock.txt'})
    (directory/'reports/result.json').write_text('{}')
    finish_run(directory)
    manifest = json.loads((directory/'run.json').read_text())
    assert manifest['status']=='completed'
    assert manifest['git_commit']
    assert manifest['source_sha256']['src/predict.py']==sha256(ROOT/'src/predict.py')
    assert manifest['outputs_sha256']['reports/result.json']==sha256(directory/'reports/result.json')
    with pytest.raises(FileExistsError): create_run(ROOT,'fixture',directory)


def test_demo_and_prediction_cli_without_cloud(tmp_path):
    demo = tmp_path/'demo'
    subprocess.run([sys.executable,'-m','src.demo','--output-dir',str(demo)],cwd=ROOT,check=True)
    prediction = tmp_path/'prediction'
    subprocess.run([sys.executable,'-m','src.predict','--artifact',str(demo/'models/demo.joblib'),
        '--input',str(demo/'data/new_features.csv'),'--output-dir',str(prediction)],cwd=ROOT,check=True)
    expected = pd.read_csv(demo/'data/predictions.csv')
    actual = pd.read_csv(prediction/'data/predictions.csv')
    np.testing.assert_allclose(expected.probability_risk,actual.probability_risk,atol=1e-14)
    summary = json.loads((demo/'reports/demo.json').read_text())
    assert summary['real_world_metrics'] is False
    assert summary['reload_predictions_identical'] is True
