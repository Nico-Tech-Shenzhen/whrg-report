"""Validate typed research extensions and exact archived source rows using stdlib."""
from functools import lru_cache
from pathlib import PurePosixPath
import re
import xml.etree.ElementTree as ET
from zipfile import ZipFile

NS = {'s':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
REL = '{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id'
PAYLOADS = {
    'question': {'question','reported_status'},
    'license_audit': {'asset_name','asset_type','license_found','result'},
    'license_audit_summary': {'asset_name','result'},
    'rule_change': {'old_rule','new_rule','evidence_text'},
    'case_study': {'organization','key_finding','evidence_text'},
    'open_data_audit': {'audit_item','finding'},
    'open_data_state': {'state','definition','finding'},
    'census_metric': {'metric','value','source_keys'},
    'recruitment_cohort': {'team_name','formation_type','evidence_text'},
    'identity_mapping': {'candidate_types','reason','open_knowledge'},
    'entry_source_assessment': {'competition_name','recoverability','coverage_type'},
    'entry_recovery_summary': {'competition_name','recoverability','unresolved'},
    'competition_count_summary': {'Competition ID','Count Type','Total teams stated (reported)'},
    'historical_validation': {'check','reported_result'},
    'workbook_context': {'role'},
}

def string(value):
    return isinstance(value,str) and bool(value.strip())

def col_number(cell):
    number=0
    for char in re.match(r'[A-Z]+',cell)[0]:
        number=number*26+ord(char)-64
    return number

def column_name(number):
    result=''
    while number:
        number,rem=divmod(number-1,26)
        result=chr(65+rem)+result
    return result

@lru_cache(maxsize=16)
def workbook_rows(path):
    """Read inert OOXML values, not formulas, macros, relationships, or web links."""
    result={}
    with ZipFile(path) as archive:
        names=archive.namelist()
        strings=[]
        if 'xl/sharedStrings.xml' in names:
            tree=ET.fromstring(archive.read('xl/sharedStrings.xml'))
            strings=[''.join(t.text or '' for t in e.findall('.//s:t',NS))
                     for e in tree.findall('s:si',NS)]
        relations=ET.fromstring(archive.read('xl/_rels/workbook.xml.rels'))
        targets={r.attrib['Id']:r.attrib['Target'] for r in relations}
        tree=ET.fromstring(archive.read('xl/workbook.xml'))
        for sheet in tree.findall('s:sheets/s:sheet',NS):
            target=targets[sheet.attrib[REL]]
            member=target.lstrip('/') if target.startswith('/') else str(PurePosixPath('xl')/target)
            if '..' in PurePosixPath(member).parts:
                raise ValueError('Unexpected workbook relationship path')
            data=ET.fromstring(archive.read(member))
            rows={}
            for row in data.findall('s:sheetData/s:row',NS):
                values={}
                for cell in row.findall('s:c',NS):
                    index=col_number(cell.attrib['r'])
                    kind=cell.attrib.get('t')
                    value=cell.find('s:v',NS)
                    if cell.find('s:f',NS) is not None:
                        raise ValueError('Source formulas require explicit review before canonical extraction')
                    if kind=='inlineStr':
                        value=''.join(t.text or '' for t in cell.findall('.//s:t',NS)) if cell.find('s:is',NS) is not None else None
                    elif value is not None:
                        value=value.text
                        if kind=='s': value=strings[int(value)]
                        elif kind=='b': value=value=='1'
                        elif kind not in ('str','e'):
                            value=float(value) if any(x in value.lower() for x in ['.','e']) else int(value)
                    else:
                        value=None
                    if value is not None: values[index]=value
                if values: rows[int(row.attrib['r'])]=values
            result[sheet.attrib['name']]=rows
    return result

def validate_source_rows(root,item,imports):
    rows=item.get('source_rows')
    if rows is None:
        return
    if not isinstance(rows,list) or not rows:
        raise ValueError('source_rows must be nonempty')
    identities=[]
    for source in rows:
        if source.get('path') not in imports or not string(source.get('locator')):
            raise ValueError('Invalid archived row source')
        path=root/source['path']
        if path.suffix=='.xlsx':
            sheet=source.get('sheet')
            number=source.get('row')
            values=source.get('values')
            if not isinstance(number,int) or not isinstance(values,list) or not values:
                raise ValueError('Invalid workbook row locator')
            expected=workbook_rows(path).get(sheet,{}).get(number)
            if expected is None:
                raise ValueError(f'Missing worksheet row: {source}')
            actual={i:v for i,v in enumerate(values,1) if v is not None}
            headers=source.get('headers')
            if headers is not None:
                header_row=source.get('header_row')
                source_headers=workbook_rows(path).get(sheet,{}).get(header_row)
                if not isinstance(headers,list) or {i:v for i,v in enumerate(headers,1) if v is not None}!=source_headers:
                    raise ValueError('Worksheet headers differ from the archived header row')
            if actual!=expected:
                raise ValueError(f'Changed extracted values: {sheet}/{number}')
            if source['locator']!=f"'{sheet}'!A{number}:{column_name(len(values))}{number}":
                raise ValueError('Worksheet range does not match extracted row')
            if source.get('source_id') is not None:
                column=source.get('id_column')
                if not isinstance(column,int) or column<1 or column>len(values):
                    raise ValueError('Missing source ID column')
                if not isinstance(values[column-1],str) or values[column-1]!=source['source_id']:
                    raise ValueError('Source identifier cell mismatch')
        elif path.suffix=='.md':
            start,end=source.get('line_start'),source.get('line_end')
            lines=path.read_text(encoding='utf-8').splitlines()
            if not isinstance(start,int) or not isinstance(end,int) or not 1<=start<=end<=len(lines):
                raise ValueError('Invalid Markdown source lines')
            if source.get('text')!='\n'.join(lines[start-1:end]):
                raise ValueError('Changed extracted Markdown')
            if source['locator']!=f'lines {start}-{end}':
                raise ValueError('Markdown locator mismatch')
            if source.get('source_id') is not None:
                if not re.match(r'^## '+re.escape(source['source_id'])+r'\s',lines[start-1]):
                    raise ValueError('Markdown ID does not match source heading')
        else:
            raise ValueError('Unsupported source row format')
        identities.append({k:source.get(k) for k in ('path','locator','source_id')})
    for p in item['provenance']:
        if p not in identities:
            raise ValueError('Provenance is not backed by an exact source row')

def validate_references(item,keys,allowed):
    if not isinstance(item.get('evidence_refs'),list) or not isinstance(item.get('relationships'),list):
        raise ValueError('Reference fields must be lists')
    for ref in item['evidence_refs']:
        if ref.get('entity_type')!='Evidence' or ('Evidence',ref.get('id')) not in keys:
            raise ValueError(f'Unresolved evidence reference: {ref}')
    for relation in item['relationships']:
        target=relation.get('target',{})
        if not string(relation.get('relation')) or (target.get('entity_type'),target.get('id')) not in keys:
            raise ValueError(f'Unresolved typed relationship: {relation}')
    gaps=item.get('unresolved_references',[])
    if not isinstance(gaps,list):
        raise ValueError('unresolved_references must be a list')
    for ref in gaps:
        if ref.get('entity_type') not in allowed or not string(ref.get('id')) or not string(ref.get('reason')):
            raise ValueError('Unresolved references require type, exact ID, and reason')
    for field in ['asset_mention','license_mention']:
        mention=item.get(field)
        if mention is not None and (mention.get('entity_type') not in allowed or mention.get('id') is not None):
            raise ValueError('Unidentified mentions must retain a separate type and null ID')

def field_only_entry(item, evidence):
    """Whether every linked supporting Evidence record is field evidence."""
    refs = item.get('evidence_refs', [])
    return bool(refs) and all(
        evidence.get(ref['id'], {}).get('evidence_kind') == 'field_evidence'
        for ref in refs
    )

def apply_entry_verification_policy(records):
    """Preserve source status; downgrade field-only entries in canonical status."""
    evidence = {r['id']: r for r in records if r['entity_type'] == 'Evidence'}
    for item in records:
        if item['entity_type'] != 'Competition Entry':
            continue
        verification = item['verification']
        reported = verification['reported_status']
        canonical = 'Research Lead' if field_only_entry(item, evidence) else reported
        verification['canonical_status'] = canonical
        if canonical != reported:
            verification['policy_adjustment'] = {
                'reason': 'Only Field Evidence supports this entry; no Primary Web Evidence is linked. Retained as a Research Lead under repository evidence policy.',
                'evidence_refs': [dict(ref) for ref in item['evidence_refs']],
            }

def validate_extensions(root,records,supplemental,imports,allowed):
    if not isinstance(supplemental,list):
        raise ValueError('Supplemental research must be a list')
    keys={(r['entity_type'],r['id']) for r in records}
    evidence={r['id']:r for r in records if r['entity_type']=='Evidence'}
    supplemental_keys=set()
    for item in supplemental:
        kind=item.get('record_type')
        if kind not in PAYLOADS or not isinstance(item.get(kind),dict) or not PAYLOADS[kind]<=item[kind].keys():
            raise ValueError(f'Invalid supplemental record payload: {kind}')
        if 'entity_type' in item:
            raise ValueError('Supplemental research is not an entity')
        identity=item.get('id')
        if identity is not None and not string(identity):
            raise ValueError('Invalid supplemental source ID')
        if not string(item.get('label')) or item.get('status') not in ['unverified','verified','disputed']:
            raise ValueError('Invalid supplemental label or status')
        provenance=item.get('provenance')
        if not isinstance(provenance,list) or not provenance:
            raise ValueError('Supplemental provenance required')
        for p in provenance:
            if p.get('path') not in imports or p.get('source_id')!=identity or not string(p.get('locator')):
                raise ValueError('Supplemental provenance mismatch')
        key=(kind,identity) if identity is not None else (kind,provenance[0]['path'],provenance[0]['locator'])
        if key in supplemental_keys:
            raise ValueError('Duplicate supplemental identity')
        supplemental_keys.add(key)
        if not item.get('source_rows'):
            raise ValueError('Supplemental source rows required')
    for item in records+supplemental:
        validate_source_rows(root,item,imports)
        validate_references(item,keys,allowed)
        if item.get('evidence_kind') in ['field_evidence','search_audit'] and item['status']=='verified':
            raise ValueError('A field/search lead cannot be an independently verified web claim')
        verification=item.get('verification')
        if verification:
            if item.get('entity_type')!='Competition Entry' or verification.get('reported_status') not in ['Verified','Research Lead']:
                raise ValueError('Invalid imported verification state')
            if verification.get('authority')!='Kimi' or verification.get('independent_status')!='not_checked':
                raise ValueError('Imported Kimi state must be distinguished from independent verification')
            if item['status']=='verified' or verification.get('origin') not in item['provenance']:
                raise ValueError('Imported verification needs historical provenance and unverified independent status')
            origin=verification['origin']
            rows=[r for r in item['source_rows'] if all(r.get(k)==origin[k] for k in origin)]
            if not rows or 'Verification Status' not in (rows[0].get('headers') or []):
                raise ValueError('Imported status has no historical column')
            offset=rows[0]['headers'].index('Verification Status')
            if rows[0]['values'][offset]!=verification['reported_status']:
                raise ValueError('Reported status differs from archived historical row')
            if item.get('entry_history',{}).get('Verification Status')!=verification['reported_status']:
                raise ValueError('Entry history and reported status differ')
            reported=verification['reported_status']
            expected='Research Lead' if field_only_entry(item,evidence) else reported
            if verification.get('canonical_status')!=expected:
                raise ValueError('Canonical status must retain Research Lead for field-only entries')
            if expected!=reported:
                adjustment=verification.get('policy_adjustment',{})
                if not string(adjustment.get('reason')) or adjustment.get('evidence_refs')!=item['evidence_refs']:
                    raise ValueError('Canonical downgrade requires an explanation and linked evidence basis')
        if 'possible_duplicate_ids' in item:
            for identity in item['possible_duplicate_ids']:
                if ('Competition Entry',identity) not in keys or identity==item['id']:
                    raise ValueError('Invalid possible duplicate reference')
    return len(supplemental)
