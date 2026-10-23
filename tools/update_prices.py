#!/usr/bin/env python3
"""Apply freshly checked prices to index.html.

Usage:  python3 tools/update_prices.py prices.json [--date "1 Nov 2026"]

prices.json:
  {
    "aldi":       {"<aldi product slug>": 1.65, ...},          # slug = the part after aldi.co.uk/product/
    "sainsburys": {"Sainsbury's Passata|500g": 0.60, ...}      # "<product name>|<pack label>" as in P
  }

Only prices change. Products, names and pack sizes are left alone, and anything
not in prices.json keeps its current price. Prints a summary of what changed.
"""
import json, re, sys, datetime
from pathlib import Path

HTML = Path(__file__).resolve().parent.parent / 'index.html'

def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    prices = json.loads(Path(sys.argv[1]).read_text())
    aldi, sains = prices.get('aldi', {}), prices.get('sainsburys', {})
    date = sys.argv[sys.argv.index('--date') + 1] if '--date' in sys.argv else datetime.date.today().strftime('%-d %b %Y')
    s = HTML.read_text()
    changes, seen = [], set()

    def note(name, old, new):
        if abs(old - new) > 0.004:
            changes.append(f'{name}: £{old:.2f} → £{new:.2f}')

    # 1) Everyday catalogue: const CAT = [[name, brand, size, price, slug, aisle], ...];
    m = re.search(r'^const CAT = (\[.*\]);$', s, re.M)
    cat = json.loads(m.group(1))
    for row in cat:
        slug = row[4]
        if slug in aldi:
            seen.add(slug); note(f'{row[1]} {row[0]}', row[3], float(aldi[slug])); row[3] = round(float(aldi[slug]), 2)
    s = s[:m.start(1)] + json.dumps(cat, ensure_ascii=False, separators=(',', ':')) + s[m.end(1):]

    # 2) Recipe products: lines like  'Chicken breast': {s:'A', n:'…', packs:[[300,2.29,'300g','slug'],…], u:AL+'slug'},
    out = []
    for line in s.split('\n'):
        pm = re.match(r"\s*'[^']+':\s*\{s:'([AS])', n:(\"[^\"]*\"|'[^']*')", line)
        if pm and 'packs:[' in line:
            shop, name = pm.group(1), pm.group(2)[1:-1]
            u = re.search(r"u:AL\+'([^']+)'", line)
            packs = re.findall(r"\[(\d+(?:\.\d+)?),(\d+(?:\.\d+)?),'([^']*)'(?:,'([^']*)')?\]", line)
            for size, price, label, slug in packs:
                if shop == 'A':
                    slug = slug or (u.group(1) if u and len(packs) == 1 else '')
                    new = aldi.get(slug); seen.add(slug) if new is not None else None
                else:
                    new = sains.get(f'{name}|{label}')
                if new is None:
                    continue
                new = round(float(new), 2); note(f'{name} {label}', float(price), new)
                old_pack = f"[{size},{price},'{label}'"
                line = line.replace(old_pack, f"[{size},{new:.2f}".rstrip('0').rstrip('.') + f",'{label}'", 1)
        elif pm and 'perKg:' in line:
            u = re.search(r"u:AL\+'([^']+)'", line)
            if u and u.group(1) in aldi:
                old = float(re.search(r'perKg:([\d.]+)', line).group(1)); new = round(float(aldi[u.group(1)]), 2)
                seen.add(u.group(1)); note(pm.group(2)[1:-1] + ' per kg', old, new)
                line = re.sub(r'perKg:[\d.]+', f'perKg:{new}', line)
        out.append(line)
    s = '\n'.join(out)

    # 3) Date stamps
    s = re.sub(r"const PRICED = '[^']*';", f"const PRICED = '{date}';", s)
    s = re.sub(r'(// Aldi everyday range, prices checked )[^:]*:', rf'\g<1>{date}:', s)

    HTML.write_text(s)
    unknown = sorted(set(aldi) - seen)
    print(f'Prices dated {date}. {len(changes)} price change(s).')
    for c in changes: print('  ' + c)
    if unknown: print(f'{len(unknown)} Aldi slug(s) in prices.json not found in the app (ignored).')

if __name__ == '__main__':
    main()
