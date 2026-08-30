# WHRG Master v2.1 candidate review

Candidate only. Structural acceptance passed; canonical migration was not performed. No web research, external Kimi workspace edits, report drafting, source snapshot changes, or publication occurred.

The current canonical corpus is the factual and verification authority. Original Master and staging snapshots supply historical provenance. Rejected v2 is used only to compare intended schema concepts and record migration history. Its assertions are not promoted by this review.

## Four-way comparison

| Check | Original Master | Rejected v2 | Current canonical corpus | Corrected v2.1 |
|---|---|---|---|---|
| Competitions | 51 | 51 | 51 | 51 |
| Original Evidence identities | 100 | 100 | 100, plus 42 field/observation identities | 100, plus 42 separate field/observation identities |
| Original Evidence text column | 39 nonempty text cells | Column removed; 37 texts absent elsewhere; two repeated in titles | All original text retained | All 39 text cells retained exactly; all 37 lost texts restored |
| Japanese summary column | 39 populated placeholders | Removed | Preserved verbatim | Preserved verbatim, not translated or summarized |
| Original Unknown Questions | 31; mixed Q/UQ layouts | 31; layout ambiguity unchanged | 31 source-specific payloads, plus 6 historical questions | 31 source-specific payloads, plus 6 separate historical questions |
| Competition Entries | 35 source rows | 22 selected rows | 35 independent historical records with 13 candidate pairs | 22 candidate identities plus all 35 complete historical records |
| Participation | Absent in Master; supplied by historical staging | Blank for all 22 | Available in entry_history | 14 Finished, 2 DNS, 2 Disqualified, 1 Started, 3 Unknown |
| Verification | No column; history reports 32 Verified / 3 Research Lead | 16 Verified / 6 Research Lead | 28 Verified / 7 Research Lead over 35 rows; mapped targets 17 / 5 | 17 inherited Verified / 5 Research Lead; zero independent verifications |
| Deduplication content | Two pairs have extra Evidence links | Two links and historical facets dropped | Histories intact | All 13 unions complete; zero dropped links |
| Original date semantics | Some columns generic Date/Source Date | Generic values asserted as Publication Date | Original values/headers intact | Generic dates retain Unknown meaning; explicit Event/Published fields kept separate |
| Entry Source Map | In historical staging, not Master | Earlier phase1 map only; C-021 regresses to Medium | Phase1 and later assessments retained | Stable map retains latest C-021 Low and C-005 Medium plus all earlier payloads |

## Identity mapping and historical attribute union

All 13 candidate duplicate pairs were rechecked against the current records and exact original Master values. Every identity/result field in each pair matches after excluding the ID and Evidence list; Evidence lists are unioned. The handoff classification alone is not the basis for acceptance. No fuzzy name matching is used.

Historical attributes remain source-qualified, including nulls, group/heat, notes, participation, result, ranking, original Kimi verification, current policy correction, and all source file/sheet/row locators. A selected row never replaces the other row payload.

| Historical ID | Candidate ID | Participation | Group / heat | Historical notes | Unioned Evidence IDs |
|---|---|---|---|---|---|
| E-C005-01 | E-005-01 | Finished | Final | 冠军 | EV-ESM-005, EV-ESM-005A |
| E-C005-02 | E-005-02 | Finished | Final | 亚军 | EV-ESM-005A |
| E-C005-03 | E-005-03 | Finished | Final | 季军; FP-002第2组确认 | EV-ESM-005A, FP-002 |
| E-C005-04 | E-005-04 | Finished | Final Group 2 | FP-002第2组第3名 | EV-ESM-005A, FP-002 |
| E-C005-05 | E-005-05 | DNS | Final Group 2 | FP-002第2组DNS | FP-002 |
| E-C005-06 | E-005-06 | DNS | Final Group 2 | FP-002第2组DNS | FP-002 |
| E-C005-07 | E-005-07 | Finished | Final Group 3 | 新华社图片第3组第5名 | EV-ESM-005B |
| E-B01-004-01 | E-004-01 | Finished | Final | 冠军; 新浪财经交叉验证 | EV-ESM-004, EV-ESM-004A |
| E-B01-004-02 | E-004-02 | Finished | Final | 亚军 | EV-ESM-004 |
| E-B01-004-03 | E-004-03 | Finished | Final | 季军 | EV-ESM-004 |
| E-B01-004-04 | E-004-04 | Finished | Final | 第4名 | EV-ESM-004 |
| E-B01-036-02 | E-036-01 | Disqualified |  | 赛后审查成绩无效 | EV-ESM-036 |
| E-B01-040-02 | E-040-01 | Disqualified |  | 赛后审查成绩无效 | EV-ESM-040 |

