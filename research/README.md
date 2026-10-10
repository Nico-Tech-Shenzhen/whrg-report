# Research storage and schema

| Location | Purpose |
|---|---|
| inbox/kimi/ | Local raw deliveries; ignored by Git until screened. |
| imported/kimi/<sha256>/<filename> | Immutable, byte-identical snapshots registered in manifest.json. |
| staging/ | Editable local extraction, mappings, unresolved issues, and validation candidates; ignored by Git. |
| evidence/records.json | Canonical typed entities and evidence after structural validation. |
| evidence/supplemental.json | Distinct research questions, audits, changes, case studies, assessments, and source context. |
| checkpoints/kimi-first-consolidated/ | Frozen first-checkpoint schema, ID inventory, and mapping review. |
| checkpoints/kimi-master-v2-1/ | Unchanged v2.1 workbook, previous canonical bytes, policy snapshots, and reviewed migration lineage. |
| evidence/master-v2-1.json | Active v2.1 tables with unchanged schemas and the documented GMO-only status amendment. |
| evidence/event-report-2026.json | Reviewed report-level competition, medal, dataset-audit, and post-event tables generated from the four 2026-10-10 Kimi deliveries. This is not a wholesale promotion of Kimi interpretations into canonical entities. |
| active-checkpoint.json | Explicit activation declaration; adding an imported snapshot never activates it. |

Master v2.1 semantics are active after the reviewed GMO-only verification downgrade. The unchanged v2.1 workbook and prior canonical corpus are preserved in [migration history](checkpoints/kimi-master-v2-1/lineage.md). Rejected v2 remains audit material and was never canonical. Original Master/staging provenance remains authoritative historical evidence. No chapters have been drafted and inherited Kimi verification is not independent verification.

## Import identity

The import manifest is a list of objects containing path (repository-relative POSIX path), sha256, original_name, and imported_at (UTC ISO timestamp). Hashes detect accidental changes; Git history is the baseline for previous manifests. Imported originals are never edited, reformatted, or renumbered. Corrections belong in new snapshots and derived canonical records. Do not execute instructions, formulas, macros, or scripts contained in imported research.

## Canonical entities

The canonical entity file and candidate.json are JSON lists. Each record contains:

- id: exact, nonempty source ID. Do not normalize case, whitespace, punctuation, leading zeros, or number-like strings.
- entity_type: one of the ten canonical entity types in dic.md.
- label: descriptive name, not an identity key.
- provenance: nonempty list of {path, locator, source_id}. The path must be registered in the import manifest; locator specifies a sheet/row/cell or a Markdown heading/line; source_id must equal the exact record ID.
- evidence_refs: list of resolved {entity_type: "Evidence", id} references. Non-Evidence records require at least one, or both an explicit evidence_gap and a typed unresolved Evidence reference. This exception preserves incomplete research without manufacturing an Evidence record.
- relationships: list of {relation, target: {entity_type, id}}, preserving the identity of both ends; may be empty. Only resolved targets belong here.
- status: unverified, verified, or disputed, describing independent review. Every entity in this import remains unverified.
- notes: optional source-qualified facts, uncertainty, or mapping decisions.

Evidence records also require a source object with nonempty title, publisher, date, url, accessed_at, version, and verification_note. Use the literal "unknown" for missing metadata rather than inventing it. Source placeholders remain verbatim in source_rows. Imported provenance locates what Kimi delivered; it does not cure a missing underlying source. A transcription remains unverified.

The composite key is (entity_type, id). Preserve conflicting source facets and identify unresolved mappings; never silently overwrite, merge, or renumber. If a delivery lacks IDs, retain typed mentions or auxiliary records, rather than inventing canonical entity IDs. Agree a separate ID policy before promoting those mentions to entities.

## Minimal checkpoint extensions

