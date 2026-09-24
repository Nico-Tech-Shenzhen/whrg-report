#!/usr/bin/env python3
"""Build the reviewed additive candidate from delivered Kimi workbooks."""

import hashlib
import json
from pathlib import Path
import shutil

from research_schema import column_name, workbook_rows


ROOT = Path(__file__).resolve().parents[1]
STAGING = ROOT / 'research/staging/kimi-official-archive-import-actual'
REVIEW = ROOT / 'research/reviews/kimi-official-archive-import-actual/review.md'
STATE_NAME = 'kimi-official-archive-import-actual.json'

EXPANSION = 'research/imported/kimi/185019e6ace844f608b1a029a238167e5aa7b6dd1273abd704b947bc2bdc2d37/china-source-expansion-2025-2026.xlsx'
ARCHIVE_2025 = 'research/imported/kimi/43861d618a902a175ab0e82ea66aa4d480512b3d5459f3090c51fc2d9c615627/whrg-2025-archive-team-recovery.xlsx'
CAS = 'research/imported/kimi/32340418eef504949b1182a1e2ed2eb4da378b22cc6344a9520dbedc473b9b60/cas-wechat-ecosystem-2025-2026.xlsx'
NORMALIZED = 'research/imported/kimi/fa88c16875c7c8accc14e0540da859bf23462e3925724cb35e45fc5a3e8c6239/source-cross-reference-normalized-2025-2026.xlsx'

EXPANSION_ACCEPTED = ['EV-057','EV-059','EV-060','EV-061','SRC-003']
ARCHIVE_ACCEPTED = [f'EV-{number:03d}' for number in range(65,81)]
NORMALIZED_ACCEPTED = [
    'EV-081','EV-082','EV-084','EV-085','EV-086','EV-087','EV-088','EV-089',
    'EV-090','EV-091','EV-092','EV-093','EV-094','EV-095','EV-096','EV-098',
    'EV-099','EV-100','EV-101','EV-102','EV-104','EV-115','EV-117','EV-118',
    'EV-120','EV-121','EV-122',
]

DEDUPLICATED = [
    ('EV-052','EV-067','same Xinhua URL and 2025 1500m source'),
    ('EV-053','EV-066','same Xinhua URL and 2025 100m source'),
    ('EV-054','EV-068','same Beijing government URL'),
    ('EV-055','EV-069','same Xinhua URL and 2025 football source'),
    ('EV-056','EV-074','same Zhihu URL'),
    ('EV-058','EV-072','same official 2025 registration URL'),
    ('EV-063','EV-076','same Xinhua dance source URL'),
    ('EV-064','EV-ESM-001','same existing official 2026 draw notice'),
    ('EV-083','EV-122','same official 2026 C-005 result PDF'),
    ('EV-097','EV-092','same cls.cn source URL'),
    ('EV-103','EV-100','same Beijing Daily source URL'),
    ('EV-105','EV-100','same Beijing Daily source URL'),
    ('EV-106','EV-ESM-005B','same Xinhua 2026 event report'),
    ('EV-123','EV-122','same official 2026 C-005 result PDF'),
    ('EV-124','EV-ESM-005B','same Xinhua 2026 event report'),
    ('EV-125','EV-ESM-005B','same Xinhua 2026 event report'),
    ('EV-023(Master)','EV-023','existing canonical repository Evidence'),
    ('EV-024(Master)','EV-024','existing canonical repository Evidence'),
    ('EV-133','EV-010~EV-014','announced dataset lead already covered canonically'),
]

REJECTED = [
    ('EV-062','publication date and URL path year conflict'),
    ('SRC-001','generic platform homepage is not a claim-level source'),
    ('SRC-002','generic platform homepage is not a claim-level source'),
    ('SRC-004','aggregator knowledge hub is only a partial lead'),
    ('EV-107','synthetic relationship summary without a direct source URL'),
    ('EV-108','synthetic relationship summary without a direct source URL'),
    ('EV-109','synthetic relationship summary without a direct source URL'),
    ('EV-110','synthetic relationship summary without a direct source URL'),
    ('EV-111','synthetic relationship summary without a direct source URL'),
    ('EV-112','synthetic relationship summary without a direct source URL'),
    ('EV-113','official account mention has no directly accessible article'),
    ('EV-116','research-self negative search result is not source Evidence'),
    ('EV-119','official account mention has no directly accessible article'),
    ('EV-126','explicitly reports that no source was found'),
    ('EV-127','synthetic relationship summary without a direct source URL'),
    ('EV-128','synthetic relationship summary without a direct source URL'),
    ('EV-129','synthetic relationship summary without a direct source URL'),
    ('EV-130','synthetic relationship summary without a direct source URL'),
    ('EV-131','media description has no repository, paper, or license source'),
    ('EV-132','media open-source claim has no repository or license source'),
]


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write(path,value):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')


