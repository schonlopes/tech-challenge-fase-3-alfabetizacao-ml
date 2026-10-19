"""Software integration only: artificial fixture, never a real-world model benchmark."""
import json
import hashlib
import sys
import numpy as np
import pandas as pd
import pytest
from src import run
from src.preprocessing.dataset import SOURCE, prepare


def fixture_data():
    rng = np.random.default_rng(7)
    municipalities = np.repeat([str(1000000 + n) for n in range(100)], 8)
    count = len(municipalities)
    history = np.repeat(rng.uniform(35, 90, size=100), 8)
    return pd.DataFrame({
        'row_id':[f'test-only-{n}' for n in range(count)],
        'ano':2024, 'ano_contexto':2023, 'ano_populacao':2022,
        'id_municipio':municipalities, 'taxa_municipal_anterior':history,
        'populacao_anterior':np.repeat(rng.integers(1000, 500000, size=100), 8),
        'risco':np.tile([0,1,0,1,0,1,0,1], 100),
        # Contract field only. All rows are fabricated in this test, not source evidence.
        'origem':SOURCE, 'rede':'Municipal', 'serie':'2',
        'sigla_uf':np.repeat(['SP','RJ'], count//2), 'regiao':'Sudeste',
        'nome_municipio':['Fixture']*count,
    })


def test_group_holdout_has_no_municipal_overlap():
    prepared = prepare(fixture_data())
    assert prepared.groupby('id_municipio').split.nunique().eq(1).all()
    assert set(prepared.split) == {'train','validation','test'}


def test_snapshot_integrity_rejects_modified_data(tmp_path):
    path = tmp_path / 'snapshot.parquet'
    manifest = tmp_path / 'manifest.json'
    payload = b'fixture for integrity checking only'
    path.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest()
    manifest.write_text(json.dumps({'snapshot_sha256':digest}), encoding='utf-8')
    assert run.verify_snapshot(path, manifest) == digest
    path.write_bytes(payload + b' modified')
    with pytest.raises(ValueError, match='proveniência'):
        run.verify_snapshot(path, manifest)


def test_end_to_end_outputs_with_artificial_fixture(tmp_path, monkeypatch):
    snapshot = tmp_path / 'fixture.parquet'
    fixture_data().to_parquet(snapshot, index=False)
    monkeypatch.setattr(run, 'ROOT', tmp_path)
    monkeypatch.setattr(sys, 'argv', ['run', '--data', str(snapshot), '--search-iterations', '1'])
    run.main()
    result = json.loads((tmp_path / 'reports/v1/experiment.json').read_text())
    assert result['positive_class'] == 'nao_alfabetizado'
    assert result['test']['rows'] > 0
    assert result['winner'] in {'dummy','historical_rate','logistic','random_forest'}
    assert len(list((tmp_path / 'images/v1').glob('*.png'))) == 8
    assert (tmp_path / 'models/risk_v1.joblib').exists()
