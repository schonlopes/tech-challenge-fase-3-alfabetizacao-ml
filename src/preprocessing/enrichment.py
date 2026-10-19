"""Historical public context joins with strict uniqueness and date validation."""
import json
import hashlib
from pathlib import Path
import numpy as np
import pandas as pd
from src.preprocessing.dataset import NUMERIC, CATEGORICAL, prepare

SOCIAL = ['idhm_renda','indice_gini','ivs_renda_trabalho','proporcao_vulneravel',
          'proporcao_sem_agua_esgoto','proporcao_responsavel_fundamental_incompleto']
ECONOMIC = ['log_pib_2021','fracao_va_administracao','fracao_va_industria']
ENRICHED_NUMERIC = NUMERIC + SOCIAL + ECONOMIC
ENRICHED_FEATURES = ENRICHED_NUMERIC + CATEGORICAL


def read_territorial(root: Path, name: str) -> pd.DataFrame:
    manifest = json.loads((root / 'reports/evidence/territorial_manifest.json').read_text())
    item = manifest[name]
    path = root / item['snapshot']
    # Stored paths from Windows also work when the repo is moved to a POSIX host.
    if not path.exists():
        path = root / item['snapshot'].replace('\\','/')
    if hashlib.sha256(path.read_bytes()).hexdigest() != item['sha256']:
        raise ValueError('Snapshot territorial alterado.')
    frame = pd.read_parquet(path)
    if len(frame) != item['rows']:
        raise ValueError('Contagem territorial difere do manifest.')
    return frame


def numeric_social(frame: pd.DataFrame) -> pd.DataFrame:
    result = frame.copy()
    if result.id_municipio.isna().any() or result.id_municipio.duplicated().any():
        raise ValueError('Chave municipal duplicada/nula no contexto socioeconômico.')
    fields = SOCIAL + ['ano_social','ano_pib','pib','fracao_va_administracao','fracao_va_industria']
    if 'populacao_2022' in result:
        fields += ['populacao_2022']
    for name in fields:
        result[name] = pd.to_numeric(result[name], errors='raise')
    for name in ['idhm_renda','indice_gini','ivs_renda_trabalho']:
        if not result[name].dropna().between(0,1).all():
            raise ValueError(f'Índice ou fração fora do intervalo: {name}')
    # Sector/total accounting ratios may be outside [0,1]. They are not suitable
    # as the intended nonnegative composition features: preserve raw values and
    # mark those derived features unavailable, rather than clipping their values.
    for name in ['fracao_va_administracao','fracao_va_industria']:
        result[name+'_original'] = result[name]
        invalid = result[name].notna() & ~result[name].between(0,1)
        result[name+'_indisponivel'] = invalid
        result[name] = result[name].mask(invalid)
    for name in SOCIAL[3:]:
        if not result[name].dropna().between(0,100).all():
            raise ValueError(f'Proporção inválida: {name}')
    if not result.ano_social.dropna().eq(2010).all() or not result.ano_pib.dropna().eq(2021).all():
        raise ValueError('Ano não previsto no contexto histórico.')
    if not result.pib.dropna().ge(0).all():
        raise ValueError('PIB negativo.')
    result['log_pib_2021'] = np.log1p(result.pib)
    if 'populacao_2022' in result:
        if not result.populacao_2022.dropna().ge(0).all():
            raise ValueError('População negativa.')
        result['log_populacao_2022'] = np.log1p(result.populacao_2022)
    return result


def development_data(students: pd.DataFrame, public_context: pd.DataFrame) -> pd.DataFrame:
    original = prepare(students)
    original = original[original.split.ne('test')].copy()
    context = numeric_social(public_context)
    keep = ['id_municipio'] + SOCIAL + ECONOMIC
    merged = original.merge(context[keep], on='id_municipio', how='left', validate='many_to_one')
    if len(merged) != len(original) or merged.row_id.duplicated().any():
        raise ValueError('Junção alterou a população de desenvolvimento.')
    assert not merged.split.eq('test').any()
    return merged
