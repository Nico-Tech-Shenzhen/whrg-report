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
FINAL_IMPORT_STATE_NAME = 'kimi-official-archive-final-import.json'


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


def validate_post_v21_import(root,records,supplemental,migration,state_path,imports,
                             allowed_updates=None,allow_entry_changes=False):
    allowed_updates=set(allowed_updates or ())
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
    by_key={(r['entity_type'],r['id']):r for r in records}
    declared={(r['entity_type'],r['id']):r['sha256'] for r in state.get('records',[])}
    observed={key:canonical_hash(by_key[key]) for key in declared if key in by_key and key not in allowed_updates}
    expected={key:value for key,value in declared.items() if key not in allowed_updates}
    if len(declared)!=len(state.get('records',[])) or set(declared)-set(by_key) or observed!=expected:
        raise ValueError('Post-v2.1 imported records differ from reviewed declaration')
    additions=[by_key[key] for key in declared]
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
    if not allow_entry_changes and counts!=state.get('canonical_entry_counts'):
        raise ValueError('Post-v2.1 import changed canonical Entry counts')
    if len(state.get('accepted_evidence_ids',[]))!=len(additions) or set(state['accepted_evidence_ids'])!={r['id'] for r in additions}:
        raise ValueError('Accepted Evidence inventory differs from reviewed records')
    return len(additions)


