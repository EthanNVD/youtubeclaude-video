"""python projects/ww1-turning-point/plan_src/build.py  ->  projects/ww1-turning-point/plan.json"""
import importlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import lib  # noqa: E402

PARTS = [p for p in ("part1", "part2", "part3", "part4") if os.path.exists(os.path.join(HERE, p + ".py"))]
for p in PARTS:
    importlib.import_module(p).build()

CAST = {n: {"preset": n} for n in [
    "host", "aide", "kaiser_wilhelm", "hindenburg", "ludendorff", "moltke", "schlieffen", "kluck", "falkenhayn", "scheer", "holtzendorff",
    "zimmermann", "bauer", "joffre", "lanrezac", "gallieni", "foch", "jellicoe", "brusilov", "wilson", "lenin", "monash", "currie",
    "ww1_german_1914", "ww1_german", "ww1_french_1914", "ww1_french", "ww1_british", "ww1_american", "ww1_russian", "ww1_austrian",
    "ww1_australian", "ww1_sailor_uk", "ww1_sailor_de", "civilian_man", "civilian_woman", "worker", "reporter",
]}
CAST["ww1_canadian"] = {"preset": "ww1_british", "facial": "none", "color": "#857a50"}
CAST["congressman"] = {"preset": "civilian_man", "outfit": "suit", "color": "#3b3a3f", "age": 0.6}
CAST["clerk_de"] = {"preset": "ww1_german", "hat": "peaked", "hatColor": "#6e7066", "glasses": "round"}

META = {"title": "What Was The REAL Turning Point of WW1?", "lang": "en", "fps": 24, "duration": lib.END, "voice": "input/voice.wav", "grain": 0.5}
lib.finish(META, CAST, os.path.join(HERE, "..", "plan.json"))
