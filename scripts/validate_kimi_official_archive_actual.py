#!/usr/bin/env python3
"""Validate the reviewed additive Kimi import and its negative controls."""

import argparse
import copy
import json
from pathlib import Path

from master_v21 import STATE_NAME, derive, load_bundle, read, record_key, validate_migration
from validate_research import (FINAL_IMPORT_STATE_NAME, NORMALIZATION_STATE_NAME, POST_V21_STATE_NAME,
                               TRANSCRIPTION_STATE_NAME, ROOT,
                               validate_final_import, validate_post_v21_import)


def audit(directory,negative_checks=False):
    records=read(directory/'records.json')
    supplemental=read(directory/'supplemental.json')
    prior=read(directory/POST_V21_STATE_NAME)
    final_path=directory/FINAL_IMPORT_STATE_NAME
    final=read(final_path) if final_path.is_file() else None
    transcription_path=directory/TRANSCRIPTION_STATE_NAME
    transcription=read(transcription_path) if transcription_path.is_file() else None
    normalization_path=directory/NORMALIZATION_STATE_NAME
    normalization=read(normalization_path) if normalization_path.is_file() else None
    normalization_additions={(r['entity_type'],r['id']) for r in (normalization or {}).get('records_added',[])}
    normalization_updates={(r['entity_type'],r['id']) for r in (normalization or {}).get('records_updated',[])}
    later={(r['entity_type'],r['id']) for r in (transcription or {}).get('records_added',[])}|normalization_additions
    prior_keys={(r['entity_type'],r['id']) for r in prior['records']}
    allowed={(r['entity_type'],r['id']) for r in (final or {}).get('records_updated',[])}|normalization_updates
    base_keys={record_key(r) for r in derive(load_bundle(ROOT))[0]}
    migration=validate_migration(ROOT,records,supplemental,read(directory/STATE_NAME),allowed&base_keys)
    manifest=read(ROOT/'research/imported/kimi/manifest.json')
    imports={item['path']:item for item in manifest}
    state_path=directory/POST_V21_STATE_NAME
    accepted=validate_post_v21_import(ROOT,records,supplemental,migration,state_path,imports,
                                      allowed,final is not None)
    if final is not None:
        validate_final_import(ROOT,records,supplemental,migration,final_path,imports,prior,later,
                              bool(transcription),normalization_updates)
    controls=0
    if negative_checks:
        state=read(state_path)
        mutations=[]

        dropped=copy.deepcopy(records)
        dropped.pop(next(i for i,r in enumerate(dropped) if r['id']=='EV-122'))
        mutations.append((dropped,supplemental,'dropped accepted Evidence'))

        reclassified=copy.deepcopy(records)
        next(r for r in reclassified if r['id']=='EV-086')['evidence']['source_type']='Enterprise'
        mutations.append((reclassified,supplemental,'reversed publisher-based source class'))

        invented=copy.deepcopy(records)
        extra=copy.deepcopy(next(r for r in invented if r['id']=='EV-081'))
        extra['id']='EV-INVENTED'
        invented.append(extra)
        mutations.append((invented,supplemental,'unregistered Evidence identity'))

        upgraded=copy.deepcopy(records)
        next(r for r in upgraded if r['id']=='EV-122')['status']='verified'
        mutations.append((upgraded,supplemental,'independent verification upgrade'))

        changed_base=copy.deepcopy(records)
        next(r for r in changed_base if r['id']=='E-005-04')['verification']['canonical_status']='Research Lead'
        mutations.append((changed_base,supplemental,'reviewed GMO promotion reversal'))

        extra_supplemental=copy.deepcopy(supplemental)
        item=copy.deepcopy(extra_supplemental[0])
        item['id']='NEGATIVE-CONTROL'
        extra_supplemental.append(item)
        mutations.append((records,extra_supplemental,'unauthorized supplemental addition'))

        for changed,extra,label in mutations:
            try:
                changed_migration=validate_migration(ROOT,changed,extra,read(directory/STATE_NAME),allowed&base_keys)
                validate_post_v21_import(ROOT,changed,extra,changed_migration,state_path,imports,
                                         allowed,final is not None)
                if final is not None:
                    validate_final_import(ROOT,changed,extra,changed_migration,final_path,imports,prior,later,
                                          bool(transcription),normalization_updates)
            except ValueError:
                controls+=1
            else:
                raise ValueError('Negative control was accepted: '+label)
    result={
        'structural_status':'PASS',
        'accepted_evidence_records':accepted,
        'prior_import_entry_counts':read(state_path)['canonical_entry_counts'],
        'current_entry_counts':final['canonical_entry_counts'] if final else read(state_path)['canonical_entry_counts'],
        'negative_controls_passed':controls,
        'v2_1_base_preserved_with_reviewed_amendments':True,
    }
    print(json.dumps(result,indent=2))
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--directory',type=Path,default=ROOT/'research/evidence')
    parser.add_argument('--negative-checks',action='store_true')
    args=parser.parse_args()
    audit(args.directory,args.negative_checks)


if __name__=='__main__':
    main()
