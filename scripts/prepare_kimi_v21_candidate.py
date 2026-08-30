"""Prepare a lossless v2.1 workbook specification; never promote canonical data.

Run with repository Python, then author the XLSX using build_kimi_v21_workbook.mjs.
All factual values come from canonical records; rejected v2 is comparison only.
"""
from collections import Counter, defaultdict
from hashlib import sha256
import json
from pathlib import Path

from research_schema import workbook_rows
from validate_kimi_checkpoint import checkpoint_imports
from validate_research import ROOT

WORK = ROOT/'research/staging/v2-1-work'
REVIEW = ROOT/'research/reviews/kimi-master-v2-1'
CANDIDATE = ROOT/'research/staging/WHRG_2026_Master_v2_1.xlsx'
# Reviewed identity directions; validated against every current pair and source row.
ALIASES = {
    **{f'E-C005-{n:02}':f'E-005-{n:02}' for n in range(1,8)},
    **{f'E-B01-004-{n:02}':f'E-004-{n:02}' for n in range(1,5)},
    'E-B01-040-02':'E-040-01', 'E-B01-036-02':'E-036-01',
}
PARTICIPATION = ['Registered','Scheduled','Started','Finished','DNF','DNS','Disqualified','Unknown']

def read(path):
    return json.loads(path.read_text(encoding='utf-8'))

def packed(value):
    return json.dumps(value,ensure_ascii=False,separators=(',',':'))

def digest(path):
    return sha256(path.read_bytes()).hexdigest()

def unique(values):
    output=[]
    for value in values:
        if value not in output: output.append(value)
    return output

