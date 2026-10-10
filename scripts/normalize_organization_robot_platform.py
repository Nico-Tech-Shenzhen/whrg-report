#!/usr/bin/env python3
"""Normalize evidence-backed Organization and Robot Platform relationships."""

import argparse
import copy
import hashlib
import json
import re
from collections import Counter, defaultdict

from validate_research import ROOT, canonical_hash


REVIEW_PATH = 'research/reviews/organization-robot-platform-normalization/review.md'
DECISIONS_PATH = 'research/reviews/organization-robot-platform-normalization/decisions.json'
STATE_PATH = 'research/evidence/organization-robot-platform-normalization.json'


ORGANIZATION_SPECS = {
    'CNO-043': ('清华大学', [('Evidence', 'EV-099'), ('Evidence', 'EV-100')]),
    'CNO-044': ('中国农业大学', [('Evidence', 'EV-101'), ('Evidence', 'EV-102')]),
    'CNO-045': ('河南科技学院', [('Competition Entry', 'E-042-01')]),
    'CNO-046': ('深圳大学', [('Competition Entry', 'E-042-03')]),
    'CNO-047': ('北京航空航天大学', [('Competition Entry', 'E-B01-040-03'), ('Team', 'CTN-134')]),
    'CNO-048': ('上海戏剧学院', [('Competition Entry', 'TR-046')]),
    'CNO-049': ('上海体育大学', [('Competition Entry', 'TR-048'), ('Competition Entry', 'TR-050')]),
    'CNO-050': ('北京舞蹈学院', [('Competition Entry', 'TR-055'), ('Team', 'CTN-132')]),
    'CNO-051': ('中国戏曲学院', [('Competition Entry', 'TR-061')]),
    'CNO-052': ('北京星动纪元科技股份有限公司', [('Competition Entry', 'OEC-2026-0018'), ('Evidence', 'EV-093')]),
    'CNO-053': ('河北工业大学', [('Competition Entry', 'TR-001')]),
    'CNO-054': ('华中科技大学', [('Competition Entry', 'TR-002')]),
    'CNO-055': ('松延动力', [('Evidence', 'EV-120'), ('Team', 'CTN-133'), ('Team', 'CTN-278')]),
    'CNO-056': ('首都体育学院', [('Team', 'CTN-278')]),
    'CNO-057': ('银河通用', [('Evidence', 'EV-121'), ('Team', 'CTN-265')]),
    'CNO-058': ('中国科学院自动化研究所', [('Team', 'CTN-065')]),
    'CNO-059': ('武汉大学', [('Team', 'CTN-199'), ('Team', 'CTN-209')]),
    'CNO-060': ('智树天成', [('Team', 'CTN-199')]),
}


ROBOT_SPECS = {
    'CRP-006': {
        'label': 'Booster K1', 'manufacturer': '加速进化 (中国)', 'manufacturer_id': 'CNO-011',
        'family': 'Booster', 'model': 'K1', 'sources': [('Evidence', 'EV-092'), ('Evidence', 'EV-100')],
    },
    'CRP-007': {
        'label': 'Booster T2', 'manufacturer': '加速进化 (中国)', 'manufacturer_id': 'CNO-011',
        'family': 'Booster', 'model': 'T2', 'sources': [('Evidence', 'UF-011')],
    },
    'CRP-008': {
        'label': 'Unitree H1', 'manufacturer': '宇树科技', 'manufacturer_id': 'UNITREE',
        'family': 'H1', 'model': 'H1', 'sources': [('Evidence', 'EV-088')],
    },
    'CRP-009': {
        'label': '灵犀X2', 'manufacturer': '智元机器人', 'manufacturer_id': 'AGIBOT',
        'family': '灵犀', 'model': 'X2', 'sources': [('Evidence', 'EV-086'), ('Evidence', 'EV-087')],
    },
    'CRP-010': {
        'label': '远征A3', 'manufacturer': '智元机器人', 'manufacturer_id': 'AGIBOT',
        'family': '远征', 'model': 'A3', 'sources': [('Evidence', 'EV-086'), ('Evidence', 'EV-087')],
    },
    'CRP-011': {
        'label': '天工3.0', 'manufacturer': '北京人形机器人创新中心', 'manufacturer_id': 'BIC',
        'family': '天工', 'model': '3.0', 'sources': [('Evidence', 'EV-090')],
    },
    'CRP-012': {
        'label': '天轶2.0', 'manufacturer': '北京人形机器人创新中心', 'manufacturer_id': 'BIC',
        'family': '天轶', 'model': '2.0', 'sources': [('Evidence', 'EV-090')],
    },
    'CRP-013': {
        'label': '星动L7', 'manufacturer': '北京星动纪元科技股份有限公司', 'manufacturer_id': 'CNO-052',
        'family': '星动', 'model': 'L7', 'sources': [('Evidence', 'EV-093')],
    },
    'CRP-014': {
        'label': '小顽童', 'manufacturer': '松延动力', 'manufacturer_id': 'CNO-055',
        'family': '小顽童', 'model': '小顽童', 'sources': [('Evidence', 'EV-120')],
    },
    'CRP-015': {
        'label': 'Galbot G1', 'manufacturer': '银河通用', 'manufacturer_id': 'CNO-057',
        'family': 'Galbot', 'model': 'G1', 'sources': [('Evidence', 'EV-121')],
    },
}


JOINT_ENTRY_ORGANIZATIONS = {
    'E-042-01': ['BIC', 'CNO-045'],
    'E-042-03': ['BIC', 'CNO-046'],
    'E-B01-040-03': ['CNO-047', 'AGIBOT'],
    'TR-046': ['CNO-048', 'CNO-017'],
    'TR-048': ['CNO-049', 'CNO-017'],
    'TR-050': ['CNO-049', 'CNO-017'],
    'TR-055': ['CNO-050', 'CNO-017'],
    'TR-061': ['CNO-022', 'CNO-051', 'CNO-017'],
    'TR-068': ['BIC', 'CNO-013'],
}


