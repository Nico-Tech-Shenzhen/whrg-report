import copy
import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))

from normalize_organization_robot_platform import normalize, protected_entry_facts  # noqa: E402


class OrganizationRobotPlatformNormalizationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.records = json.loads((ROOT / 'research/evidence/records.json').read_text(encoding='utf-8'))

    def by_key(self):
        return {(item['entity_type'], item['id']): item for item in self.records}

    def test_expected_counts(self):
        by_type = {}
        for item in self.records:
            by_type[item['entity_type']] = by_type.get(item['entity_type'], 0) + 1
        self.assertEqual(by_type['Organization'], 64)
        self.assertEqual(by_type['Robot Platform'], 15)
        entries = [item for item in self.records if item['entity_type'] == 'Competition Entry']
        self.assertEqual(sum(bool(item['entry'].get('organization_id')) for item in entries), 84)
        self.assertEqual(sum(bool(item['entry'].get('robot_id')) for item in entries), 5)

    def test_joint_team_preserves_multiple_organizations(self):
        team = self.by_key()[('Team', 'TR-061')]
        members = {
            item['target']['id'] for item in team['relationships']
            if item['relation'] == 'joint_team_member'
        }
        self.assertEqual(members, {'CNO-022', 'CNO-051', 'CNO-017'})
        entry = self.by_key()[('Competition Entry', 'TR-061')]
        self.assertIsNone(entry['entry']['organization_id'])

    def test_gmo_entry_has_only_supported_platform_link(self):
        entry = self.by_key()[('Competition Entry', 'E-005-04')]
        self.assertEqual(entry['entry']['robot_id'], 'CRP-005')
        self.assertIn({'entity_type': 'Evidence', 'id': 'EV-021'}, entry['evidence_refs'])
        other_entries = [
            item for item in self.records
            if item['entity_type'] == 'Competition Entry' and item['entry'].get('team_id') == 'INT-003'
            and item['id'] != 'E-005-04'
        ]
        self.assertFalse(other_entries)

    def test_provider_is_not_team_affiliation(self):
        team = self.by_key()[('Team', 'INT-001')]
        self.assertIn(
            {'relation': 'platform_provider', 'target': {'entity_type': 'Organization', 'id': 'CNO-011'}},
            team['relationships'],
        )
        self.assertNotIn(
            {'relation': 'affiliated_with', 'target': {'entity_type': 'Organization', 'id': 'CNO-011'}},
            team['relationships'],
        )

    def test_entry_protected_facts_are_unchanged_by_normalizer(self):
        state_path = ROOT / 'research/evidence/organization-robot-platform-normalization.json'
        state = json.loads(state_path.read_text(encoding='utf-8'))
        by_key = self.by_key()
        for item in state['records_updated']:
            if item['entity_type'] == 'Competition Entry':
                self.assertEqual(protected_entry_facts(by_key[(item['entity_type'], item['id'])]),
                                 item['protected_facts'])

    def test_normalizer_refuses_reapplication(self):
        with self.assertRaises(ValueError):
            normalize(copy.deepcopy(self.records))


if __name__ == '__main__':
    unittest.main()
