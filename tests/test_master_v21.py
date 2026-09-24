"""Regression checks for frozen v2.1 history and reviewed later imports."""
import copy
from pathlib import Path
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from master_v21 import derive, load_bundle, read, validate_migration
from validate_research import ROOT, validate, validate_final_import


class MasterV21Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records=read(ROOT/'research/evidence/records.json')
        cls.extra=read(ROOT/'research/evidence/supplemental.json')
        cls.state=read(ROOT/'research/evidence/master-v2-1.json')
        cls.bundle=load_bundle(ROOT)
        cls.final=read(ROOT/'research/evidence/kimi-official-archive-final-import.json')
        cls.prior=read(ROOT/'research/evidence/kimi-official-archive-import-actual.json')
        prior_keys={(r['entity_type'],r['id']) for r in cls.prior['records']}
        cls.allowed_updates={(r['entity_type'],r['id']) for r in cls.final['records_updated']} - prior_keys

    def check(self,records=None,state=None):
        return validate_migration(ROOT,records if records is not None else self.records,
                                  self.extra,state if state is not None else self.state,
                                  self.allowed_updates)

    def final_check(self,records):
        migration=self.check(records=records)
        manifest=read(ROOT/'research/imported/kimi/manifest.json')
        imports={item['path']:item for item in manifest}
        return validate_final_import(ROOT,records,self.extra,migration,
            ROOT/'research/evidence/kimi-official-archive-final-import.json',imports,self.prior)

    def test_active_counts_and_original_history(self):
        self.assertEqual(validate()[1],1355)
        self.assertEqual(self.check()['counts'],{'Verified':16,'Research Lead':6,'Unresolved':0})
        entries=[r for r in self.records if r['entity_type']=='Competition Entry']
        self.assertEqual(len(entries),770)
        self.assertEqual(sum(len(r.get('entry_histories',[])) for r in entries),35)
        old=[r for r in self.bundle['original'] if r['entity_type']=='Competition Entry']
        self.assertEqual({r['id']:r for e in entries for r in e.get('entry_histories',[])},
                         {r['id']:r for r in old})

    def test_reviewed_promotions_preserve_gmo_history(self):
        before={r['Entry ID']:r['Verification Status'] for r in self.bundle['tables']['Competition Entry Map']}
        after={r['id']:r['verification']['canonical_status'] for r in self.records
               if r['entity_type']=='Competition Entry'}
        self.assertEqual({k:(before[k],after[k]) for k in before if before[k]!=after[k]},
                         {'E-042-01':('Research Lead','Verified'),
                          'E-042-02':('Research Lead','Verified'),
                          'E-042-03':('Research Lead','Verified')})
        gmo=next(r for r in self.records if r['id']=='E-005-04')
        self.assertEqual(gmo['verification']['previous_inherited_verification']['canonical_status'],'Verified')
        self.assertEqual(gmo['verification']['previous_official_archive_status'],'Research Lead')
        self.assertEqual(gmo['verification']['canonical_status'],'Verified')
        self.assertEqual(gmo['entry']['ranking'],'7')
        self.assertEqual({r['id'] for r in gmo['entry_histories']},{'E-005-04','E-C005-04'})

    def test_unamended_v21_payloads_and_supplemental_unchanged(self):
        expected,_,_=derive(self.bundle)
        expected_by_key={(r['entity_type'],r['id']):r for r in expected}
        actual_by_key={(r['entity_type'],r['id']):r for r in self.records}
        unchanged={key:value for key,value in expected_by_key.items() if key not in self.allowed_updates}
        self.assertEqual({key:actual_by_key[key] for key in unchanged},unchanged)
        self.assertEqual(self.extra,self.bundle['supplemental'])

    def test_post_v21_import_layers_are_declared(self):
        result=self.check()
        additions=[r for r in self.records if (r['entity_type'],r['id']) not in result['base_record_keys']]
        self.assertEqual(len(additions),1121)
        self.assertEqual({r['entity_type'] for r in additions},{'Evidence','Competition Entry','Team'})
        self.assertEqual({r['status'] for r in additions},{'unverified'})

    def test_gmo_official_rank_cannot_revert(self):
        changed=copy.deepcopy(self.records)
        next(r for r in changed if r['id']=='E-005-04')['entry']['ranking']='4'
        with self.assertRaises(ValueError): self.final_check(changed)

    def test_restored_evidence_link_cannot_be_dropped(self):
        changed=copy.deepcopy(self.records)
        entry=next(r for r in changed if r['id']=='E-005-03')
        entry['evidence_refs']=[r for r in entry['evidence_refs'] if r['id']!='FP-002']
        with self.assertRaises(ValueError): self.final_check(changed)

    def test_historical_group_note_cannot_be_lost(self):
        changed=copy.deepcopy(self.records)
        entry=next(r for r in changed if r['id']=='E-005-04')
        history=next(r for r in entry['entry_histories'] if r['id']=='E-C005-04')
        history['entry_history']['Notes']=None
        with self.assertRaises(ValueError): self.final_check(changed)

    def test_unknown_date_cannot_become_publication_date(self):
        changed=copy.deepcopy(self.state)
        row=changed['tables']['Date Semantics'][0]
        row['Publication Date']=row['Original Date']; row['Date Meaning']='Publication Date'
        with self.assertRaises(ValueError): self.check(state=changed)

    def test_frozen_crosswalk_cannot_be_reassigned(self):
        changed=copy.deepcopy(self.state)
        row=next(r for r in changed['tables']['ID Crosswalk'] if r['Historical ID']=='E-C005-03')
        row['Candidate ID']='E-005-04'
        with self.assertRaises(ValueError): self.check(state=changed)

    def test_reviewed_participation_cannot_revert(self):
        changed=copy.deepcopy(self.records)
        next(r for r in changed if r['id']=='E-B01-040-03')['entry']['participation_status']='Started'
        with self.assertRaises(ValueError): self.final_check(changed)


if __name__=='__main__': unittest.main()