TEAM_ORGANIZATIONS = {
    'CTN-062': [('university_team', 'CNO-044')],
    'CTN-216': [('university_team', 'CNO-043')],
    'CTN-265': [('company_team', 'CNO-057')],
    'CTN-279': [('company_team', 'CNO-052')],
    'CTN-119': [('joint_team_member', 'BIC'), ('joint_team_member', 'CNO-045')],
    'CTN-118': [('joint_team_member', 'BIC'), ('joint_team_member', 'CNO-046')],
    'CTN-150': [('joint_team_member', 'CNO-047'), ('joint_team_member', 'AGIBOT')],
    'TR-046': [('joint_team_member', 'CNO-048'), ('joint_team_member', 'CNO-017')],
    'TR-048': [('joint_team_member', 'CNO-049'), ('joint_team_member', 'CNO-017')],
    'TR-050': [('joint_team_member', 'CNO-049'), ('joint_team_member', 'CNO-017')],
    'TR-055': [('joint_team_member', 'CNO-050'), ('joint_team_member', 'CNO-017')],
    'TR-061': [('joint_team_member', 'CNO-022'), ('joint_team_member', 'CNO-051'), ('joint_team_member', 'CNO-017')],
    'TR-068': [('joint_team_member', 'BIC'), ('joint_team_member', 'CNO-013')],
    'CTN-132': [('joint_team_member', 'CNO-050'), ('joint_team_member', 'AGIBOT')],
    'CTN-133': [('joint_team_member', 'CNO-050'), ('joint_team_member', 'CNO-055')],
    'CTN-278': [('joint_team_member', 'CNO-056'), ('joint_team_member', 'CNO-055')],
    'CTN-149': [('joint_team_member', 'CNO-050'), ('joint_team_member', 'BIC')],
    'CTN-134': [('joint_team_member', 'CNO-047'), ('joint_team_member', 'BIC')],
    'CTN-104': [('joint_team_member', 'CNO-047'), ('joint_team_member', 'BIC')],
    'CTN-105': [('joint_team_member', 'CNO-047'), ('joint_team_member', 'BIC')],
    'CTN-116': [('joint_team_member', 'BIC'), ('joint_team_member', 'CNO-022'), ('joint_team_member', 'CNO-047')],
    'CTN-199': [('joint_team_member', 'CNO-060'), ('joint_team_member', 'CNO-059')],
    'CTN-065': [('joint_team_member', 'CNO-058'), ('joint_team_member', 'AGIBOT')],
    'CTN-215': [('joint_team_member', 'CNO-043'), ('joint_team_member', 'AGIBOT')],
    'CTN-161': [('joint_team_member', 'AGIBOT')],
    'CTN-209': [('joint_team_member', 'CNO-059'), ('joint_team_member', 'AGIBOT')],
    'CTN-157': [('joint_team_member', 'CNO-054'), ('joint_team_member', 'AGIBOT')],
    'CTN-158': [('joint_team_member', 'CNO-054'), ('joint_team_member', 'AGIBOT')],
    'CTN-155': [('joint_team_member', 'AGIBOT')],
    'CTN-156': [('joint_team_member', 'AGIBOT')],
    'CTN-243': [('joint_team_member', 'AGIBOT')],
    'CTN-252': [('joint_team_member', 'AGIBOT')],
    'CTN-247': [('joint_team_member', 'CNO-043')],
}


TEAM_PLATFORM_RELATIONS = {
    'TR-002': ['CRP-001'],
    'TR-005': ['CRP-001'],
    'CTN-196': ['CRP-002'],
    'DOM-002': ['CRP-003'],
    'DOM-003': ['CRP-004'],
    'INT-001': ['CRP-004', 'CRP-006', 'CRP-007'],
    'INT-002': ['CRP-004', 'CRP-006', 'CRP-007'],
    'INT-003': ['CRP-005'],
    'CTN-216': ['CRP-004', 'CRP-006'],
    'CTN-062': ['CRP-004'],
    'CTN-265': ['CRP-015'],
    'CTN-279': ['CRP-013'],
}


TEAM_SUPPORT_RELATIONS = {
    'DOM-002': [('platform_provider', 'GALAXEA'), ('sponsor', 'GALAXEA')],
    'DOM-003': [('platform_provider', 'CNO-011')],
    'INT-001': [('platform_provider', 'CNO-011'), ('technical_support', 'CNO-011')],
    'INT-002': [('platform_provider', 'CNO-011'), ('technical_support', 'CNO-011')],
    'INT-003': [('platform_provider', 'UNITREE')],
}


TEAM_EVIDENCE_ADDITIONS = {
    'CTN-062': ['EV-101', 'EV-102'],
    'CTN-216': ['EV-099', 'EV-100'],
    'CTN-265': ['EV-121'],
    'CTN-279': ['EV-093'],
}


