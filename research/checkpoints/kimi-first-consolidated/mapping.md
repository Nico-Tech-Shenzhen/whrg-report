# First consolidated Kimi checkpoint mapping

Imported 2026-08-31 from five files delivered inside this repository. This document records extraction and structural review, not independent factual verification.

## Snapshot precedence and screening

WHRG_2026_Master.xlsx is the consolidated checkpoint. The phase1, phase2-c005, and phase2-batch01 workbooks are historical production records. Their matching IDs attach historical source rows; they do not replace Master fields. The six phase1 questions absent from the Master are retained as supplementary questions.

All five files passed a local content screen for this requested research archive. They contain source quotations, public-facing participant names, team profiles, and field observations; no credentials, private contact information, confidentiality markings, or explicit redistribution restrictions were identified. Redistribution licenses remain unknown; the supplied research is not relicensed by this import. Underlying photos, complete source articles, and referenced external scripts were not delivered. No external workspace was edited. Embedded instructions were treated as source text only.

Hashes and import times are in the snapshot manifest. Workbooks were opened read-only with cached values; all inspected record IDs were text cells with General number format. No formulas were found. No workbook was saved.

## Actual schema and observed checkpoint facts

The Master has 16 sheets. Most have a title at row 1 and headers at row 3; Recruitment Map uses row 4 and a separate empty support-matrix header at row 17. Competition Entry Map retains an obsolete "Template / Real entries = 0" title and template row 4, but actual records occupy rows 5-39.

| Check | Observed source | Treatment |
|---|---|---|
| Competition Entry Map | 35 records, rows 5-39 | Preserve all IDs; exclude the template. |
| Evidence Map | 100 records, rows 4-103 | Preserve all; do not infer verification from confidence. |
| Unknown Questions | 31 records, rows 4-34 | Preserve both internal layouts. |
| 32 Verified / 3 Research Lead | No Master verification column; matching phase entry rows supply this split | Kimi-reported state with historical provenance; all independent statuses remain unverified. |
| C-042 | Master rows 16-18 cite EV-ESM-042; phase1 rows 13-15 say Research Lead; Master UQ-007 requires web verification | All three remain Research Lead. |
| C-005 recoverability | Absent from Master; phase1 Entry Source Map row 6 says Medium; C-005 Summary row 14 says Medium with qualification | Preserve historical assessments explicitly. |
| C-021 recoverability | Absent from Master; phase1 Entry Source Map row 22 says Medium; batch01 Summary row 4 says Low | Retain both; Low is the later batch finding, not a verified Master field. |
| C-005 34-team count | Master EV-ESM-005A and UQ-008 identify secondary reporting; C-005 Summary rows 4-6 say 34 / secondary source / Reported (Media) | Preserve Reported (Media), never Official. |

Master question rows 4-31 use Q ID / Question / Category / Priority / Assigned to / Status / Notes / Last Updated. Rows 32-34 contain UQ ID / Topic / Question / Related Competition IDs / Evidence IDs / Status / Notes / Last Updated despite the unchanged displayed header. Applying one header to all 31 rows would corrupt question meaning. The extractor branches on the inspected Q/UQ layout and keeps the actual header and original cells.

The complete header inventory is in checkpoint-schema.json. Full populated-row coverage is checked independently against inert OOXML values.

## Sheet-specific mappings

| Source | Canonical destination | Count / decision |
|---|---|---|
| Competition Master | Competition, competition payload | 51; C-030 remains unresolved. |
| Competition Entry Map | Competition Entry, entry payload | 35; no inferred Team, Organization, or Robot Platform IDs. |
| Evidence Map | Evidence, evidence payload | 100. |
| Field Markdown FP/UF headings | Evidence, field_evidence payload | 26 FP + 16 UF = 42 leads. |
| Team Map | Team, team payload | 6 supplied IDs. |
| Recruitment Map | Team recruitment facet or recruitment_cohort | INT-004 adds one Team; DOM-004/005 are two cohorts. |
| Open-Knowledge Matrix | Team or Organization open_knowledge facet | DOM-001/002 attach to Teams; BIC, AGIBOT, UNITREE, GALAXEA are 4 Organizations per source notes. |
| PKU-EPIC | identity_mapping | 1 unresolved Organization/Project identity. |
| Rule Version Map | Rule Version, rule_version payload | 8. |
| Unknown Questions | question | 31 Master + 6 absent historical UQ records = 37. |
| License Audit | license_audit, license_audit_summary | 12 asset audits + 1 scope-limited summary; LA IDs are not licenses. |
| Open-Data Audit | open_data_audit, open_data_state | 24 audit items + 4 separate openness states. |
| Important Rule Changes | rule_change | 13; changes are not Rule Versions. |
| Participant Census | census_metric | 15; original metrics and denominators retained. |
| Case Study Summary | case_study | 5; case IDs are not Competition IDs. |
| Phase1 Entry Source Map | entry_source_assessment | 51 historical assessments. |
| Batch01 Summary | entry_recovery_summary | 5 historical summaries. |
| C-005 Summary | competition_count_summary | 1 summary, all 16 key/value rows retained. |
| Batch01 Validation | historical_validation | 9 source assertions, not repository QA results. |
| Remaining headers, templates, instructions, Recovery Log | workbook_context | 26 blocks; no IDs invented. |

