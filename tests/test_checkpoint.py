"""Regression checks for checkpoint identity, provenance, and epistemic boundaries."""
import copy
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from research_schema import validate_extensions
from validate_research import ROOT, entity_types
from validate_kimi_checkpoint import audit

class CheckpointTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records=json.loads((ROOT/'research/evidence/records.json').read_text(encoding='utf-8'))
        cls.extra=json.loads((ROOT/'research/evidence/supplemental.json').read_text(encoding='utf-8'))
        cls.imports={r['path']:r for r in json.loads((ROOT/'research/imported/kimi/manifest.json').read_text(encoding='utf-8'))}
        cls.allowed=entity_types(ROOT)

    def check(self,records=None,extra=None):
        return validate_extensions(ROOT,records if records is not None else self.records,
                                   extra if extra is not None else self.extra,self.imports,self.allowed)

    def test_checkpoint_reconciliation(self):
        result=audit(ROOT/'research/evidence')
        self.assertEqual(result['reported_entry_status'],{'Verified':32,'Research Lead':3})
        self.assertEqual(result['canonical_entry_status'],{'Verified':28,'Research Lead':7})
        self.assertEqual(result['distinct_preserved_ids'],318)
        self.assertEqual(result['possible_duplicate_pairs'],13)

    def test_field_only_canonical_upgrade_rejected(self):
        records=copy.deepcopy(self.records)
        record=next(r for r in records if r['id']=='E-005-05')
        record['verification']['canonical_status']='Verified'
        with self.assertRaises(ValueError): self.check(records=records)

    def test_four_policy_downgrades_preserve_kimi_history(self):
        corrected=[r for r in self.records if r.get('verification',{}).get('policy_adjustment')]
        self.assertEqual({r['id'] for r in corrected},
                         {'E-005-05','E-005-06','E-C005-05','E-C005-06'})
        for record in corrected:
            self.assertEqual(record['verification']['canonical_status'],'Research Lead')
            self.assertEqual(record['verification']['reported_status'],'Verified')
            self.assertEqual(record['entry_history']['Verification Status'],'Verified')
            self.assertEqual(record['evidence_refs'],[{'entity_type':'Evidence','id':'FP-002'}])
            self.assertIn(record['verification']['origin'],record['provenance'])

    def test_altered_cached_source_value_rejected(self):
        records=copy.deepcopy(self.records)
        records[0]['source_rows'][0]['values'][3]='Invented title'
        with self.assertRaises(ValueError): self.check(records=records)

    def test_altered_markdown_transcription_rejected(self):
        records=copy.deepcopy(self.records)
        record=next(r for r in records if r['id']=='FP-002')
        record['source_rows'][0]['text']+=' Changed'
        with self.assertRaises(ValueError): self.check(records=records)

    def test_research_lead_cannot_be_relabelled_verified(self):
        records=copy.deepcopy(self.records)
        record=next(r for r in records if r['id']=='E-042-01')
        record['verification']['reported_status']='Verified'
        with self.assertRaises(ValueError): self.check(records=records)

    def test_reported_verified_is_not_independent_verification(self):
        records=copy.deepcopy(self.records)
        record=next(r for r in records if r['id']=='E-005-01')
        record['status']='verified'
        with self.assertRaises(ValueError): self.check(records=records)

    def test_field_evidence_cannot_be_verified_web_claim(self):
        records=copy.deepcopy(self.records)
        record=next(r for r in records if r['id']=='FP-001')
        record['status']='verified'
        with self.assertRaises(ValueError): self.check(records=records)

    def test_missing_evidence_stays_unresolved(self):
        record=next(r for r in self.records if r['id']=='RV-003')
        self.assertEqual(record['evidence_refs'],[])
        self.assertEqual(record['unresolved_references'][0]['id'],'EV-RV003')
        records=copy.deepcopy(self.records)
        next(r for r in records if r['id']=='RV-003')['evidence_refs']=[{'entity_type':'Evidence','id':'EV-RV003'}]
        with self.assertRaises(ValueError): self.check(records=records)

    def test_license_audit_is_not_a_license_entity(self):
        extra=copy.deepcopy(self.extra)
        record=next(r for r in extra if r['id']=='LA-001')
        self.assertEqual(record['asset_mention']['entity_type'],'Dataset')
        self.assertIsNone(record['asset_mention']['id'])
        record['entity_type']='License'
        with self.assertRaises(ValueError): self.check(extra=extra)

    def test_mixed_question_schemas_preserve_question_meaning(self):
        by_id={r['id']:r for r in self.extra if r['record_type']=='question'}
        for identity in ['Q-001','UQ-007','UQ-008','UQ-009']:
            record=by_id[identity]
            values=record['source_rows'][0]['values']
            expected=values[2] if identity.startswith('UQ-') else values[1]
            self.assertEqual(record['question']['question'],expected)
        self.assertEqual(by_id['UQ-007']['question']['reported_status'],'Open')

    def test_entry_entity_ids_are_not_inferred_from_names(self):
        for r in self.records:
            if r['entity_type']=='Competition Entry':
                self.assertIsNone(r['entry']['team_id'])
                self.assertIsNone(r['entry']['organization_id'])
                self.assertIsNone(r['entry']['robot_id'])
                self.assertEqual({x['target']['entity_type'] for x in r['relationships']},{'Competition'})

    def test_conflicting_historical_assessments_are_both_retained(self):
        old=next(r for r in self.extra if r['record_type']=='entry_source_assessment' and r['id']=='C-021')
        new=next(r for r in self.extra if r['record_type']=='entry_recovery_summary' and r['id']=='C-021')
        self.assertEqual(old['entry_source_assessment']['recoverability'],'Medium')
        self.assertEqual(new['entry_recovery_summary']['recoverability'],'Low')

if __name__=='__main__':
    unittest.main()
