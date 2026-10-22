# WHRG 2026 report plan

## Purpose

Produce a reader-first Japanese report that explains what happened at the 2026 World Humanoid Robot Games, what the results reveal about humanoid-robot capability, and how far the announced data release can be independently accessed and reused.

The report must answer four questions:

1. What did the event ask robots to do?
2. What did the most informative results actually demonstrate?
3. Which organizations, platforms, and rules made those results possible?
4. What evidence exists for post-event data publication and reuse?

## Public structure

| Page | Purpose | Required evidence and tables | Boundary |
|---|---|---|---|
| Introduction | Orient a first-time reader to the event before stating the report's argument | Official name; edition, dates, venue, organizers, scale, public status; 2025→2026 overview; reading route | No import or validation narrative |
| Chapter 1 | Give a whole-event mental model before representative results | Organizer and participant model; venue layout; 30+21 structure; autonomy distinction; three closing narratives | Detailed rules and complete inventory belong in Chapter 2 |
| Chapter 2 | Explain how the competition families worked and expose the complete reader inventory | Concrete mechanics for six families; concise 51-row list with operation mode and representative result | Source-audit detail remains in the appendix |
| Chapter 3 | Explain all 21 real-world task competitions | 21-task table; representative task sequences; result status | Results overview belongs in Chapter 4 |
| Chapter 4 | Reconstruct results and compare compatible performance | Key marks; medal reconstruction; cautious 2025 comparison | No unsupported ranking or causality |
| Chapter 5 | Describe the announced 2,500+ hour dataset and the seven named releasers | 12 application scenarios; 44 operations; 100+ skills; 10,000+ detailed tasks; content-type table; organization-role table | Do not call the 12 application scenarios modalities or equate naming with contribution |
| Chapter 6 | Audit publication and compare operational release mechanics | Four-state audit; missing artifacts; five-dataset comparison | No claim that comparison datasets are event components |
| Chapter 7 | Separate organizations, teams, manufacturers, platforms, and entries | Role model; concrete relationship cases | No identity merger based on naming |
| Chapter 8 | Explain the enabling system around rules, training, venues, robot access, and data infrastructure | Evidence-backed ecosystem map/table | Post-event announcements belong in Chapter 9 |
| Chapter 9 | Assess change from 2025 and documented post-event developments | Compatible scale comparison; announced programs; dated status | Avoid treating announcements as operational outcomes |
| Appendix | Make the report auditable without interrupting the narrative | Method; complete 51-event inventory; medal reconstruction; access-audit detail; definitions; unresolved items | No new interpretive thesis |

## Evidence priorities

1. Organizer and official event documents.
2. Versioned rules and official result pages.
3. University, research institute, company, and team publications.
4. Public repositories, data cards, manifests, and licenses.
5. Attributable reporting.
6. Imported research material, used only as a route to underlying sources or as explicitly bounded internal evidence.

## Dataset-publication test

The publication chapter must separately verify:

- announcement and scope;
- landing page or catalog record;
- stable download or API path;
- retrievable files;
- manifest or equivalent inventory;
- version identifier and release history;
- checksums or other integrity metadata;
- schema and annotation documentation;
- explicit license or terms;
- citation information;
- reproducible access instructions.

The comparison set is RoboMIND, AgiBot World, Unitree open datasets, WorldSimReady-Home, and RekaDaily-10K. The comparison is limited to publication mechanics and does not imply equivalence of content, scale, quality, or event affiliation.

## Current known gaps

- Five of 51 competition-result source paths remain unresolved in the canonical event ledger, including the identity of competition 30.
- Twenty-three of 159 medal slots are not assigned to a team in the current reconstruction.
- The announced WHRG dataset lacks a verified complete public package meeting the reusable-state test.
- The specific data contribution of each named releasing organization is not established.
- Some competition operation modes are documented only for particular teams or runs.
- Cross-year result definitions and field conditions are not uniformly compatible.
- A final WHRG 2026 attendance count with an explicit event denominator has not been verified; ticketed public access is verified.
- The 21 competition real-world task events and the dataset's 12 application scenarios are separate classifications; no public crosswalk has been verified.

## Deliverables and completion

Public deliverables are the MkDocs site and full-report PDF. Research deliverables are immutable Kimi snapshots, a persistent import review, canonical evidence records, report-specific generated evidence, and validation output. Local completion does not authorize publication or synchronization to the external Kimi workspace.
