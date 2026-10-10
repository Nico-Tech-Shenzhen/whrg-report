# WHRG 2026 research report

Source and publication repository for the Japanese [WHRG 2026 working research report](https://takasumasakazu.net/whrg-report/). The report reconstructs competitions, Entries, Teams, Organizations, Robot Platforms, Evidence, and Rule Versions from the canonical corpus. A successful build validates structure, not factual completeness.

## Windows setup

Use Python 3.11 or newer. Commands run from the repository root:

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe scripts/validate.py
.\.venv\Scripts\python.exe -m unittest discover -s tests
.\.venv\Scripts\python.exe -m mkdocs build --strict
.\.venv\Scripts\python.exe scripts/build_pdf.py
git diff --check
```

Regenerate the public statistics appendix after canonical data changes:

```powershell
.\.venv\Scripts\python.exe scripts\generate_report_tables.py
```

In this Windows Codex environment, Python was found at `C:\Users\takasu\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe`. If `python` is not on PATH, use that executable for the first command. Activate `.venv` or use its explicit executable for subsequent commands. Bootstrap used `--system-site-packages` to reuse the bundled ReportLab; a normal fresh environment can install all requirements instead.

The site is generated into `site/`; the PDF into `output/pdf/whrg-report.pdf`. Both are ignored. CI uses the same validators and PDF builder and uploads the combined `whrg-report-site-and-pdf` artifact. To assemble the same artifact locally after the builds:

```powershell
New-Item -ItemType Directory -Force site/pdf | Out-Null
Copy-Item -LiteralPath output/pdf/whrg-report.pdf -Destination site/pdf/whrg-report.pdf
```

Only generated `site/` content is a publication artifact. Keep research snapshots, staging files, review records, and the repository root out of it.

## GitHub Pages publication

Pushes to `main` and manual runs on `main` validate, build, and deploy the generated site to `gh-pages`; pull requests and other refs do not deploy. The build job has read-only repository permissions, and write access is scoped to the deploy job.

Before publication:

1. Resolve all QA failures and review exactly which pending research and infrastructure changes belong in the release. Do not bypass checkpoint tests or promote research/review status merely to get a green build.
2. Regenerate the tables, run the commands above, and inspect the generated HTML and every PDF page. Review source support, rights, privacy, and font coverage; confirm that the artifact contains only intended reader-facing files.
3. Commit and push only the approved files, confirm that build and deploy jobs succeed, then check the [published site](https://takasumasakazu.net/whrg-report/) and its PDF, navigation, assets, and search.

Deployment success and public URL availability are checked separately; one does not prove the other.

## PDF limits

The adapted ReportLab renderer handles headings (levels 1-3), paragraphs, simple lists/tables, bold/inline code, external links, and local numeric citations. Its page order comes from `mkdocs.yml`; there is no fixed chapter list. It rejects common unsupported media, snippets, code fences, and local page links rather than silently dropping them. Other complex Markdown needs explicit renderer support and visual QA before use.

The portable default uses ReportLab's CJK CID font for CI builds. For a locally installed licensed TrueType font, set `REPORT_FONT` to its path. Visually review every page after any font change.

## Project map

- `AGENTS.md`: stable operating rules and routing.
- `RULES.md`: evidence and prose policy.
- `REPORT_PLAN.md`: provisional workstreams and next milestone.
- `dic.md`: canonical terminology and entity types.
- `research/README.md`: storage, import manifest, and canonical record schema.
- `.agents/skills/`: QA and Kimi import procedures.
- `MIGRATION.md`: reference revision and adaptation decisions.

Research deliveries are processed through the import workflow and retained outside the public `site/` artifact. Reader-facing claims cite underlying public sources, not internal workbooks or review files.