ORGANIZATION_ALIASES_RESOLVED = [
    {'raw': '北京人形机器人创新中心', 'display': '北京人形机器人创新中心', 'id': 'BIC'},
    {'raw': '北京人形机器人创新中心有限公司', 'display': '北京人形机器人创新中心', 'id': 'BIC'},
    {'raw': '北京人形', 'display': '北京人形机器人创新中心', 'id': 'BIC'},
    {'raw': '智元', 'display': '智元机器人', 'id': 'AGIBOT'},
    {'raw': '智元机器人', 'display': '智元机器人', 'id': 'AGIBOT'},
    {'raw': '宇树科技 (中国)', 'display': '宇树科技', 'id': 'UNITREE'},
    {'raw': '宇树科技股份有限公司', 'display': '宇树科技', 'id': 'UNITREE'},
    {'raw': '宇树科技', 'display': '宇树科技', 'id': 'UNITREE'},
    {'raw': '加速进化', 'display': '加速进化 (中国)', 'id': 'CNO-011'},
    {'raw': '者北京星动纪元科技股份有限公司', 'display': '北京星动纪元科技股份有限公司', 'id': 'CNO-052'},
    {'raw': '清华大学自动化系', 'display': '清华大学', 'id': 'CNO-043', 'relationship_scope': 'parent institution'},
    {'raw': '中国农业大学工学院', 'display': '中国农业大学', 'id': 'CNO-044', 'relationship_scope': 'parent institution'},
]


ROBOT_ALIASES_RESOLVED = [
    {'raw': '加速进化Booster T1', 'display': 'Booster T1', 'id': 'CRP-004'},
    {'raw': '加速进化T1', 'display': 'Booster T1', 'id': 'CRP-004'},
    {'raw': 'Booster T1', 'display': 'Booster T1', 'id': 'CRP-004'},
    {'raw': 'Booster K1', 'display': 'Booster K1', 'id': 'CRP-006'},
    {'raw': 'Booster T2', 'display': 'Booster T2', 'id': 'CRP-007'},
    {'raw': '宇树 G1', 'display': '宇树 G1', 'id': 'CRP-005'},
    {'raw': 'Unitree G1', 'display': '宇树 G1', 'id': 'CRP-005'},
    {'raw': 'Unitree H1', 'display': 'Unitree H1', 'id': 'CRP-008'},
    {'raw': '精灵G2', 'display': '精灵G2', 'id': 'CRP-002'},
    {'raw': '灵犀X2', 'display': '灵犀X2', 'id': 'CRP-009'},
    {'raw': '远征A3', 'display': '远征A3', 'id': 'CRP-010'},
    {'raw': '天工Ultra', 'display': '天工Ultra', 'id': 'CRP-001'},
    {'raw': '天工3.0', 'display': '天工3.0', 'id': 'CRP-011'},
    {'raw': '天轶2.0', 'display': '天轶2.0', 'id': 'CRP-012'},
    {'raw': '星动L7', 'display': '星动L7', 'id': 'CRP-013'},
    {'raw': '小顽童', 'display': '小顽童', 'id': 'CRP-014'},
    {'raw': 'Galbot G1', 'display': 'Galbot G1', 'id': 'CRP-015'},
]


UNRESOLVED_ALIASES = [
    {'kind': 'Organization', 'raw': '巴西多所大学RoboCup团队', 'reason': 'consortium wording does not identify each university'},
    {'kind': 'Organization', 'raw': '澳大利亚三所高校', 'reason': 'consortium wording does not identify each university'},
    {'kind': 'Organization', 'raw': '养老护理机器人联合实验室 / 养老护理机器人联合实验室（河北工业大学-北京人形机器人创新中心）', 'reason': 'short and expanded labels may denote the same lab, but identity continuity is not explicit'},
    {'kind': 'Organization', 'raw': '工业具身智能机器人联合实验室 / 工业具身智能机器人联合实验室（华中科技大学-北京人形机器人创新中心）', 'reason': 'short and expanded labels may denote the same lab, but identity continuity is not explicit'},
    {'kind': 'Organization', 'raw': '情感智能应用联合实验室 / 情感智能应用联合实验室（北京大学-北京人形机器人创新中心）', 'reason': 'short and expanded labels may denote the same lab, but identity continuity is not explicit'},
    {'kind': 'Organization', 'raw': '北京松延动力深饪餐饮有限公司 / 松延动力', 'reason': 'malformed-looking legal name is not silently merged with the manufacturer label'},
    {'kind': 'Organization', 'raw': '荣耀 / 上海荣耀 / 深圳荣耀 / 北京荣耀', 'reason': 'generic brand evidence does not establish a parent or subsidiary relationship'},
    {'kind': 'Organization', 'raw': '智元 / 智元创新（城市）公司 / 北京智元新创技术有限公司', 'reason': 'brand similarity does not establish corporate ownership or subsidiary relationships'},
    {'kind': 'Organization', 'raw': '华工、同济、上交、苏大、计算所、国科大、湖北人形、荔枝', 'reason': 'abbreviated joint-team labels are insufficient for new canonical identities'},
    {'kind': 'Robot Platform', 'raw': 'Q5', 'reason': 'Evidence explicitly scopes it to WRC, not WHRG'},
    {'kind': 'Robot Platform', 'raw': '夸父(Kuavo)', 'reason': 'platform evidence is not linked to a WHRG Team or Entry'},
    {'kind': 'Robot Platform', 'raw': '格斗机器人“豆汁”“卤煮”', 'reason': 'named robot instances are not established as reusable platform models'},
    {'kind': 'Robot Platform', 'raw': 'OmniHand', 'reason': 'dexterous-hand component is not normalized as a Robot Platform'},
    {'kind': 'Robot Platform', 'raw': '松延 N2 / 松延 E1', 'reason': 'no canonical Evidence in the current corpus supports these review targets'},
]


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')


def present(value):
    return value not in (None, '', 'Unknown', 'N/A')


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
    for record in records:
        if record['entity_type'] == 'Evidence':
            evidence_refs.append({'entity_type': 'Evidence', 'id': record['id']})
    evidence_refs = dedupe(evidence_refs, lambda item: (item.get('entity_type'), item.get('id')))
    source_entities = [{'entity_type': record['entity_type'], 'id': record['id']} for record in records]
    return provenance, source_rows, evidence_refs, source_entities