The two missing links are restored in the candidate identity rows: E-C005-03 -> E-005-03 retains FP-002; E-B01-004-01 -> E-004-01 retains EV-ESM-004A. FP-002 remains Field Evidence and a search lead. A restored link is not new factual verification.

E-036-01 and E-040-01 preserve the historical result text from their batch aliases as well as the Master Disqualified result. E-005-04 retains overall ranking 4 and the note identifying Group 2 rank 3; these scopes are not silently reconciled.

The complete 35 -> 22 map is in the workbook ID Crosswalk and review.json. All 35 supplied Entry IDs remain available. The candidate Canonical Archive reconstructs every one of the 247 current entity records; Supplemental Archive reconstructs all 206 current supplemental records. These archive counts are not additional unique entities.

## Evidence text preservation

Every original Master Evidence row is reproduced with its detailed source text, Japanese placeholders, notes, title, publisher, URL, date value, confidence, scope, typed metadata, and all historical source rows. No detailed text is replaced by a summary. The separate Evidence Text Contents reading view splits long text into exact fragments; concatenation in Part order reproduces each original text without adding separators.

The 37 restored texts belong to: EV-001, EV-002, EV-003, EV-004, EV-005, EV-006, EV-007, EV-008, EV-009, EV-010, EV-011, EV-012, EV-013, EV-014, EV-015, EV-016, EV-017, EV-018, EV-019, EV-020, EV-021, EV-022, EV-023, EV-024, EV-025, EV-026, EV-027, EV-028, EV-029, EV-030, EV-031, EV-032, EV-033, EV-C001, EV-IRC001, EV-IRC002, EV-PART001.

## Verification decisions

All six v2 Research Lead classifications were evaluated using existing linked records. The user required evaluation, not automatic adoption of six downgrades. The current canonical corpus has priority over rejected v2.

| Entry | Existing evidence and decision | Candidate status |
|---|---|---|
| E-005-04 | EV-ESM-005A is secondary media reporting; FP-002 already exists as a field transcription. The v2 assertion that FP-002 is absent is not a valid reason to overwrite the higher-priority canonical status. Retain its current classification and explicitly flag the unresolved claim-level support and ranking scope. This is not a new verification or an upgrade against the canonical baseline. | Verified, inherited and unresolved |
| E-005-05 | FP-002 only; retain canonical field-only policy downgrade and original Kimi Verified history. | Research Lead |
| E-005-06 | FP-002 only; retain canonical field-only policy downgrade and original Kimi Verified history. | Research Lead |
| E-042-01 | Existing field-source support and historical Research Lead status; no stronger support established. | Research Lead |
| E-042-02 | Existing field-source support and historical Research Lead status; no stronger support established. | Research Lead |
| E-042-03 | Existing field-source support and historical Research Lead status; no stronger support established. | Research Lead |

Final candidate identity counts: 17 Verified / 5 Research Lead. Historical Kimi counts remain 32 / 3 and current canonical row counts remain 28 / 7. All independent statuses remain not_checked or unverified. E-005-02 and E-005-03 also retain inherited classifications without adopting v2's unsupported Primary Web Evidence labels. This migration does not certify the sufficiency of their sources.

## Schema mapping and remaining gaps

Each data sheet has one stable header row. The candidate adds Verification Status, Verification Basis, Participation Status, Group or Heat, historical attributes, typed ID crosswalk, and explicit unresolved mappings. Entry Source Map uses a stable schema with current and historical assessments separated.

Count Claims keeps Count Type separate from Source Class. C-005 34 remains Reported / Media, with the original Reported (Media) wording and complete count-summary payload retained. Other count classifications remain Unknown unless existing source data explicitly qualifies them; v2's inferred Official labels are not imported.

Evidence Map and Entry Source Map retain Original Date/Source Date and Date Meaning Unknown, with separate Event Date, Publication Date, and Audit Date fields left empty when unsupported. Date Semantics separately identifies explicit competition dates and published rule dates, preserving the original text and ranges. Existing last-updated, development, effective, and recovery dates remain in their named source payloads; they are not coerced into publication dates. No access/audit date is invented.

Unknown Questions retains 28 master_question records and 3 phase1-layout UQ records (UQ-007 through UQ-009), their exact original headers/positional values, typed payload, and provenance. The six additional historical UQ records remain separate. Question workflow status is never substituted for Verification Status.

Organization, Team, Competition, Competition Entry, Robot Platform, Resource, Dataset, Evidence, License, and Rule Version remain distinct. No Team/Organization/Robot ID is inferred from a name. Empty entity registries are explicit. License audits, resource mentions, cohorts, counts, and questions remain supplemental records rather than invented entity identities.

