"""Regression checks for manual image-result transcription normalization."""
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]

class ImageResultTranscriptionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records=json.loads((ROOT/'research/evidence/records.json').read_text(encoding='utf-8'))
        cls.state=json.loads((ROOT/'research/evidence/kimi-image-result-transcription-import.json').read_text(encoding='utf-8'))
        cls.decisions=json.loads((ROOT/'research/reviews/kimi-image-result-transcription-import/decisions.json').read_text(encoding='utf-8'))

    def test_normalized_counts(self):
        self.assertEqual(self.state['rows_to_entries'],{'rows':91,'entries':79,'teams':68,'unresolved_rows':5,'duplicate_rows':7})
        self.assertEqual(self.state['participation_statuses'],{'Finished':41,'DNF':1,'DNS':7,'Scheduled':20,'Started':10})
        self.assertEqual(self.state['new_entry_statuses'],{'Verified':69,'Research Lead':10})

    def test_every_row_decided_and_uncertain_rows_excluded(self):
        self.assertEqual(len(self.decisions),91)
        self.assertEqual(len({d['transcription_id'] for d in self.decisions}),91)
        by_key={(r['entity_type'],r['id']) for r in self.records}
        for identity in {'TR-056','TR-058','TR-079','TR-082','TR-089'}:
            self.assertNotIn(('Team',identity),by_key);self.assertNotIn(('Competition Entry',identity),by_key)

    def test_target_competition_counts(self):
        counts={cid:sum(r['entity_type']=='Competition Entry' and r['entry']['competition_id']==cid for r in self.records)
                for cid in ['C-001','C-002','C-016','C-017','C-022','C-028']}
        self.assertEqual(counts,{'C-001':5,'C-002':5,'C-016':0,'C-017':10,'C-022':17,'C-028':42})

if __name__=='__main__': unittest.main()