def derived_record(identity, entity_type, label, sources, payload_name, payload, decision, raw_names):
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
            'authority': 'Organization / Robot Platform relationship normalization review',
            'review_path': REVIEW_PATH,
            'source_entities': source_entities,
            'raw_names': sorted(set(raw_names)),
            'decision': decision,
        },
    }


def add_relation(record, relation, entity_type, identity):
    target = {'entity_type': entity_type, 'id': identity}
    if not any(item.get('relation') == relation and item.get('target') == target
               for item in record['relationships']):
        record['relationships'].append({'relation': relation, 'target': target})


def add_evidence(record, identity):
    ref = {'entity_type': 'Evidence', 'id': identity}
    if ref not in record['evidence_refs']:
        record['evidence_refs'].append(ref)


def source_values(records, headers):
    values = set()
    for record in records:
        for row in record.get('source_rows', []):
            names = row.get('headers') or []
            data = row.get('values') or []
            for offset, name in enumerate(names):
                if name in headers and offset < len(data) and present(data[offset]):
                    values.add(str(data[offset]).strip())
    return sorted(values)


def relationship_count(record, entity_type=None, relation=None):
    return sum(
        (entity_type is None or item.get('target', {}).get('entity_type') == entity_type)
        and (relation is None or item.get('relation') == relation)
        for item in record.get('relationships', [])
    )


def metrics(records, families=None):
    entries = [item for item in records if item['entity_type'] == 'Competition Entry']
    teams = [item for item in records if item['entity_type'] == 'Team']
    organizations = [item for item in records if item['entity_type'] == 'Organization']
    robots = [item for item in records if item['entity_type'] == 'Robot Platform']
    teams_by_id = {item['id']: item for item in teams}
    entries_through_team_org = sum(
        bool(entry['entry'].get('team_id'))
        and relationship_count(teams_by_id[entry['entry']['team_id']], 'Organization') > 0
        for entry in entries
    )
    manufacturers = {
        item['target']['id'] for robot in robots for item in robot.get('relationships', [])
        if item.get('relation') == 'manufactured_by' and item.get('target', {}).get('entity_type') == 'Organization'
    }
    return {
        'records': len(records),
        'entries': len(entries),
        'teams': len(teams),
        'organizations': len(organizations),
        'robot_platforms': len(robots),
        'teams_with_organization_relationship': sum(relationship_count(team, 'Organization') > 0 for team in teams),
        'teams_with_organization_text': sum(present(team.get('team', {}).get('organization_name')) for team in teams),
        'teams_with_organization_text_no_relationship': sum(
            present(team.get('team', {}).get('organization_name')) and not relationship_count(team, 'Organization')
            for team in teams
        ),
        'teams_with_manufacturer_provider_text': sum(
            any(present(team.get('team', {}).get(field)) for field in
                ('robot_manufacturer', 'robot_platform_name', 'hardware_support', 'company_support'))
            for team in teams
        ),
        'entries_with_organization_id': sum(present(entry['entry'].get('organization_id')) for entry in entries),
        'entries_with_team_id': sum(present(entry['entry'].get('team_id')) for entry in entries),
        'entries_with_direct_organization_relationship': sum(relationship_count(entry, 'Organization') > 0 for entry in entries),
        'entries_linked_through_team_organization': entries_through_team_org,
        'joint_organization_relationships': sum(
            relationship_count(team, 'Organization', 'joint_team_member') for team in teams
        ),
        'entries_with_robot_platform_id': sum(present(entry['entry'].get('robot_id')) for entry in entries),
        'entries_with_robot_text_no_id': sum(
            not present(entry['entry'].get('robot_id')) and
            (present(entry['entry'].get('robot_manufacturer')) or present(entry['entry'].get('robot_model')))
            for entry in entries
        ),
        'teams_with_known_robot_platform': sum(relationship_count(team, 'Robot Platform') > 0 for team in teams),
        'unique_manufacturers': len(manufacturers),
        'unique_robot_families': len(set(families or [])),
        'unique_robot_models': len(robots),
    }


def raw_audit(records):
    organization_headers = {
        'Account / Organization', 'Organization', 'Organization (as shown)', 'Organization Name',
        'Source Organization', 'Subject Organization', 'Team / Organization', 'University/Lab',
    }
    organization = source_values(records, organization_headers)
    university = sorted({
        item for item in organization
        if re.search(r'大学|学院|高校|University|College', item, re.IGNORECASE)
    } | set(source_values(records, {'University/Lab'})))
    research_institute = sorted({
        item for item in organization
        if re.search(r'研究所|研究院|实验室|中心|Institute|Laboratory|\bLab\b', item, re.IGNORECASE)
    })
    manufacturer = source_values(records, {'Manufacturer'})
    robot_manufacturer = source_values(records, {'Robot manufacturer', 'Robot Manufacturer'})
    robot_model = source_values(records, {'Robot Model'})
    robot_platform = source_values(records, {'Robot platform', 'Robot Platform'})
    for record in records:
        if record['entity_type'] == 'Team':
            for field in ('robot_manufacturer',):
                value = record.get('team', {}).get(field)
                if present(value):
                    robot_manufacturer.append(str(value).strip())
            value = record.get('team', {}).get('robot_platform_name')
            if present(value):
                robot_platform.append(str(value).strip())
        elif record['entity_type'] == 'Competition Entry':
            value = record.get('entry', {}).get('robot_manufacturer')
            if present(value):
                robot_manufacturer.append(str(value).strip())
            value = record.get('entry', {}).get('robot_model')
            if present(value):
                robot_model.append(str(value).strip())
    platform_provider = sorted({
        'GALAXEA', '加速进化 (中国)', '宇树科技 (中国)'
    })
    family_level_raw = sorted({item for item in robot_platform if item in {'天工', '夸父(Kuavo)', 'Q5'}})
    return {
        'organization': sorted(set(organization)),
        'university': university,
        'research_institute': research_institute,
        'manufacturer': sorted(set(manufacturer)),
        'robot_manufacturer': sorted(set(robot_manufacturer)),
        'robot_family': family_level_raw,
        'robot_model': sorted(set(robot_model)),
        'robot_platform': sorted(set(robot_platform)),
        'platform_provider': platform_provider,
    }


