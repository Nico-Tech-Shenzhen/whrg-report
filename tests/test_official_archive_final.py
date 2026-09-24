"""Regression checks for the independently reviewed official archive import."""
import json
from pathlib import Path
import unittest


ROOT=Path(__file__).resolve().parents[1]


class OfficialArchiveFinalTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records=json.loads((ROOT/'research/evidence/records.json').read_text(encoding='utf-8'))
        cls.state=json.loads((ROOT/'research/evidence/kimi-official-archive-final-import.json').read_text(encoding='utf-8'))
        cls.decisions=json.loads((ROOT/'research/reviews/kimi-official-archive-final-import/entry-decisions.json').read_text(encoding='utf-8'))

    def test_reviewed_counts(self):
        self.assertEqual(len(self.records),1355)
        self.assertEqual(self.state['evidence_disposition'],{
            'accepted_new':257,'new_pages':124,'new_attachment_payloads':133,
            'deduplicated':49,'rejected':0})
        self.assertEqual(self.state['entry_summary']['new_identities'],669)
        self.assertEqual(self.state['canonical_entry_counts'],{
            'Verified':689,'Research Lead':2,'Unresolved':0})

    def test_every_candidate_has_one_effect(self):
        self.assertEqual(len(self.decisions),1005)
        self.assertEqual(len({d['candidate_id'] for d in self.decisions}),1005)
        self.assertEqual({name:sum(d['effect']==name for d in self.decisions) for name in 'ABCD'},
                         {'A':12,'B':4,'C':918,'D':71})

    def test_priority_result_treatments(self):
        by_id={r['id']:r for r in self.records}
        self.assertEqual(by_id['OEC-2026-0405']['entry']['participation_status'],'DNF')
        self.assertIsNone(by_id['OEC-2026-0405']['entry']['ranking'])
        self.assertEqual(by_id['OEC-2026-0193']['entry']['ranking'],'1')
        self.assertEqual(by_id['E-005-04']['entry']['ranking'],'7')
        self.assertEqual(by_id['E-005-04']['verification']['canonical_status'],'Verified')

    def test_ambiguities_and_entity_boundaries(self):
        by_id={r['id']:r for r in self.records}
        for identity in ['OEC-2026-0721','OEC-2026-0725','OEC-2026-0726',
                         'OEC-2026-0702','OEC-2026-0703','OEC-2026-0709']:
            self.assertNotIn(identity,by_id)
        self.assertEqual(self.state['entity_additions'],{'Evidence':257,'Competition Entry':669})


if __name__=='__main__': unittest.main()
