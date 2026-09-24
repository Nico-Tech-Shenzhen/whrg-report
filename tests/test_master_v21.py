"""Regression checks for accepted v2.1 history and the GMO-only downgrade."""
import copy
from pathlib import Path
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from master_v21 import derive, load_bundle, read, validate_migration
from validate_research import ROOT, validate


class MasterV21Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records=read(ROOT/'research/evidence/records.json')
        cls.extra=read(ROOT/'research/evidence/supplemental.json')
        cls.state=read(ROOT/'research/evidence/master-v2-1.json')
        cls.bundle=load_bundle(ROOT)

    def check(self,records=None,state=None):
        return validate_migration(ROOT,records if records is not None else self.records,
                                  self.extra,state if state is not None else self.state)

    def test_active_counts_and_original_history(self):
        self.assertEqual(validate()[1],282)
        self.assertEqual(self.check()['counts'],{'Verified':16,'Research Lead':6,'Unresolved':0})
        entries=[r for r in self.records if r['entity_type']=='Competition Entry']
        self.assertEqual(len(entries),22)
        self.assertEqual(sum(len(r['entry_histories']) for r in entries),35)
        old=[r for r in self.bundle['original'] if r['entity_type']=='Competition Entry']
        self.assertEqual({r['id']:r for e in entries for r in e['entry_histories']},
                         {r['id']:r for r in old})

    def test_gmo_downgrade_is_only_verification_change(self):
        before={r['Entry ID']:r['Verification Status'] for r in self.bundle['tables']['Competition Entry Map']}
        after={r['id']:r['verification']['canonical_status'] for r in self.records if r['entity_type']=='Competition Entry'}
        self.assertEqual({k:(before[k],after[k]) for k in after if before[k]!=after[k]},
                         {'E-005-04':('Verified','Research Lead')})
        gmo=next(r for r in self.records if r['id']=='E-005-04')
        self.assertEqual(gmo['verification']['previous_inherited_verification']['canonical_status'],'Verified')
        self.assertEqual(gmo['verification']['reported_status'],'Verified')
        self.assertEqual(gmo['verification']['independent_status'],'not_checked')
        self.assertEqual({r['id'] for r in gmo['evidence_refs']},{'FP-002','EV-ESM-005A'})
        self.assertEqual({r['id'] for r in gmo['entry_histories']},{'E-005-04','E-C005-04'})

    def test_non_entry_data_and_all_evidence_text_unchanged(self):
        expected,_,_=derive(self.bundle)
        expected_by_key={(r['entity_type'],r['id']):r for r in expected}
        actual_by_key={(r['entity_type'],r['id']):r for r in self.records}
        self.assertEqual({key:actual_by_key[key] for key in expected_by_key},expected_by_key)
        self.assertEqual(self.extra,self.bundle['supplemental'])

    def test_post_v21_import_is_additive_evidence_only(self):
        result=self.check()
        additions=[r for r in self.records if (r['entity_type'],r['id']) not in result['base_record_keys']]
        self.assertEqual(len(additions),48)
        self.assertEqual({r['entity_type'] for r in additions},{'Evidence'})
        self.assertEqual({r['status'] for r in additions},{'unverified'})

    def test_gmo_cannot_revert_to_inherited_verified(self):
        changed=copy.deepcopy(self.records)
        next(r for r in changed if r['id']=='E-005-04')['verification']['canonical_status']='Verified'
        with self.assertRaises(ValueError): self.check(records=changed)

    def test_restored_evidence_link_cannot_be_dropped(self):
        changed=copy.deepcopy(self.records)
        entry=next(r for r in changed if r['id']=='E-005-03')
        entry['evidence_refs']=[r for r in entry['evidence_refs'] if r['id']!='FP-002']
        with self.assertRaises(ValueError): self.check(records=changed)

    def test_historical_group_note_cannot_be_lost(self):
        changed=copy.deepcopy(self.records)
        entry=next(r for r in changed if r['id']=='E-005-04')
        history=next(r for r in entry['entry_histories'] if r['id']=='E-C005-04')
        history['entry_history']['Notes']=None
        with self.assertRaises(ValueError): self.check(records=changed)

    def test_unknown_date_cannot_become_publication_date(self):
        changed=copy.deepcopy(self.state)
        row=changed['tables']['Date Semantics'][0]
        row['Publication Date']=row['Original Date']
        row['Date Meaning']='Publication Date'
        with self.assertRaises(ValueError): self.check(state=changed)

    def test_frozen_crosswalk_cannot_be_reassigned(self):
        changed=copy.deepcopy(self.state)
        row=next(r for r in changed['tables']['ID Crosswalk'] if r['Historical ID']=='E-C005-03')
        row['Candidate ID']='E-005-04'
        with self.assertRaises(ValueError): self.check(state=changed)

    def test_no_participation_upgrade(self):
        changed=copy.deepcopy(self.records)
        next(r for r in changed if r['id']=='E-B01-040-03')['entry']['participation_status']='Finished'
        with self.assertRaises(ValueError): self.check(records=changed)


if __name__=='__main__': unittest.main()
