#!/usr/bin/env python3
"""Validate canonical entity normalization and run mutation controls."""

import argparse
import copy
import json
import shutil
import tempfile
from pathlib import Path

from validate_research import (NORMALIZATION_STATE_NAME, ROOT, canonical_hash,
                               protected_entry_hash, validate)


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write(path,value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')


def update_hash(state,record):
    key=(record['entity_type'],record['id'])
    for field in ('records_added','records_updated'):
        for item in state[field]:
            if (item['entity_type'],item['id'])==key:
                item['after_sha256' if field=='records_updated' else 'sha256']=canonical_hash(record)
                return
    if record['entity_type']=='Competition Entry':
        state['records_updated'].append({
            'entity_type':record['entity_type'],'id':record['id'],
            'before_sha256':'negative-control-only',
            'after_sha256':canonical_hash(record),
            'protected_sha256':protected_entry_hash(record),
        })
        return
    raise ValueError('Mutation is outside the normalization declaration')


def variant(records,state):
    with tempfile.TemporaryDirectory(prefix='entity-normalization-negative-',dir=ROOT/'research/staging') as name:
        directory=Path(name)
        write(directory/'candidate.json',records)
        write(directory/NORMALIZATION_STATE_NAME,state)
        for filename in ('supplemental.json','master-v2-1.json','kimi-official-archive-import-actual.json',
                         'kimi-official-archive-final-import.json','kimi-image-result-transcription-import.json'):
            shutil.copyfile(ROOT/'research/evidence'/filename,directory/filename)
        validate(candidate=directory/'candidate.json',supplemental=directory/'supplemental.json')


def audit(negative_checks=False):
    imports,count=validate()
    records=read(ROOT/'research/evidence/records.json')
    state=read(ROOT/'research/evidence'/NORMALIZATION_STATE_NAME)
    tests=[]
    if negative_checks:
        changed=copy.deepcopy(records); changed_state=copy.deepcopy(state)
        entry=next(r for r in changed if r['entity_type']=='Competition Entry' and r['id']=='OEC-2026-0021')
        entry['entry']['team_id']='TR-005'
        entry['relationships'].append({'relation':'represented_by','target':{'entity_type':'Team','id':'TR-005'}})
        update_hash(changed_state,entry)
        tests.append(('measurement string promoted to Team',changed,changed_state))

        changed=copy.deepcopy(records); changed_state=copy.deepcopy(state)
        entry=next(r for r in changed if r['entity_type']=='Competition Entry' and r['id']=='E-004-01')
        entry['entry']['team_id']='TR-002'
        entry['relationships']=[r for r in entry['relationships'] if r['target']['entity_type']!='Team']
        entry['relationships'].append({'relation':'represented_by','target':{'entity_type':'Team','id':'TR-002'}})
        update_hash(changed_state,entry)
        tests.append(('reviewed alias remapped',changed,changed_state))

        changed=copy.deepcopy(records); changed_state=copy.deepcopy(state)
        entry=next(r for r in changed if r['entity_type']=='Competition Entry' and r['id']=='E-005-01')
        entry['entry']['ranking']='99'
        update_hash(changed_state,entry)
        tests.append(('protected result fact changed',changed,changed_state))

        changed=copy.deepcopy(records); changed_state=copy.deepcopy(state)
        team=next(r for r in changed if r['entity_type']=='Team' and r['id']=='CTN-001')
        team['label']='Altered derived identity'
        update_hash(changed_state,team)
        tests.append(('derived Team display name changed',changed,changed_state))

        passed=0
        for label,changed,changed_state in tests:
            try:
                variant(changed,changed_state)
            except (ValueError,OSError,KeyError,TypeError,AttributeError):
                passed+=1
            else:
                raise ValueError('Negative control accepted: '+label)
    else:
        passed=0
    result={'status':'PASS','immutable_imports':imports,'canonical_records':count,
            'negative_controls_passed':passed,'before':state['before'],'after':state['after'],
            'new_team_entities':state['new_team_entities'],
            'new_organization_entities':state['new_organization_entities'],
            'new_robot_platform_entities':state['new_robot_platform_entities']}
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return result


if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--negative-checks',action='store_true')
    audit(parser.parse_args().negative_checks)
