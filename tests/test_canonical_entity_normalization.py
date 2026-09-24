"""Regression checks for canonical Team, Organization, and Robot identity links."""
import json
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]


class CanonicalEntityNormalizationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records=json.loads((ROOT/'research/evidence/records.json').read_text(encoding='utf-8'))
        cls.state=json.loads((ROOT/'research/evidence/canonical-entity-normalization.json').read_text(encoding='utf-8'))
        cls.decisions=json.loads((ROOT/'research/reviews/canonical-entity-normalization/decisions.json').read_text(encoding='utf-8'))
        cls.by_key={(r['entity_type'],r['id']):r for r in cls.records}

    def test_before_after_metrics(self):
        self.assertEqual(self.state['before'],{
            'records':1355,'entries':770,'teams':75,'organizations':4,'robot_platforms':0,
            'entries_with_team_id':79,'entries_with_organization_id':0,
            'entries_with_robot_platform_id':0})
        self.assertEqual(self.state['after'],{
            'records':1683,'entries':770,'teams':356,'organizations':46,'robot_platforms':5,
            'entries_with_team_id':744,'entries_with_organization_id':83,
            'entries_with_robot_platform_id':4})

    def test_aliases_and_unresolved_names(self):
        expected={'天工队':'TR-005','⽆锡智元赛队':'TR-022',
                  '北⽅⼯⼤博远智⾏-璇玑队':'TR-031','⼆进制⻮轮':'TR-035',
                  '上海高奕队':'TR-021','RUC-HiLigh':'TR-069'}
        self.assertEqual({d['raw_name']:d['team_id'] for d in self.decisions['team_aliases_resolved']},expected)
        entries=[r for r in self.records if r['entity_type']=='Competition Entry']
        for raw,team_id in expected.items():
            self.assertTrue(all(r['entry']['team_id']==team_id for r in entries if r['entry']['team_name']==raw))
        blocked=set(self.decisions['blocked_team_names'])
        self.assertEqual(sum(r['entry']['team_id'] is None for r in entries),26)
        self.assertTrue(all((r['entry']['team_name'] in blocked)==(r['entry']['team_id'] is None) for r in entries))

    def test_duplicate_class_entries_remain_distinct(self):
        a=self.by_key[('Competition Entry','TR-062')]
        b=self.by_key[('Competition Entry','TR-086')]
        self.assertEqual((a['entry']['team_id'],b['entry']['team_id']),('TR-023','TR-023'))
        self.assertEqual({a['entry']['group'],b['entry']['group']},{'58KG','40KG'})
        self.assertEqual(self.state['duplicate_entries_consolidated'],0)

    def test_robot_and_verification_safety(self):
        self.assertEqual(self.by_key[('Competition Entry','E-005-01')]['entry']['robot_id'],'CRP-001')
        self.assertEqual(self.by_key[('Competition Entry','E-B01-036-01')]['entry']['robot_id'],'CRP-002')
        self.assertEqual(self.state['entry_status_counts'],{'Verified':758,'Research Lead':12})
        self.assertEqual(sum(r['entity_type']=='Competition Entry' for r in self.records),770)


if __name__=='__main__': unittest.main()
