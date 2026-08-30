"""Regression tests for import boundaries and canonical identity integrity."""

import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from import_kimi import archive
from validate_research import validate


class ResearchTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for directory in ('research/inbox/kimi', 'research/imported/kimi', 'research/evidence'):
            (self.root / directory).mkdir(parents=True)
        (self.root / 'dic.md').write_text('| Source form | Canonical | Forbidden | Meaning |\n| Evidence | Evidence | | Source |\n| Team | Team | | Group |\n', encoding='utf-8')
        (self.root / 'research/imported/kimi/manifest.json').write_text('[]', encoding='utf-8')
        self.canonical = self.root / 'research/evidence/records.json'
        self.canonical.write_text('[]', encoding='utf-8')
        self.source = self.root / 'research/inbox/kimi/input.md'
        self.source.write_bytes(b'Kimi-0001\r\nOriginal bytes\r\n')

    def records(self):
        target = archive(self.source, self.root)
        evidence = {'id': 'Kimi-0001', 'entity_type': 'Evidence', 'label': 'Test source',
                    'status': 'unverified', 'provenance': [{'path': target.relative_to(self.root).as_posix(), 'locator': 'line 1', 'source_id': 'Kimi-0001'}],
                    'evidence_refs': [], 'relationships': [],
                    'source': {field: 'unknown' for field in ('title', 'publisher', 'date', 'url', 'accessed_at', 'version', 'verification_note')}}
        self.canonical.write_text(json.dumps([evidence]), encoding='utf-8')
        return evidence

    def test_byte_identity_and_idempotence(self):
        target = archive(self.source, self.root)
        self.assertEqual(target.read_bytes(), self.source.read_bytes())
        self.assertEqual(archive(self.source, self.root), target)
        self.assertEqual(validate(self.root), (1, 0))

    def test_external_source_rejected(self):
        outside = self.root / 'outside.md'
        outside.write_text('external', encoding='utf-8')
        with self.assertRaises(ValueError):
            archive(outside, self.root)
        self.assertEqual(outside.read_text(encoding='utf-8'), 'external')

    def test_changed_snapshot_rejected(self):
        target = archive(self.source, self.root)
        target.write_bytes(b'changed')
        with self.assertRaises(ValueError):
            validate(self.root)
        with self.assertRaises(ValueError):
            archive(self.source, self.root)

    def test_changed_id_rejected(self):
        evidence = self.records()
        evidence['id'] = 'Kimi-1'
        self.canonical.write_text(json.dumps([evidence]), encoding='utf-8')
        with self.assertRaises(ValueError):
            validate(self.root)

    def test_duplicate_identity_rejected(self):
        evidence = self.records()
        self.canonical.write_text(json.dumps([evidence, evidence]), encoding='utf-8')
        with self.assertRaises(ValueError):
            validate(self.root)

    def test_typed_identity_and_dangling_reference(self):
        evidence = self.records()
        team = copy.deepcopy(evidence)
        team['entity_type'] = 'Team'
        team.pop('source')
        team['evidence_refs'] = [{'entity_type': 'Evidence', 'id': evidence['id']}]
        self.canonical.write_text(json.dumps([evidence, team]), encoding='utf-8')
        self.assertEqual(validate(self.root), (1, 2))
        team['evidence_refs'][0]['id'] = 'missing'
        self.canonical.write_text(json.dumps([evidence, team]), encoding='utf-8')
        with self.assertRaises(ValueError):
            validate(self.root)


if __name__ == '__main__':
    unittest.main()
