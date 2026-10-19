"""Isolated local runs: never replace the historical delivery evidence."""
from datetime import datetime, timezone
import hashlib
import importlib.metadata
import json
from pathlib import Path
import platform
import subprocess
from uuid import uuid4


def sha256(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def create_run(root, name, output=None, inputs=None, parameters=None):
    root = Path(root)
    directory = Path(output) if output else root/'runs'/(
        f'{name}-{datetime.now(timezone.utc):%Y%m%dT%H%M%S%fZ}-{uuid4().hex[:8]}')
    directory = directory.resolve()
    # exist_ok=False also refuses a previously failed/incomplete run.
    directory.mkdir(parents=True, exist_ok=False)
    for child in ('reports', 'images', 'models', 'data'):
        (directory/child).mkdir()
    def git(*args):
        result = subprocess.run(['git', *args], cwd=root, capture_output=True)
        return result.stdout if result.returncode == 0 else None
    top = git('rev-parse', '--show-toplevel')
    own_repository = top is not None and Path(top.decode().strip()).resolve()==root.resolve()
    commit = git('rev-parse', 'HEAD') if own_repository else None
    status = git('status', '--porcelain') if own_repository else None
    source_files = sorted({p for folder in ('src','scripts','tests')
        for p in (root/folder).rglob('*.py')} | set(root.glob('requirements*.txt')))
    source_hashes = {p.relative_to(root).as_posix():sha256(p) for p in source_files}
    metadata = {
        'run_id':directory.name, 'name':name, 'status':'started',
        'started_at_utc':datetime.now(timezone.utc).isoformat(),
        'git_commit':commit.decode().strip() if commit else None,
        'git_dirty':bool(status) if status is not None else None,
        'source_sha256':source_hashes,
        'python':platform.python_version(),
        'packages':{p:importlib.metadata.version(p) for p in
            ('numpy','pandas','scikit-learn','pyarrow','joblib')},
        'inputs':{name:sha256(path) for name,path in (inputs or {}).items()},
        'parameters':parameters or {},
    }
    (directory/'run.json').write_text(json.dumps(metadata, indent=2), encoding='utf-8')
    return directory


def finish_run(directory):
    path = Path(directory)/'run.json'
    metadata = json.loads(path.read_text(encoding='utf-8'))
    metadata.update(status='completed', finished_at_utc=datetime.now(timezone.utc).isoformat())
    metadata['outputs_sha256'] = {p.relative_to(directory).as_posix():sha256(p)
        for p in sorted(Path(directory).rglob('*')) if p.is_file() and p != path}
    path.write_text(json.dumps(metadata, indent=2), encoding='utf-8')
