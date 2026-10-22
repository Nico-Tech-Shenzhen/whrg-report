# Event overview editorial correction review

Review date: 2026-10-22

## Scope

This review supports the reader-orientation rewrite of the introduction and Chapters 1–3. It does not reopen the full Kimi import or reconstruct Chapters 4–9.

## Published-report comparison

The published RoboMaster report was inspected as a structural benchmark. Its opening establishes match mechanics, robot roles, competition series, and the division between standard and team-designed platforms before analysis. The WHRG opening previously led with three results. The revised WHRG opening now supplies event identity, venue, organizers, participants, competition structure, public status, and operation modes before those examples.

No prose, evidence identifiers, chapter architecture, or review state was copied from the comparison report.

## Verified event overview

- Canonical Japanese event name: 世界人型ロボット競技大会（WHRG）. This follows the Japanese-language Beijing government page. First use includes `World Humanoid Robot Games`.
- Edition: second edition; the first edition was in 2025.
- Dates and principal venue: 2026-08-22 through 2026-08-26, National Speed Skating Oval (Ice Ribbon), Beijing.
- Organizers: Beijing Municipal People's Government; China Media Group; World Robot Cooperation Organization; RoboCup Asia-Pacific Confederation Board of Trustees. The last form follows RoboCup's official event page; the prior Japanese rendering was editorial and is not retained as an official name.
- Scale: 16 countries, 666 teams, 2,056 robots, 51 events, 1,301 matches/attempts; 30 competition events and 21 real-world task events.
- Domestic participant detail: 157 companies and 200 universities/research institutes, preserved as organization counts and not added to the 666-team denominator.
- Public status: paid public sessions and ticket sales verified. People's Police Daily reported more than 10,000 spectators during the event, but did not identify whether this was unique people, aggregate admissions, or another measure. It is not treated as an organizer-certified total.
- Venue model: the main Ice Ribbon competition floor, Robot House, Robot Street, outdoor areas, and off-site hotel, fire-service, and school-library settings.
- Growth context: the competition schedule changed from three days in 2025 (August 15–17, after the August 14 opening ceremony) to five days in 2026, alongside 280 to 666 teams, about 500 to 2,056 robots, 26 to 51 events, and 487 to 1,301 matches/attempts.

## Dataset terminology correction

The source-backed scale is:

- 2,500+ hours;
- 12 application scenarios;
- 44 operations;
- 100+ skills;
- 10,000+ detailed tasks.

Canonical Japanese is `2,500時間超、12の応用場面、44種類の作業、100種類超の技能、1万件超の詳細タスク`.

The 12 application scenarios are not modalities. Multi-view video, joint motion information, robot state, task outcomes, failure cases, boundary conditions, semantic labels, object recognition/detection annotations, long-horizon trajectories, and dynamic disturbances are content types or described data elements. The 21 real-world task events are competition-program entries and are not the dataset's 12 application scenarios. No public crosswalk was verified.

## Reader dossier use

The imported read-only reader dossier was consulted at:

`research/imported/kimi/0f6fb46d0e8094f09970bca4f17e5fd09368f0ae72aca9494ac2dfc0bba16c18/whrg-2026-reader-event-dossier.xlsx`

Relevant rows were C034–C043 and the dexterous-hand entries. Workbook statements were used only to locate or organize public sources. Public prose cites underlying official, institutional, or attributable media pages.

## Public sources checked

- Beijing government Japanese-language preview: event name, date, venue, team and robot counts, 30+21 structure, event facilities.
- Beijing government event listing and press conference: organizers, dates, public tickets, operational infrastructure.
- Beijing Economic-Technological Development Area and Beijing government reporting: international and domestic participant counts, 2025→2026 expansion, venue distribution.
- Beijing government task reports and Xinhua: hotel, library, office, industrial, park, charging, and emergency-response mechanics.
- Official corrected result PDFs: household, hotel, and firefighting results.
- Xinhua dataset announcement: dataset scale and separately described content types.

## Remaining uncertainty

- No attendance figure with a disclosed counting method or organizer certification was found; the attributed People's Police Daily report of more than 10,000 remains bounded accordingly.
- Competition 30 remains unidentified in the current official-list mapping.
- Several event result-source paths and some operation modes remain unresolved.
- A complete public dataset package and a verified 21-to-12 mapping remain unavailable.
