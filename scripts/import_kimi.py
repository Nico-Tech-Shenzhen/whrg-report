#!/usr/bin/env python3
"""Archive a screened inbox delivery without altering its bytes."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re

from validate_research import ROOT, validate


def archive(source, root=ROOT):
    source = source.resolve()
    inbox = (root / 'research/inbox/kimi').resolve()
    if not source.is_relative_to(inbox) or not source.is_file():
        raise ValueError('Source must be a regular file inside research/inbox/kimi')
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*', source.name):
        raise ValueError('Delivery filename must use English/ASCII letters, digits, dots, underscores, or hyphens')
    if source.suffix.lower() not in {'.xlsx', '.md', '.json', '.csv', '.tsv', '.txt'}:
        raise ValueError('Unsupported delivery format; review before adding support')
    validate(root)
    data = source.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    target = root / 'research/imported/kimi' / digest / source.name
    if not target.resolve().is_relative_to((root / 'research/imported/kimi').resolve()):
        raise ValueError('Archive path escapes repository')
    manifest_path = root / 'research/imported/kimi/manifest.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    relative = target.relative_to(root).as_posix()
    if any(item['path'] == relative for item in manifest):
        return target
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open('xb') as stream:
        stream.write(data)
    manifest.append({'path': relative, 'sha256': digest, 'original_name': source.name,
                     'imported_at': datetime.now(timezone.utc).isoformat()})
    temporary = manifest_path.with_suffix('.json.tmp')
    temporary.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
    temporary.replace(manifest_path)
    return target


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('source', type=Path)
    args = parser.parse_args()
    try:
        print(archive(args.source))
        return 0
    except (ValueError, OSError, KeyError, TypeError, AttributeError) as error:
        print(f'FAIL: {error}')
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