def protected_entry_facts(record):
    return {
        'verification': copy.deepcopy(record.get('verification')),
        'participation_status': record['entry'].get('participation_status'),
        'result': record['entry'].get('result'),
        'ranking': record['entry'].get('ranking'),
    }


def normalize(records):
    original = copy.deepcopy(records)
    before_by_key = {(item['entity_type'], item['id']): item for item in original}
    by_key = {(item['entity_type'], item['id']): item for item in records}
    existing_families = {
        'CRP-001': '天工', 'CRP-002': '精灵', 'CRP-003': 'Galaxea R1',
        'CRP-004': 'Booster', 'CRP-005': 'Unitree G1',
    }
    before = metrics(records, existing_families.values())
    audit = raw_audit(records)

    for identity, (label, refs) in ORGANIZATION_SPECS.items():
        if ('Organization', identity) in by_key:
            raise ValueError(f'Organization ID already exists: {identity}')
        sources = [by_key[ref] for ref in refs]
        record = derived_record(
            identity, 'Organization', label, sources, 'organization', {'official_name': label},
            'Organization identity is explicitly named by canonical source fields or Evidence; relationship scope is reviewed separately',
            [label],
        )
        records.append(record)
        by_key[('Organization', identity)] = record

    for identity, spec in ROBOT_SPECS.items():
        if ('Robot Platform', identity) in by_key:
            raise ValueError(f'Robot Platform ID already exists: {identity}')
        sources = [by_key[ref] for ref in spec['sources']]
        record = derived_record(
            identity, 'Robot Platform', spec['label'], sources, 'robot_platform',
            {'manufacturer': spec['manufacturer'], 'model': spec['label']},
            'specific model/version is explicitly named by canonical Evidence', [spec['label']],
        )
        add_relation(record, 'manufactured_by', 'Organization', spec['manufacturer_id'])
        records.append(record)
        by_key[('Robot Platform', identity)] = record

    # Complete manufacturer relationships on previously normalized models.
    add_relation(by_key[('Robot Platform', 'CRP-002')], 'manufactured_by', 'Organization', 'AGIBOT')
    add_relation(by_key[('Robot Platform', 'CRP-003')], 'manufactured_by', 'Organization', 'GALAXEA')

    # A malformed source prefix is resolved, while the raw value remains in the Entry source row.
    star_entry = by_key[('Competition Entry', 'OEC-2026-0018')]
    star_entry['entry']['organization_id'] = 'CNO-052'
    add_relation(star_entry, 'affiliated_with', 'Organization', 'CNO-052')

    for entry_id, organization_ids in JOINT_ENTRY_ORGANIZATIONS.items():
        entry = by_key[('Competition Entry', entry_id)]
        for organization_id in organization_ids:
            add_relation(entry, 'joint_team_member', 'Organization', organization_id)

    teams = {item['id']: item for item in records if item['entity_type'] == 'Team'}
    for team_id, relations in TEAM_ORGANIZATIONS.items():
        team = teams[team_id]
        for relation, organization_id in relations:
            add_relation(team, relation, 'Organization', organization_id)
    for team_id, evidence_ids in TEAM_EVIDENCE_ADDITIONS.items():
        for evidence_id in evidence_ids:
            add_evidence(teams[team_id], evidence_id)

    # Preserve the joint lab as an Organization and separately represent its constituent institutions.
    for lab_id, members in {
        'CNO-010': ['CNO-053', 'BIC'],
        'CNO-030': ['CNO-054', 'BIC'],
        'CNO-032': ['CNO-016', 'BIC'],
    }.items():
        for member in members:
            add_relation(by_key[('Organization', lab_id)], 'joint_lab_member', 'Organization', member)
    for team_id, labs, members in (
        ('TR-001', ['CNO-009', 'CNO-010'], ['CNO-053', 'BIC']),
        ('TR-002', ['CNO-029', 'CNO-030'], ['CNO-054', 'BIC']),
        ('TR-004', ['CNO-031', 'CNO-032'], ['CNO-016', 'BIC']),
    ):
        for lab in labs:
            add_relation(teams[team_id], 'joint_lab_team', 'Organization', lab)
        for member in members:
            add_relation(teams[team_id], 'joint_team_member', 'Organization', member)

    for team_id, robot_ids in TEAM_PLATFORM_RELATIONS.items():
        for robot_id in robot_ids:
            add_relation(teams[team_id], 'used_robot_platform', 'Robot Platform', robot_id)
    for team_id, relations in TEAM_SUPPORT_RELATIONS.items():
        for relation, organization_id in relations:
            add_relation(teams[team_id], relation, 'Organization', organization_id)

    # EV-021 explicitly identifies GMO Robots, Unitree G1, and the 1500 m competition.
    gmo_entry = by_key[('Competition Entry', 'E-005-04')]
    gmo_entry['entry']['robot_id'] = 'CRP-005'
    add_relation(gmo_entry, 'used_robot_platform', 'Robot Platform', 'CRP-005')
    add_evidence(gmo_entry, 'EV-021')

    for key, before_record in before_by_key.items():
        if key[0] == 'Competition Entry' and protected_entry_facts(before_record) != protected_entry_facts(by_key[key]):
            raise ValueError(f'Normalization changed protected Entry facts: {key}')

    families = {
        **existing_families,
        **{identity: spec['family'] for identity, spec in ROBOT_SPECS.items()},
    }
    after = metrics(records, families.values())
    after_by_key = {(item['entity_type'], item['id']): item for item in records}
    added_keys = set(after_by_key) - set(before_by_key)
    updated_keys = {
        key for key in before_by_key
        if canonical_hash(before_by_key[key]) != canonical_hash(after_by_key[key])
    }

    provider_teams = defaultdict(set)
    for team in teams.values():
        for item in team['relationships']:
            if item['relation'] in {'platform_provider', 'robot_provider'} and item['target']['entity_type'] == 'Organization':
                provider_teams[item['target']['id']].add(team['id'])
    multi_team_providers = {
        identity: sorted(team_ids) for identity, team_ids in provider_teams.items() if len(team_ids) > 1
    }
    independent_platform_teams = []
    for team_id, robot_ids in TEAM_PLATFORM_RELATIONS.items():
        organization_ids = {
            item['target']['id'] for item in teams[team_id]['relationships']
            if item['target']['entity_type'] == 'Organization'
            and item['relation'] in {'affiliated_with', 'company_team', 'university_team', 'research_institute_team', 'joint_team_member'}
        }
        manufacturer_ids = {
            item['target']['id'] for robot_id in robot_ids
            for item in by_key[('Robot Platform', robot_id)]['relationships']
            if item['relation'] == 'manufactured_by'
        }
        if manufacturer_ids - organization_ids:
            independent_platform_teams.append({
                'team_id': team_id,
                'robot_platform_ids': robot_ids,
                'manufacturer_ids': sorted(manufacturer_ids),
                'organization_ids': sorted(organization_ids),
            })

    before_team_org_edges = {
        (record['id'], item['relation'], item['target']['id'])
        for record in original if record['entity_type'] == 'Team'
        for item in record.get('relationships', [])
        if item.get('target', {}).get('entity_type') == 'Organization'
    }
    after_team_org_edges = {
        (record['id'], item['relation'], item['target']['id'])
        for record in records if record['entity_type'] == 'Team'
        for item in record.get('relationships', [])
        if item.get('target', {}).get('entity_type') == 'Organization'
    }
    before_team_robot_edges = {
        (record['id'], item['relation'], item['target']['id'])
        for record in original if record['entity_type'] == 'Team'
        for item in record.get('relationships', [])
        if item.get('target', {}).get('entity_type') == 'Robot Platform'
    }
    after_team_robot_edges = {
        (record['id'], item['relation'], item['target']['id'])
        for record in records if record['entity_type'] == 'Team'
        for item in record.get('relationships', [])
        if item.get('target', {}).get('entity_type') == 'Robot Platform'
    }

    decisions = {
        'organization_aliases_resolved': ORGANIZATION_ALIASES_RESOLVED,
        'robot_platform_aliases_resolved': ROBOT_ALIASES_RESOLVED,
        'aliases_unresolved': UNRESOLVED_ALIASES,
        'organizations_created': [
            {'id': identity, 'display': label, 'source_entities': [f'{kind}:{source_id}' for kind, source_id in refs]}
            for identity, (label, refs) in ORGANIZATION_SPECS.items()
        ],
        'organizations_reused': sorted({
            identity for relations in TEAM_ORGANIZATIONS.values() for _, identity in relations
            if identity not in ORGANIZATION_SPECS
        } | {'CNO-011', 'UNITREE', 'GALAXEA'}),
        'robot_platforms_created': [
            {'id': identity, 'display': spec['label'], 'manufacturer_id': spec['manufacturer_id'],
             'family': spec['family'], 'model': spec['model']}
            for identity, spec in ROBOT_SPECS.items()
        ],
        'robot_platforms_reused': ['CRP-001', 'CRP-002', 'CRP-003', 'CRP-004', 'CRP-005'],
        'team_organization_relationships': [
            {'team_id': team_id, 'relation': relation, 'organization_id': organization_id}
            for team_id, relations in TEAM_ORGANIZATIONS.items() for relation, organization_id in relations
        ],
        'entry_organization_relationships': [
            {'entry_id': entry_id, 'relation': 'joint_team_member', 'organization_id': organization_id}
            for entry_id, organization_ids in JOINT_ENTRY_ORGANIZATIONS.items() for organization_id in organization_ids
        ] + [{'entry_id': 'OEC-2026-0018', 'relation': 'affiliated_with', 'organization_id': 'CNO-052'}],
        'team_robot_platform_relationships': [
            {'team_id': team_id, 'relation': 'used_robot_platform', 'robot_platform_id': robot_id}
            for team_id, robot_ids in TEAM_PLATFORM_RELATIONS.items() for robot_id in robot_ids
        ],
        'entry_robot_platform_relationships': [
            {'entry_id': 'E-005-04', 'relation': 'used_robot_platform', 'robot_platform_id': 'CRP-005',
             'evidence_id': 'EV-021'},
        ],
        'manufacturer_platform_provider_distinctions': [
            {'team_id': team_id, 'relation': relation, 'organization_id': organization_id}
            for team_id, relations in TEAM_SUPPORT_RELATIONS.items() for relation, organization_id in relations
        ],
        'robot_families': families,
        'raw_strings': audit,
    }

    status_counts = Counter(item['verification']['canonical_status'] for item in records
                            if item['entity_type'] == 'Competition Entry')
    participation_counts = Counter(item['entry']['participation_status'] for item in records
                                   if item['entity_type'] == 'Competition Entry')
    state = {
        'schema_version': '1',
        'review_id': 'organization-robot-platform-normalization',
        'review_path': REVIEW_PATH,
        'decision_path': DECISIONS_PATH,
        'before': before,
        'after': after,
        'records_added': [
            {'entity_type': key[0], 'id': key[1], 'sha256': canonical_hash(after_by_key[key])}
            for key in sorted(added_keys)
        ],
        'records_updated': [
            {'entity_type': key[0], 'id': key[1],
             'before_sha256': canonical_hash(before_by_key[key]),
             'after_sha256': canonical_hash(after_by_key[key]),
             **({'protected_facts': protected_entry_facts(after_by_key[key])} if key[0] == 'Competition Entry' else {})}
            for key in sorted(updated_keys)
        ],
        'entry_status_counts': dict(status_counts),
        'participation_status_counts': dict(participation_counts),
        'organizations_created': len(ORGANIZATION_SPECS),
        'organizations_reused': len(decisions['organizations_reused']),
        'robot_platforms_created': len(ROBOT_SPECS),
        'robot_platforms_reused': len(decisions['robot_platforms_reused']),
        'team_organization_relationships_added': len(after_team_org_edges - before_team_org_edges),
        'team_robot_platform_relationships_added': len(after_team_robot_edges - before_team_robot_edges),
        'entry_organization_relationships_added': len(decisions['entry_organization_relationships']),
        'entry_robot_platform_relationships_added': len(decisions['entry_robot_platform_relationships']),
        'joint_teams_identified': sum(
            any(relation == 'joint_team_member' for relation, _ in relations)
            for relations in TEAM_ORGANIZATIONS.values()
        ),
        'multi_team_platform_providers': multi_team_providers,
        'independent_platform_teams': independent_platform_teams,
        'raw_string_counts': {key: len(value) for key, value in audit.items()},
    }
    return records, decisions, state


