#!/usr/bin/env python3
"""Validate Organization/Robot Platform normalization and mutation controls."""

import argparse
import copy
import json
import shutil
import tempfile
from pathlib import Path

from validate_research import (
    ORGANIZATION_ROBOT_STATE_NAME,
    ROOT,
    canonical_hash,
    validate,
)


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8', newline='\n')


def update_hash(state, record):
    key = (record['entity_type'], record['id'])
    for field in ('records_added', 'records_updated'):
        for item in state[field]:
            if (item['entity_type'], item['id']) == key:
                item['after_sha256' if field == 'records_updated' else 'sha256'] = canonical_hash(record)
                return
    raise ValueError('Mutation is outside the Organization/Robot normalization declaration')


def variant(records, state):
    with tempfile.TemporaryDirectory(prefix='organization-robot-negative-', dir=ROOT / 'research/staging') as name:
        directory = Path(name)
        write(directory / 'candidate.json', records)
        write(directory / ORGANIZATION_ROBOT_STATE_NAME, state)
        for filename in (
            'supplemental.json', 'master-v2-1.json', 'kimi-official-archive-import-actual.json',
            'kimi-official-archive-final-import.json', 'kimi-image-result-transcription-import.json',
            'canonical-entity-normalization.json',
        ):
            shutil.copyfile(ROOT / 'research/evidence' / filename, directory / filename)
        validate(candidate=directory / 'candidate.json', supplemental=directory / 'supplemental.json')


def audit(negative_checks=False):
    imports, count = validate()
    records = read(ROOT / 'research/evidence/records.json')
    state = read(ROOT / 'research/evidence' / ORGANIZATION_ROBOT_STATE_NAME)
    tests = []
    if negative_checks:
        changed = copy.deepcopy(records)
        changed_state = copy.deepcopy(state)
        entry = next(item for item in changed if item['entity_type'] == 'Competition Entry' and item['id'] == 'E-005-04')
        entry['entry']['ranking'] = '99'
        update_hash(changed_state, entry)
        tests.append(('protected Entry ranking changed', changed, changed_state))

        changed = copy.deepcopy(records)
        changed_state = copy.deepcopy(state)
        team = next(item for item in changed if item['entity_type'] == 'Team' and item['id'] == 'CTN-118')
        target = {'entity_type': 'Organization', 'id': 'CNO-046'}
        team['relationships'] = [
            item for item in team['relationships']
            if not (item['relation'] == 'joint_team_member' and item['target'] == target)
        ]
        update_hash(changed_state, team)
        tests.append(('joint Team member removed', changed, changed_state))

        changed = copy.deepcopy(records)
        changed_state = copy.deepcopy(state)
        robot = next(item for item in changed if item['entity_type'] == 'Robot Platform' and item['id'] == 'CRP-013')
        robot['relationships'] = []
        update_hash(changed_state, robot)
        tests.append(('Robot Platform manufacturer removed', changed, changed_state))

        changed = copy.deepcopy(records)
        changed_state = copy.deepcopy(state)
        entry = next(item for item in changed if item['entity_type'] == 'Competition Entry' and item['id'] == 'E-005-04')
        entry['entry']['robot_id'] = None
        entry['relationships'] = [
            item for item in entry['relationships']
            if item['target'].get('entity_type') != 'Robot Platform'
        ]
        update_hash(changed_state, entry)
        tests.append(('reviewed Entry platform removed', changed, changed_state))

        passed = 0
        for label, changed, changed_state in tests:
            try:
                variant(changed, changed_state)
            except (ValueError, OSError, KeyError, TypeError, AttributeError):
                passed += 1
            else:
                raise ValueError('Negative control accepted: ' + label)
    else:
        passed = 0
    result = {
        'status': 'PASS',
        'immutable_imports': imports,
        'canonical_records': count,
        'negative_controls_passed': passed,
        'before': state['before'],
        'after': state['after'],
        'organizations_created': state['organizations_created'],
        'robot_platforms_created': state['robot_platforms_created'],
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--negative-checks', action='store_true')
    audit(parser.parse_args().negative_checks)
