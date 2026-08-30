"""Independently validate exported v2.1 XLSX values and lossless source lineage.

Uses the standard-library OOXML reader, independently of the authoring library.
Does not promote, rewrite the workbook, or change canonical data.
"""
import argparse
from collections import Counter, defaultdict
import copy
import json
from pathlib import Path

from prepare_kimi_v21_candidate import CANDIDATE, WORK, REVIEW, digest, read
from research_schema import workbook_rows
from validate_research import ROOT, validate


def require(condition,message):
    if not condition: raise ValueError(message)


def tables(book):
    result={}
    for name,rows in book.items():
        header=rows[1]
        require(len(set(header.values()))==len(header),'Duplicate headers: '+name)
        result[name]=[{key:row.get(c) for c,key in header.items()} for n,row in sorted(rows.items()) if n>1]
    return result


def check_semantics(t,records,supplemental,prior):
    require([json.loads(r['Canonical Record JSON']) for r in t['Canonical Archive']]==records,'Canonical archive lost or changed information')
    require([json.loads(r['Canonical Record JSON']) for r in t['Supplemental Archive']]==supplemental,'Supplemental archive lost or changed information')
    entries={r['id']:r for r in records if r['entity_type']=='Competition Entry'}
    ev={r['id']:r for r in records if r['entity_type']=='Evidence'}
    crosswalk={r['Historical ID']:r['Candidate ID'] for r in t['ID Crosswalk']}
    require(len(t['ID Crosswalk'])==35 and set(crosswalk)==set(entries),'35 historical IDs not exactly mapped')
    require(crosswalk=={r['legacy_id']:r['canonical_id'] for r in prior['mapping_35_to_22']},'Reviewed canonical ID directions changed')
    current_pairs={tuple(sorted((r['id'],alias))) for r in entries.values() for alias in r.get('possible_duplicate_ids',[])}
    candidate_pairs={tuple(sorted((old,new))) for old,new in crosswalk.items() if old!=new}
    require(candidate_pairs==current_pairs and len(candidate_pairs)==13,'Duplicate mappings changed')
    history={r['Historical Entry ID']:r for r in t['Entry History']}
    require(len(history)==35 and set(history)==set(entries),'Historical Entries missing')
    for identity,r in history.items():
        require(json.loads(r['Canonical Record JSON'])==entries[identity],'Historical row changed: '+identity)
        require(r['Candidate Entry ID']==crosswalk[identity],'Historical crosswalk differs')
    groups=defaultdict(list)
    for identity,target in crosswalk.items(): groups[target].append(entries[identity])
    view={r['Entry ID']:r for r in t['Competition Entry Map']}
    require(len(view)==22 and set(view)==set(groups),'22 identity coverage differs')
    allowed={'Registered','Scheduled','Started','Finished','DNF','DNS','Disqualified','Unknown'}
    for identity,group in groups.items():
        row=view[identity]
        expected_refs={x['id'] for r in group for x in r['evidence_refs']}
        actual_refs=set((row['Evidence IDs'] or '').split(','))-{''}
        require(actual_refs==expected_refs,'Evidence link union differs: '+identity)
        require(actual_refs<=set(ev),'Invented Evidence ID')
        expected_part={r['entry_history'].get('Participation Status') or 'Unknown' for r in group}
        expected_part=next(iter(expected_part)) if len(expected_part)==1 else 'Unknown'
        require(row['Participation Status'] in allowed and row['Participation Status']==expected_part,'Participation changed/strengthened: '+identity)
        expected_status='Research Lead' if any(r['verification']['canonical_status']=='Research Lead' for r in group) else 'Verified'
        require(row['Verification Status']==expected_status,'Canonical verification changed without source authority: '+identity)
        require(row['Independent Status']=='not_checked','Unsupported independent verification')
        attrs={r['historical_entry_id']:r for r in json.loads(row['Historical Attributes JSON'])}
        require(set(attrs)=={r['id'] for r in group},'Historical facet omitted')
        for r in group:
            for facet in ['entry','entry_history','verification','provenance']:
                require(attrs[r['id']][facet]==r[facet],f'Historical {facet} changed: {r["id"]}')
            if r['id']!=identity:
                require({k:v for k,v in r['entry'].items() if k!='evidence_text'}=={k:v for k,v in entries[identity]['entry'].items() if k!='evidence_text'},'Distinct identity information merged')
        expected_provenance={json.dumps(p,sort_keys=True) for r in group for p in r['provenance']}
        require({json.dumps(p,sort_keys=True) for p in json.loads(row['Provenance JSON'])}==expected_provenance,'Provenance union incomplete')
        for name,key in [('Group or Heat','Group'),('Notes','Notes')]:
            values=[]
            for r in group:
                value=r['entry_history'].get(key)
                if value is not None and value not in values: values.append(value)
            require((row[name] or '')=='\n'.join(map(str,values)),name+' union incomplete')
        require(row['Result']==entries[identity]['entry']['result'] and row['Ranking']==entries[identity]['entry']['ranking'],'Selected result or ranking changed')
    require('FP-002' in view['E-005-03']['Evidence IDs'].split(','),'Missing restored FP-002 link')
    require('EV-ESM-004A' in view['E-004-01']['Evidence IDs'].split(','),'Missing restored EV-ESM-004A link')
    master=prior['source_master']
    original_ev={r['id']:r for r in ev.values() if r['source_rows'][0]['path']==master}
    require(len(t['Evidence Map'])==100 and {r['Evidence ID'] for r in t['Evidence Map']}==set(original_ev),'100 Evidence IDs not preserved')
    for r in t['Evidence Map']:
        original=original_ev[r['Evidence ID']]
        require(json.loads(r['Canonical Record JSON'])==original,'Evidence record text/content altered')
        require(r['Original Chinese Evidence']==original['evidence']['original_text'],'Detailed Evidence text lost')
        require(r['Japanese Summary']==original['evidence']['japanese_summary'],'Japanese text/placeholder lost')
        require(r['Original Date']==original['evidence']['date'],'Original date value changed')
        require(r['Date Meaning']=='Unknown' and all(r[k] is None for k in ['Event Date','Publication Date','Audit Date']),'Ambiguous date semantics guessed')
        require(r['Source Class']==(original['evidence']['source_type'] or 'Unknown'),'Source class invented')
    fragments=defaultdict(list)
    for r in t['Evidence Text Contents']:
        fragments[(r['Evidence ID'],r['Source Field'])].append((r['Part'],r['Exact Text Fragment'] or ''))
    expected_texts={}
    for identity,r in ev.items():
        for field,value in [('original_text',r.get('evidence',{}).get('original_text')),
                            ('japanese_summary',r.get('evidence',{}).get('japanese_summary')),
                            ('field_text',r.get('field_evidence',{}).get('text'))]:
            if value: expected_texts[identity,field]=value
    require({key:''.join(value for _,value in sorted(parts)) for key,parts in fragments.items()}==expected_texts,'Long-text reading view lost information')
    count=t['Count Claims'][-1]
    require(count['Count Type']=='Reported' and count['Source Class']=='Media','C-005 count qualification changed')
    require(len(t['Competition Master'])==51,'Competition count changed')
    for r in t['Competition Master']:
        require(json.loads(r['Canonical Record JSON'])==next(x for x in records if x['entity_type']=='Competition' and x['id']==r['ID']),'Competition information changed')
    master_questions=[r for r in supplemental if r['record_type']=='question' and r['source_rows'][0]['path']==master]
    require(len(t['Unknown Questions'])==31,'Master question count changed')
    require([json.loads(r['Canonical Record JSON']) for r in t['Unknown Questions']]==master_questions,'Mixed question source layouts/payload lost')
    for r in t['Unknown Questions']:
        original=next(x for x in master_questions if x['id']==r['Question ID'])
        require(r['Source Layout']==original['layout'] and json.loads(r['Source Payload JSON'])==original['question'],'Mixed question layout normalized')
    require(len(t['Historical Questions'])==6,'Additional historical questions lost')
    field=[r for r in t['Field Evidence'] if r['ID']=='FP-002']
    require(len(t['Field Evidence'])==42 and len(field)==1,'Field evidence coverage differs')
    require(json.loads(field[0]['Canonical Record JSON'])==ev['FP-002'],'FP-002 field text/provenance changed')
    warnings={r['Supplied ID'] for r in t['Unresolved Mappings'] if r['Gap Type']=='Team Name = Organization Name'}
    require(warnings==set(prior['team_equals_organization_warnings']),'Team/Organization warnings dropped')
    source={r['Competition ID']:r for r in t['Entry Source Map']}
    require(len(source)==51 and source['C-005']['Latest Recoverability']=='Medium' and source['C-021']['Latest Recoverability']=='Low','Entry Source Map regressed')
    require(len(t['Verification Review'])==6,'Six v2 downgrade decisions not evaluated')
    return {'structural_status':'PASS','information_loss':False,'dropped_evidence_links':0,
            'participation_status_counts':dict(Counter(r['Participation Status'] for r in view.values())),
            'verification_status_counts':dict(Counter(r['Verification Status'] for r in view.values())),
            'independently_verified':0,'canonical_migration_performed':False}


