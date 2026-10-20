"""Batch scoring of trusted local artifacts; no refit and no automatic intervention."""
import argparse
import json
from pathlib import Path
import warnings

import joblib
import numpy as np
import pandas as pd
from src.experiments import create_run, finish_run
from src.preprocessing.dataset import CATEGORICAL

ROOT = Path(__file__).resolve().parents[1]


def decision_policy(artifact):
    protocol = artifact.get('protocol')
    if protocol == 'v1':
        return {'name':'historical_f2', 'threshold':float(artifact['threshold']),
            'evidence':'retrospective_2024_municipality_holdout',
            'limitation':'High alert volume; not validated for future cohorts or deployment.'}
    if protocol == 'v2_validation_only':
        return {'name':'exploratory_capacity20', 'threshold':float(artifact['threshold']),
            'evidence':'validation_only',
            'limitation':'Not independently tested. A fixed threshold does not guarantee a 20% cap on new data.'}
    if protocol == 'synthetic_demo':
        return {'name':'synthetic_demo', 'threshold':float(artifact['threshold']),
            'evidence':'artificial_software_demo_only', 'limitation':'No educational performance claim.'}
    raise ValueError('Protocolo do artefato desconhecido; política não pode ser inferida.')


def validate_features(frame, artifact):
    features = artifact['features']
    if not features or len(set(features)) != len(features):
        raise ValueError('Contrato de atributos inválido no artefato.')
    missing = set(features)-set(frame.columns)
    if frame.empty or missing:
        raise ValueError(f'Entrada vazia ou atributos ausentes: {sorted(missing)}')
    data = frame[features].copy()
    for column in features:
        if column in CATEGORICAL:
            # Codes are strings, as in the source snapshot; do not map 3 to "Municipal".
            data[column] = data[column].map(lambda x: str(x) if pd.notna(x) else np.nan).astype(object)
        else:
            data[column] = pd.to_numeric(data[column], errors='raise').astype(float)
            if np.isinf(data[column].to_numpy()).any():
                raise ValueError(f'Valor infinito em {column}.')
    if 'taxa_municipal_anterior' in data and not data.taxa_municipal_anterior.dropna().between(0,100).all():
        raise ValueError('Taxa municipal fora de 0 a 100.')
    if 'log_populacao_anterior' in data and not data.log_populacao_anterior.dropna().ge(0).all():
        raise ValueError('Log da população negativo.')
    return data


def score(frame, artifact, use_artifact_threshold=False):
    if artifact.get('positive_class') != 'nao_alfabetizado':
        raise ValueError('Classe positiva incompatível.')
    data = validate_features(frame, artifact)
    classes = list(artifact['model'].classes_)
    if set(classes) != {0,1}:
        raise ValueError('Modelo não tem as classes binárias esperadas.')
    probabilities = artifact['model'].predict_proba(data)[:,classes.index(1)]
    if not np.isfinite(probabilities).all() or not ((probabilities>=0)&(probabilities<=1)).all():
        raise ValueError('Modelo produziu probabilidades inválidas.')
    policy = decision_policy(artifact)
    # Input ordering is preserved; no pupil identifier or extra input field is exported.
    result = pd.DataFrame({'input_row':np.arange(1,len(data)+1), 'probability_risk':probabilities})
    if use_artifact_threshold:
        warnings.warn('Limiar histórico/experimental: não autoriza decisões automáticas.', UserWarning)
        result['research_alert'] = probabilities >= policy['threshold']
    return result, policy


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--artifact',type=Path,required=True,help='Somente joblib local de origem confiável.')
    parser.add_argument('--input',type=Path,required=True,help='CSV ou Parquet com os atributos já preparados.')
    parser.add_argument('--output-dir',type=Path)
    parser.add_argument('--use-artifact-threshold',action='store_true')
    args = parser.parse_args()
    if args.input.suffix.lower()=='.parquet':
        frame = pd.read_parquet(args.input)
    elif args.input.suffix.lower()=='.csv':
        frame = pd.read_csv(args.input,dtype={c:'string' for c in CATEGORICAL})
    else:
        raise ValueError('Entrada deve ser CSV ou Parquet.')
    # Pickle/joblib can execute code. Never load artifacts downloaded from untrusted sources.
    artifact = joblib.load(args.artifact)
    result, policy = score(frame,artifact,args.use_artifact_threshold)
    output = create_run(ROOT,'prediction',args.output_dir,
        inputs={'artifact':args.artifact,'input':args.input},
        parameters={'mode':'research_alert' if args.use_artifact_threshold else 'scores_only'})
    result.to_csv(output/'data/predictions.csv',index=False)
    (output/'reports/policy.json').write_text(json.dumps(policy,indent=2),encoding='utf-8')
    finish_run(output)
    print(f'Previsões locais: {output}. Nenhuma métrica de desempenho foi calculada.')


if __name__=='__main__':
    main()
