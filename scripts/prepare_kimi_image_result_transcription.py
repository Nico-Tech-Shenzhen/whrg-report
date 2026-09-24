#!/usr/bin/env python3
"""Build and promote the reviewed manual image-result transcription import."""
import argparse,copy,hashlib,json,re,shutil,unicodedata
from collections import Counter,defaultdict
from pathlib import Path

from research_schema import column_name,workbook_rows
from validate_research import validate

ROOT=Path(__file__).resolve().parents[1]
SOURCE=ROOT/'research/inbox/kimi/whrg-image-result-transcription-2026.xlsx'
ARCHIVE='research/imported/kimi/25436a04e14d414673c412c50b6033532ed5eb97b4b90ff1b4efe27ae7c5fa00/whrg-image-result-transcription-2026.xlsx'
STAGING=ROOT/'research/staging/kimi-image-result-transcription-import'
REVIEW=ROOT/'research/reviews/kimi-image-result-transcription-import'
STATE='kimi-image-result-transcription-import.json'
UNRESOLVED={'TR-056':'Low-confidence team/organization text remains unreadable',
            'TR-058':'Medium-confidence team name is visibly truncated; not silently normalized',
            'TR-079':'Low-confidence organization and bye-only bracket placement',
            'TR-082':'Low-confidence team name is incomplete and organization-only text is not an Entry identity',
            'TR-089':'Low-confidence team transcription is not independently resolvable'}

def read(p): return json.loads(p.read_text(encoding='utf-8'))
def write(p,v): p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
def digest(v): return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def nkey(v): return re.sub(r'\s+','',unicodedata.normalize('NFKC',str(v or ''))).casefold()
def weight(row):
    m=re.search(r'(40|58|80)KG',str(row.get('Document Header') or ''))
    return m.group(0) if m else None
def source_row(number,row):
    book=workbook_rows(ROOT/ARCHIVE)['Transcription'];header=book[1];values=book[number];width=max(max(header),max(values))
    return {'path':ARCHIVE,'locator':f"'Transcription'!A{number}:{column_name(width)}{number}",
            'source_id':row['Transcription ID'],'sheet':'Transcription','row':number,'id_column':1,
            'headers':[header.get(c) for c in range(1,width+1)],'values':[values.get(c) for c in range(1,width+1)],'header_row':1}
def prov(row): return {k:row[k] for k in ('path','locator','source_id')}
def final_status(group):
    if any(r['Participation Status']=='Finished' for _,r in group): return 'Finished'
    special=next((r['Participation Status'] for _,r in group if r['Participation Status'] in ('DNS','DNF')),None)
    if special: return special
    for _,r in group:
        note=str(r.get('Uncertainty / Notes') or '')
        if any(x in note for x in ('WP','RSC','KO','1/4决赛','1/8决赛')) and '轮空' not in note and 'ABD' not in note:
            return 'Started'
    return 'Scheduled'

