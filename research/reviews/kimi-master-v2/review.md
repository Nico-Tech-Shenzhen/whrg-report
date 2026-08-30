# Kimi Master v2 migration external review

Decision: REJECTED. The 35-to-22 map is complete, but the delivered migration loses information. No canonical migration, commit, or push is authorized by a passing review.

## Hash verification

All three hashes declared in the handoff match: old Master, v2 Master, and schema document (delivered basename mapped from references/master-schema-v2.md). The handoff has no declared self-hash; its computed hash is recorded below. All three new files are immutable registered snapshots.

| File | SHA-256 | Handoff match |
|---|---|---|
| WHRG_2026_Master.xlsx | 5ba0c2de6a1afd4028ec8f797a5d81db43c572f979d1bff12277a53502d1dc3c | Yes |
| WHRG_2026_Master_v2.xlsx | e4e77e86b53c123d1d326fa8659bd99779fb2f08f6ad767c0c54d848b7a4f05c | Yes |
| master-schema-v2.md | 9941263fcf24cac1ba8f97be450e25b6c7deba1f4ea24bc459ad4b701f8571ca | Yes |
| master-v1-v2-migration-handoff.md | 742890e80bd607898c3ff5778d84840c5742baa020922dbe3029bfca7119db1e | No supplied digest |

## Preservation and schema checks

- 51 Competition rows and 31 Question rows are byte-value equivalent at their original row/column positions. Question IDs remain Q-001..Q-020, Q-101..Q-108, UQ-007..UQ-009, not Q-001..Q-031 as stated in the handoff.
- All 100 Evidence IDs remain, but the Original Chinese evidence column (39 populated cells) and 39 Japanese translation placeholders are removed. For 37 Evidence IDs the original text no longer occurs anywhere in the corresponding v2 row; EV-RV001/002 happen to repeat that text in their titles. The additional Source Class and Audit Date fields do not replace that evidence content.
- All supplied non-entry IDs are unchanged in the corresponding sheets. All 35 Entry IDs survive as either a v2 ID or an explicit legacy crosswalk ID; no uncovered Entry ID was found.
- Explicit Verification Status and Basis columns exist. Candidate counts are 16 Verified and 6 Research Lead, excluding the template. Existing canonical remains 28 Verified and 7 Research Lead. Among the 22 retained targets it was 17/5; only E-005-04 is newly downgraded relative to the current corpus. The three C-042 entries were already Research Lead.
- All 22 required Participation Status cells are blank. Every merged legacy record has historical participation/status, group or notes in the current canonical corpus that v2 does not carry. Group has no v2 column and every entry Notes cell is blank. Original snapshot retention prevents destructive loss locally, but does not make the replacement candidate lossless.
- Count Type and Source Class are separate Census columns and the 15 original Census metrics are retained. EV-ESM-005A is Media-Secondary. Per-competition count type remains absent from Entry Source Map. C-021 is restored from phase1 as Medium despite the later Low assessment retained in canonical history.
- Publication Date and Audit Date columns exist, but all supplied old Date values are copied to Publication Date without a Date Type=Unknown fallback or Event Date column. Known ambiguous semantics have not been resolved or marked.
- Unknown Questions still has the inherited mixed Q/UQ layout under one unchanged header. UQ-007/008/009 retain their raw information but are not a stable single-schema table.
- ID Crosswalk has 13 Confirmed Same Entry rows and one Unresolved Evidence row for FP-002. There is no unresolved Entry duplicate mapping. FP-002 already exists as Field Evidence in the current canonical corpus and must retain that provenance; absence from the v2 Evidence Map does not mean the source is absent from the repository.
- The two exact Team Name = Organization Name warnings are E-B01-040-01 and E-B01-036-01. Name equality is confirmed; the handoff assertion that these are a single entity is not accepted as identity proof.
- E-005-02 and E-005-03 are labelled Verified with Primary web evidence as their basis while their only v2 source is classified Media-Secondary. This is an internal schema/qualification inconsistency, without performing web research.
- Migration Log uses WARNING and FIX, which its supplied enum omits. The deduplication log also reverses the E-005/E-C005 direction and mentions E-005-08, which was not a delivered stable Entry ID.

## Every duplicate pair

All 13 pairs match on non-ID/non-evidence v1 fields, including competition, team, organization, platform, result, and rank. This establishes compatibility as duplicate source records, not independent proof of real-world identity. Eleven pairs retain all non-ID v1 Master fields; two drop a distinct evidence association. None is accepted for canonical promotion because the proposed replacement also omits historical attributes from all 13 pairs.

