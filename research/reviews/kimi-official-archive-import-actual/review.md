# Kimi official archive import: actual-input review

Review date: 2026-09-24

## Scope and audit continuity

This is a new review of the Kimi workbooks delivered to `research/inbox/kimi/`. It does not overwrite or supersede the missing-input audit at `research/reviews/kimi-official-archive-import/review.md`. No web research was performed, the external Kimi workspace was not accessed or modified, and the v2.1 migration was not revisited. The v2.1 canonical records and supplemental semantics are frozen baselines; this import is additive Evidence only.

The requested priority input, `whrg-official-archive-attachments-2025-2026.xlsx`, is still absent. Consequently, this review imports supported source metadata from the four delivered workbooks but makes no official-attachment-dependent Entry promotion or identity change.

## Inputs and immutable snapshots

| Input | SHA-256 | Immutable snapshot |
| --- | --- | --- |
| `china-source-expansion-2025-2026.xlsx` | `185019e6ace844f608b1a029a238167e5aa7b6dd1273abd704b947bc2bdc2d37` | `research/imported/kimi/185019e6ace844f608b1a029a238167e5aa7b6dd1273abd704b947bc2bdc2d37/china-source-expansion-2025-2026.xlsx` |
| `whrg-2025-archive-team-recovery.xlsx` | `43861d618a902a175ab0e82ea66aa4d480512b3d5459f3090c51fc2d9c615627` | `research/imported/kimi/43861d618a902a175ab0e82ea66aa4d480512b3d5459f3090c51fc2d9c615627/whrg-2025-archive-team-recovery.xlsx` |
| `cas-wechat-ecosystem-2025-2026.xlsx` | `32340418eef504949b1182a1e2ed2eb4da378b22cc6344a9520dbedc473b9b60` | `research/imported/kimi/32340418eef504949b1182a1e2ed2eb4da378b22cc6344a9520dbedc473b9b60/cas-wechat-ecosystem-2025-2026.xlsx` |
| `source-cross-reference-normalized-2025-2026.xlsx` | `fa88c16875c7c8accc14e0540da859bf23462e3925724cb35e45fc5a3e8c6239` | `research/imported/kimi/fa88c16875c7c8accc14e0540da859bf23462e3925724cb35e45fc5a3e8c6239/source-cross-reference-normalized-2025-2026.xlsx` |

Missing input: `whrg-official-archive-attachments-2025-2026.xlsx`.

All sheets in all four delivered workbooks were reviewed. The files contain no workbook formulas, macros, or external-link parts. Identifier cells used by the importer are text values, and no personal contact or confidential-data columns were found. Public names and source excerpts are retained as research provenance.

## Workbook coverage

- `china-source-expansion-2025-2026.xlsx`: `Source Map`, `Entity Leads`, `2025-2026 Cross-Year Map`, and `Open Knowledge Leads`.
- `whrg-2025-archive-team-recovery.xlsx`: `2025 Source Map`, `2025 Team Entry Map`, `2025 Result Coverage`, `2025-2026 Cross-Year Map`, `Evidence`, and `Unknown Questions`.
- `cas-wechat-ecosystem-2025-2026.xlsx`: `CAS Source Map`, `WeChat Source Map`, `Manufacturer Source Map`, `University Lab Source Map`, `Relationship Map`, `Open Knowledge Leads`, `Evidence`, and `Unknown Questions`.
- `source-cross-reference-normalized-2025-2026.xlsx`: `Evidence Cross-Reference`, `Source Classification Audit`, `WHRG Year Relation`, `Entry Leads`, `Cross-Year Continuity`, `Open Knowledge Leads`, and `Corrections Log`.

The normalized source-class audit was applied on publisher identity, not on Kimi's claim framing. For example, event-organizer material remains `Official-Event`; government sources are `Official-Gov`; university-owned pages are `University-First-Party`; Xinhua and Beijing Daily are `State-Media`; general news publishers are `Media-Secondary`; and portal or reposting services remain `Aggregator`. Every accepted record remains `unverified`; acceptance records source metadata, not independent verification of every claim on the linked page.

## Evidence disposition

