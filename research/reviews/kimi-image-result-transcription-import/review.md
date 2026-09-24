# Kimi image-result transcription import review

## Input and provenance

- Input: `whrg-image-result-transcription-2026.xlsx`
- SHA-256: `25436a04e14d414673c412c50b6033532ed5eb97b4b90ff1b4efe27ae7c5fa00`
- 91 rows were checked for Competition ID, Evidence ID, Attachment ID, source filename/SHA-256, page/order, verbatim text, normalized fields, and confidence. Every attachment exists in the immutable official archive and every supplied SHA-256 matches its canonical attachment Evidence. No OCR or web research was performed.
- No Evidence record was added: the transcription reuses the existing Official-Event attachment IDs and retains the workbook as extraction provenance.

## Normalization

| Competition | Rows | Unique Entries |
| --- | ---: | ---: |
| C-001 | 5 | 5 |
| C-002 | 5 | 5 |
| C-017 | 10 | 10 |
| C-022 | 17 | 17 |
| C-028 | 54 | 42 |
| **Total** | **91** | **79** |

Seven repeated C-028 bracket/final rows were folded into identity-level Entries and retained in `transcription_history`. Five uncertain rows were excluded, producing a net reduction of 12 rows. C-016 remains at zero: no official result row was recovered.

## Participation and uncertainty

- Canonical participation after identity normalization: Finished 41, Started 10, Scheduled 20, DNS 7, DNF 1.
- Kimi's 42 `Started` rows became 10 actual starts, 20 bracket-only `Scheduled` identities, 7 rows folded into later Finished identities, and 5 unresolved rows. Byes and opponent forfeits alone were not treated as starts.
- The 11 Medium and 4 Low C-028 rows were reviewed individually. Ten Medium rows are retained as Research Leads with their `[UNCERTAIN: ...]` text. `TR-058` and all four Low rows (`TR-056`, `TR-079`, `TR-082`, `TR-089`) remain unresolved and create neither Team nor Entry. Exact decisions: [decisions.json](decisions.json).

## Canonical effects

- Existing Team IDs reused: 0; the seven pre-existing Team identities do not exactly match these entries.
- New Team identities: 68. Similar names were not merged; Organization IDs were not inferred.
- New Competition Entries: 79 (69 Verified, 10 Research Lead).
- Canonical records: 1,208 -> 1,355; Entries: 691 -> 770; Teams: 7 -> 75; Evidence: 447 -> 447.
- Canonical Entry statuses: Verified 689 -> 758; Research Lead 2 -> 12.

## QA gate

All required checks passed: the repository validator suite; the five transcription negative controls; the six prior-import, seven official-archive, and six frozen-v2.1 negative controls; the frozen checkpoint audit; 39 unit tests; strict MkDocs build; PDF build; and Git diff checks. This import is committed separately and is not pushed.
