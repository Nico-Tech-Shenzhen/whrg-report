#!/usr/bin/env python3
"""Validate immutable imports and typed research references, never factual truth."""

import argparse
import hashlib
import json
from pathlib import Path

from research_schema import validate_extensions
from master_v21 import STATE_NAME, read, validate_migration

ROOT = Path(__file__).resolve().parents[1]
POST_V21_STATE_NAME = 'kimi-official-archive-import-actual.json'


def entity_types(root):
    return {line.split('|')[2].strip() for line in (root / 'dic.md').read_text(encoding='utf-8').splitlines()
            if line.startswith('| ') and line.split('|')[2].strip() not in {'Canonical', '---'}}


def inside(root, name):
    path = (root / name).resolve()
    if not path.is_relative_to(root.resolve()):
        raise ValueError(f'Path outside repository: {name}')
    return path


def canonical_hash(item):
    payload=json.dumps(item,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
    return hashlib.sha256(payload).hexdigest()


def validate_post_v21_import(root,records,supplemental,migration,state_path,imports):
    state=read(state_path)
    if state.get('schema_version')!='1' or state.get('import_id')!='kimi-official-archive-import-actual':
        raise ValueError('Unknown post-v2.1 import declaration')
    review=inside(root,state.get('review_path',''))
    if review!=root/'research/reviews/kimi-official-archive-import-actual/review.md' or not review.is_file():
        raise ValueError('Post-v2.1 import review is missing')
    for item in state.get('inputs',[]):
        registered=imports.get(item.get('path'))
        if registered is None or registered.get('sha256')!=item.get('sha256') or registered.get('original_name')!=item.get('original_name'):
            raise ValueError('Post-v2.1 input declaration differs from immutable import manifest')
    base=migration['base_record_keys']
    additions=[r for r in records if (r['entity_type'],r['id']) not in base]
    declared={(r['entity_type'],r['id']):r['sha256'] for r in state.get('records',[])}
    observed={(r['entity_type'],r['id']):canonical_hash(r) for r in additions}
    if len(declared)!=len(state.get('records',[])) or observed!=declared:
        raise ValueError('Post-v2.1 imported records differ from reviewed declaration')
    if any(r['entity_type']!='Evidence' or r['status']!='unverified' for r in additions):
        raise ValueError('This post-v2.1 import authorizes only unverified Evidence additions')
    extra_supplemental=[]
    for item in supplemental:
        if item['id'] is not None:
            key=item['record_type'],item['id']
        else:
            source=item['provenance'][0]
            key=item['record_type'],source['path'],source['locator']
        if key not in migration['base_supplemental_keys']:
            extra_supplemental.append(key)
    if extra_supplemental:
        raise ValueError('Post-v2.1 import does not authorize supplemental additions')
    counts={'Verified':0,'Research Lead':0,'Unresolved':0}
    for item in records:
        if item['entity_type']=='Competition Entry':
            status=item['verification']['canonical_status']
            counts[status]=counts.get(status,0)+1
    if counts!=state.get('canonical_entry_counts'):
        raise ValueError('Post-v2.1 import changed canonical Entry counts')
    if len(state.get('accepted_evidence_ids',[]))!=len(additions) or set(state['accepted_evidence_ids'])!={r['id'] for r in additions}:
        raise ValueError('Accepted Evidence inventory differs from reviewed records')
    return len(additions)


def validate(root=ROOT, candidate=None, supplemental=None):
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
            gaps = record.get('unresolved_references', [])
            if not record.get('evidence_gap') or not any(g.get('entity_type') == 'Evidence' for g in gaps):
                raise ValueError(f'Entity has no evidence or explicit unresolved evidence gap: {key}')
    for record in records:
        for ref in record['evidence_refs']:
            if ref.get('entity_type') != 'Evidence' or (ref.get('entity_type'), ref.get('id')) not in keys:
                raise ValueError(f'Unresolved evidence reference: {ref}')
        for relation in record['relationships']:
            ref = relation.get('target', {})
            if not relation.get('relation') or (ref.get('entity_type'), ref.get('id')) not in keys:
                raise ValueError(f'Unresolved typed relationship: {relation}')
    supplemental_path = supplemental or (candidate.parent if candidate else root / 'research/evidence') / 'supplemental.json'
    if any(r.get('source_rows') for r in records) and not supplemental_path.is_file():
        raise ValueError('Extended candidate requires its supplemental.json sidecar')
    extra = json.loads(supplemental_path.read_text(encoding='utf-8')) if supplemental_path.is_file() else []
    state_path=(candidate.parent if candidate else root/'research/evidence')/STATE_NAME
    activation=root/'research/active-checkpoint.json'
    migration=None
    if activation.exists():
        active=read(activation)
        if active!={'checkpoint_id':'kimi-master-v2-1','schema_version':'2.1',
                   'state_path':'research/evidence/master-v2-1.json'}:
            raise ValueError('Unknown active checkpoint declaration')
    if state_path.is_file():
        migration=validate_migration(root,records,extra,read(state_path))
    elif activation.exists() or any('entry_histories' in r for r in records):
        raise ValueError('Active v2.1 research requires its reviewed semantics sidecar')
    validate_extensions(root, records, extra, imports, allowed,
                        migration['reviewed_statuses'] if migration else None)
    if migration:
        post_state=(candidate.parent if candidate else root/'research/evidence')/POST_V21_STATE_NAME
        has_additions=any((r['entity_type'],r['id']) not in migration['base_record_keys'] for r in records)
        if post_state.is_file():
            validate_post_v21_import(root,records,extra,migration,post_state,imports)
        elif has_additions:
            raise ValueError('Post-v2.1 additions require a reviewed import declaration')
    if candidate:
        existing = json.loads((root / 'research/evidence/records.json').read_text(encoding='utf-8'))
        missing = {(r['entity_type'], r['id']) for r in existing} - keys
        if migration:
            missing-={('Competition Entry',identity) for identity in migration['retired_ids']}
        if missing:
            raise ValueError(f'Candidate deletes canonical identities: {sorted(missing)}')
        canonical_extra = root / 'research/evidence/supplemental.json'
        if canonical_extra.is_file():
            old = json.loads(canonical_extra.read_text(encoding='utf-8'))
            def extra_key(item):
                p = item['provenance'][0]
                return (item['record_type'], item['id']) if item['id'] is not None else (item['record_type'], p['path'], p['locator'])
            if {extra_key(r) for r in old} - {extra_key(r) for r in extra}:
                raise ValueError('Candidate deletes canonical supplemental records')
    return len(imports), len(records)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--candidate', type=Path)
    parser.add_argument('--supplemental', type=Path)
    args = parser.parse_args()
    try:
        candidate = inside(ROOT, args.candidate) if args.candidate else None
        supplemental = inside(ROOT, args.supplemental) if args.supplemental else None
        imports, records = validate(candidate=candidate, supplemental=supplemental)
        print(f'OK: {imports} immutable imports; {records} structurally valid records (not fact-checked).')
        return 0
    except (ValueError, OSError, KeyError, TypeError, AttributeError) as error:
        print(f'FAIL: {error}')
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
