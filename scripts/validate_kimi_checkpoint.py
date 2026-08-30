"""Reconcile the first checkpoint against its snapshots, without checking web truth."""
import argparse
from collections import Counter
import json
from pathlib import Path
import re

from research_schema import workbook_rows
from validate_research import ROOT, validate

MASTER = 'WHRG_2026_Master.xlsx'

def audit(directory):
    directory=directory.resolve()
    records_path=directory/('candidate.json' if directory.name=='staging' else 'records.json')
    validate(candidate=records_path if directory.name=='staging' else None)
    records=json.loads(records_path.read_text(encoding='utf-8'))
    supplemental=json.loads((directory/'supplemental.json').read_text(encoding='utf-8'))
    manifest=json.loads((ROOT/'research/imported/kimi/manifest.json').read_text(encoding='utf-8'))
    master=next(m['path'] for m in manifest if m['original_name']==MASTER)
    rows=workbook_rows(ROOT/master)
    items=records+supplemental
    all_sources=[s for item in items for s in item['source_rows']]
    # Exact coverage of every populated workbook row, including context/templates.
    for imported in manifest:
        if not imported['path'].endswith('.xlsx'): continue
        book=workbook_rows(ROOT/imported['path'])
        expected={(sheet,row) for sheet,table in book.items() for row in table}
        actual={(s['sheet'],s['row']) for s in all_sources if s['path']==imported['path']}
        if expected!=actual:
            raise ValueError(f'Lost or invented workbook rows: {imported["original_name"]}')
    # Every actual text ID remains its own identity (repeated facets are not new IDs).
    found_ids={s['source_id'] for s in all_sources if s['source_id'] is not None}
    entity_ids={r['id'] for r in items if r['id'] is not None}
    if found_ids!=entity_ids:
        raise ValueError('Source ID inventory differs from preserved entity/auxiliary identities')
    entries=[r for r in records if r['entity_type']=='Competition Entry']
    evidence=[r for r in records if r['entity_type']=='Evidence']
    master_evidence=[r for r in evidence if r['source_rows'][0]['path']==master]
    master_questions=[r for r in supplemental if r['record_type']=='question' and r['source_rows'][0]['path']==master]
    expected_counts={'entries':35,'master_evidence':100,'master_questions':31}
    observed={'entries':len(entries),'master_evidence':len(master_evidence),'master_questions':len(master_questions)}
    if observed!=expected_counts:
        raise ValueError(f'Checkpoint expectations differ from observed records: {observed}')
    # The expected facts are comparisons to source rows, never extraction constants.
    if {r['id'] for r in entries}!={v[1] for n,v in rows['Competition Entry Map'].items() if n>=5}:
        raise ValueError('Master entry IDs changed')
    status=Counter(r['verification']['reported_status'] for r in entries)
    if status!={'Verified':32,'Research Lead':3}:
        raise ValueError(f'Historical verification split changed: {status}')
    c042=[r for r in entries if r['entry']['competition_id']=='C-042']
    if len(c042)!=3 or any(r['verification']['reported_status']!='Research Lead' for r in c042):
        raise ValueError('C-042 leads counted as verified')
    for item in entries:
        v=item['source_rows'][0]['values']
        for key,column in [('competition_id',1),('team_name',5),('organization_name',6),
                           ('robot_model',10),('result',13),('ranking',14),('evidence_text',15)]:
            if item['entry'][key]!=v[column]:
                raise ValueError(f'Entry field mapping mismatch: {item["id"]}/{key}')
    for item in master_questions:
        v=item['source_rows'][0]['values']
        if item['question']['question']!=v[2 if item['id'].startswith('UQ-') else 1]:
            raise ValueError('Mixed Master question layouts collapsed')
    count=next(i for i in supplemental if i['record_type']=='competition_count_summary')['competition_count_summary']
    if count['Total teams stated (reported)']!='34' or count['Count Type']!='Reported (Media)':
        raise ValueError('C-005 count qualification changed')
    if not count['Recoverability'].startswith('Medium'):
        raise ValueError('C-005 historical recoverability differs')
    c021=next(i for i in supplemental if i['record_type']=='entry_recovery_summary' and i['id']=='C-021')
    if c021['entry_recovery_summary']['recoverability']!='Low':
        raise ValueError('C-021 batch assessment differs')
    if any(r['status']=='verified' for r in records):
        raise ValueError('Import has unexpectedly claimed independent verification')
    field=[r for r in evidence if r['id'].startswith(('FP-','UF-'))]
    if len(field)!=42 or any(r['evidence_kind']!='field_evidence' for r in field):
        raise ValueError('Field evidence/search leads changed')
    index={r['id']:r for r in evidence}
    field_only=[r['id'] for r in entries if r['evidence_refs'] and
                all(index[ref['id']]['evidence_kind']=='field_evidence' for ref in r['evidence_refs'])]
    # Similar entry names are flagged without using them as identity keys.
    pairs={tuple(sorted([r['id'],other])) for r in entries for other in r.get('possible_duplicate_ids',[])}
    missing={ref['id'] for r in items for ref in r['unresolved_references'] if ref['id'] not in index}
    result={'snapshots':len(manifest),'entities':len(records),'supplemental_records':len(supplemental),
            'distinct_preserved_ids':len(entity_ids),'master_counts':observed,
            'reported_entry_status':dict(status),'independently_verified':0,
            'field_evidence_records':len(field),'field_only_entry_ids':field_only,
            'possible_duplicate_pairs':len(pairs),'absent_evidence_ids':sorted(missing),
            'historical_C005_count':count['Total teams stated (reported)'],
            'historical_C005_count_type':count['Count Type'],
            'historical_C005_recoverability':count['Recoverability'],
            'historical_C021_recoverability':c021['entry_recovery_summary']['recoverability'],
            'master_verification_column_present':'Verification Status' in rows['Competition Entry Map'][3].values(),
            'master_recoverability_sheet_present':'Entry Source Map' in rows,
            'structural_status':'PASS','factual_review':'not_performed'}
    print(json.dumps(result,ensure_ascii=True,indent=2))
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory',type=Path,default=ROOT/'research/evidence')
    args=parser.parse_args()
    audit(args.directory)
