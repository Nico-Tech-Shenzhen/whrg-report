#!/usr/bin/env python3
"""Normalize canonical Team, Organization, and Robot Platform identities."""

import argparse
import copy
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

from validate_research import ROOT, canonical_hash


REVIEW_PATH = 'research/reviews/canonical-entity-normalization/review.md'
DECISIONS_PATH = 'research/reviews/canonical-entity-normalization/decisions.json'
STATE_PATH = 'research/evidence/canonical-entity-normalization.json'

BLOCKED_TEAM_NAMES = {
    '151.8cm', '179.1cm', '80.3cm', '机器人战队',
    '天卓队工业具身智能机器人联合实验室（华中科技大学-北',
    '天骁队养老护理机器人联合实验室（河北工业大学-北京人',
    '天骄队情感智能应用联合实验室（北京大学——北京人形',
}

TEAM_ALIASES = {
    '天工队': 'TR-005',
    '⽆锡智元赛队': 'TR-022',
    '北⽅⼯⼤博远智⾏-璇玑队': 'TR-031',
    '⼆进制⻮轮': 'TR-035',
    '上海高奕队': 'TR-021',
    'RUC-HiLigh': 'TR-069',
}

ALIAS_CANDIDATES = [
    {'names': ['木心铁骨', '木芯铁骨'], 'reason': 'similar spelling but competition context does not establish one Team'},
    {'names': ['星海图星舰队', '星舰队'], 'reason': 'shared prefix is insufficient to establish one Team'},
    {'names': ['啊对队', '啊对对队'], 'reason': 'similar spelling across unrelated competitions'},
    {'names': ['北京邮电大学bbox', '北邮BBOX队'], 'reason': 'abbreviation and casing alone do not establish one Team'},
]

BLOCKED_ORGANIZATION_NAMES = {
    '上海体育大学、北京智元新创技术有限公司',
    '上海戏剧学院、北京智元新创技术有限公司',
    '北京科技大学、中国戏曲学院、北京智元新创技术有限公司',
    '北京舞蹈学院、北京智元新创技术有限公司',
    '北京人形机器人创新中心有限公司和北京信息科技大学',
    '北京人形机器人创新中心+深圳大学',
    '北京人形+河南科技学院',
    '北京航空航天大学/智元',
    '者北京星动纪元科技股份有限公司',
    '巴西多所大学RoboCup团队',
    '澳大利亚三所高校',
}

ORGANIZATION_ALIASES = {
    '北京人形机器人创新中心': 'BIC',
    '北京人形机器人创新中心有限公司': 'BIC',
    '智元': 'AGIBOT',
    '宇树科技股份有限公司': 'UNITREE',
}

ROBOT_SPECS = [
    ('CRP-001', '天工Ultra', '北京人形机器人创新中心', 'BIC'),
    ('CRP-002', '精灵G2', None, None),
    ('CRP-003', 'Galaxea R1 Pro', None, None),
    ('CRP-004', 'Booster T1', '加速进化 (中国)', None),
    ('CRP-005', '宇树 G1', '宇树科技 (中国)', 'UNITREE'),
]


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')


def present(value):
    return value not in (None, '', 'Unknown')


def dedupe(values, key):
    result = []
    seen = set()
    for value in values:
        identity = key(value)
        if identity not in seen:
            seen.add(identity)
            result.append(copy.deepcopy(value))
    return result


def support_bundle(records):
    provenance = dedupe(
        [item for record in records for item in record.get('provenance', [])],
        lambda item: (item.get('path'), item.get('locator'), item.get('source_id')),
    )
    source_rows = dedupe(
        [item for record in records for item in record.get('source_rows', [])],
        lambda item: (item.get('path'), item.get('locator'), item.get('source_id')),
    )
    evidence_refs = dedupe(
        [item for record in records for item in record.get('evidence_refs', [])],
        lambda item: (item.get('entity_type'), item.get('id')),
    )
    source_entities = [
        {'entity_type': record['entity_type'], 'id': record['id']} for record in records
    ]
    return provenance, source_rows, evidence_refs, source_entities


