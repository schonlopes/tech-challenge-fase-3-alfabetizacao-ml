import pandas as pd
import pytest
from src.preprocessing.dataset import SOURCE, FEATURES, split_for_municipality, validate_dataset


def frame():
    return pd.DataFrame(dict(row_id=['a','b'], ano=[2024]*2, ano_contexto=[2023]*2,
        ano_populacao=[2022]*2, id_municipio=['3550308']*2, populacao_anterior=[1000]*2,
        risco=[0,1], origem=[SOURCE]*2, taxa_municipal_anterior=[50.]*2,
        rede=['Municipal']*2, serie=['2']*2, sigla_uf=['SP']*2, regiao=['Sudeste']*2))


def test_rejects_join_fanout():
    df = frame(); df['row_id'] = 'duplicado'
    with pytest.raises(ValueError, match='duplicado'):
        validate_dataset(df)


def test_rejects_synthetic_sources():
    df = frame(); df.loc[0, 'origem'] = 'pubsub'
    with pytest.raises(ValueError, match='simulada'):
        validate_dataset(df)


def test_rejects_future_context():
    df = frame(); df.loc[0, 'ano_contexto'] = 2024
    with pytest.raises(ValueError, match='futuro'):
        validate_dataset(df)


def test_forbidden_features_never_reach_estimator():
    assert not set(FEATURES) & {'proficiencia','risco','alfabetizado','id_aluno','row_id',
                              'id_municipio','id_escola','presenca','peso_aluno','ano'}


def test_municipality_split_is_repeatable():
    codes = [str(1000000+i) for i in range(200)]
    first = {c: split_for_municipality(c) for c in codes}
    assert first == {c: split_for_municipality(c) for c in reversed(codes)}
    assert set(first.values()) == {'train','validation','test'}