| Legacy ID | Retained ID | v1 rows | v2 row | Lost Evidence association | Current history retained? | Decision |
|---|---|---|---|---|---|---|
| E-C005-01 | E-005-01 | 21, 5 | 5 | None | No | Reject promotion |
| E-C005-02 | E-005-02 | 22, 6 | 6 | None | No | Reject promotion |
| E-C005-03 | E-005-03 | 23, 7 | 7 | FP-002 | No | Reject promotion |
| E-C005-04 | E-005-04 | 24, 8 | 8 | None | No | Reject promotion |
| E-C005-05 | E-005-05 | 25, 9 | 9 | None | No | Reject promotion |
| E-C005-06 | E-005-06 | 26, 10 | 10 | None | No | Reject promotion |
| E-C005-07 | E-005-07 | 27, 11 | 11 | None | No | Reject promotion |
| E-B01-004-01 | E-004-01 | 29, 12 | 12 | EV-ESM-004A | No | Reject promotion |
| E-B01-004-02 | E-004-02 | 30, 13 | 13 | None | No | Reject promotion |
| E-B01-004-03 | E-004-03 | 31, 14 | 14 | None | No | Reject promotion |
| E-B01-004-04 | E-004-04 | 32, 15 | 15 | None | No | Reject promotion |
| E-B01-040-02 | E-040-01 | 36, 20 | 20 | None | No | Reject promotion |
| E-B01-036-02 | E-036-01 | 39, 19 | 19 | None | No | Reject promotion |

E-C005-03 -> E-005-03 loses FP-002 (old Master row 23, Evidence IDs); E-B01-004-01 -> E-004-01 loses EV-ESM-004A (old Master row 29). FP-002 appears in the crosswalk notes, but its association is not carried to E-005-03 and that row remains Verified. EV-ESM-004A survives as an Evidence row but its association with E-004-01 is lost.

Example of lost scope: E-C005-04 preserves Final Group 2 and the note that the field board showed third place in that group, while v1/v2 Ranking is 4. Dropping the group and note discards the distinction between group rank and the imported overall rank.

## Exact 35-to-22 mapping

| v1 Entry ID | v1 row | v2 Entry ID | v2 row | Action |
|---|---|---|---|---|
| E-005-01 | 5 | E-005-01 | 5 | retained |
| E-005-02 | 6 | E-005-02 | 6 | retained |
| E-005-03 | 7 | E-005-03 | 7 | retained |
| E-005-04 | 8 | E-005-04 | 8 | retained |
| E-005-05 | 9 | E-005-05 | 9 | retained |
| E-005-06 | 10 | E-005-06 | 10 | retained |
| E-005-07 | 11 | E-005-07 | 11 | retained |
| E-004-01 | 12 | E-004-01 | 12 | retained |
| E-004-02 | 13 | E-004-02 | 13 | retained |
| E-004-03 | 14 | E-004-03 | 14 | retained |
| E-004-04 | 15 | E-004-04 | 15 | retained |
| E-042-01 | 16 | E-042-01 | 16 | retained |
| E-042-02 | 17 | E-042-02 | 17 | retained |
| E-042-03 | 18 | E-042-03 | 18 | retained |
| E-036-01 | 19 | E-036-01 | 19 | retained |
| E-040-01 | 20 | E-040-01 | 20 | retained |
| E-C005-01 | 21 | E-005-01 | 5 | merged |
| E-C005-02 | 22 | E-005-02 | 6 | merged |
| E-C005-03 | 23 | E-005-03 | 7 | merged |
| E-C005-04 | 24 | E-005-04 | 8 | merged |
| E-C005-05 | 25 | E-005-05 | 9 | merged |
| E-C005-06 | 26 | E-005-06 | 10 | merged |
| E-C005-07 | 27 | E-005-07 | 11 | merged |
| E-C005-08 | 28 | E-C005-08 | 21 | retained |
| E-B01-004-01 | 29 | E-004-01 | 12 | merged |
| E-B01-004-02 | 30 | E-004-02 | 13 | merged |
| E-B01-004-03 | 31 | E-004-03 | 14 | merged |
| E-B01-004-04 | 32 | E-004-04 | 15 | merged |
| E-B01-012-01 | 33 | E-B01-012-01 | 22 | retained |
| E-B01-012-02 | 34 | E-B01-012-02 | 23 | retained |
| E-B01-040-01 | 35 | E-B01-040-01 | 24 | retained |
| E-B01-040-02 | 36 | E-040-01 | 20 | merged |
| E-B01-040-03 | 37 | E-B01-040-03 | 25 | retained |
| E-B01-036-01 | 38 | E-B01-036-01 | 26 | retained |
| E-B01-036-02 | 39 | E-036-01 | 19 | merged |

## Review boundary

No web research was performed. No external Kimi workspace, delivered file, imported snapshot, canonical record, schema, or migration history was rewritten. These results describe the frozen candidate. Source snapshots and this review remain local and uncommitted because the migration failed the user-required lossless gate.

The detailed JSON retains source locators, every pair comparison, original source-status provenance, all omitted historical attributes, and all removed Evidence fields.

## Validation outcome

- Migration review: FAIL. No canonical migration candidate was constructed after the lossless gate failed.
- Existing canonical repository validators: PASS (8 immutable imports; 247 unchanged canonical entities).
- Regression tests: 18 PASS, 1 ERROR. test_checkpoint_reconciliation calls the original checkpoint audit, which scans every registered XLSX and incorrectly expects the quarantined v2 workbook to have been promoted. The error is "Lost or invented workbook rows: WHRG_2026_Master_v2.xlsx". No validator changes were made in this rejected-migration review.
- Strict MkDocs build and PDF build: PASS. No site deployment was performed.
- Staged and unstaged Git whitespace checks: PASS.
- Canonical records, supplemental records, and disabled Pages workflow are byte-identical to HEAD.
- No commit created; no push attempted. The three new snapshots, manifest additions, and rejection review remain local/uncommitted.