The candidate is a lossless workbook contract, not yet a drop-in replacement for records.json. Future authorized promotion needs an explicit canonical alias/history adapter and a versioned active-checkpoint declaration; simply deleting 13 canonical records would violate the current validator and this preservation contract.

Unresolved items remain preserved:

- FP-002 is present in canonical Field Evidence. Its underlying photo was not delivered, and the mapping to verified underlying/Primary Web Evidence remains unresolved. The rejected crosswalk assertion remains in the immutable v2 snapshot and prior review; it is not treated as a newly resolved web claim.
- The alleged unresolved duplicate in the v2 handoff is actually one unresolved Evidence crosswalk, not an additional Entry duplicate. No fourteenth Entry merge is invented.
- Team Name = Organization Name warnings remain for E-B01-040-01 and E-B01-036-01.
- All 56 absent Evidence IDs, shorthand source keys, case-study Evidence namespace conflicts, missing entity IDs, PKU-EPIC entity ambiguity, rights gaps, and other canonical uncertainties remain present.
- C-005 timing and ranking-scope differences, C-021 historical recoverability differences, and existing training/development-duration ambiguities remain source-qualified and unresolved.
- GMO verification support remains flagged as described above. No factual unknown was resolved through web research.

## Validation and test scope

The exported XLSX was read independently using the standard-library OOXML reader. Every cell was compared with the prepared specification; all full canonical and supplemental JSON payloads were compared with the current corpus. All Entry identity unions, history facets, Evidence text, mixed question layouts, status constraints, and original source hashes passed. Source snapshots and both canonical files remain byte-identical.

Six negative controls were rejected: dropped Evidence link, summarized/replaced Evidence text, Started -> Finished upgrade, Field Evidence-only -> Verified upgrade, lost historical notes, and guessed publication date.

Repository checkpoint coverage now uses the frozen first-checkpoint ID inventory to select its five declared sources. The manifest remains an archive registry, not an activation signal. All eight snapshots are still hash-validated; three rejected migration files remain historical audit material. Removing a declared source still fails, and adding an unpromoted snapshot does not activate it.

Full QA passed: 21 unit tests, repository validators, original JSON candidate validation, v2.1 workbook validation with six negative controls, strict MkDocs build, PDF build, and Git whitespace checks. All 38 sheet previews were rendered and visually inspected. Large archival JSON is retained in full cells for machine reconstruction; Evidence Text Contents provides a readable long-text view. No publication was performed.

## Candidate inventory

| Sheet | Data rows |
|---|---:|
| Read Me | 13 |
| Competition Master | 51 |
| Competition Entry Map | 22 |
| Entry History | 35 |
| ID Crosswalk | 35 |
| Evidence Map | 100 |
| Field Evidence | 42 |
| Evidence Text Contents | 249 |
| Team Map | 7 |
| Organization Map | 4 |
| Rule Version Map | 8 |
| Robot Platforms | 0 |
| Resources | 0 |
| Datasets | 0 |
| Licenses | 0 |
| Unknown Questions | 31 |
| Historical Questions | 6 |
| Entry Source Map | 51 |
| Count Claims | 16 |
| License Audits | 12 |
| License Audit Summary | 1 |
| Rule Changes | 13 |
| Case Studies | 5 |
| Open Data Audits | 24 |
| Open Data States | 4 |
| Recruitment Cohorts | 2 |
| Identity Questions | 1 |
| Recovery History | 5 |
| C005 Count History | 1 |
| Historical Validation | 9 |
| Workbook Context | 26 |
| Canonical Archive | 247 |
| Supplemental Archive | 206 |
| Unresolved Mappings | 249 |
| Verification Review | 6 |
| Date Semantics | 210 |
| Migration History | 10 |
| Schema | 37 |

Candidate: `research/staging/WHRG_2026_Master_v2_1.xlsx`.
Candidate SHA-256: `64bd0eab5fcc230f69bbc9b4d9fe07e7c4470c2d4db5bd85cc30ce2682c8fa4d`.

Authoritative source hashes are listed in review.json and the Migration History worksheet. The prior rejected migration review and all immutable archives remain unchanged.

## Reproduction and promotion recommendation

Run `python scripts/prepare_kimi_v21_candidate.py`. Place a copy of `scripts/build_kimi_v21_workbook.mjs` as `research/staging/v2-1-work/build.mjs`, with a local node_modules junction to the bundled runtime dependency directory. Run it with the bundled Node runtime and @oai/artifact-tool. Then run `python scripts/validate_kimi_v21_candidate.py --negative-checks`. The preparer and validator never promote the candidate.

Keep v2.1 unpromoted. Review the documented inherited verification exception, then authorize a separate lossless canonical migration if desired. Preserve all historical Entry IDs, source payloads, snapshots, and unresolved factual gaps during that later step. Do not replace canonical files with the 22 display rows alone.