def prepare():
    if (ROOT/'research/active-checkpoint.json').exists():
        raise ValueError('Master v2.1 is frozen after promotion; do not regenerate it from the active corpus. Use its preserved workbook and migration history.')
    WORK.mkdir(parents=True,exist_ok=True)
    REVIEW.mkdir(parents=True,exist_ok=True)
    records=read(ROOT/'research/evidence/records.json')
    supplemental=read(ROOT/'research/evidence/supplemental.json')
    manifest=read(ROOT/'research/imported/kimi/manifest.json')
    prior=read(ROOT/'research/reviews/kimi-master-v2/review.json')
    active=checkpoint_imports(manifest)
    master=next(m['path'] for m in active if m['original_name']=='WHRG_2026_Master.xlsx')
    rejected=next(m['path'] for m in manifest if m['original_name']=='WHRG_2026_Master_v2.xlsx')
    v1=workbook_rows(ROOT/master)
    v2=workbook_rows(ROOT/rejected)
    hashes={p:digest(ROOT/p) for p in ['research/evidence/records.json','research/evidence/supplemental.json']+[m['path'] for m in manifest]}
    entities={(r['entity_type'],r['id']):r for r in records}
    entries=[r for r in records if r['entity_type']=='Competition Entry']
    index={r['id']:r for r in entries}
    mapping={r['id']:ALIASES.get(r['id'],r['id']) for r in entries}
    assert mapping=={r['legacy_id']:r['canonical_id'] for r in prior['mapping_35_to_22']}
    assert len(entries)==35 and len(set(mapping.values()))==22 and len(ALIASES)==13
    for legacy,target in ALIASES.items():
        assert target in index[legacy]['possible_duplicate_ids']
        # Compare the entire actual Master payload, not only team names.
        assert {k:v for k,v in index[legacy]['entry'].items() if k!='evidence_text'}=={k:v for k,v in index[target]['entry'].items() if k!='evidence_text'}
    sheets=[]
    def sheet(name,headers,rows,note):
        assert len(name)<=31
        for row in rows:
            assert len(row)==len(headers),(name,len(row),len(headers))
            for value in row:
                if isinstance(value,str):
                    assert len(value.encode('utf-16-le'))//2<=32767,(name,'Excel cell limit')
        sheets.append({'name':name,'headers':headers,'rows':rows,'note':note})
    def typed_sheet(name,items,payload):
        keys=unique(k for item in items for k in item.get(payload,{}))
        rows=[[r['id'],r['label']]+[r.get(payload,{}).get(k) if not isinstance(r.get(payload,{}).get(k),(dict,list)) else packed(r[payload][k]) for k in keys]+[packed(r['provenance']),packed(r)] for r in items]
        sheet(name,['ID','Label']+keys+['Provenance JSON','Canonical Record JSON'],rows,'Typed '+payload+' payload. Exact full records and source rows are retained in the final column.')
    groups=defaultdict(list)
    for r in entries: groups[mapping[r['id']]].append(r)
    merged=[]
    pair_review=[]
    for target,history in groups.items():
        base=index[target]
        statuses=unique(r.get('entry_history',{}).get('Participation Status') or 'Unknown' for r in history)
        assert set(statuses)<=set(PARTICIPATION)
        participation=statuses[0] if len(statuses)==1 else 'Unknown'
        verification='Research Lead' if any(r['verification']['canonical_status']=='Research Lead' for r in history) else 'Verified'
        basis=('Inherited current canonical Research Lead classification; not independently checked.' if verification=='Research Lead' else 'Inherited current canonical Verified classification; not independently checked. This does not assert Primary Web Evidence.')
        if target=='E-005-04':
            basis+=' Rejected v2 proposed Research Lead; canonical remains Verified. FP-002 is Field Evidence, EV-ESM-005A is secondary reporting; claim-level support and ranking scope remain unresolved.'
        refs=sorted({ref['id'] for r in history for ref in r['evidence_refs']})
        historical=[{'historical_entry_id':r['id'],'entry':r['entry'],'entry_history':r.get('entry_history',{}),'verification':r['verification'],'provenance':r['provenance']} for r in history]
        facet=lambda key: '\n'.join(str(v) for v in unique(r.get('entry_history',{}).get(key) for r in history) if v is not None)
        m={'id':target,'entry':base['entry'],'historical_ids':[r['id'] for r in history],
           'evidence_ids':refs,'participation_status':participation,'verification_status':verification,
           'verification_basis':basis,'group':facet('Group'),'notes':facet('Notes'),
           'historical_attributes':historical,'provenance':unique(p for r in history for p in r['provenance']),
           'unresolved_references':unique(u for r in history for u in r['unresolved_references'])}
        merged.append(m)
        for r in history:
            if r['id']!=target:
                pair_review.append({'legacy_id':r['id'],'canonical_id':target,'identity_fields_equal':True,
                  'union_evidence_ids':refs,'historical_ids':m['historical_ids'],
                  'all_attributes_preserved':True,'legacy_master_locator':r['provenance'][0],
                  'canonical_master_locator':base['provenance'][0]})
    sheet('Read Me',['Topic','Value'],[
        ['Release','WHRG Master v2.1 - candidate only; not promoted'],
        ['Authority','Current canonical corpus, then original Master/staging snapshots. Rejected v2 contributes schema ideas only.'],
        ['Identity','22 candidate Entry identities; all 35 historical IDs retained in Entry History and ID Crosswalk.'],
        ['Verification','17 inherited Verified / 5 Research Lead identities; zero independently verified. See Verification Review.'],
        ['Lossless storage','Typed data sheets retain complete canonical JSON including all original source rows. Source JSON null is not an inferred value.'],
        ['Historical attributes','Entry Map presents all group/notes and exact Historical Attributes JSON. Entry History retains every original row and verification provenance.'],
        ['Evidence','100 original Master Evidence rows plus 42 separate Field Evidence records. Full source text, notes, and placeholders preserved.'],
        ['Dates','Ambiguous original dates retained as text; Date Meaning Unknown; no publication date inferred from a URL or a generic Date column.'],
        ['Questions','31 original Master questions; Q and UQ layouts retained explicitly. Six additional historical questions are separate.'],
        ['Counts','Count Type describes a denominator claim. Source Class describes provenance. Neither implies the other.'],
        ['Entity boundaries','Organization, Team, Competition, Entry, Robot Platform, Resource, Dataset, Evidence, License, Rule Version remain distinct.'],
        ['Archive payloads','Canonical Archive and Supplemental Archive allow exact reconstruction of all 247 + 206 current records. They are typed audit payloads, not a generic entity model.'],
        ['Use','No web research. No source snapshots or canonical records edited. No report chapters. No promotion or publishing.'],
    ],'Candidate use and preservation contract.')
    typed_sheet('Competition Master',[r for r in records if r['entity_type']=='Competition'],'competition')
    headers=['Entry ID','Competition ID','Team ID','Organization ID','Country','Team Name','Organization Name','Organization Type','Robot ID','Robot Manufacturer','Robot Model','Robot Ownership','Control Mode','Participation Status','Group or Heat','Result','Ranking','Evidence IDs','Verification Status','Verification Basis','Notes','Historical Entry IDs','Historical Attributes JSON','Provenance JSON','Unresolved References JSON','Independent Status']
    entrykeys=['competition_id','team_id','organization_id','country','team_name','organization_name','organization_type','robot_id','robot_manufacturer','robot_model','robot_ownership','control_mode']
    sheet('Competition Entry Map',headers,[[m['id']]+[m['entry'][k] for k in entrykeys]+[m['participation_status'],m['group'],m['entry']['result'],m['entry']['ranking'],','.join(m['evidence_ids']),m['verification_status'],m['verification_basis'],m['notes'],','.join(m['historical_ids']),packed(m['historical_attributes']),packed(m['provenance']),packed(m['unresolved_references']),'not_checked'] for m in merged],'Canonical identity view for this candidate only. Historical Attributes JSON retains all distinct values and their origins.')
    sheet('Entry History',['Historical Entry ID','Candidate Entry ID','Competition ID','Participation Status','Group or Heat','Historical Result','Historical Ranking','Notes','Kimi Reported Status','Current Canonical Status','Verification Provenance JSON','Canonical Record JSON'],[[r['id'],mapping[r['id']],r['entry']['competition_id'],r['entry_history'].get('Participation Status') or 'Unknown',r['entry_history'].get('Group'),r['entry_history'].get('Result'),r['entry_history'].get('Ranking'),r['entry_history'].get('Notes'),r['verification']['reported_status'],r['verification']['canonical_status'],packed(r['verification']),packed(r)] for r in entries],'All 35 pre-migration records exactly retained. Historical result values are not overwritten by a selected Master value.')
    sheet('ID Crosswalk',['Entity Type','Historical ID','Candidate ID','Action','Evidence IDs Union','Source Provenance JSON'],[['Competition Entry',r['id'],mapping[r['id']],'Confirmed Same - reviewed' if r['id'] in ALIASES else 'Retained',','.join(next(m['evidence_ids'] for m in merged if m['id']==mapping[r['id']])),packed(r['provenance'])] for r in entries],'35 mappings: 22 self mappings and 13 reviewed duplicate mappings. No supplied ID is discarded.')
    master_evidence=[r for r in records if r['entity_type']=='Evidence' and r['source_rows'][0]['path']==master]
    ek=['topic','publisher','title','date','source_type','url','original_text','japanese_summary','scope','confidence','notes']
    sheet('Evidence Map',['Evidence ID','Topic','Publisher','Title','Original Date','Source Type','URL','Original Chinese Evidence','Japanese Summary','Scope','Confidence','Notes','Source Class','Date Meaning','Event Date','Publication Date','Audit Date','Independent Status','Provenance JSON','Canonical Record JSON'],[[r['id']]+[r['evidence'][k] for k in ek]+[r['evidence']['source_type'] or 'Unknown','Unknown',None,None,None,r['status'],packed(r['provenance']),packed(r)] for r in master_evidence],'Exact original Evidence text, including blanks and placeholders. Source Class preserves existing source classification verbatim; it is not a new verification.')
    typed_sheet('Field Evidence',[r for r in records if r.get('evidence_kind')=='field_evidence' and r['id'].startswith(('FP-','UF-'))],'field_evidence')
    text_parts=[]
    for r in [x for x in records if x['entity_type']=='Evidence']:
        texts={'original_text':r.get('evidence',{}).get('original_text'),
               'japanese_summary':r.get('evidence',{}).get('japanese_summary'),
               'field_text':r.get('field_evidence',{}).get('text')}
        for field,value in texts.items():
            if not value: continue
            for part,start in enumerate(range(0,len(value),160),1):
                text_parts.append([r['id'],field,part,value[start:start+160],packed(r['provenance'])])
    sheet('Evidence Text Contents',['Evidence ID','Source Field','Part','Exact Text Fragment','Provenance JSON'],text_parts,'Reading view for long text. Concatenate fragments in Part order without adding separators to reconstruct the exact original text, including newlines. Full unsplit text remains in typed Evidence records.')
    for name,typ,payload in [('Team Map','Team','team'),('Organization Map','Organization','open_knowledge'),('Rule Version Map','Rule Version','rule_version')]:
        typed_sheet(name,[r for r in records if r['entity_type']==typ],payload)
    # Explicitly keep empty entity registries distinct from audits and mentions.
    for name,typ in [('Robot Platforms','Robot Platform'),('Resources','Resource'),('Datasets','Dataset'),('Licenses','License')]:
        sheet(name,['ID','Label','Canonical Record JSON'],[[r['id'],r['label'],packed(r)] for r in records if r['entity_type']==typ],'No stable '+typ+' entity IDs supplied. Mentions and audits are preserved in typed supplemental records; no identity is invented.')
    questions=[r for r in supplemental if r['record_type']=='question']
    for name,qs in [('Unknown Questions',[r for r in questions if r['source_rows'][0]['path']==master]),('Historical Questions',[r for r in questions if r['source_rows'][0]['path']!=master])]:
        sheet(name,['Question ID','Source Layout','Question','Reported Status','Source Payload JSON','Provenance JSON','Canonical Record JSON'],[[r['id'],r.get('layout','historical_phase1_question'),r['question']['question'],r['question']['reported_status'],packed(r['question']),packed(r['provenance']),packed(r)] for r in qs],'Q and UQ layouts are not interchangeable. Original headers, raw positional values, and source-specific payload remain in full records.')
    assessment=[r for r in supplemental if r['record_type']=='entry_source_assessment']
    recovery={r['id']:r for r in supplemental if r['record_type']=='entry_recovery_summary'}
    count=next(r for r in supplemental if r['record_type']=='competition_count_summary')
    source_rows=[]
    for r in assessment:
        p=r['entry_source_assessment'];later=recovery.get(r['id']);latest=p['recoverability'];origin=r['provenance']
        if later:
            latest=later['entry_recovery_summary']['recoverability'];origin=later['provenance']
        if r['id']=='C-005': latest=count['competition_count_summary']['Recoverability'].split(' ')[0];origin=count['provenance']
        source_rows.append([r['id'],p['competition_name'],latest,packed(origin),p['source_date'],'Unknown',None,None,None,p['best_source_type'],p['evidence_text'],packed(p),packed(r),packed(later) if later else None,packed(count) if r['id']=='C-005' else None])
    sheet('Entry Source Map',['Competition ID','Competition Name','Latest Recoverability','Assessment Provenance JSON','Original Source Date','Date Meaning','Event Date','Publication Date','Audit Date','Source Class','Evidence IDs','Phase1 Payload JSON','Phase1 Canonical Record JSON','Batch Recovery Record JSON','C005 Summary Record JSON'],source_rows,'Stable schema with all earlier assessments retained. C-021 Low is retained alongside historical Medium; C-005 Medium is retained.')
    census=[r for r in supplemental if r['record_type']=='census_metric']
    countrows=[]
    for r in census:
        p=r['census_metric'];countrows.append([r['id'],r['label'],packed(p),'Unknown','Unknown',packed(r)])
    countrows.append([count['id'],'C-005 reported team count',packed(count['competition_count_summary']),'Reported','Media',packed(count)])
    sheet('Count Claims',['Supplied ID','Metric','Source Claim Payload JSON','Count Type','Source Class','Canonical Record JSON'],countrows,'Count Type is Unknown unless explicitly qualified in canonical history. C-005 34 is Reported / Media, never Official. Original Reported (Media) wording is retained.')
    names={'license_audit':'License Audits','license_audit_summary':'License Audit Summary','rule_change':'Rule Changes','case_study':'Case Studies','open_data_audit':'Open Data Audits','open_data_state':'Open Data States','recruitment_cohort':'Recruitment Cohorts','identity_mapping':'Identity Questions','entry_recovery_summary':'Recovery History','competition_count_summary':'C005 Count History','historical_validation':'Historical Validation','workbook_context':'Workbook Context'}
    for typ,name in names.items(): typed_sheet(name,[r for r in supplemental if r['record_type']==typ],typ)
    sheet('Canonical Archive',['Entity Type','Supplied ID','Label','Canonical Record JSON'],[[r['entity_type'],r['id'],r['label'],packed(r)] for r in records],'Exact 247 pre-migration typed entity records, including 35 historical Entries; not the 22-row candidate identity view.')
    sheet('Supplemental Archive',['Record Type','Supplied ID','Label','Canonical Record JSON'],[[r['record_type'],r['id'],r['label'],packed(r)] for r in supplemental],'Exact 206 typed supplemental records; no record IDs or source layouts are normalized.')
    unresolved=[]
    for r in records+supplemental:
        typ=r.get('entity_type',r.get('record_type'))
        for key in ['unresolved_references','source_key_gaps','identity_gaps','mapping_gap','identity_mapping','evidence_gap']:
            value=r.get(key)
            if value: unresolved.append([typ,r['id'],key,packed(value),packed(r['provenance'])])
    unresolved += [['Evidence','FP-002','underlying_source_mapping','Field Evidence record resolves to existing transcription. Original photo not delivered; mapping to verified underlying/Primary Web Evidence remains unresolved.',packed(entities['Evidence','FP-002']['provenance'])],['Competition Entry','E-005-04','verification_and_ranking_scope','Current Verified classification retained, rejected v2 Research Lead proposal not authoritative. Secondary report and Field Evidence do not establish Primary Web Evidence. Overall rank 4 and Group 2 rank 3 note both retained.',packed(index['E-005-04']['provenance'])]]
    warning_ids=[m['id'] for m in merged if m['entry']['team_name'] and m['entry']['team_name']==m['entry']['organization_name']]
    for ident in warning_ids: unresolved.append(['Competition Entry',ident,'Team Name = Organization Name','Keep Team and Organization distinct; supplied identity IDs remain absent.',packed(index[ident]['provenance'])])
    sheet('Unresolved Mappings',['Record Type','Supplied ID','Gap Type','Details JSON or Text','Provenance JSON'],unresolved,'Existing unresolved references and source/identity gaps remain unresolved. No factual unknown is researched or resolved here.')
    v2entry={v[1]:v for n,v in v2['Competition Entry Map'].items() if n>=5 and v.get(1) in set(mapping.values())}
    verification_review=[]
    for m in merged:
        if v2entry[m['id']].get(15)=='Research Lead':
            decision='Retain current canonical Research Lead' if m['verification_status']=='Research Lead' else 'Do not import v2 downgrade; flag unresolved'
            verification_review.append([m['id'],'Research Lead',m['verification_status'],decision,','.join(m['evidence_ids']),m['verification_basis'],packed([{'id':e,'source':entities['Evidence',e].get('evidence',entities['Evidence',e].get('field_evidence'))} for e in m['evidence_ids']])])
    assert len(verification_review)==6
    sheet('Verification Review',['Entry ID','Rejected v2 Status','Candidate Status','Decision','Evidence IDs','Basis','Existing Evidence Payload JSON'],verification_review,'Six v2 Research Lead decisions evaluated from existing data. Five match current canonical classifications; GMO remains a flagged inherited classification, not a factual upgrade.')
    dates=[]
    for r in master_evidence: dates.append(['Evidence',r['id'],'evidence.date',r['evidence']['date'],'Unknown',None,None,None,packed(r['provenance'])])
    for r in records:
        if r['entity_type']=='Competition': dates.append(['Competition',r['id'],'competition.dates',r['competition']['dates'],'Event Date',r['competition']['dates'],None,None,packed(r['provenance'])])
        if r['entity_type']=='Rule Version':
            p=r['rule_version']; value=p.get('published_date',p.get('publication_date'))
            # Retain source spelling via exact source column labelled Published Date.
            value=r['source_rows'][0]['values'][2]
            dates.append(['Rule Version',r['id'],'Published Date',value,'Publication Date',None,value,None,packed(r['provenance'])])
    for r in assessment: dates.append(['entry_source_assessment',r['id'],'source_date',r['entry_source_assessment']['source_date'],'Unknown',None,None,None,packed(r['provenance'])])
    sheet('Date Semantics',['Record Type','Supplied ID','Original Field','Original Date','Date Meaning','Event Date','Publication Date','Audit Date','Provenance JSON'],dates,'Only explicit source field semantics are assigned. Text ranges and unknowns are preserved without parsing or guesses. No audit date is invented for Evidence.')
    sheet('Migration History',['Source','Role','SHA256','Path'],[[m['original_name'],'Current checkpoint provenance' if m in active else 'Rejected migration audit only',m['sha256'],m['path']] for m in manifest]+[['records.json','Current canonical authority',hashes['research/evidence/records.json'],'research/evidence/records.json'],['supplemental.json','Current canonical authority',hashes['research/evidence/supplemental.json'],'research/evidence/supplemental.json']],'v1 -> current canonical -> lossless v2.1 candidate. Rejected v2 remains history, not canonical data.')
    schema_rows=[[s['name'],len(s['rows']),packed(s['headers']),s['note']] for s in sheets]
    sheet('Schema',['Sheet','Data Rows','Ordered Columns JSON','Meaning'],schema_rows,'Row 1 always contains stable headers; row 2 begins data. All provenance and archival JSON retain typed source payloads. No formulas execute imported content.')
    evidence_lost=[]
    v2ev={v[1]:v for n,v in v2['Evidence Map'].items() if n>=4 and v.get(1)}
    for r in master_evidence:
        text=r['evidence']['original_text']
        if text and text not in v2ev[r['id']].values(): evidence_lost.append(r['id'])
    assert len(evidence_lost)==37
    restored_links=[]
    for m in merged:
        before=set(str(v2entry[m['id']].get(14) or '').replace(';',',').split(','))-{''}
        restored_links.extend({'entry_id':m['id'],'evidence_id':e} for e in set(m['evidence_ids'])-before)
    assert sorted((r['entry_id'],r['evidence_id']) for r in restored_links)==[('E-004-01','EV-ESM-004A'),('E-005-03','FP-002')]
    report={'candidate_path':CANDIDATE.relative_to(ROOT).as_posix(),'canonical_migration_performed':False,
      'source_hashes':hashes,'row_counts':{s['name']:len(s['rows']) for s in sheets},
      'mapping_35_to_22':mapping,'duplicate_reviews':pair_review,'evidence_texts_restored':evidence_lost,
      'original_text_cells_preserved':sum(bool(r['evidence']['original_text']) for r in master_evidence),
      'japanese_summary_cells_preserved':sum(bool(r['evidence']['japanese_summary']) for r in master_evidence),
      'evidence_links_restored':restored_links,'participation_status_counts':dict(Counter(m['participation_status'] for m in merged)),
      'verification_status_counts':dict(Counter(m['verification_status'] for m in merged)),
      'verification_review':verification_review,'team_organization_warning_ids':warning_ids,
      'source_priority':'current canonical > original snapshots > v2 schema intentions > migration history',
      'information_loss':False,'validation_status':'PENDING independent XLSX validation'}
    (WORK/'spec.json').write_text(json.dumps({'sheets':sheets},ensure_ascii=False),encoding='utf-8',newline='\n')
    (WORK/'expected.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps({k:report[k] for k in ['row_counts','participation_status_counts','verification_status_counts','evidence_links_restored']},ensure_ascii=True,indent=2))
    return report

if __name__=='__main__': prepare()
