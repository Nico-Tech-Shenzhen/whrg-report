#!/usr/bin/env python3
"""Validate the reviewed additive Kimi import and its negative controls."""

import argparse
import copy
import json
from pathlib import Path

from master_v21 import STATE_NAME, read, validate_migration
from validate_research import POST_V21_STATE_NAME, ROOT, validate_post_v21_import


def audit(directory,negative_checks=False):
    records=read(directory/'records.json')
    supplemental=read(directory/'supplemental.json')
    migration=validate_migration(ROOT,records,supplemental,read(directory/STATE_NAME))
    manifest=read(ROOT/'research/imported/kimi/manifest.json')
    imports={item['path']:item for item in manifest}
    state_path=directory/POST_V21_STATE_NAME
    accepted=validate_post_v21_import(ROOT,records,supplemental,migration,state_path,imports)
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
        next(r for r in changed_base if r['id']=='E-005-04')['verification']['canonical_status']='Verified'
        mutations.append((changed_base,supplemental,'v2.1 GMO downgrade reversal'))

        extra_supplemental=copy.deepcopy(supplemental)
        item=copy.deepcopy(extra_supplemental[0])
        item['id']='NEGATIVE-CONTROL'
        extra_supplemental.append(item)
        mutations.append((records,extra_supplemental,'unauthorized supplemental addition'))

        for changed,extra,label in mutations:
            try:
                changed_migration=validate_migration(ROOT,changed,extra,read(directory/STATE_NAME))
                validate_post_v21_import(ROOT,changed,extra,changed_migration,state_path,imports)
            except ValueError:
                controls+=1
            else:
                raise ValueError('Negative control was accepted: '+label)
    result={
        'structural_status':'PASS',
        'accepted_evidence_records':accepted,
        'canonical_entry_counts':read(state_path)['canonical_entry_counts'],
        'negative_controls_passed':controls,
        'v2_1_base_unchanged':True,
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
