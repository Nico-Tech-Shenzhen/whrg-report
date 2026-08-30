# Infrastructure provenance

Reference: [Nico-Tech-Shenzhen/robomaster-report](https://github.com/Nico-Tech-Shenzhen/robomaster-report/tree/996a92997abd235f01ceb4fed0ccb18bb2349bfa), inspected at commit `996a92997abd235f01ceb4fed0ccb18bb2349bfa`.

| Reference | WHRG adaptation |
|---|---|
| `mkdocs.yml`, `docs/` | Material theme, Markdown extensions, and docs layout; replaced navigation with a single infrastructure preview. |
| `scripts/build_pdf.py` | Reused ReportLab layout, table rendering, citation anchors, and footer; removed fixed chapter list, author, subtitle/date, chapter-specific spacing, and hard-coded Windows font paths. |
| `.github/workflows/mkdocs-pdf.yml` | Reused checkout/setup/build/artifact/gh-pages pattern; runs the actual ReportLab builder, adds PR QA, strict build and least-privilege deployment. Removed unused PDF-plugin installation. |
| `scripts/validate_links.py` | Reused bare-link and local numeric-citation checks; scoped to docs and all pages. |
| `scripts/validate_headings.py` | Reused duplicate-heading checks without fixed chapters. |
| `scripts/validate_terminology.py`, `dic.md` | Reused machine-readable forbidden/canonical terminology pattern; no event terms migrated; empty forbidden list is valid at bootstrap. |
| `scripts/validate_source_ids.py` | Adapted the referential-integrity concept into `validate_research.py`; typed exact IDs replace a hard-coded event prefix and legacy-ID bypass. |
| `.agents/skills/robomaster-report-qa/SKILL.md` | Adapted scoped deterministic QA plus evidence judgment and render checks as `whrg-report-qa`. |
| `AGENTS.md`, `RULES.md`, `REPORT_PLAN.md`, `research/` | Reused separation of operating rules, evidence policy, evolving plan, terminology, source records and provenance; all WHRG content starts fresh. |

Added `whrg-kimi-import`, immutable hash-addressed snapshot handling, a canonical JSON schema, and boundary/integrity regression tests. The reference's source-card/provenance patterns informed this structure; its corpus is not WHRG evidence.

Intentionally omitted: report prose and research data; all reference evidence/source IDs; nine-chapter architecture; event terminology and fixed numerical assertions; completed/frozen review state; global review, revision status, cross-chapter matrices, field-note/media plans and obsolete task files; chapter/media/history Skills; old generated output, temporary files and bytecode; shell wrappers and event-specific number/stale-reference/Chinese-character validators. Link targets are checked by strict MkDocs validation instead of a fixed chapter blacklist. Numeric and evidentiary consistency remain manual until actual WHRG data defines useful checks.

The full reference clone is retained only in ignored `.reference/` for implementation comparison and is never committed. No external Kimi workspace files were accessed or changed during bootstrap. No blanket content license has been invented; imported material retains its source rights.
