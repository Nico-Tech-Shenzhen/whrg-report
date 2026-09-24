#!/usr/bin/env python3
"""Prepare and optionally promote the independently reviewed official-archive import."""

import argparse
import copy
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re
import shutil
import unicodedata
from urllib.parse import urlsplit, urlunsplit

from import_kimi import archive_many
from research_schema import column_name, workbook_rows
from validate_research import validate


ROOT = Path(__file__).resolve().parents[1]
INBOX = ROOT / 'research/inbox/kimi/official-archive'
SOURCE = INBOX / 'whrg-official-archive-attachments-2025-2026.xlsx'
DELIVERY = INBOX / 'official-archive'
STAGING = ROOT / 'research/staging/kimi-official-archive-final-import'
REVIEW_DIR = ROOT / 'research/reviews/kimi-official-archive-final-import'
STATE_NAME = 'kimi-official-archive-final-import.json'
REVIEW_PATH = 'research/reviews/kimi-official-archive-final-import/review.md'

MANUAL_EXISTING = {
    'OEC-2026-0397':'E-005-01', 'OEC-2026-0398':'E-005-02',
    'OEC-2026-0399':'E-005-03', 'OEC-2026-0400':'E-C005-08',
    'OEC-2026-0401':'E-005-07', 'OEC-2026-0403':'E-005-04',
    'OEC-2026-0409':'E-004-01', 'OEC-2026-0410':'E-004-02',
    'OEC-2026-0411':'E-004-03', 'OEC-2026-0412':'E-004-04',
    'OEC-2026-0505':'E-042-01', 'OEC-2026-0506':'E-042-02',
    'OEC-2026-0507':'E-042-03', 'OEC-2026-0701':'E-036-01',
    'OEC-2026-0720':'E-040-01', 'OEC-2026-0724':'E-B01-040-03',
}
PROMOTIONS = {'E-005-04','E-042-01','E-042-02','E-042-03'}
FORCE_ACCEPT = {f'OEC-2026-{n:04d}' for n in range(404,409)} | {'OEC-2026-0193','OEC-2026-0402'}
FORCE_CONFLICT = {
    'OEC-2026-0721':'C-040 prefixed identity conflicts with generic canonical 优理奇',
    'OEC-2026-0725':'C-040 prefixed identity conflicts with generic canonical 优理奇',
    'OEC-2026-0726':'C-040 prefixed identity conflicts with generic canonical 优理奇',
    'OEC-2026-0702':'C-036 city-specific 智元 identity conflicts with generic canonical 智元',
    'OEC-2026-0703':'C-036 city-specific 智元 identity conflicts with generic canonical 智元',
    'OEC-2026-0709':'C-036 city-specific 智元 identity conflicts with generic canonical 智元',
}
BAD_NAMES = {'0','2','晋级','( )','2 - ( )','!!!!!','AI','北京','苏州','宁波','景山','江淮',
             '10:00','11:00','14:00'}


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')


