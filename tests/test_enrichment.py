import hashlib
import json
import numpy as np
import pandas as pd
import pytest
from src.preprocessing.enrichment import numeric_social, development_data, read_territorial
from src.preprocessing.dataset import split_for_municipality
from src.evaluation.territorial import scenarios, check_official_municipal, persistence_backtest
from test_experiment import fixture_data


def context():
    ids = fixture_data().id_municipio.unique()
    return pd.DataFrame({'id_municipio':ids,'ano_social':2010,'ano_pib':2021,
        'idhm_renda':0.6,'indice_gini':0.5,'ivs_renda_trabalho':0.4,
        'proporcao_vulneravel':40.,'proporcao_sem_agua_esgoto':10.,
        'proporcao_responsavel_fundamental_incompleto':30.,
        'pib':100000.,'fracao_va_administracao':0.3,'fracao_va_industria':0.2,'populacao_2022':1000})


def test_context_rejects_duplicate_join_keys():
    data = context()
    with pytest.raises(ValueError,match='duplicada'):
        numeric_social(pd.concat([data,data.iloc[:1]]))


def test_context_rejects_unexpected_reference_year():
    data = context(); data.loc[0,'ano_social']=2024
    with pytest.raises(ValueError,match='Ano'):
        numeric_social(data)


def test_out_of_range_accounting_ratios_remain_auditable_and_are_not_clipped():
    data = context()
    data.loc[0,'fracao_va_administracao']=-0.25
    data.loc[0,'fracao_va_industria']=2.1
    cleaned = numeric_social(data)
    assert pd.isna(cleaned.loc[0,'fracao_va_administracao'])
    assert pd.isna(cleaned.loc[0,'fracao_va_industria'])
    assert cleaned.loc[0,'fracao_va_industria_original']==2.1
    assert cleaned.loc[0,'fracao_va_industria_indisponivel']


def test_v2_development_excludes_every_v1_test_municipality():
    data = development_data(fixture_data(),context())
    assert not data.id_municipio.map(split_for_municipality).eq('test').any()
    assert set(data.split)=={'train','validation'}
    assert data.row_id.is_unique


def test_territorial_manifest_rejects_tampering(tmp_path):
    (tmp_path/'reports/evidence').mkdir(parents=True)
    (tmp_path/'data/raw').mkdir(parents=True)
    path = tmp_path/'data/raw/public.parquet'
    context().to_parquet(path,index=False)
    item = {'snapshot':'data\\raw\\public.parquet','rows':100,
            'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    (tmp_path/'reports/evidence/territorial_manifest.json').write_text(json.dumps({'socioeconomic':item}))
    assert len(read_territorial(tmp_path,'socioeconomic'))==100
    path.write_bytes(path.read_bytes()+b'altered')
    with pytest.raises(ValueError,match='alterado'):
        read_territorial(tmp_path,'socioeconomic')


def gold():
    return pd.DataFrame({'ano':[2023,2024,2023,2024], 'id_municipio':['1000001','1000001','1000002','1000002'],
        'rede':['3']*4,'serie':['2']*4,'taxa_alfabetizacao':[50.,60.,40.,30.],
        'meta_2024':[55.,55.,np.nan,np.nan],'meta_2025':[65.]*4,'meta_2030':[80.,80.,np.nan,np.nan]})


def test_missing_goals_are_not_treated_as_achieved():
    result = scenarios(gold()).set_index('id_municipio')
    assert pd.isna(result.loc['1000002','abaixo_meta_persistencia_2030'])
    assert result.loc['1000001','abaixo_meta_persistencia_2030']==1
    assert result.loc['1000001','ganho_anual_necessario_2030_pp']==pytest.approx(20/6)
    assert result.loc['1000001','cenario_ganho_constante_2030']==100
    assert result.loc['1000002','cenario_ganho_constante_2030']==0


def test_network_join_without_matching_targets_fails():
    data = gold(); data['meta_2030']=np.nan
    with pytest.raises(ValueError,match='códigos de rede'):
        check_official_municipal(data)


def test_duplicate_gold_keys_fail_before_aggregation():
    with pytest.raises(ValueError,match='duplicada'):
        scenarios(pd.concat([gold(),gold().iloc[:1]]))


def test_persistence_is_fixed_and_excludes_missing_targets():
    result = persistence_backtest(scenarios(gold()))
    assert result['municipalities']==1
    assert result['mae_pp']==10
    assert result['rmse_pp']==10
    assert result['confusion_matrix']==[[0,1],[0,0]]
    assert result['does_not_validate_2030_scenarios']
