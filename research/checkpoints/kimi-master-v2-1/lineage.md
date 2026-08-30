# Accepted Master v2.1 lineage

Master v2.1 semantics are active. The original candidate workbook is preserved byte for byte with its existing schema. The canonical model applies one documented amendment: E-005-04, GMO Robots, changes from inherited Verified to Research Lead after the narrow existing-evidence review. See [GMO review](../../reviews/kimi-master-v2-1/gmo-verification.md).

## Lineage

1. Original Kimi Master and staging snapshots produced the first canonical checkpoint. The pre-migration canonical commit is 49335162823dab24840de72c8309961c2de5cd21. Its 247 entity records and 206 supplemental records are preserved as exact bytes in previous-canonical/. Its source snapshots and first-checkpoint schema/ID inventory remain in their original locations.
2. Rejected Kimi v2 remains in the content-addressed import archive, with its [rejection review](../../reviews/kimi-master-v2/review.md). It was never canonical and supplies no factual authority for this promotion. It documents the attempted migration, not an accepted intermediate dataset.
3. Corrected v2.1 was built from the pre-migration canonical data and original snapshots. Its [candidate review](../../reviews/kimi-master-v2-1/review.md) remains unchanged, including the then-unresolved GMO exception. Its 35 -> 22 crosswalk and all 13 duplicate mappings are carried forward exactly, without reconsideration.
4. The narrow GMO review resolves that verification exception by downgrade. The accepted canonical corpus has 234 entities: 22 Competition Entries, 51 Competitions, 142 Evidence, 7 Teams, 4 Organizations, and 8 Rule Versions. All 206 supplemental records remain byte-identical in canonical storage. All 35 historical Entry records remain complete inside the 22 active Entry records and in previous-canonical/.

## Canonical mapping

- records.json remains the typed entity corpus. Each Entry retains exact source-row provenance for its selected ID, the complete union of Evidence links, and the v2.1 participation/group/notes values. historical_entry_ids, entry_histories, and historical_provenance preserve all old identities and source-qualified attributes. Historical IDs do not add to active Entry counts.
- master-v2-1.json stores the existing v2.1 table schemas and values for the Entry view, ID Crosswalk, Evidence Map, Entry Source Map, Count Claims, Date Semantics, Unresolved Mappings, Verification Review, and Schema. Only GMO's active verification status/basis and associated review disposition differ from the frozen candidate. Its historical attributes remain unchanged.
- Ambiguous dates retain original values and Unknown meaning. Count Type remains separate from Source Class. Mixed question layouts remain in their original typed supplemental payloads. Field Evidence, unresolved source mappings, missing identities, and Team/Organization warnings remain distinct.
- research/active-checkpoint.json explicitly activates this checkpoint. The import manifest is an archive registry, not an activation signal. Historical row coverage continues to audit the frozen first checkpoint; active validation checks the accepted v2.1 mapping and its complete history.

## Preservation checks

migration.json records SHA-256 hashes for the unchanged workbook, previous corpus, policy snapshots, original candidate review, and narrow GMO decision. The validator checks these assets before accepting a canonical candidate. It also rejects omitted history, changed schema/crosswalk, Evidence text/link loss, changed dates, and unsupported verification or participation upgrades.

All original Evidence text, the 31 original Master questions, six additional historical questions, all historical Entry payloads, and both previously restored Evidence links remain preserved. No imported file, source workbook, or external Kimi workspace was modified. Other factual gaps remain unresolved.

## Review and publication scope

Final Entry verification counts are 16 Verified / 6 Research Lead / 0 Unresolved statuses; independent verification remains unperformed. The promotion is a structural and provenance-preserving research migration, not a completed factual review or publication approval.

The user authorized a local migration commit. Earlier push authorization applied to a private checkpoint; no authorization for the current public repository workflow was established. Do not push or enable Pages from this migration. Unrelated pending README.md and workflow edits are excluded from the migration commit.
