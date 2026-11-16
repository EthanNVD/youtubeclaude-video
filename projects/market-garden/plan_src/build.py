"""python projects/market-garden/plan_src/build.py  ->  projects/market-garden/plan.json"""
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from lib import finish  # noqa: E402
import part1  # noqa: E402
import part2  # noqa: E402
import part3  # noqa: E402

part1.build()
part2.build()
part3.build()

CAST = {name: {"preset": name} for name in [
    "host", "aide", "montgomery", "eisenhower", "brereton", "horrocks", "browning", "roy_urquhart", "brian_urquhart", "frost", "gavin",
    "lindquist", "julian_cook", "bedell_smith", "cunningham", "sosabowski", "model", "bittrich", "krafft", "grabner", "chill", "harmel_old",
    "lindemans", "pinto", "ernest_archer", "bernhard",
]}
CAST["shaef_officer"] = {"preset": "american_soldier", "hat": "none", "hair": "part", "glasses": "round", "age": 0.45}

META = {"title": "Why Operation Market Garden Was COMPLETELY Avoidable", "lang": "en", "fps": 24, "duration": 2044.72,
        "voice": "input/voice.wav", "grain": 0.5}
finish(META, CAST, os.path.join(os.path.dirname(__file__), "..", "plan.json"))
