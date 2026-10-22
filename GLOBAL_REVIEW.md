# WHRG 2026 global editorial review

Review date: 2026-10-22

## Human requirements

| Requirement | Result | Evidence in the publication |
|---|---|---|
| A first-time reader can understand what happened without the appendix | Pass | Chapter 1 opens with the 8.64-second sprint, 10–1 autonomous football final, and 26-minute household sequence, then gives event scale and the autonomy distinction. |
| The 2,500+ hour dataset and practical access question are central | Pass | Chapters 5 and 6 separately cover production claims, contents, seven releasers, unknown technical fields, four publication states, the 2026-10-13 access audit, and operational comparisons. |
| Chinese, English, and Japanese terminology is controlled and natural | Pass | `dic.md` records source form, verified official English or `Not Found`, canonical Japanese, forbidden forms, and usage notes. Public prose marks official Chinese team names and otherwise uses Japanese. |
| The structure tells an event and engineering story | Pass | The numbered route moves from visible competition scenes to event families, real-world tasks, results, data production, data access, organizational roles, infrastructure, and cross-year outcomes. Method and full enumerations are in the appendix. |

## Report-wide editorial checks

| Check | Result | Review note |
|---|---|---|
| Excessive Chinese terminology | Pass | Raw Simplified Chinese is limited to marked official names and reference titles. |
| Internal English schema terminology | Pass | Reader-facing chapters do not use internal entity labels. |
| Repeated defensive caveats | Pass | Uncertainty is stated where it changes interpretation; the dataset access conclusion is bounded once and then operationalized. |
| Repeated methodology | Pass | Detailed procedure appears in Appendix A; chapters contain only method needed to interpret a result. |
| Duplicate chapter content | Pass | `CROSS_CHAPTER_MATRIX.md` assigns each recurring topic a primary home. |
| Database-like main tables | Pass | Chapter 2 groups event families; the 51-row inventory is in Appendix B. The 21-row task table remains in Chapter 3 because it directly answers what each real-world competition required. |
| Unsupported causality | Pass | Performance, platform use, organizational relationship, and post-event announcements are not presented as causal proof. |
| Misleading 2025→2026 comparison | Pass | Only compatible events are compared; class and rule differences are explicit. |
| “Open” equated with downloadable or licensed | Pass | Announcement, description, access, download, license, and reuse are separate states. |
| Invented company English names | Pass | Only verified brand forms are recorded; unverified official English remains `Not Found`. |
| Public exposure of internal paths or Kimi workflow | Pass | No public chapter cites import paths, staging records, or internal review files. |

## Evidence and content coverage

- The appendix exposes all 51 competition rows and the chapter text explains all 21 real-world task competitions.
- Six representative narrative clusters were reviewed: 100-metre sprint, 1,500-metre endurance, 5-on-5 football, household service, industrial packing/storage, and dexterous-hand tasks.
- Corrected household, hotel, and firefighting results replace superseded values.
- The medal section keeps 159 total slots, 136 assigned slots, 47 gold, 44 silver, 45 bronze, and 23 unresolved slots.
- The seven dataset release participants are listed without inferring equal or specific contribution roles.
- The dataset audit conclusion is dated 2026-10-13 and does not claim that the dataset is nonexistent or permanently unavailable.

## Deliberate omissions and unresolved claims

- The reported 1,500-metre joint-overheating retirement explanation was not elevated into public prose because the reviewed source path did not support a sufficiently precise, attributable statement.
- The reported firefighting unseen-task element and 4–5 kilogram extinguisher detail were not used because the available support did not justify the exact combined claim.
- The reported “three vehicles within 30 minutes” electric-vehicle charging detail was not used as a result claim because the directly accessible source path was insufficient; the verified task sequence remains.
- Five competition-result source paths, 23 medal slots, the identity of competition 30, the full 2025 team roster, organization-level dataset contributions, and the complete dataset access package remain substantive gaps.

## Rendering review

- Strict MkDocs build completed with the fixed eleven-page navigation.
- Representative HTML views were inspected at narrow width; navigation, chapter links, citations, and the 51-row appendix table remained discoverable.
- The complete PDF contains all eleven navigation documents in 20 A4 pages.
- Every PDF page was rendered to PNG; representative narrative, comparison, wide-table, medal, audit, method, and reference pages were visually inspected.
- The PDF builder now removes HTML language markers while preserving official names and embeds an available Noto CJK font to prevent missing Japanese or Simplified-Chinese glyphs.
