#!/usr/bin/env python3
"""Validate the reviewed image-result transcription import and controls."""
import argparse,copy,json,shutil,tempfile
from pathlib import Path
from validate_research import ROOT,canonical_hash,validate

STATE='kimi-image-result-transcription-import.json'
def read(p): return json.loads(p.read_text(encoding='utf-8'))
def write(p,v): p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def rehash(state,record):
    item=next(x for x in state['records_added'] if x['entity_type']==record['entity_type'] and x['id']==record['id'])
    item['sha256']=canonical_hash(record)
def variant(records,state):
    with tempfile.TemporaryDirectory(prefix='transcription-negative-',dir=ROOT/'research/staging') as name:
        d=Path(name);write(d/'candidate.json',records);write(d/STATE,state)
        for f in ('supplemental.json','master-v2-1.json','kimi-official-archive-import-actual.json',
                  'kimi-official-archive-final-import.json','canonical-entity-normalization.json'):
            source=ROOT/'research/evidence'/f
            if source.is_file():
                shutil.copyfile(source,d/f)
        validate(candidate=d/'candidate.json',supplemental=d/'supplemental.json')
def audit(negative=False):
    imports,count=validate();records=read(ROOT/'research/evidence/records.json');state=read(ROOT/'research/evidence'/STATE);tests=[]
    if negative:
        changed=copy.deepcopy(records);s=copy.deepcopy(state);r=next(x for x in changed if x['id']=='TR-050' and x['entity_type']=='Competition Entry');r['entry']['participation_status']='Started';rehash(s,r);tests.append(('bye upgraded to Started',changed,s))
        changed=copy.deepcopy(records);s=copy.deepcopy(state);r=next(x for x in changed if x['id']=='TR-051' and x['entity_type']=='Competition Entry');r['verification']['canonical_status']='Verified';rehash(s,r);tests.append(('Medium uncertainty upgraded',changed,s))
        changed=copy.deepcopy(records);s=copy.deepcopy(state);r=copy.deepcopy(next(x for x in changed if x['id']=='TR-051' and x['entity_type']=='Competition Entry'));r['id']='TR-058';changed.append(r);s['records_added'].append({'entity_type':r['entity_type'],'id':r['id'],'sha256':canonical_hash(r)});tests.append(('unresolved transcription promoted',changed,s))
        changed=copy.deepcopy(records);s=copy.deepcopy(state);r=next(x for x in changed if x['id']=='TR-001' and x['entity_type']=='Competition Entry');r['entry']['competition_id']='C-016';rehash(s,r);tests.append(('C-016 identity invented',changed,s))
        changed=copy.deepcopy(records);s=copy.deepcopy(state);changed.pop(next(i for i,x in enumerate(changed) if x['id']=='TR-001' and x['entity_type']=='Team'));tests.append(('reviewed Team dropped',changed,s))
        passed=0
        for label,r,s in tests:
            try: variant(r,s)
            except (ValueError,OSError,KeyError,TypeError,AttributeError): passed+=1
            else: raise ValueError('Negative control accepted: '+label)
    else: passed=0
    result={'status':'PASS','immutable_imports':imports,'canonical_records':count,'negative_controls_passed':passed,
            'rows_to_entries':state['rows_to_entries'],'participation_statuses':state['participation_statuses'],
            'new_entry_statuses':state['new_entry_statuses']};print(json.dumps(result,ensure_ascii=False,indent=2));return result
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--negative-checks',action='store_true');audit(p.parse_args().negative_checks)