The four workbooks supplied 87 distinct source/evidence identifiers after cross-workbook normalization:

- Accepted as new canonical Evidence: **48**.
- Deduplicated to existing or accepted canonical Evidence: **19**.
- Rejected from canonical import: **20**.

Accepted identifiers:

`EV-057`, `EV-059`, `EV-060`, `EV-061`, `SRC-003`, `EV-065`, `EV-066`, `EV-067`, `EV-068`, `EV-069`, `EV-070`, `EV-071`, `EV-072`, `EV-073`, `EV-074`, `EV-075`, `EV-076`, `EV-077`, `EV-078`, `EV-079`, `EV-080`, `EV-081`, `EV-082`, `EV-084`, `EV-085`, `EV-086`, `EV-087`, `EV-088`, `EV-089`, `EV-090`, `EV-091`, `EV-092`, `EV-093`, `EV-094`, `EV-095`, `EV-096`, `EV-098`, `EV-099`, `EV-100`, `EV-101`, `EV-102`, `EV-104`, `EV-115`, `EV-117`, `EV-118`, `EV-120`, `EV-121`, and `EV-122`.

The exact machine-readable inventory and record hashes are in `research/evidence/kimi-official-archive-import-actual.json`. Accepted source classes are: 9 `Official-Gov`, 1 `Official-Event`, 4 `Official-Org`, 3 `University-First-Party`, 1 `Research-Inst`, 1 `Enterprise`, 9 `State-Media`, 9 `Media-Secondary`, 1 `Media-Clue`, 9 `Aggregator`, and 1 `Encyclopedia/Baike`.

### Deduplicated identifiers

| Supplied ID | Canonical ID | Reason |
| --- | --- | --- |
| `EV-052` | `EV-067` | Same Xinhua URL and 2025 1500 m source. |
| `EV-053` | `EV-066` | Same Xinhua URL and 2025 100 m source. |
| `EV-054` | `EV-068` | Same Beijing government URL. |
| `EV-055` | `EV-069` | Same Xinhua URL and 2025 football source. |
| `EV-056` | `EV-074` | Same Zhihu URL. |
| `EV-058` | `EV-072` | Same official 2025 registration URL. |
| `EV-063` | `EV-076` | Same Xinhua dance source URL. |
| `EV-064` | `EV-ESM-001` | Same existing official 2026 draw notice. |
| `EV-083` | `EV-122` | Same official 2026 C-005 result PDF. |
| `EV-097` | `EV-092` | Same CLS source URL. |
| `EV-103` | `EV-100` | Same Beijing Daily source URL. |
| `EV-105` | `EV-100` | Same Beijing Daily source URL. |
| `EV-106` | `EV-ESM-005B` | Same Xinhua 2026 event report. |
| `EV-123` | `EV-122` | Same official 2026 C-005 result PDF. |
| `EV-124` | `EV-ESM-005B` | Same Xinhua 2026 event report. |
| `EV-125` | `EV-ESM-005B` | Same Xinhua 2026 event report. |
| `EV-023(Master)` | `EV-023` | Existing canonical repository Evidence. |
| `EV-024(Master)` | `EV-024` | Existing canonical repository Evidence. |
| `EV-133` | `EV-010` through `EV-014` | Announced dataset lead already covered canonically. |

### Rejected identifiers

| Supplied ID | Reason |
| --- | --- |
| `EV-062` | Publication date and URL-path year conflict. |
| `SRC-001`, `SRC-002` | Generic platform homepages, not claim-level sources. |
| `SRC-004` | Aggregator knowledge hub is only a partial lead. |
| `EV-107` through `EV-112` | Synthetic relationship summaries without direct source URLs. |
| `EV-113`, `EV-119` | Official-account mentions without directly accessible articles. |
| `EV-116` | Research-self negative search result, not source Evidence. |
| `EV-126` | Explicitly reports that no source was found. |
| `EV-127` through `EV-130` | Synthetic relationship summaries without direct source URLs. |
| `EV-131` | Media description without repository, paper, or license source. |
| `EV-132` | Media open-source claim without repository or license source. |

## Official-archive-specific review

