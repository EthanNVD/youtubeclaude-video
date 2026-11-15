"""Download + simplify historical basemaps (aourednik/historical-basemaps, GPL-3.0).

Output: assets/maps/world_<year>.json  (GeoJSON, simplified, coords rounded)
Usage:  python tools/fetch_maps.py [year ...]
"""
import json, sys, urllib.request
from pathlib import Path
from shapely.geometry import shape, mapping, Polygon, MultiPolygon
from shapely.geometry.polygon import orient

BASE = "https://raw.githubusercontent.com/aourednik/historical-basemaps/master/geojson/world_{}.geojson"
DEFAULT = ("bc323 bc200 bc1 100 400 800 1100 1200 1279 1400 1492 1600 1700 1715 1783 "
           "1800 1815 1880 1914 1920 1938 1945 1960 1994 2010").split()
OUT = Path(__file__).resolve().parent.parent / "public" / "maps"


def rnd(c):
    if isinstance(c[0], (int, float)):
        return [round(c[0], 3), round(c[1], 3)]
    return [rnd(x) for x in c]


def main(years):
    OUT.mkdir(parents=True, exist_ok=True)
    for y in years:
        raw = json.loads(urllib.request.urlopen(BASE.format(y), timeout=60).read())
        feats = []
        for f in raw["features"]:
            if not f.get("geometry"):
                continue
            g = shape(f["geometry"]).simplify(0.02, preserve_topology=True)
            if g.is_empty:
                continue
            # d3-geo wants clockwise exterior rings (planar lon/lat), else the polygon covers the globe
            if isinstance(g, Polygon):
                g = orient(g, sign=-1.0)
            elif isinstance(g, MultiPolygon):
                g = MultiPolygon([orient(p, sign=-1.0) for p in g.geoms])
            else:
                continue
            m = mapping(g)
            p = f.get("properties") or {}
            feats.append({"type": "Feature",
                          "properties": {"name": p.get("NAME") or "", "subject": p.get("SUBJECTO") or "",
                                         "part": p.get("PARTOF") or ""},
                          "geometry": {"type": m["type"], "coordinates": rnd(m["coordinates"])}})
        path = OUT / f"world_{y}.json"
        path.write_text(json.dumps({"type": "FeatureCollection", "features": feats}, separators=(",", ":")))
        print(y, len(feats), path.stat().st_size // 1024, "KB")


if __name__ == "__main__":
    main(sys.argv[1:] or DEFAULT)
