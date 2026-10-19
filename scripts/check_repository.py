"""Packaging checks requiring no GCP credentials and no private snapshot."""
from pathlib import Path
import hashlib
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def main():
    files = subprocess.run(['git','ls-files','-z'],cwd=ROOT,capture_output=True,check=True).stdout.decode('utf-8').split('\0')
    files = [name for name in files if name]
    forbidden = [name for name in files if name.startswith(('.venv/','models/','reports/private/','runs/'))
        or (name.startswith(('data/raw/','data/processed/')) and not name.endswith('/.gitkeep'))]
    if forbidden:
        raise ValueError('Arquivos privados no índice: '+str(forbidden))
    for name in files:
        if not name.endswith('.md'):
            continue
        source = ROOT/name
        for target in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)',source.read_text(encoding='utf-8')):
            target = target.strip('<>')
            if target.startswith(('https://','http://','#')):
                continue
            resolved = source.parent / target.split('#')[0]
            if not resolved.exists():
                raise ValueError(f'Link local inexistente em {name}: {target}')
    manifest = json.loads((ROOT/'reports/evidence/screenshots_manifest.json').read_text())
    for item in manifest['screenshots']:
        path = (ROOT/item['file']).resolve()
        if ROOT.resolve() not in path.parents:
            raise ValueError('Caminho de screenshot fora do projeto.')
        if hashlib.sha256(path.read_bytes()).hexdigest()!=item['sha256']:
            raise ValueError('Screenshot difere do manifest: '+item['file'])
    print(f'Índice sem arquivos privados; links locais válidos; {len(manifest["screenshots"])} screenshots íntegros.')


if __name__=='__main__':
    main()