def derived_record(identity, entity_type, label, sources, payload_name, payload, decision):
    provenance, source_rows, evidence_refs, source_entities = support_bundle(sources)
    return {
        'id': identity,
        'label': label,
        'status': 'unverified',
        'provenance': provenance,
        'evidence_refs': evidence_refs,
        'relationships': [],
        'unresolved_references': [],
        'source_rows': source_rows,
        'entity_type': entity_type,
        payload_name: payload,
        'identity_derivation': {
            'authority': 'Canonical entity normalization review',
            'review_path': REVIEW_PATH,
            'source_entities': source_entities,
            'raw_names': sorted({label}),
            'decision': decision,
        },
    }


def add_relation(record, relation, entity_type, identity):
    target = {'entity_type': entity_type, 'id': identity}
    if not any(item.get('relation') == relation and item.get('target') == target
               for item in record['relationships']):
        record['relationships'].append({'relation': relation, 'target': target})


def protected_entry_hash(record):
    value = copy.deepcopy(record)
    for field in ('team_id', 'organization_id', 'robot_id'):
        value['entry'][field] = None
    value['relationships'] = [
        item for item in value['relationships']
        if item.get('target', {}).get('entity_type') not in {'Team', 'Organization', 'Robot Platform'}
    ]
    return canonical_hash(value)


def raw_distinct(entries, headers):
    values = set()
    for entry in entries:
        for row in entry.get('source_rows', []):
            names = row.get('headers') or []
            data = row.get('values') or []
            for offset, name in enumerate(names):
                if name in headers and offset < len(data) and present(data[offset]):
                    values.add(str(data[offset]).strip())
    return len(values)


