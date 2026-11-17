"""Sides (armies) by era: who their soldiers are, their flag/nation key, tanks, planes, ships.

A card says `"side": "german"`; the film says `"era": "ww1"` (cards/_film.json). This table turns that into the right
uniform preset, nation colour, tank, aircraft and ship — so writers never pick uniforms or vehicles by hand.
Override per film in _film.json: "sides_override": {"german": {"soldier": "ss_soldier"}}.
"""
from __future__ import annotations

import re
from pathlib import Path

SRC = Path(__file__).resolve().parents[2] / "src"
PRESETS = set(re.findall(r"^\s{2}(\w+): \{", (SRC / "char/presets.ts").read_text(encoding="utf-8"), re.M))

ERAS = ("ww1", "ww2", "napoleonic", "ancient", "vietnam", "modern")

# era -> side -> fields
TABLE = {
    "ww1": {
        "german": dict(soldier="ww1_german", soldier_early="ww1_german_1914", officer="ww1_german@officer", nation="GERI", tank="markiv", plane="fighter", bomber="bomber", ship="battleship", sub="uboat", sailor="ww1_sailor_de"),
        "british": dict(soldier="ww1_british", officer="ww1_british@officer", nation="UK", tank="markiv", plane="fighter", bomber="bomber", ship="battleship", sub="submarine", sailor="ww1_sailor_uk"),
        "french": dict(soldier="ww1_french", soldier_early="ww1_french_1914", officer="ww1_french@officer", nation="FRA", tank="renault", plane="fighter", bomber="bomber", ship="battleship", sub="submarine", sailor="ww1_sailor_uk"),
        "american": dict(soldier="ww1_american", officer="ww1_american@officer", nation="USA", tank="renault", plane="fighter", bomber="bomber", ship="battleship", sub="submarine", sailor="american_sailor"),
        "russian": dict(soldier="ww1_russian", officer="ww1_russian@officer", nation="RUS", tank="markiv", plane="fighter", bomber="bomber", ship="battleship", sub="submarine", sailor="ww1_sailor_uk"),
        "austrian": dict(soldier="ww1_austrian", officer="ww1_austrian@officer", nation="AUS", tank="markiv", plane="fighter", bomber="bomber", ship="battleship", sub="uboat", sailor="ww1_sailor_de"),
        "australian": dict(soldier="ww1_australian", officer="ww1_australian@officer", nation="UK", tank="markiv", plane="fighter", bomber="bomber", ship="battleship", sub="submarine", sailor="ww1_sailor_uk"),
        "ottoman": dict(soldier="ww1_german@ottoman", officer="ww1_german@ottoman_officer", nation="OTT", tank="markiv", plane="fighter", bomber="bomber", ship="cruiser", sub="uboat", sailor="ww1_sailor_de"),
        "italian": dict(soldier="ww1_french@italian", officer="ww1_french@italian_officer", nation="ITA", tank="renault", plane="fighter", bomber="bomber", ship="battleship", sub="submarine", sailor="ww1_sailor_uk"),
    },
    "ww2": {
        "german": dict(soldier="german_soldier", officer="german_officer", nation="GER", tank="panzer4", tank_heavy="tiger", plane="fighter", bomber="bomber", ship="battleship", sub="uboat", sailor="ww1_sailor_de", pilot="german_pilot", tanker="german_tanker"),
        "british": dict(soldier="british_soldier", officer="british_soldier@officer", nation="UK", tank="sherman", plane="fighter", bomber="bomber", ship="battleship", sub="submarine", sailor="ww1_sailor_uk", pilot="raf_pilot", para="british_para"),
        "american": dict(soldier="american_soldier", officer="american_soldier@officer", nation="USA", tank="sherman", plane="fighter", bomber="bomber", ship="carrier", sub="submarine", sailor="american_sailor", pilot="american_pilot", para="us_para"),
        "soviet": dict(soldier="soviet_soldier", soldier_winter="soviet_winter", officer="soviet_officer", nation="USSR", tank="t34", plane="fighter", bomber="bomber", ship="cruiser", sub="submarine", sailor="ww1_sailor_uk"),
        "japanese": dict(soldier="japanese_soldier", officer="japanese_officer", nation="JPN", tank="tank", plane="fighter", bomber="divebomber", ship="carrier", sub="submarine", sailor="japanese_sailor", pilot="japanese_pilot"),
        "french": dict(soldier="french_soldier", officer="french_soldier@officer", nation="FRA", tank="tank", plane="fighter", bomber="bomber", ship="battleship", sub="submarine", sailor="ww1_sailor_uk"),
        "italian": dict(soldier="italian_soldier", officer="italian_soldier@officer", nation="ITA", tank="tank", plane="fighter", bomber="bomber", ship="battleship", sub="submarine", sailor="ww1_sailor_uk"),
        "polish": dict(soldier="polish_soldier", officer="polish_soldier@officer", nation="POL", tank="tank", plane="fighter", bomber="bomber", ship="destroyer", sub="submarine", sailor="ww1_sailor_uk", para="polish_para"),
        "finnish": dict(soldier="finnish_soldier", officer="finnish_soldier@officer", nation="FIN", tank="tank", plane="fighter", bomber="bomber", ship="destroyer", sub="submarine", sailor="ww1_sailor_uk"),
        "chinese": dict(soldier="japanese_soldier@chinese", officer="japanese_officer@chinese_officer", nation="CHN", tank="tank", plane="fighter", bomber="bomber", ship="cruiser", sub="submarine", sailor="ww1_sailor_uk"),
        "dutch": dict(soldier="british_soldier@dutch", officer="british_soldier@dutch_officer", nation="NED", tank="tank", plane="fighter", bomber="bomber", ship="destroyer", sub="submarine", sailor="ww1_sailor_uk"),
    },
    "napoleonic": {
        "french": dict(soldier="napoleon@line", officer="napoleon", nation="FRA", tank=None, plane=None, bomber=None, ship="cruiser", sub=None, sailor="ww1_sailor_uk"),
        "british": dict(soldier="wellington@redcoat", officer="wellington", nation="UK", tank=None, plane=None, bomber=None, ship="cruiser", sub=None, sailor="ww1_sailor_uk"),
        "russian": dict(soldier="kutuzov@line", officer="kutuzov", nation="RUS", tank=None, plane=None, bomber=None, ship="cruiser", sub=None, sailor="ww1_sailor_uk"),
    },
    "ancient": {
        "roman": dict(soldier="roman_legionary", officer="caesar", nation="SPQR", tank=None, plane=None, bomber=None, ship="boat", sub=None, sailor="roman_legionary"),
        "carthaginian": dict(soldier="roman_legionary@carthage", officer="hannibal", nation="CARTH", tank=None, plane=None, bomber=None, ship="boat", sub=None, sailor="roman_legionary@carthage"),
    },
    "vietnam": {
        "vietnamese": dict(soldier="vn_soldier", officer="vn_soldier@officer", nation="VN", tank="t34", plane="fighter", bomber="bomber", ship="cruiser", sub=None, sailor="vn_soldier"),
        "american": dict(soldier="american_soldier", officer="american_soldier@officer", nation="USA", tank="sherman", plane="fighter", bomber="bomber", ship="carrier", sub="submarine", sailor="american_sailor", pilot="american_pilot"),
        "french": dict(soldier="french_soldier", officer="french_soldier@officer", nation="FRA", tank="tank", plane="fighter", bomber="bomber", ship="cruiser", sub=None, sailor="ww1_sailor_uk"),
    },
}
TABLE["modern"] = TABLE["ww2"]