The absence of `whrg-official-archive-attachments-2025-2026.xlsx` prevents independent review of its proposed attachment inventory. No substitute was inferred from media, field transcription, or the other workbooks.

- **Page/attachment lineage:** unresolved. The delivered cross-reference includes URLs and a C-005 PDF lead, but it does not supply the missing workbook's page-to-attachment chain.
- **Attachment hashes/provenance:** unresolved. The four delivered workbook hashes are recorded above; no claimed official attachment was delivered for byte-level hashing.
- **Evidence ID reuse/deduplication:** the 19 mappings above were reviewed and recorded. Reused URLs and existing canonical records were not imported twice.
- **Competition ID mappings:** workbook claims were checked against the canonical competition IDs. No Competition or Entry mapping was changed. C-005 material remains claim evidence only.
- **C-003 parsing:** timing/result interpretation remains ambiguous; no canonical parsing or Entry change was made.
- **C-006 parsing:** unavailable because the requested official-attachment input is missing; no canonical change was made.
- **Participation Status:** no delivered evidence met the threshold to change a canonical Entry's participation status.
- **2025/2026 separation:** 2025 sources were retained as 2025 evidence only and were not used to verify 2026 participation or continuity.
- **RoboCup separation:** `EV-099` is retained as unverified RoboCup-related source metadata and was not used to establish WHRG participation.
- **Proposed promotions:** no Kimi-proposed `Research Lead` to `Verified` promotion was accepted. Kimi's proposed status is not authority, field evidence alone cannot establish `Verified`, and official-event evidence was not available to close the gaps.
- **New Entry identities:** none. The delivered Entry and entity leads did not provide canonical IDs, and no identifiers were invented.

## Canonical effects

| Class | Result |
| --- | --- |
| A. Existing Entry confirmed | **0**. New source metadata did not independently close an Entry's identity and participation evidence chain. |
| B. Research Lead -> Verified | **0**. No proposed promotion met the policy threshold. |
| C. Genuinely new Entry identity | **0**. No stable canonical identity was supplied. |
| D. Conflict/ambiguity; no canonical change | Retained. Includes the missing official-attachment workbook; C-003 timing ambiguity; unavailable C-006 parsing; C-005 result/rank claims that do not independently resolve existing Entry status, including GMO Robots; 2025-to-2026 continuity leads; and entity names without canonical IDs. |

New canonical entity records: **0 Team, 0 Organization, 0 Robot Platform, 0 Competition Entry**.

Open Knowledge canonical changes: **0**. Media descriptions of open source were not treated as verified artifacts; `EV-131` and `EV-132` were rejected because no repository or license source was supplied. Existing repository/dataset evidence was deduplicated rather than recreated.

## Canonical counts before and after

| Record/count | Before | After |
| --- | ---: | ---: |
| All canonical records | 234 | 282 |
| Evidence | 142 | 190 |
| Competition Entries | 22 | 22 |
| Verified Entries | 16 | 16 |
| Research Lead Entries | 6 | 6 |
| Unresolved Entries | 0 | 0 |
| Teams | 7 | 7 |
| Organizations | 4 | 4 |
| Robot Platforms | 0 | 0 |

All 48 additions are `Evidence` records with canonical status `unverified`. The 234 pre-import records are byte-semantically unchanged, and `research/evidence/supplemental.json` and `research/evidence/master-v2-1.json` are unchanged.

## Validation

All required checks passed:

- Repository validators: PASS (`scripts/validate.py`), including research structure, citations, duplicate headings, and terminology.
- Import validator: PASS with 48 accepted Evidence records, unchanged Entry counts, unchanged v2.1 base, and 6/6 negative controls.
- Frozen v2.1 candidate validator: PASS with 6/6 negative controls and no historical-review rewrite.
- Frozen checkpoint audit: PASS.
- Unit tests: 31 passed.
- Strict MkDocs build: PASS. Material for MkDocs emitted its upstream MkDocs 2.0 informational warning; the strict build completed successfully.
- PDF build: PASS; `output/pdf/whrg-report.pdf` generated.
- `git diff --check`: PASS.
- Staged diff check: PASS before commit.
