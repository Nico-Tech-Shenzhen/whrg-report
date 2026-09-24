#!/usr/bin/env python3
"""Validate the final official-archive import and run mutation controls."""

import argparse
import copy
import json
from pathlib import Path
import shutil
import tempfile

from validate_research import ROOT, canonical_hash, validate


STATE='kimi-official-archive-final-import.json'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write(path,value):
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')


def update_declared_hash(state,record):
    key=(record['entity_type'],record['id'])
    for field in ('records_added','records_updated'):
        for item in state[field]:
            if (item['entity_type'],item['id'])==key:
                item['sha256']=canonical_hash(record)
                return
    raise ValueError('Negative-control record is outside the reviewed import')


def validate_variant(records,state):
    staging=ROOT/'research/staging'
    staging.mkdir(parents=True,exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='negative-',dir=staging) as name:
        directory=Path(name)
        write(directory/'candidate.json',records)
        write(directory/STATE,state)
        for filename in ('supplemental.json','master-v2-1.json','kimi-official-archive-import-actual.json',
                         'kimi-image-result-transcription-import.json','canonical-entity-normalization.json'):
            source=ROOT/'research/evidence'/filename
            if source.is_file():
                shutil.copyfile(source,directory/filename)
        validate(candidate=directory/'candidate.json',supplemental=directory/'supplemental.json')


def audit(negative_checks=False):
    imports,record_count=validate()
    records=read(ROOT/'research/evidence/records.json')
    state=read(ROOT/'research/evidence'/STATE)
    controls=[]
    if negative_checks:
        variants=[]

        changed=copy.deepcopy(records); changed_state=copy.deepcopy(state)
        item=next(r for r in changed if r['id']=='OEC-2026-0405')
        item['entry']['ranking']='2'; update_declared_hash(changed_state,item)
        variants.append(('C-003 DNF given a rank',changed,changed_state))

        changed=copy.deepcopy(records); changed_state=copy.deepcopy(state)
        item=next(r for r in changed if r['id']=='E-005-04')
        item['entry']['ranking']='4'; update_declared_hash(changed_state,item)
        variants.append(('C-005 GMO old rank restored',changed,changed_state))

        changed=copy.deepcopy(records); changed_state=copy.deepcopy(state)
        item=next(r for r in changed if r['id']=='OEC-2026-0193')
        evidence=next(r['id'] for r in changed if r['entity_type']=='Evidence' and r.get('official_archive',{}).get('year')==2025)
        item['evidence_refs']=[{'entity_type':'Evidence','id':evidence}]
        update_declared_hash(changed_state,item)
        variants.append(('2025 Evidence used for 2026 Entry',changed,changed_state))

        changed=copy.deepcopy(records); changed_state=copy.deepcopy(state)
        item=next(r for r in changed if r['id']=='OEC-2026-0193')
        evidence=next(r['id'] for r in changed if r['entity_type']=='Evidence' and r.get('official_archive',{}).get('extraction_status')=='Image Only')
        item['evidence_refs']=[{'entity_type':'Evidence','id':evidence}]
        update_declared_hash(changed_state,item)
        variants.append(('image-only attachment used for Entry extraction',changed,changed_state))

        changed=copy.deepcopy(records); changed_state=copy.deepcopy(state)
        next(r for r in changed if r['id']=='E-005-05')['entry']['ranking']='1'
        variants.append(('undeclared v2.1 base mutation',changed,changed_state))

        changed=copy.deepcopy(records); changed_state=copy.deepcopy(state)
        changed.pop(next(i for i,r in enumerate(changed) if r['id']=='ATT-0001'))
        variants.append(('accepted Evidence dropped',changed,changed_state))

        changed=copy.deepcopy(records); changed_state=copy.deepcopy(state)
        next(r for r in changed if r['id']=='OEC-2026-0193')['verification']['canonical_status']='Research Lead'
        variants.append(('reviewed official Entry demoted without declaration',changed,changed_state))

        for label,changed,changed_state in variants:
            try:
                validate_variant(changed,changed_state)
            except (ValueError,OSError,KeyError,TypeError,AttributeError):
                controls.append(label)
            else:
                raise ValueError('Negative control was accepted: '+label)
    result={'status':'PASS','immutable_imports':imports,'canonical_records':record_count,
            'negative_controls_passed':len(controls),'controls':controls,
            'evidence_disposition':state['evidence_disposition'],
            'entry_summary':state['entry_summary'],'canonical_entry_counts':state['canonical_entry_counts']}
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--negative-checks',action='store_true')
    args=parser.parse_args()
    audit(args.negative_checks)


if __name__=='__main__':
    main()
