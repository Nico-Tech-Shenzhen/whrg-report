---
name: whrg-report-qa
description: Validate WHRG report structure, terminology, citations, research provenance, and site/PDF builds. Use for QA or infrastructure changes, not substantive drafting.
---

# Report QA

Adapted from the reference report QA procedure; no inherited chapter or review-state assumptions.

Read `RULES.md`, the relevant `REPORT_PLAN.md` workstream, and applicable `dic.md` entries. Start with the changed files and their research dependencies; use full scope after infrastructure or navigation changes.

Run from the repository root with the configured Python environment:

```powershell
python scripts/validate.py
python -m mkdocs build --strict
python scripts/build_pdf.py
git diff --check
git diff --cached --check
```

Use `python scripts/validate_research.py --candidate research/staging/candidate.json` for an import candidate. Run `python -m unittest discover -s tests` after changing import/validation code.

Script success checks structure, not truth. Review source support, uncertainty, licensing, numerical units/denominators, and entity boundaries manually. Empty research is valid during bootstrap and must be reported as empty, never verified. For layout changes or release, inspect rendered HTML and every PDF page. The PDF builder supports only its documented Markdown subset; unsupported content requires an explicit extension and rendering check.

Report failures with paths/lines and distinguish checks run, skipped, and unsupported. Do not rewrite substantive content during QA-only work or create completed-review status files merely because checks passed.
