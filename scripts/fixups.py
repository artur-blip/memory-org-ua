#!/usr/bin/env python3
"""
Content fixups applied to the built site/ (run AFTER build.py):
  1. Restore real "Історичні періоди" names on the homepage grid (Webflow
     shipped template remnants: Keto / Low carb / Paleo / Clean Eating / ...).
  2. Wire the empty "Clean Eating" slot to its period page.
  3. Replace the dead "ДОДАТИ ІСТОРІЮ" placeholder (href="#") with a mailto.
  4. Write a custom 404.html.
  5. Write CNAME (www.memory.org.ua).
"""
import os, re, glob, urllib.parse

SITE = os.path.expanduser('~/memory-org-ua/site')
CONTACT_EMAIL = 'avtomaydanvin@gmail.com'
DOMAIN = 'www.memory.org.ua'

# slug -> authoritative period name (from the site footer; deportaciya from its own <title>)
PERIODS = {
 'ukrayinska-revolyuciya-ta-borotba-za-zberezhennya-derzhavnoyi-nezalezhnosti-ta-period-nepu':
     'Українська революція та боротьба за збереження державної незалежності (1917-1921 рр.)',
 'deportaciya': 'Депортація',
 'golodomor-1932-1933-rr': 'Голодомор (1932-1933 рр.)',
 'chervoniy-teror-v-1917-1939-rr': 'Червоний терор в 1917-1939 рр.',
 'ukrayina-pid-chas-drugoyi-svitovoyi-viyni-1939-1945-rr': 'Україна під час Другої світової війни (1939-1945 рр.)',
 'ukrayina-v-pershi-povoienni-roki': 'Україна в перші повоєнні роки (1945 — на початку 1950-х рр.)',
 'ruh-oporu-oun-upa': 'Рух опору (ОУН, УПА)',
 'ukrayina-v-umovah-destalinizaciyi-1953-1964': 'Україна в умовах десталінізації (1953-1964 рр.)',
 'ukrayinci-v-emigraciyi': 'Українці в еміграції',
 'ukrayina-v-period-zagostrennya-krizi-radyanskoyi-sistemi': 'Україна в період загострення кризи радянської системи (1965-1985 рр.)',
 'rozpad-radyanskogo-soyuzu-ta-nezalezhna-ukrayina': 'Розпад Радянського Союзу та незалежна Україна (1985-1991 рр.)',
 'rosiysko-ukrayinska-viyna': 'Російсько-українська війна',
}
# The empty grid slot (href="#") belongs to the only period page not otherwise linked in the grid.
EMPTY_SLOT_TARGET = 'osnovni-statti/ukrayina-v-pershi-povoienni-roki/'

def fix_period_grid(t):
    def repl(m):
        pre_href, href, mid, title, post = m.groups()
        if href == '#':
            new_href = EMPTY_SLOT_TARGET
            slug = EMPTY_SLOT_TARGET.strip('/').split('/')[-1]
        else:
            new_href = href
            slug = href.strip('/').split('/')[-1]
        name = PERIODS.get(slug, title)
        return f'{pre_href}{new_href}{mid}{name}{post}'
    return re.sub(
        r'(<a\b[^>]*href=")([^"]*)("[^>]*class="one-menu[^"]*"[^>]*>.*?munu-item-title">)(.*?)(</div>)',
        repl, t, flags=re.S)

def fix_add_story_simple(t):
    mailto = 'mailto:' + CONTACT_EMAIL + '?subject=' + urllib.parse.quote('Додати історію — memory.org.ua')
    def repl(m):
        pre, href, mid, inner, post = m.groups()
        if 'ДОДАТИ' in inner.upper() and 'СТОР' in inner.upper() and href == '#':
            return f'{pre}{mailto}{mid}{inner}{post}'
        return m.group(0)
    return re.sub(r'(<a\b[^>]*href=")([^"]*)("[^>]*class="nav-link[^"]*"[^>]*>)(.*?)(</a>)',
                  repl, t, flags=re.S)

def write_404():
    html = '''<!DOCTYPE html>
<html lang="uk">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Сторінку не знайдено — Архів пам'яті українців</title>
<meta name="robots" content="noindex">
<link href="https://fonts.googleapis.com" rel="preconnect">
<link href="https://fonts.gstatic.com" rel="preconnect" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Raleway:wght@300;500;700;800&display=swap" rel="stylesheet">
<style>
  html,body{margin:0;height:100%}
  body{background:#000;color:#f9f9f9;font-family:'Raleway',sans-serif;
       display:flex;align-items:center;justify-content:center;text-align:center;padding:24px}
  .wrap{max-width:640px}
  .code{font-size:96px;font-weight:800;line-height:1;color:#eb5757;margin:0}
  h1{font-size:26px;font-weight:700;margin:16px 0 8px}
  p{font-size:17px;font-weight:300;color:#cfcfcf;margin:0 0 28px}
  .btn{display:inline-block;padding:13px 26px;border:1px solid #eb5757;border-radius:6px;
       color:#f9f9f9;text-decoration:none;font-weight:500;letter-spacing:.02em;transition:.2s}
  .btn:hover{background:#eb5757}
  .links{margin-top:22px;font-size:14px}
  .links a{color:#9aa4b2;text-decoration:none;margin:0 10px}
  .links a:hover{color:#f9f9f9}
</style>
</head>
<body>
  <div class="wrap">
    <p class="code">404</p>
    <h1>Такої сторінки немає</h1>
    <p>Можливо, адресу введено з помилкою або сторінку було переміщено.</p>
    <a class="btn" href="/">На головну</a>
    <div class="links">
      <a href="/osnovni-statti/golodomor-1932-1933-rr/">Основні статті</a>
      <a href="/some-map/">Історична карта</a>
      <a href="https://archive.memory.org.ua/">Архів</a>
    </div>
  </div>
</body>
</html>
'''
    open(os.path.join(SITE, '404.html'), 'w', encoding='utf-8').write(html)

def main():
    # 1-3: homepage grid + add-story button (grid only on index; button on all pages)
    idx = os.path.join(SITE, 'index.html')
    t = open(idx, encoding='utf-8').read()
    t = fix_period_grid(t)
    t = fix_add_story_simple(t)
    open(idx, 'w', encoding='utf-8').write(t)

    changed = 0
    for f in glob.glob(os.path.join(SITE, '**', 'index.html'), recursive=True):
        if os.path.abspath(f) == os.path.abspath(idx):
            continue
        tt = open(f, encoding='utf-8').read()
        new = fix_add_story_simple(tt)
        if new != tt:
            open(f, 'w', encoding='utf-8').write(new); changed += 1
    print(f'add-story mailto applied to homepage + {changed} other pages')

    write_404()
    print('wrote 404.html')

    open(os.path.join(SITE, 'CNAME'), 'w').write(DOMAIN + '\n')
    print('wrote CNAME:', DOMAIN)

if __name__ == '__main__':
    main()
