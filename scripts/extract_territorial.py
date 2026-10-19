"""Only public municipal aggregates; reuse the local student snapshot without re-exporting it."""
import argparse
import hashlib
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.extract_gcp import query


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--profile-only', action='store_true')
    args = parser.parse_args()
    if args.profile_only:
        sql = (ROOT / 'sql/profile_socioeconomic.sql').read_text(encoding='utf-8')
        rows = query(sql, 'tech-challenge-fase-2-506814', 1_000_000_000, 'socioeconomic_profile')
        (ROOT / 'reports/evidence/socioeconomic_profile.json').write_text(json.dumps(rows, indent=2), encoding='utf-8')
        print(json.dumps(rows[:10], ensure_ascii=False, indent=2))
        return
    import pandas as pd
    artifacts = {}
    for name in ['socioeconomic', 'municipal_gold', 'national_state_targets']:
        sql = (ROOT / f'sql/{name}.sql').read_text(encoding='utf-8')
        sql = sql.replace('__PROJECT__', 'tech-challenge-fase-2-506814')
        rows = query(sql, 'tech-challenge-fase-2-506814', 1_000_000_000, name)
        frame = pd.DataFrame(rows)
        path = ROOT / f'data/raw/{name}.parquet'
        frame.to_parquet(path, index=False)
        artifacts[name] = {'rows':len(frame), 'snapshot':str(path.relative_to(ROOT)),
                           'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
        print(name, len(frame), flush=True)
    (ROOT / 'reports/evidence/territorial_manifest.json').write_text(json.dumps(artifacts, indent=2), encoding='utf-8')


if __name__ == '__main__':
    main()