def canonical_hash(item):
    payload=json.dumps(item,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')
    return hashlib.sha256(payload).hexdigest()


def tabular(path,sheet):
    rows=workbook_rows(ROOT/path)[sheet]
    header=rows[1]
    result={}
    for number in sorted(n for n in rows if n>1):
        result[number]={header[c]:rows[number].get(c) for c in header}
    return rows,result


def source_row(path,sheet,number,source_id):
    rows=workbook_rows(ROOT/path)
    header=rows[sheet][1]
    values=rows[sheet][number]
    width=max(max(header),max(values))
    headers=[header.get(c) for c in range(1,width+1)]
    row_values=[values.get(c) for c in range(1,width+1)]
    return {
        'path':path,
        'locator':f"'{sheet}'!A{number}:{column_name(width)}{number}",
        'source_id':source_id,
        'sheet':sheet,
        'row':number,
        'id_column':1,
        'headers':headers,
        'values':row_values,
        'header_row':1,
    }


def provenance(rows):
    return [{k:r[k] for k in ('path','locator','source_id')} for r in rows]


def evidence_record(identity,label,publisher,date,url,source_class,topic,scope,confidence,notes,rows,audit='unknown'):
    text=notes if isinstance(notes,str) and notes.strip() else 'unknown'
    return {
        'id':identity,
        'label':label,
        'status':'unverified',
        'provenance':provenance(rows),
        'evidence_refs':[],
        'relationships':[],
        'unresolved_references':[],
        'source_rows':rows,
        'entity_type':'Evidence',
        'evidence':{
            'topic':topic or 'unknown',
            'publisher':publisher or 'unknown',
            'title':label,
            'date':date or 'unknown',
            'source_type':source_class or 'unknown',
            'url':url or 'unknown',
            'original_text':text,
            'japanese_summary':'unknown',
            'scope':scope or 'unknown',
            'confidence':confidence or 'unknown',
            'notes':text,
        },
        'source':{
            'title':label,
            'publisher':publisher or 'unknown',
            'date':date or 'unknown',
            'url':url or 'unknown',
            'accessed_at':audit or 'unknown',
            'version':'unknown',
            'verification_note':'Imported Kimi source metadata; source content was not independently checked during this import.',
        },
        'evidence_kind':'source_record',
    }


def rows_with_id(path,identity):
    found=[]
    for sheet,rows in workbook_rows(ROOT/path).items():
        for number in sorted(n for n in rows if n>1):
            if rows[number].get(1)==identity:
                found.append(source_row(path,sheet,number,identity))
    return found


def expansion_records():
    _,items=tabular(EXPANSION,'Source Map')
    by_id={item['Source ID']:(number,item) for number,item in items.items()}
    output=[]
    for identity in EXPANSION_ACCEPTED:
        number,item=by_id[identity]
        rows=[source_row(EXPANSION,'Source Map',number,identity)]
        output.append(evidence_record(
            identity,item['Useful For'],item['Account / Organization'],item['Publication Date'],item['URL'],
            item['Source Class'],item['WHRG Relation'],item['Competition IDs'],
            'unknown',item['Notes'],rows,
        ))
    return output


def archive_records():
    _,items=tabular(ARCHIVE_2025,'2025 Source Map')
    by_id={item['Evidence ID']:(number,item) for number,item in items.items()}
    output=[]
    for identity in ARCHIVE_ACCEPTED:
        _,item=by_id[identity]
        rows=rows_with_id(ARCHIVE_2025,identity)
        note='; '.join(str(v) for v in [item['Notes'],item['Content Type'],item['Primary / Secondary']] if v)
        output.append(evidence_record(
            identity,item['Source Title'],item['Publisher'],item['Publication Date'],item['URL'],
            item['Source Class'],item['Scope'],item['Scope'],item['Confidence'],note,rows,
        ))
    return output


def normalized_records():
    _,items=tabular(NORMALIZED,'Evidence Cross-Reference')
    by_id={item['Evidence ID']:(number,item) for number,item in items.items()}
    output=[]
    for identity in NORMALIZED_ACCEPTED:
        _,item=by_id[identity]
        rows=rows_with_id(NORMALIZED,identity)+rows_with_id(CAS,identity)
        note='; '.join(str(v) for v in [item['Notes'],f"Claim attribution: {item['Claim Attribution']}"] if v)
        output.append(evidence_record(
            identity,item['Source Title'],item['Publisher'],item['Publication Date'],item['Source URL'],
            item['New Source Class'],item['Topic'],item['Scope'],item['Confidence'],note,rows,item['Audit Date'],
        ))
    return output


def main():
    if not REVIEW.is_file():
        raise ValueError('Required review file is missing')
    existing=read(ROOT/'research/evidence/records.json')
    accepted=expansion_records()+archive_records()+normalized_records()
    keys={(r['entity_type'],r['id']) for r in existing}
    if len({r['id'] for r in accepted})!=48 or any(('Evidence',r['id']) in keys for r in accepted):
        raise ValueError('Accepted Evidence inventory is incomplete or collides with canonical data')
    candidate=existing+accepted
    manifest=read(ROOT/'research/imported/kimi/manifest.json')
    selected_names={Path(name).name for name in [EXPANSION,ARCHIVE_2025,CAS,NORMALIZED]}
    inputs=[item for item in manifest if item['original_name'] in selected_names]
    if len(inputs)!=4:
        raise ValueError('Expected four immutable imports')
    counts={'Verified':0,'Research Lead':0,'Unresolved':0}
    for item in candidate:
        if item['entity_type']=='Competition Entry':
            status=item['verification']['canonical_status']
            counts[status]=counts.get(status,0)+1
    state={
        'schema_version':'1',
        'import_id':'kimi-official-archive-import-actual',
        'review_path':'research/reviews/kimi-official-archive-import-actual/review.md',
        'inputs':inputs,
        'accepted_evidence_ids':[r['id'] for r in accepted],
        'records':[{'entity_type':r['entity_type'],'id':r['id'],'sha256':canonical_hash(r)} for r in accepted],
        'deduplicated':[{'source_id':a,'canonical_id':b,'reason':reason} for a,b,reason in DEDUPLICATED],
        'rejected':[{'source_id':identity,'reason':reason} for identity,reason in REJECTED],
        'missing_inputs':['whrg-official-archive-attachments-2025-2026.xlsx'],
        'canonical_entry_counts':counts,
    }
    write(STAGING/'candidate.json',candidate)
    shutil.copyfile(ROOT/'research/evidence/supplemental.json',STAGING/'supplemental.json')
    shutil.copyfile(ROOT/'research/evidence/master-v2-1.json',STAGING/'master-v2-1.json')
    write(STAGING/STATE_NAME,state)
    notes=[
        '# Kimi official archive actual import mapping notes',
        '',
        f'- Accepted Evidence records: {len(accepted)}',
        f'- Deduplicated supplied IDs: {len(DEDUPLICATED)}',
        f'- Rejected supplied IDs: {len(REJECTED)}',
        '- New Competition Entry, Team, Organization, and Robot Platform identities: 0',
        '- Reason: delivered entity and Entry leads do not supply canonical IDs; no IDs were invented.',
        '- Promotions: 0; the official attachment workbook is missing, so proposed official-result upgrades remain unverified.',
        '- Master v2.1 records and semantics sidecar are copied unchanged into the candidate.',
        '',
    ]
    (STAGING/'mapping-notes.md').write_text('\n'.join(notes),encoding='utf-8',newline='\n')
    print(json.dumps({'accepted':len(accepted),'deduplicated':len(DEDUPLICATED),'rejected':len(REJECTED),
                      'candidate_records':len(candidate),'entry_counts':counts},indent=2))


if __name__=='__main__':
    main()
