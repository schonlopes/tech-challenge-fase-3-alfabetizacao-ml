"""Municipal scenarios: descriptive aggregates, never individual ML targets or forecasts."""
import numpy as np
import pandas as pd


def check_official_municipal(frame):
    key = ['ano','id_municipio','rede','serie']
    if frame[key].isna().any().any() or frame.duplicated(key).any():
        raise ValueError('Chave municipal/ano/rede/série duplicada ou nula.')
    result = frame.copy()
    for name in ['ano','taxa_alfabetizacao','meta_2024','meta_2025','meta_2030']:
        result[name] = pd.to_numeric(result[name],errors='raise')
    for name in ['taxa_alfabetizacao','meta_2024','meta_2025','meta_2030']:
        if not result[name].dropna().between(0,100).all():
            raise ValueError('Indicador fora de 0 a 100: '+name)
    municipal = result[result.rede.eq('3')]
    if len(municipal) and not municipal.meta_2030.notna().any():
        raise ValueError('Nenhuma meta municipal associada; verificar códigos de rede.')
    return result


def scenarios(gold):
    source = check_official_municipal(gold)
    source = source[source.rede.eq('3') & source.serie.eq('2')]
    past = source[source.ano.eq(2023)][['id_municipio','taxa_alfabetizacao']].rename(
        columns={'taxa_alfabetizacao':'resultado_2023'})
    current = source[source.ano.eq(2024)].merge(past,on='id_municipio',how='left',validate='one_to_one')
    current = current.rename(columns={'taxa_alfabetizacao':'resultado_2024'})
    current['ganho_2023_2024_pp'] = current.resultado_2024-current.resultado_2023
    current['gap_meta_2024_pp'] = current.resultado_2024-current.meta_2024
    for year in [2025,2030]:
        horizon = year-2024
        current[f'cenario_persistencia_{year}'] = current.resultado_2024
        current[f'cenario_ganho_constante_{year}'] = (
            current.resultado_2024+horizon*current.ganho_2023_2024_pp).clip(0,100)
        current[f'ganho_anual_necessario_{year}_pp'] = (
            (current[f'meta_{year}']-current.resultado_2024)/horizon).clip(lower=0)
        valid = current.resultado_2024.notna() & current[f'meta_{year}'].notna()
        current[f'abaixo_meta_persistencia_{year}'] = np.where(valid,
            (current.resultado_2024 < current[f'meta_{year}']).astype(float),np.nan)
    return current