def build(write_canonical=False):
    existing=read(ROOT/'research/evidence/records.json');before=len(existing)
    by_key={(r['entity_type'],r['id']):r for r in existing}
    if any(r['entity_type']=='Competition Entry' and r['entry']['competition_id'] in {'C-001','C-002','C-017','C-022','C-028'} for r in existing):
        raise ValueError('Target competitions unexpectedly already have canonical Entries')
    book=workbook_rows(SOURCE)['Transcription'];header=book[1]
    rows=[(n,{header[c]:book[n].get(c) for c in header}) for n in sorted(book) if n>1]
    if len(rows)!=91: raise ValueError('Expected 91 transcription rows')
    manifest=read(ROOT/'research/imported/kimi/manifest.json')
    input_item=next(x for x in manifest if x['path']==ARCHIVE)
    # Verify every attachment lineage and payload hash against canonical Evidence.
    for _,row in rows:
        ev=by_key.get(('Evidence',row['Attachment ID']))
        if not ev or ev.get('official_archive',{}).get('sha256')!=row['Source SHA-256'] or Path(ev['official_archive']['archive_path']).name!=row['Source Filename']:
            raise ValueError('Transcription attachment lineage mismatch: '+row['Transcription ID'])
        if row['Competition ID'] not in {'C-001','C-002','C-017','C-022','C-028'}:
            raise ValueError('Unexpected transcription Competition ID')
    accepted=[(n,r) for n,r in rows if r['Transcription ID'] not in UNRESOLVED]
    entry_groups=defaultdict(list)
    for n,row in accepted:
        entry_groups[(row['Competition ID'],nkey(row['Team Name (normalized)']),weight(row) if row['Competition ID']=='C-028' else None)].append((n,row))
    team_groups=defaultdict(list)
    for n,row in accepted: team_groups[nkey(row['Team Name (normalized)'])].append((n,row))
    if len(entry_groups)!=79 or len(team_groups)!=68: raise ValueError('Reviewed normalization counts changed')
    teams=[];team_id={}
    for key,group in sorted(team_groups.items(),key=lambda x:min(n for n,_ in x[1])):
        n,row=min(group,key=lambda x:x[0]);identity=row['Transcription ID'];team_id[key]=identity
        sr=[source_row(nn,rr) for nn,rr in group];origin=prov(sr[0])
        evidence=sorted({rr['Attachment ID'] for _,rr in group})
        teams.append({'id':identity,'label':row['Team Name (normalized)'],'status':'unverified','provenance':[origin],
            'evidence_refs':[{'entity_type':'Evidence','id':e} for e in evidence], 'relationships':[],
            'unresolved_references':[],'source_rows':sr,'entity_type':'Team',
            'team':{'name':row['Team Name (normalized)'],'organization_as_shown':row.get('Organization (as shown)'),
                    'identity_note':'Stable official result identity; no Organization ID inferred.'}})
    entries=[];decisions=[]
    for key,group in sorted(entry_groups.items(),key=lambda x:min(n for n,_ in x[1])):
        preferred=[x for x in group if x[1]['Participation Status']=='Finished'] or group
        n,row=min(preferred,key=lambda x:x[0]);identity=row['Transcription ID'];sr=[source_row(nn,rr) for nn,rr in group]
        origin=prov(next(x for x in sr if x['source_id']==identity));confidence='High' if all(rr['Confidence']=='High' for _,rr in group) else 'Medium'
        canonical='Verified' if confidence=='High' else 'Research Lead';status=final_status(group)
        evidence=sorted({rr['Attachment ID'] for _,rr in group});tid=team_id[nkey(row['Team Name (normalized)'])]
        result_row=next((rr for _,rr in group if rr['Participation Status']=='Finished'),row)
        entries.append({'id':identity,'label':row['Team Name (normalized)'],'status':'unverified','provenance':[origin],
            'evidence_refs':[{'entity_type':'Evidence','id':e} for e in evidence],
            'relationships':[{'relation':'entered','target':{'entity_type':'Competition','id':row['Competition ID']}},
                             {'relation':'entered_by','target':{'entity_type':'Team','id':tid}}],
            'unresolved_references':[],'source_rows':sr,'entity_type':'Competition Entry',
            'entry':{'competition_id':row['Competition ID'],'team_id':tid,'organization_id':None,'country':None,
                'team_name':row['Team Name (normalized)'],'organization_name':row.get('Organization (as shown)'),
                'organization_type':None,'robot_id':None,'robot_manufacturer':None,'robot_model':None,
                'robot_ownership':None,'control_mode':None,'result':result_row.get('Result'),
                'ranking':str(result_row['Ranking']) if result_row.get('Ranking') is not None else None,
                'evidence_text':','.join(evidence),'participation_status':status,'group':weight(row) or row.get('Group/Heat/Lane/Seed'),
                'notes':'Manual visual transcription; bracket/result rows retained in transcription_history.'},
            'entry_history':{'Confidence':row['Confidence']},
            'transcription_history':[{'transcription_id':rr['Transcription ID'],'verbatim':rr['Transcribed Text (verbatim)'],
                'reported_status':rr['Participation Status'],'confidence':rr['Confidence'],'uncertainty':rr.get('Uncertainty / Notes')}
                for _,rr in group],
            'verification':{'reported_status':canonical,'authority':'Independent review','independent_status':'reviewed_official_event',
                'source_confidence':row['Confidence'],'origin':origin,'canonical_status':canonical,
                'basis':'Official-Event image directly supports the Entry identity; confidence and uncertainty are retained.'}})
        for _,rr in group:
            decisions.append({'transcription_id':rr['Transcription ID'],'effect':'C','canonical_entry_id':identity,
                              'team_id':tid,'disposition':'identity row' if rr['Transcription ID']==identity else 'duplicate bracket/result row retained as history'})
    for _,row in rows:
        if row['Transcription ID'] in UNRESOLVED:
            decisions.append({'transcription_id':row['Transcription ID'],'effect':'D','canonical_entry_id':None,'team_id':None,
                              'disposition':UNRESOLVED[row['Transcription ID']]})
    decisions.sort(key=lambda x:x['transcription_id']);additions=teams+entries;candidate=existing+additions
    counts=Counter(r['verification']['canonical_status'] for r in candidate if r['entity_type']=='Competition Entry')
    write(REVIEW/'decisions.json',decisions)
    state={'schema_version':'1','import_id':'kimi-image-result-transcription-import',
           'review_path':'research/reviews/kimi-image-result-transcription-import/review.md',
           'decision_path':'research/reviews/kimi-image-result-transcription-import/decisions.json','inputs':[input_item],
           'records_added':[{'entity_type':r['entity_type'],'id':r['id'],'sha256':digest(r)} for r in additions],
           'rows_to_entries':{'rows':91,'entries':79,'teams':68,'unresolved_rows':5,'duplicate_rows':7},
           'by_competition':{'C-001':{'rows':5,'entries':5},'C-002':{'rows':5,'entries':5},
                'C-017':{'rows':10,'entries':10},'C-022':{'rows':17,'entries':17},'C-028':{'rows':54,'entries':42}},
           'participation_statuses':dict(Counter(e['entry']['participation_status'] for e in entries)),
           'new_entry_statuses':dict(Counter(e['verification']['canonical_status'] for e in entries)),
           'canonical_entry_counts':{'Verified':counts['Verified'],'Research Lead':counts['Research Lead'],'Unresolved':0}}
    write(STAGING/'candidate.json',candidate);write(STAGING/STATE,state)
    for name in ('supplemental.json','master-v2-1.json','kimi-official-archive-import-actual.json','kimi-official-archive-final-import.json'):
        shutil.copyfile(ROOT/'research/evidence'/name,STAGING/name)
    review=f'''# Kimi image-result transcription import review

## Input and provenance

- Input: `whrg-image-result-transcription-2026.xlsx`
- SHA-256: `25436a04e14d414673c412c50b6033532ed5eb97b4b90ff1b4efe27ae7c5fa00`
- 91 rows were checked for Competition ID, Evidence ID, Attachment ID, source filename/SHA-256, page/order, verbatim text, normalized fields, and confidence. Every attachment exists in the immutable official archive and every supplied SHA-256 matches its canonical attachment Evidence. No OCR or web research was performed.
- No Evidence record was added: the transcription reuses the existing Official-Event attachment IDs and retains the workbook as extraction provenance.

## Normalization

| Competition | Rows | Unique Entries |
| --- | ---: | ---: |
| C-001 | 5 | 5 |
| C-002 | 5 | 5 |
| C-017 | 10 | 10 |
| C-022 | 17 | 17 |
| C-028 | 54 | 42 |
| **Total** | **91** | **79** |

Seven repeated C-028 bracket/final rows were folded into identity-level Entries and retained in `transcription_history`. Five uncertain rows were excluded, producing a net reduction of 12 rows. C-016 remains at zero: no official result row was recovered.

## Participation and uncertainty

- Canonical participation after identity normalization: Finished 41, Started 10, Scheduled 20, DNS 7, DNF 1.
- Kimi's 42 `Started` rows became 10 actual starts, 20 bracket-only `Scheduled` identities, 7 rows folded into later Finished identities, and 5 unresolved rows. Byes and opponent forfeits alone were not treated as starts.
- The 11 Medium and 4 Low C-028 rows were reviewed individually. Ten Medium rows are retained as Research Leads with their `[UNCERTAIN: ...]` text. `TR-058` and all four Low rows (`TR-056`, `TR-079`, `TR-082`, `TR-089`) remain unresolved and create neither Team nor Entry. Exact decisions: [decisions.json](decisions.json).

## Canonical effects

- Existing Team IDs reused: 0; the seven pre-existing Team identities do not exactly match these entries.
- New Team identities: 68. Similar names were not merged; Organization IDs were not inferred.
- New Competition Entries: 79 (69 Verified, 10 Research Lead).
- Canonical records: 1,208 -> 1,355; Entries: 691 -> 770; Teams: 7 -> 75; Evidence: 447 -> 447.
- Canonical Entry statuses: Verified 689 -> 758; Research Lead 2 -> 12.

## QA gate

Promotion requires repository validators, import/negative controls, frozen v2.1 and checkpoint audits, unit tests, strict MkDocs, PDF build, and Git diff checks to pass. This import is committed separately and is not pushed.
'''
    (REVIEW/'review.md').write_text(review,encoding='utf-8',newline='\n')
    validate(candidate=STAGING/'candidate.json',supplemental=STAGING/'supplemental.json')
    if write_canonical:
        shutil.copyfile(STAGING/'candidate.json',ROOT/'research/evidence/records.json')
        shutil.copyfile(STAGING/STATE,ROOT/'research/evidence'/STATE);validate()
    print(json.dumps({'entries':79,'teams':68,'unresolved':5,'duplicates':7,'statuses':state['participation_statuses'],
                      'verification':state['new_entry_statuses'],'records_after':len(candidate)},ensure_ascii=False,indent=2))

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--write',action='store_true');build(p.parse_args().write)