ALL_SIDES = sorted({s for era in TABLE.values() for s in era})

# derived looks: "<preset>@<variant>" -> a cast spec built on the preset (registered in the cast automatically)
DERIVED = {
    "officer": {"hat": "peaked", "glasses": None},
    "ottoman": {"hat": "kepi", "hatColor": "#a8322a", "color": "#8a7a52"},
    "ottoman_officer": {"hat": "kepi", "hatColor": "#a8322a", "color": "#7a6a48"},
    "italian": {"color": "#7d7f6a", "hatColor": "#6e705c"},
    "italian_officer": {"color": "#7d7f6a", "hat": "peaked", "hatColor": "#6e705c"},
    "chinese": {"color": "#5f6a52", "hatColor": "#5f6a52"},
    "chinese_officer": {"color": "#5f6a52", "hat": "peaked", "hatColor": "#5f6a52"},
    "dutch": {"color": "#6f7563", "hatColor": "#5d6353"},
    "dutch_officer": {"color": "#6f7563", "hat": "peaked", "hatColor": "#5d6353"},
    "line": {"color": "#2e4a8a"},
    "redcoat": {"color": "#b23a2e"},
    "carthage": {"color": "#8a5a3a"},
}

CIVILIANS = {"man": "civilian_man", "woman": "civilian_woman", "worker": "worker", "reporter": "reporter", "diplomat": "diplomat"}


class Side:
    def __init__(self, name, era, row):
        self.name, self.era = name, era
        for k, v in row.items():
            setattr(self, k, v)
        self.row = row

    def get(self, k, default=None):
        return self.row.get(k) or default


def side(name, era, film=None):
    era_t = TABLE.get(era) or TABLE["ww2"]
    row = era_t.get(name)
    if row is None:
        # fall back to any era that has this side
        row = next((t[name] for t in TABLE.values() if name in t), None)
    if row is None:
        raise KeyError(name)
    row = dict(row)
    over = ((film or {}).get("sides_override") or {}).get(name) or {}
    row.update(over)
    return Side(name, era, row)


def resolve_who(who: str, cast: dict) -> str:
    """'ww1_german@officer' -> registers a derived cast entry and returns its id; plain presets/cast ids pass through."""
    if "@" not in who:
        return who
    base, var = who.split("@", 1)
    cid = f"{base}__{var}"
    if cid not in cast:
        spec = {"preset": base}
        spec.update({k: v for k, v in DERIVED.get(var, {}).items() if v is not None})
        cast[cid] = spec
    return cid
