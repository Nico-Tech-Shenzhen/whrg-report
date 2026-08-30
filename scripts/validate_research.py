#!/usr/bin/env python3
"""Validate immutable imports and typed research references, never factual truth."""

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def entity_types(root):
    return {line.split('|')[2].strip() for line in (root / 'dic.md').read_text(encoding='utf-8').splitlines()
            if line.startswith('| ') and line.split('|')[2].strip() not in {'Canonical', '---'}}


def inside(root, name):
    path = (root / name).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError(f'Path outside repository: {name}')
    return path


def validate(root=ROOT, candidate=None):
    manifest = json.loads((root / 'research/imported/kimi/manifest.json').read_text(encoding='utf-8'))
    if not isinstance(manifest, list):
        raise ValueError('Import manifest must be a list')
    imports = {}
    for item in manifest:
        for field in ('path', 'sha256', 'original_name', 'imported_at'):
            if not isinstance(item.get(field), str) or not item[field].strip():
                raise ValueError(f'Missing manifest field: {field}')
        path = inside(root, item['path'])
        archive = (root / 'research/imported/kimi').resolve()
        if not path.is_relative_to(archive) or item['path'] in imports:
            raise ValueError(f'Invalid or duplicate archive path: {path}')
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        if digest != item['sha256'] or path.parent.name != digest or path.name != item['original_name']:
            raise ValueError(f'Changed import or invalid address: {path}')
        imports[item['path']] = item
    for path in (root / 'research/imported/kimi').rglob('*'):
        if path.is_file() and path != root / 'research/imported/kimi/manifest.json' and path.relative_to(root).as_posix() not in imports:
            raise ValueError(f'Unregistered import: {path}')

    records = json.loads((candidate or root / 'research/evidence/records.json').read_text(encoding='utf-8'))
    if not isinstance(records, list):
        raise ValueError('Records must be a list')
    allowed = entity_types(root)
    keys = set()
    for record in records:
        for field in ('id', 'entity_type', 'label'):
            if not isinstance(record.get(field), str) or not record[field].strip():
                raise ValueError(f'Missing string field: {field}')
        key = (record['entity_type'], record['id'])
        if key[0] not in allowed or key in keys:
            raise ValueError(f'Invalid type or duplicate identity: {key}')
        keys.add(key)
        if record.get('status') not in {'unverified', 'verified', 'disputed'}:
            raise ValueError(f'Invalid verification status: {key}')
        provenance = record.get('provenance')
        if not isinstance(provenance, list) or not provenance:
            raise ValueError(f'Missing provenance: {key}')
        for source in provenance:
            if source.get('path') not in imports or source.get('source_id') != record['id']:
                raise ValueError(f'Unregistered provenance or altered ID: {key}')
            if not isinstance(source.get('locator'), str) or not source['locator'].strip():
                raise ValueError(f'Missing source locator: {key}')
        if not isinstance(record.get('evidence_refs'), list) or not isinstance(record.get('relationships'), list):
            raise ValueError(f'Reference fields must be lists: {key}')
        if key[0] == 'Evidence':
            source = record.get('source', {})
            for field in ('title', 'publisher', 'date', 'url', 'accessed_at', 'version', 'verification_note'):
                if not isinstance(source.get(field), str) or not source[field].strip():
                    raise ValueError(f'Missing evidence metadata {field}: {key}')
        elif not record['evidence_refs']:
            raise ValueError(f'Entity has no evidence: {key}')
    for record in records:
        for ref in record['evidence_refs']:
            if ref.get('entity_type') != 'Evidence' or (ref.get('entity_type'), ref.get('id')) not in keys:
                raise ValueError(f'Unresolved evidence reference: {ref}')
        for relation in record['relationships']:
            ref = relation.get('target', {})
            if not relation.get('relation') or (ref.get('entity_type'), ref.get('id')) not in keys:
                raise ValueError(f'Unresolved typed relationship: {relation}')
    return len(imports), len(records)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidate', type=Path)
    args = parser.parse_args()
    try:
        candidate = inside(ROOT, args.candidate) if args.candidate else None
        imports, records = validate(candidate=candidate)
        print(f'OK: {imports} immutable imports; {records} structurally valid records (not fact-checked).')
        return 0
    except (ValueError, OSError, KeyError, TypeError, AttributeError) as error:
        print(f'FAIL: {error}')
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
