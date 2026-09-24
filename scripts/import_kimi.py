#!/usr/bin/env python3
"""Archive a screened inbox delivery without altering its bytes."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re

from validate_research import ROOT, validate


ALLOWED_SUFFIXES = {'.xlsx', '.md', '.json', '.csv', '.tsv', '.txt',
                    '.pdf', '.docx', '.jpg', '.jpeg', '.png'}


def _screen_source(source, root):
    source = source.resolve()
    inbox = (root / 'research/inbox/kimi').resolve()
    if not source.is_relative_to(inbox) or not source.is_file():
        raise ValueError('Source must be a regular file inside research/inbox/kimi')
    if not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_.-]*', source.name):
        raise ValueError('Delivery filename must use English/ASCII letters, digits, dots, underscores, or hyphens')
    if source.suffix.lower() not in ALLOWED_SUFFIXES:
        raise ValueError('Unsupported delivery format; review before adding support')
    return source


def archive_many(sources, root=ROOT):
    """Archive screened files with a single pre-import validation."""
    screened = [_screen_source(Path(source), root) for source in sources]
    if len(set(screened)) != len(screened):
        raise ValueError('Duplicate delivery source')
    validate(root)
    manifest_path = root / 'research/imported/kimi/manifest.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    registered = {item['path']: item for item in manifest}
    targets = []
    changed = False
    for source in screened:
        data = source.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        target = root / 'research/imported/kimi' / digest / source.name
        if not target.resolve().is_relative_to((root / 'research/imported/kimi').resolve()):
            raise ValueError('Archive path escapes repository')
        relative = target.relative_to(root).as_posix()
        existing = registered.get(relative)
        if existing:
            if existing['sha256'] != digest or existing['original_name'] != source.name:
                raise ValueError('Existing manifest registration differs')
            targets.append(target)
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        with target.open('xb') as stream:
            stream.write(data)
        item = {'path': relative, 'sha256': digest, 'original_name': source.name,
                'imported_at': datetime.now(timezone.utc).isoformat()}
        manifest.append(item)
        registered[relative] = item
        targets.append(target)
        changed = True
    if changed:
        temporary = manifest_path.with_suffix('.json.tmp')
        temporary.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')
        temporary.replace(manifest_path)
    return targets


def archive(source, root=ROOT):
    return archive_many([source], root)[0]


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
