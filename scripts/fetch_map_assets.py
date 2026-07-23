#!/usr/bin/env python3
"""
One-time (idempotent) download of the historical-map assets into site/static/,
so the map no longer depends on gyborg.github.io or unpkg.com.

  site/static/map-tiles/{z}/{x}/{y}.png   - tile pyramid (TMS)
  site/static/leaflet/leaflet.{js,css}    - Leaflet 1.9.4
  site/static/leaflet/images/*            - Leaflet marker/layer icons

site/static/ is in build.py's PRESERVE list, so rebuilds don't wipe it.
"""
import math, os, sys, urllib.request, concurrent.futures

SITE = os.path.expanduser('~/memory-org-ua/site')
STATIC = os.path.join(SITE, 'static')
TILE_SRC = 'https://gyborg.github.io/map/tiles/{z}/{x}/{y}.png'
LEAFLET = 'https://unpkg.com/leaflet@1.9.4/dist/'
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120 Safari/537.36'

# Map geometry, mirrored from the Leaflet init in some-map/index.html
W, H, MAXZ, MAXRES = 15942, 13303, 5, 2
MINRES = 2 ** MAXZ * MAXRES

LEAFLET_FILES = ['leaflet.js', 'leaflet.css',
                 'images/marker-icon.png', 'images/marker-icon-2x.png',
                 'images/marker-shadow.png', 'images/layers.png',
                 'images/layers-2x.png']


def fetch(url, dest):
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        return 'skip', 0
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    req = urllib.request.Request(url, headers={'User-Agent': UA})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            data = r.read()
    except Exception as e:
        return f'FAIL {getattr(e, "code", e)}', 0
    with open(dest, 'wb') as f:
        f.write(data)
    return 'ok', len(data)


def main():
    jobs = []
    for z in range(MAXZ + 1):
        s = 2 ** z / MINRES
        cols, rows = math.ceil(W * s / 256), math.ceil(H * s / 256)
        for x in range(cols):
            for y in range(rows):
                jobs.append((TILE_SRC.format(z=z, x=x, y=y),
                             os.path.join(STATIC, 'map-tiles', str(z), str(x), f'{y}.png')))
    for f in LEAFLET_FILES:
        jobs.append((LEAFLET + f, os.path.join(STATIC, 'leaflet', f)))

    print(f'{len(jobs)} files to fetch (existing are skipped)...')
    ok = skip = 0
    fails = []
    total = 0
    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as ex:
        futs = {ex.submit(fetch, u, d): (u, d) for u, d in jobs}
        for i, fut in enumerate(concurrent.futures.as_completed(futs), 1):
            u, d = futs[fut]
            st, n = fut.result()
            total += n
            if st == 'ok':
                ok += 1
            elif st == 'skip':
                skip += 1
            else:
                fails.append((u, st))
            if i % 200 == 0:
                print(f'  {i}/{len(jobs)}...')
    print(f'downloaded={ok} skipped={skip} failed={len(fails)} bytes={total/1024/1024:.1f} MB')
    for u, st in fails[:20]:
        print('  FAIL', st, u)
    return 1 if fails else 0


if __name__ == '__main__':
    sys.exit(main())