def validate_final_import(root,records,supplemental,migration,state_path,imports,prior_state):
    state=read(state_path)
    if state.get('schema_version')!='1' or state.get('import_id')!='kimi-official-archive-final-import':
        raise ValueError('Unknown final official-archive import declaration')
    review=inside(root,state.get('review_path',''))
    if review!=root/'research/reviews/kimi-official-archive-final-import/review.md' or not review.is_file():
        raise ValueError('Final official-archive review is missing')
    for asset in state.get('review_assets',{}).values():
        path=inside(root,asset.get('path',''))
        if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=asset.get('sha256'):
            raise ValueError('Final review asset is missing or changed')
    for item in state.get('inputs',[]):
        registered=imports.get(item.get('path'))
        if registered is None or any(registered.get(k)!=item.get(k) for k in ('sha256','original_name')):
            raise ValueError('Final import input differs from immutable manifest')
    by_key={(r['entity_type'],r['id']):r for r in records}
    additions={(r['entity_type'],r['id']):r['sha256'] for r in state.get('records_added',[])}
    updates={(r['entity_type'],r['id']):r['sha256'] for r in state.get('records_updated',[])}
    if len(additions)!=len(state.get('records_added',[])) or len(updates)!=len(state.get('records_updated',[])):
        raise ValueError('Duplicate final import record declaration')
    if set(additions)&set(updates) or set(additions|updates)-set(by_key):
        raise ValueError('Invalid final import record scope')
    observed={key:canonical_hash(by_key[key]) for key in additions|updates}
    if observed!=additions|updates:
        raise ValueError('Final imported records differ from reviewed declaration')
    prior_keys={(r['entity_type'],r['id']) for r in prior_state.get('records',[])}
    expected_extras=prior_keys|set(additions)
    actual_extras={key for key in by_key if key not in migration['base_record_keys']}
    if actual_extras!=expected_extras:
        raise ValueError('Final import additions differ from prior plus reviewed inventories')
    if set(updates)-migration['base_record_keys']-prior_keys:
        raise ValueError('Final import update is not a prior canonical record')
    extra_supplemental=[]
    for item in supplemental:
        key=(item['record_type'],item['id']) if item['id'] is not None else (
            item['record_type'],item['provenance'][0]['path'],item['provenance'][0]['locator'])
        if key not in migration['base_supplemental_keys']:
            extra_supplemental.append(key)
    if extra_supplemental:
        raise ValueError('Final import does not authorize supplemental additions')
    counts={'Verified':0,'Research Lead':0,'Unresolved':0}
    for item in records:
        if item['entity_type']=='Competition Entry':
            status=item['verification']['canonical_status']
            counts[status]=counts.get(status,0)+1
    if counts!=state.get('canonical_entry_counts'):
        raise ValueError('Final canonical Entry counts differ from review')
    decisions_asset=state.get('review_assets',{}).get('entry-decisions.json',{})
    decisions=read(inside(root,decisions_asset.get('path','')))
    if len(decisions)!=1005 or len({d.get('candidate_id') for d in decisions})!=1005:
        raise ValueError('Final Entry decision ledger is incomplete')
    effects={name:sum(d.get('effect')==name for d in decisions) for name in 'ABCD'}
    if effects!=state.get('entry_effect_counts'):
        raise ValueError('Final Entry effect totals differ from decision ledger')
    conflict_ids={'OEC-2026-0721','OEC-2026-0725','OEC-2026-0726',
                  'OEC-2026-0702','OEC-2026-0703','OEC-2026-0709'}
    if any(next(d for d in decisions if d['candidate_id']==identity)['effect']!='D'
           for identity in conflict_ids):
        raise ValueError('Reviewed C-036/C-040 identity conflict was promoted')
    gmo=by_key.get(('Competition Entry','E-005-04'),{})
    if (gmo.get('entry',{}).get('ranking')!='7' or
            gmo.get('verification',{}).get('canonical_status')!='Verified'):
        raise ValueError('Reviewed C-005 GMO rank/promotion changed')
    dnf=by_key.get(('Competition Entry','OEC-2026-0405'),{})
    if dnf.get('entry',{}).get('participation_status')!='DNF' or dnf.get('entry',{}).get('ranking') is not None:
        raise ValueError('Reviewed C-003 DNF treatment changed')
    relay=by_key.get(('Competition Entry','OEC-2026-0193'),{})
    if relay.get('entry',{}).get('ranking')!='1':
        raise ValueError('Reviewed C-006 result changed')
    if state.get('entity_additions',{}).get('Team',0) or state.get('entity_additions',{}).get('Organization',0) or state.get('entity_additions',{}).get('Robot Platform',0):
        raise ValueError('Final import inferred a Team, Organization, or Robot Platform identity')
    for key in additions:
        item=by_key[key]
        if item['entity_type']!='Competition Entry':
            continue
        for ref in item['evidence_refs']:
            source=by_key[('Evidence',ref['id'])]
            archive=source.get('official_archive',{})
            if archive.get('year')==2025:
                raise ValueError('2025 Evidence was used to verify a 2026 Entry')
            if archive.get('extraction_status')=='Image Only':
                raise ValueError('Image-only attachment was used to extract an Entry')
    return {'added':len(additions),'updated':len(updates),'state':state}


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
    directory=candidate.parent if candidate else root/'research/evidence'
    final_state_path=directory/FINAL_IMPORT_STATE_NAME
    final_state=read(final_state_path) if final_state_path.is_file() else None
    allowed_updates={(r['entity_type'],r['id']) for r in (final_state or {}).get('records_updated',[])}
    prior_post_path=directory/POST_V21_STATE_NAME
    prior_post_state=read(prior_post_path) if prior_post_path.is_file() else {'records':[]}
    prior_additions={(r['entity_type'],r['id']) for r in prior_post_state.get('records',[])}
    if state_path.is_file():
        migration=validate_migration(root,records,extra,read(state_path),
                                     allowed_updates-prior_additions)
    elif activation.exists() or any('entry_histories' in r for r in records):
        raise ValueError('Active v2.1 research requires its reviewed semantics sidecar')
    reviewed_statuses=dict(migration['reviewed_statuses']) if migration else {}
    reviewed_statuses.update((final_state or {}).get('reviewed_statuses',{}))
    validate_extensions(root, records, extra, imports, allowed,reviewed_statuses or None)
    if migration:
        post_state=(candidate.parent if candidate else root/'research/evidence')/POST_V21_STATE_NAME
        has_additions=any((r['entity_type'],r['id']) not in migration['base_record_keys'] for r in records)
        if post_state.is_file():
            prior_state=read(post_state)
            validate_post_v21_import(root,records,extra,migration,post_state,imports,allowed_updates,
                                     final_state_path.is_file())
            if final_state_path.is_file():
                validate_final_import(root,records,extra,migration,final_state_path,imports,prior_state)
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
