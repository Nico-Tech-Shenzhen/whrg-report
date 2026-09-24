# Kimi official archive final import review

## Scope and audit boundary

This is a new review of the delivered official archive. The earlier missing-input review remains unchanged. No web research was performed, Master v2.1 was not reconsidered, and the external Kimi workspace was not modified. Kimi's status column was treated as a candidate only.

## Immutable input integrity

- Workbook SHA-256: `1d5edfaa71a9d456cec6a63ce12991bdd1e98fbcc636a8c971a3fa6e1c7c82b9`
- Screened immutable inputs: 151 (workbook, 138 official attachment files, 12 crawl JSON appendices)
- Attachment-map rows: 172; unique delivered files: 138; unique payload hashes: 134
- Claimed row types: 97 PDF, 1 XLSX, 4 DOCX, 38 JPG, 32 PNG
- Unique delivered file types: 97 PDF, 1 XLSX, 4 DOCX, 20 JPG, 16 PNG
- All 172 page/attachment lineages, sizes, and SHA-256 values matched. Full hashes: [input-files.json](input-files.json).
- OOXML sources contain no formulas, macros, external links, or embedded objects. PDFs were not encrypted and exposed no JavaScript, launch action, or embedded-file markers. Six image-only result PDFs were retained as Evidence only; no OCR-derived Entries were created.

## Evidence disposition

- Accepted as new canonical Evidence: 257 (124 new official pages and 133 unique attachment payloads).
- Deduplicated: 49 source rows (7 existing page URLs, 1 existing attachment URL, 38 repeated attachment payload mappings).
- Rejected: 0 integrity-valid official sources. Image-only sources remain unverified Evidence and do not establish Entry identities.
- Publisher controls Source Class: all delivered WHRG organizer pages and attachments are `Official-Event`.

## Entry decisions

- Every one of the 1,005 candidate rows is classified in [entry-decisions.json](entry-decisions.json): A=12, B=4, C=918, D=71.
- Existing Entries confirmed: 18.
- Research Lead -> Verified: 4 (`E-005-04`, `E-042-01`, `E-042-02`, `E-042-03`). The proposed C-040 NorthAir/Agibot change is not a promotion because it was already Verified.
- New canonical Entry identities: 669. Repeated preliminary/final rows are one competition/team identity with source history retained.
- C-003: four ranked finishers plus one DNF; the DNF ranking was cleared rather than accepting Kimi's duplicated rank 2.
- C-006: one official finisher, rank 1, retained as a new identity.
- C-005: GMO Robots is official rank 7 and promoted; the previous rank 4 is preserved in history. 惊鸿动力队 is a new identity.
- C-040: three 优理奇-prefixed rows remain conflicts and do not alter the generic canonical identity. City-specific C-036 智元 rows likewise remain ambiguous.
- Parser/schedule artifacts, unreliable C-027 concatenations, missing exact source strings, and duplicate result rows do not create extra identities.

## Year and domain controls

- All Entry candidates are 2026 and are linked only to 2026 official result evidence.
- The 17 official 2025 pages and their attachments are aggregate/context Evidence only. They do not verify 2026 participation.
- No RoboCup evidence was used to verify WHRG participation.
- Field Evidence was not used alone for any Verified promotion.
- Media open-source claims created no verified artifact or Open Knowledge change.

## Canonical effects

- Records before: 282; after: 1208.
- Evidence: 190 -> 447.
- Competition Entry: 22 -> 691.
- Entry statuses: Verified 16 -> 689; Research Lead 6 -> 2.
- New Team / Organization / Robot Platform records: 0 / 0 / 0. Workbook names remain Entry fields; no entity IDs were inferred.
- Open Knowledge changes: 0.

## Promotion decision

The import was promoted after candidate validation. Repository validators, the prior and final import validators, 6/6 prior-import negative controls, 7/7 final-import negative controls, the frozen v2.1 validator with 6/6 controls, the frozen checkpoint audit, 36 unit tests, strict MkDocs, PDF generation, and Git whitespace checks all passed. The import is committed separately and is not pushed in this task.