def audit(path=CANDIDATE,negative_checks=False):
    if (ROOT/'research/active-checkpoint.json').exists():
        # The frozen candidate is historical after promotion. Validate its bytes
        # and the active reviewed amendment without rewriting the old review.
        from master_v21 import load_bundle, validate_migration
        validate()
        bundle=load_bundle(ROOT)
        if path==CANDIDATE and not path.exists():
            path=bundle['assets']['workbook']
        require(digest(path)==digest(bundle['assets']['workbook']),
                'Historical v2.1 workbook changed after promotion')
        records=read(ROOT/'research/evidence/records.json')
        extra=read(ROOT/'research/evidence/supplemental.json')
        state=read(ROOT/'research/evidence/master-v2-1.json')
        current=validate_migration(ROOT,records,extra,state)
        controls=0
        if negative_checks:
            for kind in range(6):
                damaged=copy.deepcopy(records)
                altered=copy.deepcopy(state)
                if kind==0:
                    next(r for r in damaged if r['id']=='E-005-03')['evidence_refs']=[]
                elif kind==1:
                    next(r for r in damaged if r['id']=='EV-001')['evidence']['original_text']='Summary replacement'
                elif kind==2:
                    next(r for r in damaged if r['id']=='E-B01-040-03')['entry']['participation_status']='Finished'
                elif kind==3:
                    next(r for r in damaged if r['id']=='E-005-04')['verification']['canonical_status']='Verified'
                elif kind==4:
                    next(r for r in damaged if r['id']=='E-005-04')['entry_histories']=[]
                else:
                    altered['tables']['Date Semantics'][0]['Publication Date']='2026-08-30'
                try:
                    validate_migration(ROOT,damaged,extra,altered)
                except ValueError:
                    controls+=1
                else:
                    raise ValueError('Active migration accepted a destructive negative control')
        result={'structural_status':'PASS','role':'frozen v2.1 candidate with separately accepted GMO amendment',
                'workbook_schema_changed':False,'candidate_sha256':digest(path),
                'active_verification_counts':current['counts'],'negative_controls_passed':controls,
                'historical_review_rewritten':False}
        print(json.dumps(result,indent=2))
        return result
    expected=read(WORK/'expected.json')
    for source,value in expected['source_hashes'].items():
        require(digest(ROOT/source)==value,'Authoritative source bytes changed: '+source)
    validate()
    book=workbook_rows(path)
    spec=read(WORK/'spec.json')['sheets']
    require(set(book)=={s['name'] for s in spec},'Workbook sheet coverage differs')
    for s in spec:
        rows=book[s['name']]
        require(len(rows)==len(s['rows'])+1,'Sheet row count differs: '+s['name'])
        for n,values in enumerate([s['headers']]+s['rows'],1):
            for c,value in enumerate(values,1):
                observed=rows[n].get(c)
                require(observed==value or value=='' and observed is None,f'Export changed cell {s["name"]}!R{n}C{c}')
    records=read(ROOT/'research/evidence/records.json')
    supplemental=read(ROOT/'research/evidence/supplemental.json')
    prior=read(ROOT/'research/reviews/kimi-master-v2/review.json')
    t=tables(book)
    result=check_semantics(t,records,supplemental,prior)
    if negative_checks:
        mutations=[('dropped evidence union','Competition Entry Map',lambda x:x.update({'Evidence IDs':'EV-ESM-005A'}),'Entry ID','E-005-03'),
                   ('lost full Evidence text','Evidence Map',lambda x:x.update({'Original Chinese Evidence':'Summary replacement'}),'Evidence ID','EV-001'),
                   ('participation upgrade','Competition Entry Map',lambda x:x.update({'Participation Status':'Finished'}),'Entry ID','E-B01-040-03'),
                   ('field-only verification upgrade','Competition Entry Map',lambda x:x.update({'Verification Status':'Verified'}),'Entry ID','E-005-05'),
                   ('lost historical notes','Entry History',lambda x:x.update({'Canonical Record JSON':'{}'}),'Historical Entry ID','E-C005-04'),
                   ('guessed publication date','Evidence Map',lambda x:x.update({'Publication Date':'2026-08-30'}),'Evidence ID','EV-001')]
        for label,sheet,mutate,key,identity in mutations:
            damaged=copy.deepcopy(t);mutate(next(r for r in damaged[sheet] if r[key]==identity))
            try: check_semantics(damaged,records,supplemental,prior)
            except ValueError: pass
            else: raise ValueError('Negative control was not rejected: '+label)
        result['negative_controls_passed']=len(mutations)
    result['candidate_sha256']=digest(path)
    result['row_counts']={name:len(rows) for name,rows in t.items()}
    result['source_bytes_unchanged']=True
    expected.update(result);expected['validation_status']='PASS'
    (REVIEW/'review.json').write_text(json.dumps(expected,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
    print(json.dumps(result,ensure_ascii=True,indent=2))
    return expected

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--candidate',type=Path,default=CANDIDATE)
    p.add_argument('--negative-checks',action='store_true')
    args=p.parse_args()
    audit(args.candidate,args.negative_checks)
