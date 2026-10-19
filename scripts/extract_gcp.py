"""Read-only, cost-bounded extraction from phase 2 GCP tables using the logged-in bq CLI."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def query(sql: str, project: str, ceiling: int, name: str) -> list[dict]:
    executable = shutil.which('bq')
    if not executable:
        raise RuntimeError('Instale Google Cloud SDK e autentique o bq.')
    job_id = 'fase3_' + uuid.uuid4().hex
    args = [executable, '--project_id=' + project, '--location=US', '--format=json',
            'query', '--use_legacy_sql=false', '--maximum_bytes_billed=' + str(ceiling),
            '--max_rows=200000', '--job_id=' + job_id]
    result = subprocess.run(args, input=sql, encoding='utf-8', capture_output=True, timeout=300)
    if result.returncode:
        raise RuntimeError(result.stderr + result.stdout)
    rows = json.loads(result.stdout)
    evidence = ROOT / 'reports' / 'evidence'
    evidence.mkdir(parents=True, exist_ok=True)
    metadata = subprocess.run([executable, '--project_id=' + project, '--location=US',
                               '--format=json', 'show', '--job=true', job_id],
                              encoding='utf-8', capture_output=True, timeout=60)
    if metadata.returncode:
        raise RuntimeError('Consulta concluída, mas não foi possível obter metadados: ' + metadata.stderr)
    job = json.loads(metadata.stdout)
    stats = job.get('statistics', {}).get('query', {})
    record = {
        'job_id': job_id, 'project': project, 'location': 'US',
        'captured_at_utc': datetime.now(timezone.utc).isoformat(),
        'query_sha256': hashlib.sha256(sql.encode()).hexdigest(),
        'maximum_bytes_billed': ceiling, 'returned_rows': len(rows),
        'total_bytes_processed': stats.get('totalBytesProcessed'),
        'total_bytes_billed': stats.get('totalBytesBilled'),
        'cache_hit': stats.get('cacheHit'), 'status': job.get('status', {}),
        'referenced_tables': stats.get('referencedTables', []),
    }
    (evidence / (name + '_job.json')).write_text(json.dumps(record, indent=2), encoding='utf-8')
    if len(rows) >= 200000:
        raise RuntimeError('Limite de linhas atingido: extração pode estar truncada; reduza a amostra.')
    return rows


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--project', default='tech-challenge-fase-2-506814')
    parser.add_argument('--sample-percent', type=int, default=5)
    parser.add_argument('--maximum-bytes-billed', type=int, default=2_000_000_000)
    args = parser.parse_args()
    if not re.fullmatch(r'[a-z][a-z0-9-]{4,61}[a-z0-9]', args.project):
        raise ValueError('ID de projeto inválido.')
    if not 1 <= args.sample_percent <= 10:
        raise ValueError('Amostragem local deve estar entre 1% e 10%.')
    evidence = ROOT / 'reports' / 'evidence'
    evidence.mkdir(parents=True, exist_ok=True)
    audit_sql = (ROOT / 'sql/audit_source.sql').read_text(encoding='utf-8').replace('__PROJECT__', args.project)
    audit = query(audit_sql, args.project, args.maximum_bytes_billed, 'source_audit')
    (evidence / 'source_audit.json').write_text(json.dumps(audit, indent=2), encoding='utf-8')
    if any(int(row['divergencias_rotulo']) > 0 for row in audit):
        raise ValueError('Rótulo e proficiência divergentes: revisar antes de treinar.')
    sql = (ROOT / 'sql/extract_training.sql').read_text(encoding='utf-8')
    sql = sql.replace('__PROJECT__', args.project).replace('__PERCENT__', str(args.sample_percent))
    rows = query(sql, args.project, args.maximum_bytes_billed, 'training_extract')
    import pandas as pd
    from src.preprocessing.dataset import validate_dataset
    frame = pd.DataFrame(rows)
    for name in ('ano', 'ano_contexto', 'ano_populacao', 'taxa_municipal_anterior', 'populacao_anterior', 'risco'):
        frame[name] = pd.to_numeric(frame[name], errors='raise')
    validate_dataset(frame)
    out = ROOT / 'data/raw/alunos_gold_modelagem.parquet'
    out.parent.mkdir(parents=True, exist_ok=True)
    frame.to_parquet(out, index=False)
    manifest = {
        'snapshot_sha256': hashlib.sha256(out.read_bytes()).hexdigest(),
        'rows': len(frame), 'municipalities': frame.id_municipio.nunique(),
        'sample_percent': args.sample_percent, 'snapshot': str(out.relative_to(ROOT)),
        'source': 'GCP real: Silver individual + Gold municipal 2023 + IBGE população 2022',
        'gold_extension': 'local; no new cloud table was created',
        'captured_at_utc': datetime.now(timezone.utc).isoformat(),
    }
    (evidence / 'snapshot_manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
    print(json.dumps(manifest, indent=2, ensure_ascii=False))


if __name__ == '__main__':
    main()
