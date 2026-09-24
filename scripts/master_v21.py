"""Map reviewed Master v2.1 semantics without changing its schema or crosswalk."""
from collections import Counter
import copy
import hashlib
import json
from pathlib import Path

from research_schema import workbook_rows

CHECKPOINT = 'research/checkpoints/kimi-master-v2-1/migration.json'
STATE_NAME = 'master-v2-1.json'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition, message):
    if not condition:
        raise ValueError(message)


def record_key(item):
    return item['entity_type'],item['id']


def supplemental_key(item):
    if item['id'] is not None:
        return item['record_type'],item['id']
    source=item['provenance'][0]
    return item['record_type'],source['path'],source['locator']


def asset_path(root, asset):
    path=(root/asset['path']).resolve()
    require(path.is_relative_to(root.resolve()),'Migration asset outside repository')
    require(sha(path)==asset['sha256'],'Changed migration history: '+asset['path'])
    return path


def table_rows(path):
    output={}
    for name,rows in workbook_rows(path).items():
        output[name]=[{header:row.get(c) for c,header in rows[1].items()}
                      for n,row in sorted(rows.items()) if n>1]
    return output


def load_bundle(root):
    checkpoint=root/CHECKPOINT
    manifest=read(checkpoint)
    require(manifest['schema_version']=='2.1','Unexpected migration version')
    assets={name:asset_path(root,asset) for name,asset in manifest['assets'].items()}
    original=read(assets['previous_records'])
    supplemental=read(assets['previous_supplemental'])
    decision=read(assets['gmo_review'])
    require(decision['previous_status']=='Verified' and decision['final_status']=='Research Lead',
            'Narrow verification review must be a downgrade')
    require(decision['entry_id']=='E-005-04','Narrow review scope changed')
    require(decision['evidence_by_source_class']=={
        'Primary Web Evidence':[], 'Secondary / media evidence':['EV-ESM-005A'],
        'Field Evidence':['FP-002']},'GMO source classification changed')
    require(decision['policy_allows_this_secondary_support_as_verified'] is False,
            'Unsupported secondary-evidence verification allowance')
    tables=table_rows(assets['workbook'])
    # Frozen candidate checksum is the review boundary. Do not reconsider matches.
    return {'manifest':manifest,'assets':assets,'original':original,
            'supplemental':supplemental,'decision':decision,'tables':tables,
            'checkpoint_sha256':sha(checkpoint)}


def derive(bundle):
    """Apply the already-reviewed crosswalk and the single GMO status amendment."""
    original=bundle['original']; tables=copy.deepcopy(bundle['tables'])
    decision=bundle['decision']; manifest=bundle['manifest']
    entry_rows={r['Entry ID']:r for r in tables['Competition Entry Map']}
    crosswalk={r['Historical ID']:r['Candidate ID'] for r in tables['ID Crosswalk']}
    require(len(crosswalk)==35 and len(set(crosswalk.values()))==22,'Frozen crosswalk coverage differs')
    historical={r['id']:r for r in original if r['entity_type']=='Competition Entry'}
    require(set(crosswalk)==set(historical),'Historical IDs differ from frozen crosswalk')
    output=[]
    for item in original:
        if item['entity_type']!='Competition Entry':
            output.append(copy.deepcopy(item)); continue
        if crosswalk[item['id']]!=item['id']:
            continue
        row=entry_rows[item['id']]
        record=copy.deepcopy(item)
        record.pop('possible_duplicate_ids',None)
        record['historical_entry_ids']=[k for k,v in crosswalk.items() if v==item['id']]
        record['entry_histories']=[copy.deepcopy(historical[k]) for k in record['historical_entry_ids']]
        record['historical_provenance']=json.loads(row['Provenance JSON'])
        record['evidence_refs']=[{'entity_type':'Evidence','id':e} for e in row['Evidence IDs'].split(',')]
        record['entry'].update({'participation_status':row['Participation Status'],
             'group':row['Group or Heat'],'notes':row['Notes'],
             'evidence_text':row['Evidence IDs']})
        verification=record['verification']
        verification['canonical_status']=row['Verification Status']
        verification['basis']=row['Verification Basis']
        if item['id']==decision['entry_id']:
            verification['previous_inherited_verification']=copy.deepcopy(item['verification'])
            verification['canonical_status']=decision['final_status']
            verification['basis']=decision['reason']
            verification['policy_adjustment']={'reason':decision['reason'],
                 'evidence_refs':copy.deepcopy(record['evidence_refs']),
                 'review':manifest['assets']['gmo_review']}
            row['Verification Status']=decision['final_status']
            row['Verification Basis']=decision['reason']
        output.append(record)
    for row in tables['Verification Review']:
        if row['Entry ID']==decision['entry_id']:
            row['Candidate Status']=decision['final_status']
            row['Decision']='Downgrade after narrow existing-evidence policy review'
            row['Basis']=decision['reason']
    for row in tables['Unresolved Mappings']:
        if row['Supplied ID']==decision['entry_id'] and row['Gap Type']=='verification_and_ranking_scope':
            row['Details JSON or Text']='Verification decision completed: Research Lead. Underlying source support and overall rank 4 versus Group 2 rank 3 remain unresolved. Previous inherited Verified metadata remains in the frozen workbook and Entry histories.'
    names=['Competition Entry Map','ID Crosswalk','Evidence Map','Entry Source Map',
           'Count Claims','Date Semantics','Unresolved Mappings','Verification Review','Schema']
    state={'schema_version':'2.1','checkpoint':{'path':CHECKPOINT,'sha256':bundle['checkpoint_sha256']},
           'tables':{name:tables[name] for name in names}}
    return output,copy.deepcopy(bundle['supplemental']),state