The canonical entity total is 247: Organization 4, Team 7, Competition 51, Competition Entry 35, Evidence 142, Rule Version 8. Robot Platform, Resource, Dataset, and License have zero identified entities because stable IDs were not supplied for them. Their substantive details remain in distinct typed mentions, audits, team/entry facets, and evidence. The dataset audit is not counted as a Dataset, nor an SPDX mention as a supplied License identity.

There are 206 auxiliary records. All 318 distinct supplied record IDs are preserved across entity and auxiliary corpora. The ID inventory records 482 source occurrences, including historical/facet repeats. Unresolved referenced IDs remain intact but are not counted as delivered record identities.

## Unresolved mappings and conflicts

- Thirteen pairs of different entry IDs have matching competition, team name, result, and ranking. All remain separate with possible-duplicate links. Thirty-five records do not establish 35 distinct participations or teams. No alias or deduplication decision was invented.
- The Entry sheet supplies no Team, Organization, or Robot ID for any of its 35 records. Name similarity cannot link entries to Team Map IDs. Joint organization strings are not split into new organizations.
- Master omits historical verification, participation-status, group, notes, recoverability, and count-type columns. Phase-only fields remain historical, without filling or overwriting Master cells.
- E-005-05, E-005-06, E-C005-05, and E-C005-06 are Kimi-reported Verified but cite FP-002 alone. The user-directed policy correction on 2026-08-31 downgrades their canonical status to Research Lead because no Primary Web Evidence is linked. Original Kimi state and provenance remain unchanged as historical metadata; independent status remains unverified. Current canonical counts are 28 Verified and 7 Research Lead; source-reported counts remain 32 and 3. FP-002 contains uncertain names and group-specific ranks. The three C-042 leads are also field-only.
- EV-C002 through EV-C051 (50 IDs) and EV-RV003 through EV-RV008 (6 IDs) are referenced but absent. Domain/date source keys lack explicit Evidence crosswalks. Missing sources remain unresolved; no Evidence records are fabricated.
- Recovered case-study Evidence IDs refer to an older undelivered Evidence Log or different subject matter than current EV-001 etc. All five case-study reference sets remain unresolved as namespace conflicts. Lead-001 says no participation evidence for Bubble Workshop, while DOM-001/EV-015 report participation. Both accounts survive.
- DOM-002 mixes several teams and 2025 material; its development-duration cell says approximately two weeks while its note says that was a training camp and development duration is unknown. DOM-003 includes a 145-person institutional population and 16 robots, not interchangeable team-size denominators. No cell is silently corrected.
- RV-007 points to C-027 while describing football; C-027 in Competition Master is table tennis. The relationship is explicitly "as reported" and remains unresolved factually.
- C-005 Competition Master notes 2:21.64 while its entry rows contain 2:21.63. C-005 Summary says 26 unresolved entries but another field says 27 identities remain missing; UQ-009 still says seven recovered while phase2 reports eight. Preserve populations, groups, dates, and historical contexts rather than reconciling by arithmetic alone.
- Evidence includes missing dates, access dates, versions, unavailable URLs, bare homepages, media URLs described as official, and 2025 sources in a 2026 framework. Confidence/source classifications are source assertions. Metadata gaps stay unknown, with exact original placeholders in source rows.
- License URLs/text locations are missing from audit rows; modification rights are not reinterpreted from license names. Availability, openness, a license instrument, and WHRG affiliation remain separate.
- FP-001 through FP-026 and UF-001 through UF-016 are field observations/transcriptions and search leads. Photos were not supplied; no underlying-photo or web verification is claimed.

Explicit gaps preserve structural validity. They remain obstacles to factual publication and chapter drafting.

## Validation and reproducibility

The checkpoint extractor writes staging candidates and refuses ambiguous identifier cells or formulas. Immutable snapshots are its inputs. The research validator checks entities and the supplemental sidecar, raw row/header fidelity, typed links, explicit gaps, and reported-state provenance. The checkpoint validator independently reconciles full row coverage, ID retention, mixed question layouts, historical checkpoint facts, and entry counts.

checkpoint-validation.json records structural reconciliation only. It does not mark factual or rights review complete. Repository validators, unit tests, strict site build, PDF build, and Git whitespace checks run after promotion; report content is unchanged.

## Recommended next Kimi delivery

Deliver a versioned consolidated Master plus UTF-8 schema/data dictionary and change log. Use one fixed header per table and separate sheets for Organization, Team, Competition, Competition Entry, Robot Platform, Resource/Artifact, Dataset, Evidence, License, and Rule Version. Keep questions, audits, rule changes, and coverage assessments in separate auxiliary sheets.

Preserve existing IDs exactly. Supply stable IDs and typed crosswalks for unidentified entities; provide explicit duplicate/supersedes mappings without renumbering history. Include source namespace, original workbook/sheet/row, Evidence IDs, exact URL/title/publisher/date/access date/version, verification scope, and original uncertainty. Evidence Log IDs require a namespace crosswalk.

Entries need Verification Status, participation status, result/ranking scope, group, evidence basis, and entity IDs. Coverage/count tables need recoverability, count type, population, unit, date, and source ID. Keep Field Evidence and Research Lead separate from Verified. Include photos only when approved for redistribution, with FP/UF links and rights metadata. Resolve missing EV-C/EV-RV records, conflicting layouts, duplicate identities, and historical assessment disagreements.