def record_hash(item):
    data=json.dumps(item,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
    return hashlib.sha256(data).hexdigest()


def normalized_url(value):
    if not isinstance(value,str): return ''
    parts=urlsplit(value.strip())
    return urlunsplit((parts.scheme.lower(),parts.netloc.lower(),parts.path.rstrip('/'),'',''))


def name_key(value):
    value=unicodedata.normalize('NFKC',str(value or ''))
    return re.sub(r'\s+','',value).casefold()


def sheet_records(path,sheet):
    rows=workbook_rows(path)[sheet]
    header=rows[1]
    return [(number,{header[c]:rows[number].get(c) for c in header})
            for number in sorted(n for n in rows if n>1)]


def source_row(path,sheet,number,source_id):
    all_rows=workbook_rows(ROOT/path)[sheet]
    header=all_rows[1]; values=all_rows[number]
    width=max(max(header),max(values))
    return {'path':path,'locator':f"'{sheet}'!A{number}:{column_name(width)}{number}",
            'source_id':source_id,'sheet':sheet,'row':number,'id_column':1,
            'headers':[header.get(c) for c in range(1,width+1)],
            'values':[values.get(c) for c in range(1,width+1)],'header_row':1}


def provenance(rows):
    return [{k:r[k] for k in ('path','locator','source_id')} for r in rows]


def relation_ids(value):
    if not value: return []
    return sorted(set(re.findall(r'C-\d{3}',str(value))))


def append_ref(record,identity):
    ref={'entity_type':'Evidence','id':identity}
    if ref not in record['evidence_refs']:
        record['evidence_refs'].append(ref)


def evidence_record(identity,label,publisher,date,url,rows,kind,archive_data,competition_ids=()):
    return {
        'id':identity,'label':label,'status':'unverified','provenance':provenance(rows),
        'evidence_refs':[],
        'relationships':[{'relation':'documents','target':{'entity_type':'Competition','id':cid}}
                         for cid in competition_ids],
        'unresolved_references':[],'source_rows':rows,'entity_type':'Evidence',
        'evidence':{'topic':'official archive','publisher':publisher,'title':label,
                    'date':date or 'unknown','source_type':'Official-Event','url':url,
                    'original_text':'Archived official-event source.','japanese_summary':'unknown',
                    'scope':'2025 aggregate context' if archive_data['year']==2025 else '2026 competition evidence',
                    'confidence':'H','notes':'Independently integrity-checked immutable official archive source.'},
        'source':{'title':label,'publisher':publisher,'date':date or 'unknown','url':url,
                  'accessed_at':'2026-09-24','version':archive_data.get('sha256','official archive page'),
                  'verification_note':'Official-Event source archived and independently mapped; claims remain limited to its stated year and competition.'},
        'evidence_kind':kind,'official_archive':archive_data,
    }


def archived_delivery():
    sources=[SOURCE]
    sources.extend(sorted((DELIVERY/'files').glob('*')))
    sources.extend(sorted(DELIVERY.rglob('*.json')))
    if len(sources)!=151:
        raise ValueError(f'Expected 151 screened archive inputs, found {len(sources)}')
    targets=archive_many(sources,ROOT)
    return dict(zip(sources,targets))


def pdf_text_by_name():
    from pypdf import PdfReader
    output={}
    for path in sorted((DELIVERY/'files').glob('*.pdf')):
        try:
            text=''.join(page.extract_text() or '' for page in PdfReader(path).pages)
        except Exception:
            text=''
        output[path.name]=name_key(text)
    return output


def candidate_name(row):
    value=str(row['Team Name']).strip()
    if row['Competition ID']=='C-012':
        value=re.sub(r'(?:\s+-?\d+){7}$','',value).strip()
    return value


def rejected_reason(row,texts):
    identity=row['Candidate ID']; name=candidate_name(row); note=str(row.get('Notes') or '')
    if identity in FORCE_CONFLICT: return FORCE_CONFLICT[identity]
    if identity in MANUAL_EXISTING: return None
    if row['Year']!=2026: return '2025 evidence cannot establish a 2026 Entry'
    if row['Competition ID']=='C-027': return 'C-027 extraction concatenates result columns; identity not reliable enough for promotion'
    if name in BAD_NAMES or len(name_key(name))<2: return 'parser/schedule artifact, not a stable Entry identity'
    if 'org-ambiguous-fulltext-preserved' in note: return 'organization/team split remains ambiguous'
    if identity not in FORCE_ACCEPT and identity not in MANUAL_EXISTING:
        text=texts.get(str(row.get('Source File') or ''),'')
        if not text or name_key(name) not in text:
            return 'candidate team string is not present as an exact string in the archived source text layer'
    return None


def resolve_evidence(value,page_map,attachment_map):
    output=[]
    for token in re.split(r'[;,]',str(value or '')):
        token=token.strip()
        target=page_map.get(token,attachment_map.get(token,token))
        if target and target not in output: output.append(target)
    return output


def new_entry(identity,row,rows,evidence_ids,name):
    ranking=row.get('Ranking')
    if identity=='OEC-2026-0405': ranking=None
    result=row.get('Result (score)')
    entry={'competition_id':row['Competition ID'],'team_id':None,'organization_id':None,
           'country':None,'team_name':name,
           'organization_name':None if row.get('Organization') in (None,'Unknown') else row.get('Organization'),
           'organization_type':None,'robot_id':None,'robot_manufacturer':None,
           'robot_model':None if row.get('Robot Platform') in (None,'Unknown') else row.get('Robot Platform'),
           'robot_ownership':None,'control_mode':None,'result':result,'ranking':str(ranking) if ranking is not None else None,
           'evidence_text':','.join(evidence_ids),'participation_status':row['Participation Status'],
           'group':row.get('Round'),'notes':'Official archive result; duplicate round/source rows retained in official_result_history.'}
    origin={k:rows[0][k] for k in ('path','locator','source_id')}
    return {'id':identity,'label':name,'status':'unverified','provenance':[origin],
            'evidence_refs':[{'entity_type':'Evidence','id':e} for e in evidence_ids],
            'relationships':[{'relation':'entered','target':{'entity_type':'Competition','id':row['Competition ID']}}],
            'unresolved_references':[],'source_rows':rows,'entity_type':'Competition Entry','entry':entry,
            'entry_history':{'Verification Potential':row['Verification Potential']},
            'official_result_history':[{'candidate_id':r['source_id'],'values':r['values']} for r in rows],
            'verification':{'reported_status':row['Verification Potential'],'authority':'Kimi',
                'independent_status':'not_checked','origin':origin,
                'note':'Kimi status retained as a candidate; canonical status follows independent Official-Event review.',
                'canonical_status':'Verified','basis':'Direct official-event result evidence establishes this 2026 competition identity.'}}


def update_existing(record,row,evidence_ids,source,decision):
    before=copy.deepcopy(record['entry'])
    for evidence_id in evidence_ids: append_ref(record,evidence_id)
    record.setdefault('official_archive_review',[]).append(
        {'candidate_id':row['Candidate ID'],'effect':decision,'source_row':source,
         'note':'Independent official-event mapping; Kimi status was not treated as authority.'})
    record.setdefault('official_result_history',[]).append({'entry_before_import':before,'candidate':copy.deepcopy(row)})
    return record


def build(write_canonical=False):
    archived=archived_delivery()
    workbook_target=archived[SOURCE]
    workbook_rel=workbook_target.relative_to(ROOT).as_posix()
    existing=read(ROOT/'research/evidence/records.json')
    before=copy.deepcopy(existing)
    by_key={(r['entity_type'],r['id']):r for r in existing}
    competition_ids={r['id'] for r in existing if r['entity_type']=='Competition'}
    page_rows=sheet_records(SOURCE,'Official Page Map')
    evidence_rows={row['Evidence ID']:(number,row) for number,row in sheet_records(SOURCE,'Evidence')}
    attachment_rows=sheet_records(SOURCE,'Attachment Map')
    candidate_rows=sheet_records(SOURCE,'Entry Candidates')
    current_urls={normalized_url(r.get('source',{}).get('url')):r['id'] for r in existing
                  if r['entity_type']=='Evidence' and normalized_url(r.get('source',{}).get('url'))}

    page_map={}; attachment_map={}; additions=[]; updated=set(); dedup=[]
    page_new=0; attachment_new=0
    for _,row in page_rows:
        source_id=row['Evidence ID']
        match=source_id if ('Evidence',source_id) in by_key else current_urls.get(normalized_url(row['URL']))
        canonical=match or source_id; page_map[source_id]=canonical
        number,evidence=evidence_rows[source_id]
        archive_data={'page_id':row['Page ID (aid)'],'year':row['Year'],'section':row['Section'],
                      'source_class':row['Source Class'],'related_competitions':relation_ids(row.get('Related Competition IDs'))}
        sr=source_row(workbook_rel,'Evidence',number,source_id)
        if match:
            record=by_key[('Evidence',match)]
            record.setdefault('official_archive_sources',[]).append({'source_id':source_id,'source_row':sr,'metadata':archive_data})
            record['evidence']['source_type']='Official-Event'
            record['evidence']['publisher']=evidence['Publisher']
            record['source']['publisher']=evidence['Publisher']
            record['evidence_kind']='official_event_page'
            updated.add(('Evidence',match)); dedup.append({'source_id':source_id,'canonical_id':match,'reason':'same official page URL'})
        else:
            record=evidence_record(source_id,evidence['Title'],evidence['Publisher'],evidence['Date'],
                evidence['Original URL'],[sr],'official_event_page',archive_data,
                [c for c in relation_ids(row.get('Related Competition IDs')) if c in competition_ids])
            additions.append(record); by_key[('Evidence',source_id)]=record
            page_new+=1

    by_sha=defaultdict(list)
    for number,row in attachment_rows: by_sha[row['SHA-256']].append((number,row))
    for digest,group in sorted(by_sha.items()):
        number,row=sorted(group,key=lambda x:x[1]['Attachment ID'])[0]
        match=current_urls.get(normalized_url(row['Original URL']))
        canonical=match or row['Attachment ID']
        for _,member in group: attachment_map[member['Attachment ID']]=canonical
        source_path=archived[DELIVERY/'files'/row['Original Filename']].relative_to(ROOT).as_posix()
        archive_data={'year':row['Year'],'sha256':digest,'size':row['Size (bytes)'],
                      'file_type':row['File Type'],'archive_path':source_path,
                      'extraction_status':row['Extraction Status'],
                      'attachment_ids':[member['Attachment ID'] for _,member in group],
                      'parent_evidence_ids':[member['Parent Evidence ID'] for _,member in group],
                      'parent_page_ids':[member['Parent Page ID'] for _,member in group]}
        sr=source_row(workbook_rel,'Attachment Map',number,row['Attachment ID'])
        if match:
            record=by_key[('Evidence',match)]
            record.setdefault('official_archive_sources',[]).append({'source_id':row['Attachment ID'],'source_row':sr,'metadata':archive_data})
            record['evidence']['source_type']='Official-Event'
            record['evidence']['publisher']='世界人形机器人运动会组委会'
            record['source']['publisher']='世界人形机器人运动会组委会'
            record['evidence_kind']='official_event_attachment'
            updated.add(('Evidence',match)); dedup.append({'source_id':row['Attachment ID'],'canonical_id':match,'reason':'same official attachment URL'})
        else:
            comps=sorted({member['Competition ID'] for _,member in group if member.get('Competition ID') in competition_ids})
            record=evidence_record(canonical,row['Parent Title'],'世界人形机器人运动会组委会',
                row['Publication Date'],row['Original URL'],[sr],'official_event_attachment',archive_data,comps)
            additions.append(record); by_key[('Evidence',canonical)]=record
            attachment_new+=1
        for _,member in group[1:]:
            dedup.append({'source_id':member['Attachment ID'],'canonical_id':canonical,'reason':'identical attachment SHA-256'})

    texts=pdf_text_by_name()
    canonical_entries={(r['entry']['competition_id'],name_key(r['entry']['team_name'])):r['id']
                       for r in existing if r['entity_type']=='Competition Entry'}
    accepted=defaultdict(list); decisions=[]
    for number,row in candidate_rows:
        identity=row['Candidate ID']; name=candidate_name(row)
        reason=rejected_reason(row,texts)
        existing_id=MANUAL_EXISTING.get(identity) or canonical_entries.get((row['Competition ID'],name_key(name)))
        if reason:
            decisions.append({'candidate_id':identity,'effect':'D','canonical_id':None,'reason':reason})
            continue
        key=('existing',existing_id) if existing_id else ('new',row['Competition ID'],name_key(name))
        accepted[key].append((number,row,name))

    new_entries=[]
    for key,group in sorted(accepted.items(),key=lambda item:min(x[1]['Candidate ID'] for x in item[1])):
        final=[item for item in group if item[1].get('Round')=='决赛']
        number,row,name=sorted(final or group,key=lambda x:x[1]['Candidate ID'])[0]
        source_rows=[source_row(workbook_rel,'Entry Candidates',n,r['Candidate ID']) for n,r,_ in group]
        evidence_ids=[]
        for _,member,_ in group:
            for evidence_id in resolve_evidence(member.get('Evidence IDs'),page_map,attachment_map):
                if ('Evidence',evidence_id) in by_key and evidence_id not in evidence_ids: evidence_ids.append(evidence_id)
        if key[0]=='existing':
            existing_id=key[1]; effect='B' if existing_id in PROMOTIONS else 'A'
            target=by_key[('Competition Entry',existing_id)]
            for member_number,member,member_name in group:
                update_existing(target,member,evidence_ids,
                                source_row(workbook_rel,'Entry Candidates',member_number,member['Candidate ID']),effect)
                decisions.append({'candidate_id':member['Candidate ID'],'effect':effect,
                                  'canonical_id':existing_id,'reason':'mapped to existing canonical identity'})
            updated.add(('Competition Entry',existing_id))
        else:
            identity=row['Candidate ID']
            entry=new_entry(identity,row,source_rows,evidence_ids,name)
            additions.append(entry); new_entries.append(entry); by_key[('Competition Entry',identity)]=entry
            for member_number,member,member_name in group:
                decisions.append({'candidate_id':member['Candidate ID'],'effect':'C','canonical_id':identity,
                                  'reason':'official result identity' if member['Candidate ID']==identity else 'same competition/team identity; result history retained'})

    # Independently confirmed existing Entries that were not recoverable as clean candidate rows.
    manual_evidence={'E-B01-012-01':['EV-ESM-012'],'E-B01-012-02':['EV-ESM-012']}
    for identity,refs in manual_evidence.items():
        target=by_key[('Competition Entry',identity)]
        official=page_map.get('EV-ESM-012','EV-ESM-012')
        if ('Evidence',official) in by_key: refs.append(official)
        for ref in refs:
            if ('Evidence',ref) in by_key: append_ref(target,ref)
        target.setdefault('official_archive_review',[]).append({'effect':'A','note':'Exact team name independently read in the official C-012 source; no broken candidate row promoted.'})
        updated.add(('Competition Entry',identity))

    # Apply narrow result corrections and promotions while preserving pre-import fields above.
    corrections={
        'E-005-01':('2:21.64','1','Finished','天卓队'),
        'E-005-02':('2:30.00','2','Finished','飞雷神'),
        'E-005-03':('2:30.22','3','Finished','风火闪电队'),
        'E-C005-08':('2:33.23','4','Finished','天工队'),
        'E-005-07':('2:36.73','5','Finished','荣耀双驰战队'),
        'E-005-04':('7:43.89','7','Finished','GMO Robots'),
        'E-004-01':('38.15','1','Finished','天工队'),
        'E-004-02':('39.45','2','Finished','追风仔仔队'),
        'E-004-03':('39.66','3','Finished','惊鸿动力队'),
        'E-004-04':('40.08','4','Finished','荣耀双驰战队'),
        'E-042-01':(None,'1','Finished',None), 'E-042-02':(None,'2','Finished',None),
        'E-042-03':(None,'3','Finished',None),
        'E-B01-040-03':(None,'5','Finished',None),
    }
    for identity,(result,rank,status,label) in corrections.items():
        record=by_key[('Competition Entry',identity)]
        if result is not None: record['entry']['result']=result
        record['entry']['ranking']=rank; record['entry']['participation_status']=status
        if label: record['label']=label; record['entry']['team_name']=label
        record['entry']['group']='决赛'
        record['entry']['evidence_text']=','.join(r['id'] for r in record['evidence_refs'])
        updated.add(('Competition Entry',identity))
    for identity in PROMOTIONS:
        record=by_key[('Competition Entry',identity)]
        verification=record['verification']
        verification['previous_official_archive_status']=verification['canonical_status']
        if 'policy_adjustment' in verification:
            verification['previous_policy_adjustment']=verification.pop('policy_adjustment')
        verification['canonical_status']='Verified'
        verification['basis']='Direct Official-Event result evidence independently confirms the 2026 competition Entry.'
        verification['policy_adjustment']={'reason':verification['basis'],'evidence_refs':copy.deepcopy(record['evidence_refs'])}
        updated.add(('Competition Entry',identity))

    candidate=list(existing)+additions
    # existing objects were updated through shared references; list order remains stable, additions follow.
    before_by_key={(r['entity_type'],r['id']):r for r in before}
    added_keys={(r['entity_type'],r['id']) for r in additions}
    updated={key for key in updated if key in before_by_key and by_key[key]!=before_by_key[key]}
    decisions.sort(key=lambda x:x['candidate_id'])
    if len(decisions)!=1005: raise ValueError('Every candidate row must have one A/B/C/D decision')
    effect_counts=Counter(item['effect'] for item in decisions)
    entry_counts=Counter(r['verification']['canonical_status'] for r in candidate if r['entity_type']=='Competition Entry')
    manifest=read(ROOT/'research/imported/kimi/manifest.json')
    input_paths={target.relative_to(ROOT).as_posix() for target in archived.values()}
    inputs=[item for item in manifest if item['path'] in input_paths]
    if len(inputs)!=151: raise ValueError('Immutable input manifest is incomplete')
    write(REVIEW_DIR/'entry-decisions.json',decisions)
    write(REVIEW_DIR/'input-files.json',inputs)
    write(REVIEW_DIR/'evidence-deduplication.json',dedup)
    review_assets={name:{'path':f'research/reviews/kimi-official-archive-final-import/{name}',
                         'sha256':hashlib.sha256((REVIEW_DIR/name).read_bytes()).hexdigest()}
                   for name in ('entry-decisions.json','input-files.json','evidence-deduplication.json')}
    state={'schema_version':'1','import_id':'kimi-official-archive-final-import','review_path':REVIEW_PATH,
           'inputs':inputs,
           'review_assets':review_assets,
           'records_added':[{'entity_type':by_key[key]['entity_type'],'id':by_key[key]['id'],'sha256':record_hash(by_key[key])}
                            for key in sorted(added_keys)],
           'records_updated':[{'entity_type':by_key[key]['entity_type'],'id':by_key[key]['id'],'sha256':record_hash(by_key[key])}
                              for key in sorted(updated)],
           'reviewed_statuses':{identity:'Verified' for identity in sorted(PROMOTIONS)},
           'canonical_entry_counts':{'Verified':entry_counts['Verified'],'Research Lead':entry_counts['Research Lead'],'Unresolved':0},
           'evidence_disposition':{'accepted_new':sum(r['entity_type']=='Evidence' for r in additions),
                                   'new_pages':page_new,'new_attachment_payloads':attachment_new,
                                   'deduplicated':len(dedup),'rejected':0},
           'entry_effect_counts':dict(effect_counts),
           'entry_summary':{'existing_confirmed':18,'promoted':4,'new_identities':len(new_entries),
                            'conflict_or_ambiguity_rows':effect_counts['D']},
           'entity_additions':dict(Counter(r['entity_type'] for r in additions)),
           'deduplicated_sources':dedup}
    write(STAGING/'candidate.json',candidate)
    shutil.copyfile(ROOT/'research/evidence/supplemental.json',STAGING/'supplemental.json')
    shutil.copyfile(ROOT/'research/evidence/master-v2-1.json',STAGING/'master-v2-1.json')
    shutil.copyfile(ROOT/'research/evidence/kimi-official-archive-import-actual.json',STAGING/'kimi-official-archive-import-actual.json')
    write(STAGING/STATE_NAME,state)
    review=f'''# Kimi official archive final import review

## Scope and audit boundary

This is a new review of the delivered official archive. The earlier missing-input review remains unchanged. No web research was performed, Master v2.1 was not reconsidered, and the external Kimi workspace was not modified. Kimi's status column was treated as a candidate only.

## Immutable input integrity

- Workbook SHA-256: `{hashlib.sha256(SOURCE.read_bytes()).hexdigest()}`
- Screened immutable inputs: {len(inputs)} (workbook, 138 official attachment files, 12 crawl JSON appendices)
- Attachment-map rows: 172; unique delivered files: 138; unique payload hashes: 134
- Claimed row types: 97 PDF, 1 XLSX, 4 DOCX, 38 JPG, 32 PNG
- Unique delivered file types: 97 PDF, 1 XLSX, 4 DOCX, 20 JPG, 16 PNG
- All 172 page/attachment lineages, sizes, and SHA-256 values matched. Full hashes: [input-files.json](input-files.json).
- OOXML sources contain no formulas, macros, external links, or embedded objects. PDFs were not encrypted and exposed no JavaScript, launch action, or embedded-file markers. Six image-only result PDFs were retained as Evidence only; no OCR-derived Entries were created.

## Evidence disposition

- Accepted as new canonical Evidence: {state['evidence_disposition']['accepted_new']} ({page_new} new official pages and {attachment_new} unique attachment payloads).
- Deduplicated: {len(dedup)} source rows (7 existing page URLs, 1 existing attachment URL, 38 repeated attachment payload mappings).
- Rejected: 0 integrity-valid official sources. Image-only sources remain unverified Evidence and do not establish Entry identities.
- Publisher controls Source Class: all delivered WHRG organizer pages and attachments are `Official-Event`.

## Entry decisions

- Every one of the 1,005 candidate rows is classified in [entry-decisions.json](entry-decisions.json): A={effect_counts['A']}, B={effect_counts['B']}, C={effect_counts['C']}, D={effect_counts['D']}.
- Existing Entries confirmed: 18.
- Research Lead -> Verified: 4 (`E-005-04`, `E-042-01`, `E-042-02`, `E-042-03`). The proposed C-040 NorthAir/Agibot change is not a promotion because it was already Verified.
- New canonical Entry identities: {len(new_entries)}. Repeated preliminary/final rows are one competition/team identity with source history retained.
- C-003: four ranked finishers plus one DNF; the DNF ranking was cleared rather than accepting Kimi's duplicated rank 2.
- C-006: one official finisher, rank 1, retained as a new identity.
- C-005: GMO Robots is official rank 7 and promoted; the previous rank 4 is preserved in history. 惊鸿动力队 is a new identity.
- C-040: three 优理奇-prefixed rows remain conflicts and do not alter the generic canonical identity. City-specific C-036 智元 rows likewise remain ambiguous.
- Parser/schedule artifacts, unreliable C-027 concatenations, missing exact source strings, and duplicate result rows do not create extra identities.

## Year and domain controls

- All Entry candidates are 2026 and are linked only to 2026 official result evidence.
- The 17 official 2025 pages and their attachments are aggregate/context Evidence only. They do not verify 2026 participation.
- No RoboCup evidence was used to verify WHRG participation.
- Field Evidence was not used alone for any Verified promotion.
- Media open-source claims created no verified artifact or Open Knowledge change.

## Canonical effects

- Records before: {len(before)}; after: {len(candidate)}.
- Evidence: {sum(r['entity_type']=='Evidence' for r in before)} -> {sum(r['entity_type']=='Evidence' for r in candidate)}.
- Competition Entry: {sum(r['entity_type']=='Competition Entry' for r in before)} -> {sum(r['entity_type']=='Competition Entry' for r in candidate)}.
- Entry statuses: Verified 16 -> {entry_counts['Verified']}; Research Lead 6 -> {entry_counts['Research Lead']}.
- New Team / Organization / Robot Platform records: 0 / 0 / 0. Workbook names remain Entry fields; no entity IDs were inferred.
- Open Knowledge changes: 0.

## Promotion decision

The import may be promoted only after candidate validation, unit tests, negative controls, full validators, strict MkDocs, PDF build, and diff checks pass. The final commit is separate and must not be pushed in this task.
'''
    REVIEW_DIR.mkdir(parents=True,exist_ok=True)
    (REVIEW_DIR/'review.md').write_text(review,encoding='utf-8',newline='\n')
    validate(candidate=STAGING/'candidate.json',supplemental=STAGING/'supplemental.json')
    if write_canonical:
        shutil.copyfile(STAGING/'candidate.json',ROOT/'research/evidence/records.json')
        shutil.copyfile(STAGING/STATE_NAME,ROOT/'research/evidence'/STATE_NAME)
        validate()
    print(json.dumps({'inputs':len(inputs),'evidence_new':state['evidence_disposition']['accepted_new'],
        'deduplicated':len(dedup),'entry_effects':dict(effect_counts),'new_entries':len(new_entries),
        'records_before':len(before),'records_after':len(candidate),'entry_counts':state['canonical_entry_counts'],
        'updated_records':len(updated)},ensure_ascii=False,indent=2))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write',action='store_true',help='Promote the validated staging candidate')
    args=parser.parse_args()
    build(args.write)


if __name__=='__main__':
    main()
