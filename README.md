# memory.org.ua — статична копія (Архів пам'яті українців)

Повністю автономна статична копія сайту **www.memory.org.ua**, перенесена з Webflow на GitHub Pages.

- **60 сторінок**, структура URL 1:1 зі старим сайтом (`шлях/index.html`).
- **Нуль залежностей від Webflow** — усі асети (зображення, CSS, JS, шрифти) локальні; jQuery локалізовано; Webflow-бейдж нейтралізовано.
- Кастомна `404.html`, `CNAME` = `www.memory.org.ua`.
- Історична карта self-hosted: 1117 тайлів + Leaflet у `static/` (оновити: `python3 scripts/fetch_map_assets.py`).

## Що зовнішнє (навмисно не локалізовано)

- `archive.memory.org.ua` — окремий проєкт (окремий сервер).
- Google Fonts (Raleway), Google Tag Manager (`GTM-WFQCCNH`).

## Документація

- [`docs/inventory.md`](docs/inventory.md) — інвентаризація + аналіз карти
- [`docs/qa-report.md`](docs/qa-report.md) — звіт локальної перевірки
- [`docs/migration-report.md`](docs/migration-report.md) — фінальний звіт + інструкція з DNS

## Відтворення збірки (за потреби)

Джерело — сирий `wget`-мірор (не в репозиторії). Скрипти в [`scripts/`](scripts/):

- `build.py` — дзеркалення структури + переписування всіх посилань на локальні (зберігає `docs/`, `scripts/`, `.git` при повторній збірці).
- `fixups.py` — назви історичних періодів, форма «Додати історію», локалізація карти, `404.html`, `CNAME`.
- `fetch_map_assets.py` — завантаження тайлів карти + Leaflet у `static/` (ідемпотентно).
