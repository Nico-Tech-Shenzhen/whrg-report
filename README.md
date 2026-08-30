# WHRG 2026 research report

Infrastructure bootstrap for the [WHRG report repository](https://github.com/Nico-Tech-Shenzhen/whrg-report). No substantive report chapters or Kimi research are included.

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

In this Windows Codex environment, Python was found at `C:\Users\takasu\.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe`. If `python` is not on PATH, use that executable for the first command. Activate `.venv` or use its explicit executable for subsequent commands. Bootstrap used `--system-site-packages` to reuse the bundled ReportLab; a normal fresh environment can install all requirements instead.

The site is generated into `site/`; the PDF into `output/pdf/whrg-report.pdf`. Both are ignored. CI uses the same validators and PDF builder, uploads the combined site/PDF artifact, and deploys main to `gh-pages`. Enable GitHub Pages for that branch in repository settings when ready and when the repository visibility/account plan permits it. PRs build without deployment or write permissions. The configured site URL is an intended address, not proof that Pages is enabled.

## PDF limits

The adapted ReportLab renderer handles headings (levels 1-3), paragraphs, simple lists/tables, bold/inline code, external links, and local numeric citations. Its page order comes from `mkdocs.yml`; there is no fixed chapter list. It rejects common unsupported media, snippets, code fences, and local page links rather than silently dropping them. Other complex Markdown needs explicit renderer support and visual QA before use.

The portable bootstrap default is Helvetica for ASCII text. Non-ASCII prose requires an explicit font; set `REPORT_FONT` to a licensed TrueType font, such as the installed `C:/Windows/Fonts/NotoSansJP-VF.ttf`, and visually review all pages. No system font installation is required for the ASCII bootstrap CI build. Before multilingual drafting, configure the same licensed font in CI and locally; do not claim publication font coverage from this infrastructure test.

## Project map

- `AGENTS.md`: stable operating rules and routing.
- `RULES.md`: evidence and prose policy.
- `REPORT_PLAN.md`: provisional workstreams and next milestone.
- `dic.md`: canonical terminology and entity types.
- `research/README.md`: storage, import manifest, and canonical record schema.
- `.agents/skills/`: QA and Kimi import procedures.
- `MIGRATION.md`: reference revision and adaptation decisions.

Kimi files are delivered into the local inbox before processing. Use the import Skill; never treat an empty corpus or structural validation as a verified report.
