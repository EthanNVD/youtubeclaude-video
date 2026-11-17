"""Step 4 — check the cards and build plan.json from them.

python tools/cards.py projects/<slug>            check + compile -> plan.json (then run the validator)
python tools/cards.py projects/<slug> --check    only check the cards (fast; nothing is written)

Output: a JSON report. "errors" must be fixed (each one says what to change); "warnings" should be fixed.
"""
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
from cardlib import CardError, compile_project  # noqa: E402


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    proj = Path(sys.argv[1]).resolve()
    check_only = "--check" in sys.argv
    try:
        rep = compile_project(proj, write=not check_only)
    except CardError as e:
        rep = {"ok": False, "errors": [str(e)], "warnings": []}
    if rep.get("ok") and not check_only:
        r = subprocess.run([sys.executable, str(ROOT / "tools/validate_plan.py"), str(proj)], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
        try:
            v = json.loads(r.stdout[r.stdout.index("{"):])
            rep["engine_errors"] = v.get("errors", [])
            rep["engine_warnings"] = v.get("warnings", [])[:60]
            rep["coverage"] = v.get("coverage")
            if v.get("errors"):
                rep["ok"] = False
        except ValueError:
            rep["engine_errors"] = [r.stdout[-2000:] + r.stderr[-2000:]]
            rep["ok"] = False
    rep["next"] = ("fix every error above (each says what to change), run again" if not rep.get("ok") else
                   "run: python tools/make.py projects/<slug> review   then look at review/sheet_*.jpg (playbook/05-review.md)")
    print(json.dumps(rep, ensure_ascii=False, indent=1))
    sys.exit(0 if rep.get("ok") else 1)


if __name__ == "__main__":
    main()
