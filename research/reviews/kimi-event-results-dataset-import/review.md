# Kimi event/results/dataset import review

Review date: 2026-10-10

## Scope and immutable imports

The four delivered files were screened as research material for the public WHRG 2026 report. They contain public-source research, derived tables, and internal provenance notes; no newly introduced personal or confidential material was identified. The files were imported byte-for-byte and registered in `research/imported/kimi/manifest.json`:

| Delivery | SHA-256 |
| --- | --- |
| whrg-2026-event-results-report-research.xlsx | `320ab83cd4a8150ecbdc67cc3262f9289c85f2ef7ac0443cb43ee6a9e198b8d3` |
| whrg-2026-dataset-release-audit.xlsx | `7458ce35ae1dbb3e8708aa04517f789d792924ddcd393445eb34b045fd4e338c` |
| whrg-2026-report-research-summary.md | `cee28a5375309c7d4832e1fe918f0427389ec3f8c2211964633529477a217d76` |
| whrg-2026-medal-reconciliation-summary.md | `2d9d5476d24d2281230a53e8e24ab6fcdfad050fdf6f3cf340b3b9da71c0be10` |

The workbooks were opened read-only with cached values. Identifier cells were treated as text. The imported bytes were not saved or reformatted.

## Evidence and result review

- The competition sheet contains exactly 51 rows: 30 competitive events and 21 scenario events. Its IDs run from C-001 through C-051 without duplication.
- Result locators were checked against the existing canonical Evidence corpus and official archive. Thirty-eight competition rows resolve directly to a specific official result page or PDF through existing `EV-*` or `ATT-*` records. Eight dexterous-hand finals resolve to the corresponding canonical official-result records. C-013, C-014, C-016, C-029, and C-030 remain without a verified final-result source and are published as unresolved, not filled from inference.
- The 2026-08-23 official correction notices for household/home, hotel, and firefighting match existing canonical archive records `ATT-0071`, `ATT-0072`, and `ATT-0073`. The reviewed public tables use only the corrected result and do not count the superseded result.
- Dates and event years remain explicit. 2025 values are used only where the workbook identifies the same named event and the comparison page preserves rule/class caveats.

## Medal reconstruction decision

The `C4-Medal Ledger` has 159 medal-slot rows, representing 53 event or sub-event units times gold, silver, and bronze. It closes to:

| State | Gold | Silver | Bronze | Total |
| --- | ---: | ---: | ---: | ---: |
| Resolved to official Team name | 47 | 44 | 45 | 136 |
| Unresolved | 6 | 9 | 8 | 23 |
| Total slots | 53 | 53 | 53 | 159 |

The public primary table uses the official Team name from the result notice. It does not promote normalized company, organization, or platform aggregates as an official medal table. The media claims for AgiBot, Beijing Humanoid/Tiangong, Unitree, and Galbot are retained only as separately labelled reconstructions with explicit aggregation rules and unresolved differences.

This decision follows the entity boundary in `dic.md`: Team, Organization, and Robot Platform are different record types. Kimi's derived medal aggregation was reviewed but not imported wholesale as canonical fact.

## Dataset review

The strongest supplied sources support an announcement of a dataset exceeding 2,500 hours, collected during preparation/training and formal competition, spanning 12 application scenarios, 44 operations, more than 100 skills, and more than 10,000 tasks. The claimed modalities include multi-view video, joint motion, robot/body state, task results, failure cases, boundary conditions, semantic intent/action labels, object recognition/detection annotations, long-horizon trajectories, and dynamic disturbances.

The listed release organizations are 赛迪研究院, 北奥集团, 北京人形机器人创新中心, 智元机器人, 银河通用, 万境千寻, and 星海图. Being named as a joint releaser does not establish a specific contribution, collection, annotation, or custody role. The public report therefore lists publisher/releaser status and marks other roles only where separately supported.

The access audit updates the earlier canonical 2026-08-30 search audit. As of 2026-10-10, the supplied audit found no verifiable landing page, download URL, request route, manifest, version, checksum, license/terms, or API in the audited official/public sources. The accepted wording is "Announced; audited public access route not found," not proof that the dataset does not exist or is not public.

RoboMIND and AgiBot World are retained only as operational-access comparisons. Their landing pages, download mechanisms, dataset descriptions, licenses, and release/version information do not establish that either dataset is part of the WHRG dataset. The relationship remains unconfirmed.

## Post-event review

The five challenge topics, 100-robot school donation, planned 3,000 m2 training base, and announced 2027 WHRG direction have attributable public sources. Unless implementation evidence was supplied, the public report labels them announced or planned rather than operationally verified.

## Promotion outcome

The immutable snapshots and this review are committed. `research/evidence/event-report-2026.json` is a deterministic reviewed report dataset generated from fixed hashes. It supports public tables but does not replace the canonical entity corpus or convert Kimi's interpretations into independent verification. Reader-facing pages cite the underlying public sources and do not expose inbox, staging, snapshot, or review paths.
