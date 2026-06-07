"""讓 tests 能 import skill 的 stdlib-only 模組（standalone plugin repo）。"""
from __future__ import annotations

import sys
from pathlib import Path

_SKILL_SCRIPTS = (
    Path(__file__).resolve().parent.parent
    / "skills" / "fetch-tw-earnings-call" / "scripts"
)
if str(_SKILL_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SKILL_SCRIPTS))
