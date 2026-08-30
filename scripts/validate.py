#!/usr/bin/env python3
"""Run all repository validators with the same interpreter from the repo root."""

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    failed = []
    for name in ('validate_research.py', 'validate_links.py', 'validate_headings.py', 'validate_terminology.py'):
        if subprocess.run([sys.executable, str(ROOT / 'scripts' / name)], cwd=ROOT).returncode:
            failed.append(name)
    if failed:
        print('FAIL: ' + ', '.join(failed))
        return 1
    print('OK: all repository validators passed.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