def markdown_list(values):
    return ', '.join(f'`{value}`' for value in values) if values else 'None in the canonical source fields.'


def review_markdown(state, decisions):
    before = state['before']
    after = state['after']
    created_orgs = '\n'.join(
        f"- `{item['id']}` {item['display']}" for item in decisions['organizations_created']
    )
    created_robots = '\n'.join(
        f"- `{item['id']}` {item['display']} — family `{item['family']}`, manufacturer `{item['manufacturer_id']}`"
        for item in decisions['robot_platforms_created']
    )
    team_orgs = '\n'.join(
        f"- `{item['team_id']}` — `{item['relation']}` -> `{item['organization_id']}`"
        for item in decisions['team_organization_relationships']
    )
    entry_robots = '\n'.join(
        f"- `{item['entry_id']}` — `{item['relation']}` -> `{item['robot_platform_id']}` ({item['evidence_id']})"
        for item in decisions['entry_robot_platform_relationships']
    )
    unresolved = '\n'.join(
        f"- {item['kind']}: `{item['raw']}` — {item['reason']}" for item in decisions['aliases_unresolved']
    )
    raw = decisions['raw_strings']
    return f'''# Organization / Robot Platform relationship normalization review

## Methodology

This review audited all {before['teams']} Team entities and {before['entries']} Competition Entries before changing canonical data. It used only canonical Evidence, immutable official-archive source rows, historical imported snapshots already represented in canonical provenance, and normalized Team identities. No web research was performed.

Organization identity, team affiliation, manufacturer, platform provider, sponsorship, technical support, and robot use are modeled as separate typed relationships. A manufacturer or sponsor was never treated as the Team owner. Joint Teams retain one relationship per supported participant; their `organization_id` remains empty because that scalar cannot represent multiple organizations. Robot Platform use was not copied from a Team to all of its Entries.

## Before / after coverage

| Metric | Before | After |
| --- | ---: | ---: |
| Canonical records | {before['records']} | {after['records']} |
| Organizations | {before['organizations']} | {after['organizations']} |
| Teams linked to at least one Organization | {before['teams_with_organization_relationship']} | {after['teams_with_organization_relationship']} |
| Entries linked through Team/Organization relationships | {before['entries_linked_through_team_organization']} | {after['entries_linked_through_team_organization']} |
| Entries with direct Organization relationships | {before['entries_with_direct_organization_relationship']} | {after['entries_with_direct_organization_relationship']} |
| Entries with scalar Organization ID | {before['entries_with_organization_id']} | {after['entries_with_organization_id']} |
| Joint-Team Organization relationships | {before['joint_organization_relationships']} | {after['joint_organization_relationships']} |
| Robot Platforms | {before['robot_platforms']} | {after['robot_platforms']} |
| Entries linked to Robot Platform | {before['entries_with_robot_platform_id']} | {after['entries_with_robot_platform_id']} |
| Teams with at least one known Robot Platform | {before['teams_with_known_robot_platform']} | {after['teams_with_known_robot_platform']} |
| Unique manufacturers linked from Robot Platforms | {before['unique_manufacturers']} | {after['unique_manufacturers']} |
| Unique robot families | {before['unique_robot_families']} | {after['unique_robot_families']} |
| Unique Robot Platform models/versions | {before['unique_robot_models']} | {after['unique_robot_models']} |

Before normalization, {before['teams_with_organization_text_no_relationship']} Teams had Organization text but no Organization relationship, {before['teams_with_manufacturer_provider_text']} Teams carried manufacturer/provider text, and {before['entries_with_robot_text_no_id']} Entries had structured robot manufacturer/model text without a Robot Platform ID. Ten Entries had Organization text but no scalar ID; nine were multi-organization Teams and remain scalar-null while gaining typed relationships, and one malformed source alias was resolved to a canonical Organization ID.

## Distinct raw-string audit

- Organization ({len(raw['organization'])}): {markdown_list(raw['organization'])}
- University ({len(raw['university'])}): {markdown_list(raw['university'])}
- Research Institute / Lab ({len(raw['research_institute'])}): {markdown_list(raw['research_institute'])}
- Manufacturer ({len(raw['manufacturer'])}): {markdown_list(raw['manufacturer'])}
- Robot Manufacturer ({len(raw['robot_manufacturer'])}): {markdown_list(raw['robot_manufacturer'])}
- Robot Family-level source strings ({len(raw['robot_family'])}): {markdown_list(raw['robot_family'])}
- Robot Model ({len(raw['robot_model'])}): {markdown_list(raw['robot_model'])}
- Robot Platform ({len(raw['robot_platform'])}): {markdown_list(raw['robot_platform'])}
- Platform Provider ({len(raw['platform_provider'])}): {markdown_list(raw['platform_provider'])}

The corpus has no dedicated Robot Family source column. Family-level strings and normalized family assignments are therefore recorded in `decisions.json`, not added as a new schema field.

## Organizations created / reused

Created {state['organizations_created']} Organization identities:

{created_orgs}

Reused {state['organizations_reused']} existing Organization IDs: {markdown_list(decisions['organizations_reused'])}.

## Team -> Organization relationships

{team_orgs}

The three full joint-lab Organizations retain their own identities and gain `joint_lab_member` relationships to their supported constituent institutions. Their shorter labels remain separate unresolved alias candidates. Existing `affiliated_with` relationships are preserved; specific new relationships do not rewrite prior source claims.

## Robot Platforms created / reused

Created {state['robot_platforms_created']} Robot Platform identities:

{created_robots}

Reused: {markdown_list(decisions['robot_platforms_reused'])}. Existing `CRP-002` 精灵G2 and `CRP-003` Galaxea R1 Pro gain their previously missing manufacturer relationships. The family/model mapping is review metadata and does not change the entity schema.

## Entry -> Robot Platform relationships

{entry_robots}

`EV-021` explicitly states that GMO Robots used Unitree G1 in 100 m, 400 m, and 1500 m; the corpus has one exact GMO Entry, the 1500 m Entry above. No Team-level platform was propagated to other Entries.

## Manufacturer / platform-provider distinctions

- GALAXEA remains organizationally separate from `DOM-002`; it is recorded as platform provider and sponsor, not Team owner.
- 加速进化 (`CNO-011`) is a platform provider for `DOM-003`, `INT-001`, and `INT-002`; technical-support relationships are retained for both international Teams.
- UNITREE is the manufacturer/provider of GMO Robots' purchased G1 platform, while GMO Robots remains affiliated with `CNO-001`.
- Platform manufacturer relationships are attached to Robot Platforms. Team affiliations are attached independently and never inferred from robot manufacture.
- Multi-Team providers: {markdown_list([identity + ': ' + ', '.join(team_ids) for identity, team_ids in state['multi_team_platform_providers'].items()])}
- Manufacturer platforms used by organizationally independent Teams: {len(state['independent_platform_teams'])} reviewed Team cases, enumerated in `organization-robot-platform-normalization.json`.

## Joint Teams

{state['joint_teams_identified']} Teams have at least one newly reviewed `joint_team_member` relationship. Multi-party source strings retain every supported Organization. Partial mappings are intentional where a joint label also contains an unresolved abbreviation; no synthetic combined Organization was created.

## Aliases resolved

- Organization aliases: {len(decisions['organization_aliases_resolved'])}; Robot Platform aliases: {len(decisions['robot_platform_aliases_resolved'])}.
- Every decision retains the raw label, normalized display label, and canonical ID in `decisions.json`.
- The visibly malformed `者北京星动纪元科技股份有限公司` source string maps to `CNO-052`; the raw source row is unchanged.

## Aliases unresolved / unsupported relationships left unknown

{unresolved}

These cases remain unknown rather than being merged through brand similarity, abbreviated naming, sponsorship, manufacturer identity, or platform provision. No Organization ownership, subsidiary relationship, Entry result, ranking, participation status, or verification status was inferred or changed.

## QA

The normalization state hashes every added and updated record, protects Entry verification/participation/result/ranking fields, and is covered by positive and mutation-control tests. Repository validators, import and archive controls, frozen-v2.1 and checkpoint audits, unit tests, strict MkDocs, PDF generation, and Git whitespace checks are run before commit; the final command results are reported with the commit.
'''


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    records_path = ROOT / 'research/evidence/records.json'
    if (ROOT / STATE_PATH).exists():
        raise SystemExit('Organization/Robot Platform normalization state already exists; refusing to reapply')
    records, decisions, state = normalize(read(records_path))
    decision_bytes = (json.dumps(decisions, ensure_ascii=False, indent=2) + '\n').encode('utf-8')
    state['decision_sha256'] = hashlib.sha256(decision_bytes).hexdigest()
    print(json.dumps({
        'before': state['before'], 'after': state['after'],
        'organizations_created': state['organizations_created'],
        'robot_platforms_created': state['robot_platforms_created'],
        'team_organization_relationships_added': state['team_organization_relationships_added'],
        'entry_robot_platform_relationships_added': state['entry_robot_platform_relationships_added'],
    }, ensure_ascii=False, indent=2))
    if not args.write:
        return
    write(records_path, records)
    decisions_path = ROOT / DECISIONS_PATH
    decisions_path.parent.mkdir(parents=True, exist_ok=True)
    decisions_path.write_bytes(decision_bytes)
    write(ROOT / STATE_PATH, state)
    (ROOT / REVIEW_PATH).write_text(review_markdown(state, decisions), encoding='utf-8', newline='\n')


if __name__ == '__main__':
    main()
