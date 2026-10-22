# WHRG 2026 global editorial review

Review date: 2026-10-22

## First-time reader audit

The opening was reviewed against the published RoboMaster report as a reader-orientation benchmark: identify the event, show its physical and organizational structure, explain what competitors do, and only then move to interpretation. WHRG does not copy that report's prose or architecture.

| Three-minute reader question | Result | Evidence in the publication |
|---|---|---|
| What is this event, and which edition was it? | Pass | The introduction names the World Humanoid Robot Games, identifies 2026 as the second edition, and gives the dates. |
| Where did it happen, and what did the venue feel like? | Pass | The introduction names the Ice Ribbon; Chapter 1 distinguishes the main floor, Robot House, Robot Street, outdoor areas, and off-site hotel, fire-service, and library settings. |
| Who organized it? | Pass | The four organizers are named in the introduction and Chapter 1. |
| Who participated, and what did teams bring? | Pass | Team, organization, platform, and event infrastructure are separated; the domestic organization counts are given without turning them into the international team denominator. |
| What did robots actually do? | Pass | Chapter 1 gives the six-family overview; Chapter 2 explains representative mechanics and presents all 51 events; Chapter 3 describes all 21 real-world task events. |
| Was this public or only a closed technical test? | Pass | Paid public sessions and ticket routes are stated. The attributed report of more than 10,000 spectators is retained with an explicit warning that its counting method is unknown. |
| What was autonomous, remote-operated, or rule-dependent? | Pass | The distinction appears before detailed results and is carried into the 51-event table. Team- or run-specific autonomy is not generalized. |
| Are the key denominators distinct? | Pass | 16 countries, 666 teams, 2,056 robots, 51 events, 30 competition events, 21 real-world task events, 1,301 sessions, and the dataset's 12 application scenarios are labeled separately. |

## Report-wide editorial checks

| Check | Result | Review note |
|---|---|---|
| Natural Japanese and controlled terminology | Pass | The verified Japanese event name is canonical; source titles and marked official team names preserve Chinese. |
| Complete reader coverage without database prose | Pass | Chapter 2 uses a concise 51-row orientation table; the appendix remains the source and result audit. |
| Concrete mechanics | Pass | Running, football, contact events, judged performance, dexterous-hand work, and real-world services each have an observable start-to-finish explanation. |
| Event/task/data denominator control | Pass | The 21 real-world task events are never equated with the dataset's 12 application scenarios. |
| Dataset terminology | Pass | The canonical scale is 12 application scenarios, 44 operations, 100+ skills, and 10,000+ detailed tasks; modalities and content types are listed separately. |
| Chinese-name overload | Pass | The Chapter 2 reader table does not repeat a Chinese team name on every row; official names remain available where needed in Chapter 3 and the appendix. |
| Unsupported causality | Pass | Performance, platform use, organizational relationship, and post-event announcements are not presented as causal proof. |
| “Open” equated with downloadable or licensed | Pass | Announcement, description, access, download, license, and reuse remain separate states. |

## Evidence and content coverage

- The introduction supplies the event's basic facts, second-edition history, four organizers, paid public status, scale, and 2025→2026 expansion before making an analytical claim.
- Chapter 1 supplies a physical and organizational mental model, then closes with the 100-metre sprint, 5-on-5 football, and domestic-service examples.
- Chapter 2 exposes all 51 event rows to ordinary readers and explains the mechanics of all six competition families.
- Chapter 3 exposes all 21 real-world task rows and adds concrete industrial, emergency, office, household, hotel, library, outdoor-management, charging, and dexterous-hand sequences.
- Corrected household, hotel, and firefighting results replace superseded values.
- The seven dataset release participants are listed without inferring equal or specific contribution roles.
- The dataset audit conclusion is dated 2026-10-13 and does not claim that the dataset is nonexistent or permanently unavailable.

## Deliberate limits and unresolved claims

- 『人民公安報』の「1万人超」は報道値として記載するが、実人数・延べ人数など集計方法がないため、主催者認定の確定値にはしない。別イベントである2026世界ロボット大会の557,000人は使用しない。
- The firefighting task's undisclosed layout and 4–5 kilogram extinguisher are attributed to one report and are not generalized as proof of universal zero-shot operation.
- The electric-vehicle article establishes one fully autonomous run across three car models, not the operation mode of every entrant.
- Five competition-result source paths, 23 medal slots, the identity of competition 30, the full 2025 team roster, organization-level dataset contributions, and the complete dataset access package remain substantive gaps.

## Rendering review

- Strict MkDocs completed without project warnings or link/anchor failures.
- The introduction and Chapters 1–3 were inspected in the rendered site at desktop width; headings, navigation, citations, and the 51-row and 21-row tables remained legible.
- The full PDF contains all eleven navigation documents in 27 A4 pages. Every page was rendered to PNG and inspected; the introduction, Chapters 1–3, dataset chapters, and appendix tables were also checked at full-page resolution.
- A first PDF pass exposed two-digit event numbers wrapping in the narrow index column. The builder now assigns explicit widths to the Chapter 2, Chapter 3, and appendix event tables; the final render has no clipped text, overlaps, missing glyphs, or vertical number wrapping.