def validate_migration(root,records,supplemental,state):
    require(state.get('schema_version')=='2.1','Unknown canonical Master semantics')
    require(state.get('checkpoint',{}).get('path')==CHECKPOINT,'Unexpected checkpoint authority')
    require(state['checkpoint']['sha256']==sha(root/CHECKPOINT),'Checkpoint declaration changed')
    bundle=load_bundle(root)
    expected_records,expected_supplemental,expected_state=derive(bundle)
    expected_by_key={record_key(r):r for r in expected_records}
    actual_by_key={record_key(r):r for r in records}
    require(len(actual_by_key)==len(records),'Duplicate canonical record key')
    require({key:actual_by_key.get(key) for key in expected_by_key}==expected_by_key,
            'Canonical migration differs from reviewed workbook plus GMO-only amendment')
    expected_extra={supplemental_key(r):r for r in expected_supplemental}
    actual_extra={supplemental_key(r):r for r in supplemental}
    require(len(actual_extra)==len(supplemental),'Duplicate supplemental record key')
    require({key:actual_extra.get(key) for key in expected_extra}==expected_extra,
            'Migration changed original supplemental payloads')
    require(state==expected_state,'Master v2.1 schema, crosswalk, dates, counts, or unresolved mappings changed')
    base_records=[actual_by_key[key] for key in expected_by_key]
    statuses=Counter(r['verification']['canonical_status'] for r in base_records if r['entity_type']=='Competition Entry')
    require(statuses=={'Verified':16,'Research Lead':6},'Reviewed verification counts differ')
    # All 35 full historical records remain reconstructable inside the 22 identities.
    archived=[h for r in base_records if r['entity_type']=='Competition Entry' for h in r['entry_histories']]
    old=[r for r in bundle['original'] if r['entity_type']=='Competition Entry']
    require({r['id']:r for r in archived}=={r['id']:r for r in old} and len(archived)==35,
            'A historical Entry payload was lost')
    retired={r['Historical ID'] for r in state['tables']['ID Crosswalk'] if r['Historical ID']!=r['Candidate ID']}
    return {'retired_ids':retired,'reviewed_statuses':{bundle['decision']['entry_id']:bundle['decision']['final_status']},
            'counts':{'Verified':statuses['Verified'],'Research Lead':statuses['Research Lead'],'Unresolved':0},
            'base_record_keys':set(expected_by_key),'base_supplemental_keys':set(expected_extra)}