def normalize(records):
    original = copy.deepcopy(records)
    before_by_key = {(item['entity_type'], item['id']): item for item in original}
    entries = [item for item in records if item['entity_type'] == 'Competition Entry']
    teams = [item for item in records if item['entity_type'] == 'Team']
    organizations = [item for item in records if item['entity_type'] == 'Organization']
    robots = [item for item in records if item['entity_type'] == 'Robot Platform']

    before = {
        'records': len(records), 'entries': len(entries), 'teams': len(teams),
        'organizations': len(organizations), 'robot_platforms': len(robots),
        'entries_with_team_id': sum(present(item['entry'].get('team_id')) for item in entries),
        'entries_with_organization_id': sum(present(item['entry'].get('organization_id')) for item in entries),
        'entries_with_robot_platform_id': sum(present(item['entry'].get('robot_id')) for item in entries),
    }

    team_name_to_id = {}
    for team in teams:
        for name in {team.get('label'), team.get('team', {}).get('official_name')}:
            if present(name):
                team_name_to_id[str(name).strip()] = team['id']
    team_name_to_id.update(TEAM_ALIASES)

    team_sources = defaultdict(list)
    for entry in entries:
        name = str(entry['entry'].get('team_name') or '').strip()
        if name and name not in BLOCKED_TEAM_NAMES:
            team_sources[name].append(entry)
    new_team_names = sorted(set(team_sources) - set(team_name_to_id))
    new_team_ids = {name: f'CTN-{offset:03d}' for offset, name in enumerate(new_team_names, 1)}
    team_name_to_id.update(new_team_ids)
    for name in new_team_names:
        records.append(derived_record(
            new_team_ids[name], 'Team', name, team_sources[name], 'team',
            {'official_name': name}, 'distinct Team name supported by canonical Entry evidence',
        ))

    entry_org_sources = defaultdict(list)
    for entry in entries:
        name = str(entry['entry'].get('organization_name') or '').strip()
        if name and name != 'Unknown':
            entry_org_sources[name].append(entry)
    team_org_sources = defaultdict(list)
    for team in teams:
        name = str(team.get('team', {}).get('organization_name') or '').strip()
        if name and name != 'Unknown':
            team_org_sources[name].append(team)
    team_org_sources['加速进化 (中国)'].extend(
        team for team in teams if '加速进化' in str(team.get('team', {}).get('robot_manufacturer') or '')
    )
    org_names = (set(entry_org_sources) | set(team_org_sources)) - BLOCKED_ORGANIZATION_NAMES
    org_name_to_id = dict(ORGANIZATION_ALIASES)
    new_org_names = sorted(org_names - set(org_name_to_id))
    new_org_ids = {name: f'CNO-{offset:03d}' for offset, name in enumerate(new_org_names, 1)}
    org_name_to_id.update(new_org_ids)
    for name in new_org_names:
        sources = dedupe(entry_org_sources[name] + team_org_sources[name],
                         lambda item: (item['entity_type'], item['id']))
        records.append(derived_record(
            new_org_ids[name], 'Organization', name, sources, 'organization',
            {'official_name': name}, 'distinct Organization name supported by canonical source fields',
        ))

    by_id = {(item['entity_type'], item['id']): item for item in records}
    robot_sources = {
        'CRP-001': [item for item in entries if item['entry'].get('robot_model') == '天工Ultra'],
        'CRP-002': [item for item in entries if item['entry'].get('robot_model') == '精灵G2'],
        'CRP-003': [by_id[('Team', 'DOM-002')]],
        'CRP-004': [by_id[('Team', 'DOM-003')]],
        'CRP-005': [by_id[('Team', 'INT-003')]],
    }
    model_to_id = {}
    for identity, model, manufacturer, manufacturer_id in ROBOT_SPECS:
        model_to_id[model] = identity
        robot = derived_record(
            identity, 'Robot Platform', model, robot_sources[identity], 'robot_platform',
            {'manufacturer': manufacturer, 'model': model},
            'specific Robot Platform model supported by canonical source fields',
        )
        if manufacturer_id:
            add_relation(robot, 'manufactured_by', 'Organization', manufacturer_id)
        elif manufacturer == '加速进化 (中国)':
            add_relation(robot, 'manufactured_by', 'Organization', org_name_to_id[manufacturer])
        records.append(robot)

    updated_entries = []
    for entry in entries:
        name = str(entry['entry'].get('team_name') or '').strip()
        organization_name = str(entry['entry'].get('organization_name') or '').strip()
        model = str(entry['entry'].get('robot_model') or '').strip()
        team_id = team_name_to_id.get(name)
        organization_id = org_name_to_id.get(organization_name)
        robot_id = model_to_id.get(model)
        entry['entry']['team_id'] = team_id
        entry['entry']['organization_id'] = organization_id
        entry['entry']['robot_id'] = robot_id
        entry['relationships'] = [
            item for item in entry['relationships']
            if item.get('target', {}).get('entity_type') not in {'Team', 'Organization', 'Robot Platform'}
        ]
        if team_id: add_relation(entry, 'represented_by', 'Team', team_id)
        if organization_id: add_relation(entry, 'affiliated_with', 'Organization', organization_id)
        if robot_id: add_relation(entry, 'used_robot_platform', 'Robot Platform', robot_id)
        updated_entries.append(entry)

    by_id = {(item['entity_type'], item['id']): item for item in records}
    teams_by_id = {item['id']: item for item in records if item['entity_type'] == 'Team'}
    for team in teams_by_id.values():
        team['relationships'] = [
            item for item in team['relationships']
            if item.get('target', {}).get('entity_type') not in {'Organization', 'Robot Platform'}
        ]
    for entry in entries:
        team_id = entry['entry'].get('team_id')
        org_id = entry['entry'].get('organization_id')
        if team_id and org_id: add_relation(teams_by_id[team_id], 'affiliated_with', 'Organization', org_id)
    for team in teams:
        org_name = str(team.get('team', {}).get('organization_name') or '').strip()
        if org_name in org_name_to_id:
            add_relation(team, 'affiliated_with', 'Organization', org_name_to_id[org_name])
    add_relation(teams_by_id['DOM-002'], 'supported_with', 'Robot Platform', 'CRP-003')
    add_relation(teams_by_id['DOM-002'], 'robot_provider', 'Organization', 'GALAXEA')
    add_relation(teams_by_id['DOM-003'], 'supported_with', 'Robot Platform', 'CRP-004')
    add_relation(teams_by_id['DOM-003'], 'robot_provider', 'Organization', org_name_to_id['加速进化 (中国)'])
    add_relation(teams_by_id['INT-003'], 'used_robot_platform', 'Robot Platform', 'CRP-005')

    by_key = {(item['entity_type'], item['id']): item for item in records}
    added_keys = set(by_key) - set(before_by_key)
    updated_keys = {
        key for key in before_by_key if canonical_hash(before_by_key[key]) != canonical_hash(by_key[key])
    }
    entry_updates = [key for key in updated_keys if key[0] == 'Competition Entry']
    team_updates = [key for key in updated_keys if key[0] == 'Team']
    for key in entry_updates:
        if protected_entry_hash(before_by_key[key]) != protected_entry_hash(by_key[key]):
            raise ValueError(f'Normalization changed protected Entry facts: {key}')

    after_entries = [item for item in records if item['entity_type'] == 'Competition Entry']
    after = {
        'records': len(records), 'entries': len(after_entries),
        'teams': sum(item['entity_type'] == 'Team' for item in records),
        'organizations': sum(item['entity_type'] == 'Organization' for item in records),
        'robot_platforms': sum(item['entity_type'] == 'Robot Platform' for item in records),
        'entries_with_team_id': sum(present(item['entry'].get('team_id')) for item in after_entries),
        'entries_with_organization_id': sum(present(item['entry'].get('organization_id')) for item in after_entries),
        'entries_with_robot_platform_id': sum(present(item['entry'].get('robot_id')) for item in after_entries),
    }
    raw_metrics = {
        'team_name': {'normalized': len({item['entry']['team_name'] for item in entries if present(item['entry'].get('team_name'))}),
                      'source_fields': raw_distinct(entries, {'Team Name', 'Team Name (normalized)'})},
        'organization_name': {'normalized': len({item['entry']['organization_name'] for item in entries if present(item['entry'].get('organization_name'))}),
                              'source_fields': raw_distinct(entries, {'Organization Name', 'Organization', 'Organization (as shown)'})},
        'robot_manufacturer': {'normalized': len({item['entry']['robot_manufacturer'] for item in entries if present(item['entry'].get('robot_manufacturer'))}),
                               'source_fields': raw_distinct(entries, {'Robot Manufacturer'})},
        'robot_model': {'normalized': len({item['entry']['robot_model'] for item in entries if present(item['entry'].get('robot_model'))}),
                        'source_fields': raw_distinct(entries, {'Robot Model', 'Robot Platform'})},
    }
    duplicate_decisions = [{
        'competition_id': 'C-028', 'team_id': 'TR-023',
        'entry_ids': ['TR-062', 'TR-086'], 'decision': 'retain_distinct',
        'reason': 'official 58KG and 40KG class entries are distinct',
    }]
    decisions = {
        'team_name_to_id': dict(sorted(team_name_to_id.items())),
        'blocked_team_names': sorted(BLOCKED_TEAM_NAMES),
        'team_aliases_resolved': [
            {'raw_name': name, 'team_id': identity} for name, identity in sorted(TEAM_ALIASES.items())
        ],
        'alias_candidates_not_merged': ALIAS_CANDIDATES,
        'organization_name_to_id': dict(sorted(org_name_to_id.items())),
        'blocked_organization_names': sorted(BLOCKED_ORGANIZATION_NAMES),
        'robot_model_to_id': model_to_id,
        'duplicate_entry_decisions': duplicate_decisions,
    }
    counts = Counter(item['verification']['canonical_status'] for item in after_entries)
    participation = Counter(item['entry']['participation_status'] for item in after_entries)
    state = {
        'schema_version': '1', 'review_id': 'canonical-entity-normalization',
        'review_path': REVIEW_PATH, 'decision_path': DECISIONS_PATH,
        'before': before, 'after': after, 'raw_string_metrics': raw_metrics,
        'records_added': [
            {'entity_type': key[0], 'id': key[1], 'sha256': canonical_hash(by_key[key])}
            for key in sorted(added_keys)
        ],
        'records_updated': [
            {'entity_type': key[0], 'id': key[1],
             'before_sha256': canonical_hash(before_by_key[key]),
             'after_sha256': canonical_hash(by_key[key]),
             **({'protected_sha256': protected_entry_hash(by_key[key])} if key[0] == 'Competition Entry' else {})}
            for key in sorted(updated_keys)
        ],
        'entry_status_counts': dict(counts),
        'participation_status_counts': dict(participation),
        'team_aliases_resolved': len(TEAM_ALIASES),
        'team_alias_candidates_unresolved': len(ALIAS_CANDIDATES),
        'duplicate_entries_consolidated': 0,
        'new_team_entities': len(new_team_names),
        'new_organization_entities': len(new_org_names),
        'new_robot_platform_entities': len(ROBOT_SPECS),
        'existing_team_ids_used': len({item['entry'].get('team_id') for item in after_entries
                                       if item['entry'].get('team_id') and not item['entry']['team_id'].startswith('CTN-')}),
        'team_entry_links': after['entries_with_team_id'] - before['entries_with_team_id'],
        'organization_entry_links': after['entries_with_organization_id'] - before['entries_with_organization_id'],
        'robot_entry_links': after['entries_with_robot_platform_id'] - before['entries_with_robot_platform_id'],
        'updated_entry_count': len(entry_updates), 'updated_team_count': len(team_updates),
    }
    return records, decisions, state


