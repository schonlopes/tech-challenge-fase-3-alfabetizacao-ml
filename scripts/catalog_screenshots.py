"""Catalog actual UI screenshots already captured; never generate or reconstruct console screens."""
import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parents[1]
NAMES = {
    'gcp_gold_details.png':'Gold table identifier, project and actual creation metadata',
    'gcp_gold_storage_partitioning.png':'23,995 Gold rows, two partitions, clustering and storage',
    'gcp_query_processing_controls.png':'Completed municipal query: elapsed time and actual processed/billed bytes',
    'gcp_query_execution_plan.png':'Actual execution time, slot use and shuffle metrics',
    'gcp_query_execution_rows.png':'Actual execution stage with 40,051 input and 23,995 output rows',
}


def main():
    job = json.loads((ROOT/'reports/evidence/municipal_gold_job.json').read_text())
    items = []
    for name,description in NAMES.items():
        path = ROOT/'images/evidence'/name
        items.append({'file':str(path.relative_to(ROOT)).replace('\\','/'),
            'description':description,'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
            'file_last_modified_at_utc':datetime.fromtimestamp(path.stat().st_mtime,timezone.utc).isoformat(),
            'capture_type':'real browser UI screenshot; no reconstructed console image'})
    evidence = {'cataloged_at_utc':datetime.now(timezone.utc).isoformat(),
        'project':job['project'],'query_job_id':job['job_id'],
        'query_console_url':f'https://console.cloud.google.com/bigquery?project={job["project"]}&j=bq:US:{job["job_id"]}&page=queryresults',
        'purpose':'Proof of GCP data/query execution. Models were trained locally, not in GCP.',
        'screenshots':items}
    (ROOT/'reports/evidence/screenshots_manifest.json').write_text(json.dumps(evidence,indent=2),encoding='utf-8')
    print('Capturas reais catalogadas:',len(items))


if __name__=='__main__':
    main()
