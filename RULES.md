# Evidence and writing policy

## Reader and purpose

The report is for readers who want to understand what the 2026 World Humanoid Robot Games demonstrated, how the competitions worked, and what can actually be reused after the event. Lead with concrete scenes, results, and consequences. Research process belongs in the appendix unless it changes the interpretation of a claim.

## Reader-facing content

- Write public prose in natural Japanese.
- Use the verified official Japanese name at the report's first mention: 世界人型ロボット競技大会（公式英語名：World Humanoid Robot Games、略称WHRG）. Later mentions may use 世界人型ロボット競技大会 or WHRG.
- Explain a documented example before drawing a general conclusion.
- Keep one primary home for each topic and cross-reference rather than repeating whole explanations.
- Do not expose internal record IDs, import paths, validation states, or research workflow in the narrative.
- Preserve source titles, team names, organization names, product names, dataset names, and direct quotations in their original form.

## Evidence and claims

Prefer versioned official rules and organizer documents, then institutional publications, team records and repositories, and attributable reporting. Imported Kimi material is research input, not independent verification.

Distinguish source facts, field observations, analysis, hypotheses, and recommendations. Attribute single-source and team-reported claims. Preserve uncertainty, contradictions, and negative evidence. Never infer causality, participation, affiliation, adoption, autonomy, data contribution, or licensing from proximity, branding, or chronology alone.

Record consequential claims against Evidence records with the source locator, date, scope, confidence, and verification status. A search result, workbook row, or transcription is a lead until checked against the underlying material. Non-public material cannot be the only support for a public factual claim.

## Citations

Use claim-level clickable citations `[[n]](#ref-n)` with a matching `<a id="ref-n"></a>` on the same page. References must link to the specific underlying document, not a search page. Reader-facing prose must not contain bare URLs.

For every public source record, retain publisher or creator, title, publication date or an explicit unknown date, direct URL, access date, and version or commit where relevant. A Kimi identifier is not a citation.

## Numbers and results

Important numbers require date, population, definition, unit, and source. Keep organizations, teams, competition entries, people, and robots as separate denominators. Do not combine incompatible measurements.

For competition results, distinguish official result lists, organizer summaries, institutional reports, team reports, and media accounts. State whether a result is a winning mark, score, elapsed time, match score, medal count, or reconstructed value. Keep unresolved medal slots and missing result sources visible.

## Autonomy and remote operation

Do not describe an event, task, robot, or dataset as autonomous merely because it involved robots. Separate:

- fully autonomous execution;
- autonomy with permitted setup or human intervention;
- teleoperation or remote control;
- mixed or rule-dependent operation;
- operation mode not established by available evidence.

Use the rule version and event-specific evidence. If the source only describes one run or one team, do not generalize it to the entire competition.

## Dataset publication

Public visibility, a landing page, a data card, downloadable files, an API, a license, documentation, reproducibility, reuse, and adoption are separate claims. Record explicit license evidence and version; unknown rights remain unknown.

Use four publication states:

1. **Announced** — a future release or intention is public, but no retrievable artifact is verified.
2. **Described** — scope or content is documented, but retrieval and reuse conditions are incomplete.
3. **Accessible** — a stable public retrieval path and at least one retrievable artifact are verified.
4. **Reusable** — access, structure, versioning, documentation, and rights are sufficiently explicit for an independent user to reproduce a documented use.

For the WHRG 2026 dataset, the bounded conclusion is: the organizer and public reporting describe a multi-organization release of more than 2,500 hours, but as of the stated audit date the report has not verified a complete public package with a stable download path, manifest, version identifier, checksums, schema documentation, and explicit reusable license. Do not shorten this to “open dataset” or “not released.”

## Language and terminology

`dic.md` is the terminology authority. Use its canonical Japanese forms in prose. Raw Simplified Chinese is allowed only in a source title, direct quotation, official name annotation, or preserved identifier. Internal English labels such as `Team`, `Competition`, and `Evidence` belong in research data and code, not Japanese narrative.

## Chapter ownership

`REPORT_PLAN.md` and `CROSS_CHAPTER_MATRIX.md` define the chapter home of each topic. The main chapters explain the event and its implications; the appendix contains methods, full enumerations, audit details, and unresolved items.

## Completion standard

A report change is complete only when:

- public claims are supported by reader-visible citations;
- terminology, numbers, and cross-chapter ownership validate;
- the HTML site builds without warnings;
- the PDF includes the full report, not a summary subset;
- representative HTML and PDF pages have been visually inspected;
- unresolved evidence and publication gaps remain explicit;
- no publication approval, external synchronization, or push is inferred from a local edit.
