"""Explicit data contract and municipality-level holdout."""
from __future__ import annotations
import hashlib
import numpy as np
import pandas as pd

SOURCE = 'basedosdados.br_inep_avaliacao_alfabetizacao.alunos'
NUMERIC = ['taxa_municipal_anterior', 'log_populacao_anterior']
CATEGORICAL = ['rede', 'serie', 'sigla_uf', 'regiao']
FEATURES = NUMERIC + CATEGORICAL


def validate_dataset(df: pd.DataFrame) -> None:
    required = set(['row_id', 'ano', 'ano_contexto', 'ano_populacao', 'id_municipio',
                    'populacao_anterior', 'risco', 'origem', 'taxa_municipal_anterior'] + CATEGORICAL)
    missing = required - set(df)
    if missing:
        raise ValueError(f'Colunas obrigatórias ausentes: {sorted(missing)}')
    if df.empty or df.row_id.isna().any() or df.row_id.duplicated().any():
        raise ValueError('Snapshot vazio ou identificador duplicado/nulo; revisar junções.')
    if not df.origem.eq(SOURCE).all():
        raise ValueError('Fonte não oficial ou simulada no snapshot.')
    if not df.ano.eq(2024).all():
        raise ValueError('Protocolo v1 permite somente desfechos de 2024.')
    if not df.risco.isin([0, 1]).all() or df.risco.nunique() < 2:
        raise ValueError('Alvo inválido ou sem as duas classes.')
    if df.id_municipio.isna().any() or not df.id_municipio.astype(str).str.fullmatch(r'\d{7}').all():
        raise ValueError('Município ausente ou inválido.')
    if not (df.ano_contexto.lt(df.ano) & df.ano_populacao.lt(df.ano)).all():
        raise ValueError('Contexto contemporâneo/futuro não permitido.')
    if not df.taxa_municipal_anterior.dropna().between(0, 100).all():
        raise ValueError('Taxa municipal fora de 0 a 100.')
    if not df.populacao_anterior.dropna().ge(0).all():
        raise ValueError('População negativa.')


def prepare(df: pd.DataFrame) -> pd.DataFrame:
    validate_dataset(df)
    result = df.copy()
    result['log_populacao_anterior'] = np.log1p(result.populacao_anterior)
    for name in CATEGORICAL:
        result[name] = result[name].astype(object).where(result[name].notna(), np.nan)
    result['split'] = result.id_municipio.map(split_for_municipality)
    for split in ('train', 'validation', 'test'):
        part = result[result.split.eq(split)]
        if part.risco.nunique() < 2:
            raise ValueError(f'Conjunto {split} insuficiente ou sem as duas classes.')
    return result


def split_for_municipality(code: str) -> str:
    bucket = int(hashlib.sha256(('fase3-v1:' + str(code)).encode()).hexdigest()[:8], 16) % 10
    return 'train' if bucket < 6 else ('validation' if bucket < 8 else 'test')