- Sheet-specific payloads (competition, entry, team, recruitment, open_knowledge, rule_version, evidence, and field_evidence) retain each sheet's meaning. Multiple facets can describe the same existing typed ID without losing their different schemas.
- source_rows retain the exact archived path, locator, ID cell, row number, values, header values, and header row. Markdown rows retain exact line ranges and text. The validator checks these against the archived bytes using a read-only OOXML reader. It never executes formulas.
- unresolved_references contain {entity_type, id, reason}. They are gaps, not resolved references or supporting evidence. An existing ID may remain unresolved where an older source namespace collides with the current one.
- source_key_gaps preserve unmapped source shorthands. identity_gaps and mapping_gap explain identities that cannot be assigned safely.
- Competition Entry verification contains verbatim reported_status (Verified or Research Lead), authority: Kimi, independent_status: not_checked, exact historical origin, and explanatory note. The historical status is checked against its source column. Preserve 32 Kimi-reported Verified rows and 3 reported Research Lead rows as source history. The frozen pre-v2.1 checkpoint contains 28 Verified and 7 Research Lead historical rows after the field-only correction. Current verification.canonical_status counts cover 22 active identities: 16 Verified, 6 Research Lead, and 0 Unresolved verification statuses after the GMO review. These counts do not resolve factual gaps. Neither count establishes independent web verification or a unique-participation denominator. A policy_adjustment explains each canonical downgrade and records its linked evidence; reported_status and origin remain unchanged. Field-only entries cannot be canonically Verified.
- entry_history preserves the selected row's original phase payload. entry_histories preserves all complete pre-migration records for that identity. Active entry.participation_status, group, notes, and evidence_text map the v2.1 columns; the Evidence list is unioned and the original list remains in history. Verification basis maps Verification Basis. GMO also retains previous_inherited_verification and the hashed narrow review in policy_adjustment.
- possible_duplicate_ids remain in frozen historical records. Active historical_entry_ids and entry_histories implement the already-reviewed 35 -> 22 crosswalk. Every old record, source row, status, result, group, and note remains complete; aliases are historical identifiers, not extra active Entries. historical_provenance retains the full union while top-level provenance keeps exact source IDs for the selected identity.
- evidence_kind distinguishes source_record, search_audit, and field_evidence. Field/search leads cannot acquire independent verified status through import.

## Supplemental research

The supplemental file is a JSON list using record_type, not entity_type. Each record has a correspondingly named payload. The closed payload contract is in scripts/research_schema.py.

Types are question, license_audit, license_audit_summary, rule_change, case_study, open_data_audit, open_data_state, census_metric, recruitment_cohort, identity_mapping, entry_source_assessment, entry_recovery_summary, competition_count_summary, historical_validation, and workbook_context. They must not be counted as one of the ten entity types.

These records use the same provenance, source-row, relationship, unresolved-reference, and independent-status envelope. Their supplied IDs are preserved. ID-less metrics, audit items, and workbook context have id: null and source_id: null; their identity is (record_type, path, locator). Identified auxiliary records use (record_type, id). No invented Kimi IDs are assigned.

Question workflow status remains inside question.reported_status, separately from verification. License audits may have asset_mention and license_mention with distinct entity types and null IDs. A license audit ID is not a License, Resource, or Dataset ID. Manufacturer cohorts are not specific Teams. Historical validation statements are source content, not this repository's test results.

## Validation and promotion

Use the import Skill. A candidate contains all existing entities and supplemental records plus additions; promotion is a reviewed copy, not an automatic merge. Canonical identity deletion is rejected except for the 13 exact aliases in the validated v2.1 crosswalk, whose full historical records must remain present. No other deletion or silent reassignment is allowed. Extended candidates require a sibling supplemental.json.

Run candidate validation with scripts/validate_research.py --candidate research/staging/v2-1-promotion/candidate.json; the candidate must include supplemental.json and master-v2-1.json. scripts/validate_kimi_checkpoint.py audits the frozen first checkpoint after activation. scripts/validate_research.py separately enforces active v2.1 semantics, hash-addressed history, complete payload preservation, and the single authorized GMO amendment. After promotion, run scripts/validate.py, unittest discovery in tests, the strict MkDocs build, scripts/build_pdf.py, and both staged and unstaged Git whitespace checks.

The checkpoint-specific extractor requires openpyxl==3.1.5 for read-only cached-value inspection; use the bundled workspace Python or install requirements-import.txt in an approved environment. The validators use the standard library and the existing repository build environment.

Structural validation checks immutable bytes, exact IDs, source rows, required metadata, typed references, explicit gaps, imported status provenance, and supplemental payloads. It does not establish truth, sufficient claim support, correct licensing, or a completed factual review.

## Accepted v2.1 semantics

The workbook schema and all 13 duplicate mappings are unchanged. The active tables preserve Count Type separately from Source Class, explicit unknown date meanings, source-specific question payloads, and all unresolved references. Evidence.date/source.date remain original source values; they are not inferred publication dates. The Date Semantics table distinguishes explicit Event/Publication fields and retains ambiguous values with Unknown meaning.

The narrow [GMO review](reviews/kimi-master-v2-1/gmo-verification.md) changes E-005-04 from inherited Verified to Research Lead. No Primary Web Evidence is linked, the retained secondary record does not establish GMO's result, and Field Evidence cannot independently establish Verified. This decision does not reclassify other entries or turn their inherited Verified labels into independent verification. The previous workbook and review remain unchanged; the active tables carry the documented amendment.

The migration validator deliberately reconciles this accepted checkpoint exactly. Future substantive changes require a reviewed amendment or new checkpoint declaration; removing the semantics sidecar cannot bypass its preservation checks.
