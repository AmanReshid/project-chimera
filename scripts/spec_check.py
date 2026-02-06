#!/usr/bin/env python3
"""Basic spec alignment checker.

Checks a set of lightweight rules derived from `specs/_meta.md`:

- Each skill under `skills/` must contain `interface.py`, `impl.py`, and `README.md`.
- `interface.py` should expose a Pydantic `BaseModel` or similar (simple text heuristics).
- There should be at least one test referencing the skill name under `tests/`.

Exit code 0 on success, 1 on any failure.
"""
from pathlib import Path
import sys
import re

ROOT = Path(__file__).resolve().parents[1]
SKILLS_DIR = ROOT / "skills"
TESTS_DIR = ROOT / "tests"

def find_skills():
    if not SKILLS_DIR.exists():
        return []
    return [p for p in SKILLS_DIR.iterdir() if p.is_dir()]

def check_interface_has_model(path: Path) -> bool:
    try:
        text = path.read_text(encoding='utf-8')
    except Exception:
        return False
    # heuristic: look for BaseModel, TypedDict, dataclass, or pydantic import
    if re.search(r"\bBaseModel\b", text):
        return True
    if re.search(r"from\s+pydantic\b", text):
        return True
    if re.search(r"\bTypedDict\b", text):
        return True
    if re.search(r"@dataclass", text):
        return True
    return False

def tests_reference_skill(skill_name: str) -> bool:
    if not TESTS_DIR.exists():
        return False
    for tf in TESTS_DIR.rglob('*.py'):
        try:
            t = tf.read_text(encoding='utf-8')
        except Exception:
            continue
        if skill_name in t:
            return True
    return False

def main():
    failed = False
    skills = find_skills()
    if not skills:
        print("No skills/ directory found; nothing to check.")
        return 0

    for s in skills:
        name = s.name
        print(f"Checking skill: {name}")
        interface = s / 'interface.py'
        impl = s / 'impl.py'
        readme = s / 'README.md'

        if not interface.exists():
            print(f"  [FAIL] missing interface.py in {name}")
            failed = True
        else:
            ok = check_interface_has_model(interface)
            if not ok:
                print(f"  [WARN] interface.py in {name} doesn't declare an obvious model (BaseModel/TypedDict/dataclass)")

        if not impl.exists():
            print(f"  [FAIL] missing impl.py in {name}")
            failed = True

        if not readme.exists():
            print(f"  [FAIL] missing README.md in {name}")
            failed = True

        if not tests_reference_skill(name):
            print(f"  [WARN] no tests reference the skill name '{name}' under tests/")

    if failed:
        print("\nSpec check failed: see errors above.")
        return 1

    print("\nSpec check completed (no fatal failures). Review WARN lines if any.")
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
