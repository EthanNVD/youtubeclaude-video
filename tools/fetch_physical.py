"""Build public/maps/physical.json (rivers + lakes) from Natural Earth (public domain).

    python tools/fetch_physical.py <dir with ne_10m_rivers_lake_centerlines.geojson, ne_50m_lakes.geojson>

Keeps named rivers with scalerank <= 9 (10m set: includes Rhine/Waal/Maas, Don, Volga, Dnieper...),
rounds coordinates to 3 decimals and simplifies with shapely to keep the file small.
"""
import json
import sys
from pathlib import Path

from shapely.geometry import shape, mapping

ROOT = Path(__file__).resolve().parent.parent
src = Path(sys.argv[1])


def rnd(geom):
    def r(c):
        if isinstance(c[0], (int, float)):
            return [round(c[0], 3), round(c[1], 3)]
        return [r(x) for x in c]
    g = mapping(geom)
    return {"type": g["type"], "coordinates": r(g["coordinates"])}


feats = []
rivers = json.loads((src / "ne_10m_rivers_lake_centerlines.geojson").read_text(encoding="utf-8"))
for f in rivers["features"]:
    p = f["properties"]
    name = p.get("name_en") or p.get("name") or ""
    rank = p.get("scalerank", 10)
    if rank is None or rank > 9 or not f.get("geometry"):
        continue
    g = shape(f["geometry"]).simplify(0.01, preserve_topology=False)
    if g.is_empty:
        continue
    feats.append({"type": "Feature", "properties": {"k": "river", "name": name, "rank": rank}, "geometry": rnd(g)})
lakes = json.loads((src / "ne_50m_lakes.geojson").read_text(encoding="utf-8"))
for f in lakes["features"]:
    p = f["properties"]
    if not f.get("geometry"):
        continue
    g = shape(f["geometry"]).simplify(0.01)
    feats.append({"type": "Feature", "properties": {"k": "lake", "name": p.get("name_en") or p.get("name") or "", "rank": p.get("scalerank", 5)}, "geometry": rnd(g)})
out = ROOT / "public" / "maps" / "physical.json"
out.write_text(json.dumps({"type": "FeatureCollection", "features": feats}, separators=(",", ":")), encoding="utf-8")
print(out, len(feats), "features", round(out.stat().st_size / 1e6, 2), "MB")