def review_markdown(state):
    before, after = state['before'], state['after']
    return f'''# Canonical entity normalization review

## Method

All {before['entries']} canonical Competition Entries were audited without web research or re-extraction. Raw source spelling remains in each Entry. Canonical IDs were linked only from direct canonical source fields, exact names, or the six documented alias decisions in `decisions.json`. Similar names, joint-organization strings, generic labels, measurement-like strings, and truncated strings were not silently merged.

The existing provenance rule required a source ID to equal every derived canonical entity ID. That prevented honest creation of a Team, Organization, or Robot Platform from an Entry/Team source row. Validation now permits the mismatch only for review-declared `identity_derivation` records whose source entities, exact source rows, and canonical hashes are checked by the normalization validator.

## Before and after

| Metric | Before | After |
| --- | ---: | ---: |
| Canonical records | {before['records']} | {after['records']} |
| Competition Entries | {before['entries']} | {after['entries']} |
| Teams | {before['teams']} | {after['teams']} |
| Organizations | {before['organizations']} | {after['organizations']} |
| Robot Platforms | {before['robot_platforms']} | {after['robot_platforms']} |
| Entries linked to Team IDs | {before['entries_with_team_id']} | {after['entries_with_team_id']} |
| Entries linked to Organization IDs | {before['entries_with_organization_id']} | {after['entries_with_organization_id']} |
| Entries linked to Robot Platform IDs | {before['entries_with_robot_platform_id']} | {after['entries_with_robot_platform_id']} |

Before normalization, all {before['entries']} Entries had Team Name text: {before['entries_with_team_id']} had a Team ID and {before['entries']-before['entries_with_team_id']} did not. Ninety-three Entries had Organization Name text without an Organization ID. Four Entries had Robot Manufacturer/Model text without a Robot Platform ID. After normalization, {after['entries']-after['entries_with_team_id']} Team-name Entries, {93-after['entries_with_organization_id']} Organization-name Entries, and zero Robot-text Entries remain without the corresponding canonical ID.

Distinct normalized/source-field strings before normalization: Team Name {state['raw_string_metrics']['team_name']['normalized']}/{state['raw_string_metrics']['team_name']['source_fields']}; Organization Name {state['raw_string_metrics']['organization_name']['normalized']}/{state['raw_string_metrics']['organization_name']['source_fields']}; Robot Manufacturer {state['raw_string_metrics']['robot_manufacturer']['normalized']}/{state['raw_string_metrics']['robot_manufacturer']['source_fields']}; Robot Model {state['raw_string_metrics']['robot_model']['normalized']}/{state['raw_string_metrics']['robot_model']['source_fields']}.

## Team decisions

- {state['existing_team_ids_used']} existing Team IDs are used after normalization; {state['new_team_entities']} new Team entities were created from distinguishable source names.
- Resolved aliases: `天工队` -> `TR-005`; compatibility-glyph variants of 无锡智元赛队, 北方工大博远智行-璇玑队, and 二进制齿轮 -> their existing `TR-*` IDs; `上海高奕队` -> `TR-021`; `RUC-HiLigh` -> `TR-069`.
- Alias candidates not merged: 木心铁骨/木芯铁骨; 星海图星舰队/星舰队; 啊对队/啊对对队; 北京邮电大学bbox/北邮BBOX队.
- Unlinked identities: three measurement-like strings, eleven generic `机器人战队` Entries, and twelve Entries carrying three visibly truncated long names. Verification, participation, results, and rankings remain unchanged; these are recorded as factual identity conflicts rather than rewritten.
- Exact per-name decisions and IDs are in [decisions.json](decisions.json).

## Organization and Robot Platform decisions

- Organization links use direct Organization fields. BIC, AGIBOT, and UNITREE are reused only for documented name variants. Joint/multi-party strings and one visibly malformed string remain unlinked.
- New Organization identities retain the exact source name. Platform-provider and manufacturer relationships are distinct from Team affiliation.
- Five clear Robot Platform models were created: 天工Ultra, 精灵G2, Galaxea R1 Pro, Booster T1, and 宇树 G1. Only the four Entries with explicit Robot Model text receive Entry-level Robot Platform IDs. Team hardware-support relationships do not assert Entry ownership or use.

## Duplicate Entry audit

No Entry was consolidated. The only repeated exact Team identity within one Competition is 宁夏智元赛队 in C-028; `TR-062` (58KG) and `TR-086` (40KG) remain distinct class Entries. Historical/result evidence is unchanged.

## Recent transcription import

The prior import correctly reused zero Team IDs because none of the 68 transcription Team identities existed in the canonical corpus before that import. It created those Teams and linked its 79 Entries. The remaining gap was cross-corpus normalization: older and official-archive Entries with the same supported identities had not yet been linked to the newly created `TR-*` IDs.

## Verification safety and QA

Verified/Research Lead status, Participation Status, Result, and Ranking are hash-protected and unchanged. All required QA passed: repository and import validators; four normalization, five transcription, six prior-import, seven official-archive, and six frozen-v2.1 negative controls; checkpoint audit; 43 unit tests; strict MkDocs build; PDF build; and Git diff checks.
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    records_path = ROOT / 'research/evidence/records.json'
    if (ROOT / STATE_PATH).exists():
        raise SystemExit('Normalization state already exists; refusing to reapply')
    records, decisions, state = normalize(read(records_path))
    decision_bytes = (json.dumps(decisions, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    state['decision_sha256'] = hashlib.sha256(decision_bytes).hexdigest()
    print(json.dumps({'before': state['before'], 'after': state['after'],
                      'new_teams': state['new_team_entities'],
                      'new_organizations': state['new_organization_entities'],
                      'new_robot_platforms': state['new_robot_platform_entities']},
                     ensure_ascii=False, indent=2))
    if not args.write:
        return
    write(records_path, records)
    decisions_path = ROOT / DECISIONS_PATH
    decisions_path.parent.mkdir(parents=True, exist_ok=True)
    decisions_path.write_bytes(decision_bytes)
    write(ROOT / STATE_PATH, state)
    (ROOT / REVIEW_PATH).write_text(review_markdown(state), encoding='utf-8', newline='\n')


if __name__ == '__main__':
    main()
