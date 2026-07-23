# Інвентаризація сайту memory.org.ua

**Джерело:** `https://www.memory.org.ua/` (Webflow) · **Дата копії:** 2026-07-23
**Метод:** `sitemap.xml` віддавав 404, тож повний список зібрано **краулінгом** внутрішніх посилань (wget --mirror) + окремим проходом по об'єктах карти.

## Підсумок
- **Усього сторінок:** 60
- **Асетів:** 642 (~174 MB), усі з `cdn.prod.website-files.com`
- `archive.memory.org.ua` — окремий проєкт, **не чіпався** (посилання абсолютні).

| Тип сторінки | К-сть |
|---|---|
| Головна | 1 |
| `osnovni-statti/` (історичні періоди) | 13 |
| `dodatkovi-statti/` | 15 |
| `map/` (об'єкти на карті) | 12 |
| Колекція «Вінницька психіатрична лікарня» | 9 |
| Колекція «Табір для військовополонених» | 9 |
| `some-map` (карта) | 1 |
| **Разом** | **60** |

> **Приховані сторінки (не було в меню головної):** по 8 у кожній із 2 колекцій (знайдено краулінгом лендінгів колекцій) + **12 сторінок `map/…`**, посилання на які «зашиті» у JS-даних Leaflet-карти, а не в HTML-тегах — тому перший краул їх пропустив; додано окремим проходом.

## Повний список URL

| URL (шлях 1:1 зі старим сайтом) | Тип |
|---|---|
| `/` | головна |
| `/dodatkovi-statti/budenne-zhittya-selyan-1934-1935/` | dodatkovi-statti |
| `/dodatkovi-statti/finansova-zvitnist-za-2020-rik/` | dodatkovi-statti |
| `/dodatkovi-statti/istoria-z-archivu-sbu/` | dodatkovi-statti |
| `/dodatkovi-statti/istoriya-odniieyi-svitlini/` | dodatkovi-statti |
| `/dodatkovi-statti/oleksandr-kirilovich-holodkevich/` | dodatkovi-statti |
| `/dodatkovi-statti/pamyati-zhertv-golodomoriv/` | dodatkovi-statti |
| `/dodatkovi-statti/poridniti-mozhut-ne-lishe-rodinni-zvyazki/` | dodatkovi-statti |
| `/dodatkovi-statti/represivna-myasorubka-radyanskoyi-vladi/` | dodatkovi-statti |
| `/dodatkovi-statti/vladislav-borisovskiy/` | dodatkovi-statti |
| `/dodatkovi-statti/volodimir-ivanovich-barvinok/` | dodatkovi-statti |
| `/dodatkovi-statti/vyazen-mautgauzenu-ta-magadanu/` | dodatkovi-statti |
| `/dodatkovi-statti/yak-60-richniy-oficer-invalid/` | dodatkovi-statti |
| `/dodatkovi-statti/yak-graf-rzhevuskiy-ta-pomishchik-sobanskiy/` | dodatkovi-statti |
| `/dodatkovi-statti/yakiv-galchevskiy-orel/` | dodatkovi-statti |
| `/dodatkovi-statti/yuriy-slisaruk-uchasnik-studentskoyi-revolyuciyi-na-graniti/` | dodatkovi-statti |
| `/folder-vinnicka-psihiatrichna-likarnya/akciya-t4/` | колекція: психлікарня |
| `/folder-vinnicka-psihiatrichna-likarnya/golokost-i-vbivstva-ievreyskih-paciientiv-u-vinnickiy-psihiatrichniy-likarni/` | колекція: психлікарня |
| `/folder-vinnicka-psihiatrichna-likarnya/istoriya-vinnickoyi-psihiatrichnoyi-likarni/` | колекція: психлікарня |
| `/folder-vinnicka-psihiatrichna-likarnya/masovi-vbivstva-paciientiv-psihiatrichnih-zakladiv-na-teritoriyi-radyanskoyi-ukrayini/` | колекція: психлікарня |
| `/folder-vinnicka-psihiatrichna-likarnya/nashi-partneri-ta-vikonavci-proektu/` | колекція: психлікарня |
| `/folder-vinnicka-psihiatrichna-likarnya/pamyat-pro-vbitih-paciientiv-i-personal-vinnickoyi-psihiatrichnoyi-likarni/` | колекція: психлікарня |
| `/folder-vinnicka-psihiatrichna-likarnya/povoienni-sudi-nad-personalom-vinnickoyi-psihiatrichnoyi-likarni/` | колекція: психлікарня |
| `/folder-vinnicka-psihiatrichna-likarnya/vinnicka-psihiatrichna-likarnya/` | колекція: психлікарня |
| `/folder-vinnicka-psihiatrichna-likarnya/znishchennya-paciientiv-psihiatrichnoyi-likarni-1942-1944-rr/` | колекція: психлікарня |
| `/map/kalichanskiy-rinok/` | map (об’єкт на карті) |
| `/map/kraieznavchiy-muzey/` | map (об’єкт на карті) |
| `/map/kulikov-vasil/` | map (об’єкт на карті) |
| `/map/nataliya-borshchevska---bereginya-knizhkovoyi-spadshchini/` | map (об’єкт на карті) |
| `/map/nezabuti-tragediya-centralnogo-parku/` | map (об’єкт на карті) |
| `/map/nezlamniy-duh-borotbi-zhittya-prisvyachene-ukrayini/` | map (об’єкт на карті) |
| `/map/rodina-bochkovih-pravedniki-narodiv-svitu-z-vinnici/` | map (об’єкт на карті) |
| `/map/rodina-radan----pravedniki-narodiv-svitu-u-vinnici/` | map (об’єкт на карті) |
| `/map/vinnickiy-radiovuzol-mizh-kulturoyu-ta-propagandoyu/` | map (об’єкт на карті) |
| `/map/yan-miezhanovskiy-mizh-fotografiieyu-ta-okupaciieyu/` | map (об’єкт на карті) |
| `/map/zhinka-yaka-ne-zlamalasya-istoriya-lidiyi-postolovskoyi/` | map (об’єкт на карті) |
| `/map/zhittya-prisvyachene-pravdi-istoriya-lyudevita-yuraka/` | map (об’єкт на карті) |
| `/osnovni-statti/chervoniy-teror-v-1917-1939-rr/` | osnovni-statti |
| `/osnovni-statti/deportaciya/` | osnovni-statti |
| `/osnovni-statti/golodomor-1932-1933-rr/` | osnovni-statti |
| `/osnovni-statti/korisni-posilannya/` | osnovni-statti |
| `/osnovni-statti/rosiysko-ukrayinska-viyna/` | osnovni-statti |
| `/osnovni-statti/rozpad-radyanskogo-soyuzu-ta-nezalezhna-ukrayina/` | osnovni-statti |
| `/osnovni-statti/ruh-oporu-oun-upa/` | osnovni-statti |
| `/osnovni-statti/ukrayina-pid-chas-drugoyi-svitovoyi-viyni-1939-1945-rr/` | osnovni-statti |
| `/osnovni-statti/ukrayina-v-period-zagostrennya-krizi-radyanskoyi-sistemi/` | osnovni-statti |
| `/osnovni-statti/ukrayina-v-pershi-povoienni-roki/` | osnovni-statti |
| `/osnovni-statti/ukrayina-v-umovah-destalinizaciyi-1953-1964/` | osnovni-statti |
| `/osnovni-statti/ukrayinci-v-emigraciyi/` | osnovni-statti |
| `/osnovni-statti/ukrayinska-revolyuciya-ta-borotba-za-zberezhennya-derzhavnoyi-nezalezhnosti-ta-period-nepu/` | osnovni-statti |
| `/some-map/` | карта (Leaflet) |
| `/tabir-dlya-radyanskih-viyskovopolonenih-u-vinnici/golokost-i-radyanski-viyskovopoloneni/` | колекція: табір |
| `/tabir-dlya-radyanskih-viyskovopolonenih-u-vinnici/istoriya-taboru-dlya-radyanskih-viyskovopolonenih-u-vinnici/` | колекція: табір |
| `/tabir-dlya-radyanskih-viyskovopolonenih-u-vinnici/lyudski-doli-radyanskih-viyskovopolonenih/` | колекція: табір |
| `/tabir-dlya-radyanskih-viyskovopolonenih-u-vinnici/ohorona-vinnickogo-taboru-shtalagu-329/` | колекція: табір |
| `/tabir-dlya-radyanskih-viyskovopolonenih-u-vinnici/pamyat-pro-radyanskih-viyskovopolonenih-u-vinnici/` | колекція: табір |
| `/tabir-dlya-radyanskih-viyskovopolonenih-u-vinnici/tabir-dlya-radyanskih-viyskovopolonenih-u-vinnici/` | колекція: табір |
| `/tabir-dlya-radyanskih-viyskovopolonenih-u-vinnici/vikoristannya-praci-radyanskih-viyskovopolonenih-v-tretomu-rayhu-shtalag-326-vi-k-v-zenne/` | колекція: табір |
| `/tabir-dlya-radyanskih-viyskovopolonenih-u-vinnici/vinnickiy-tabir-dlya-nimeckih-viyskovopolonenih-no-253/` | колекція: табір |
| `/tabir-dlya-radyanskih-viyskovopolonenih-u-vinnici/zabuti-i-zradzheni-radyanski-viyskovopoloneni-pid-chas-ii-svitovoyi-viyni/` | колекція: табір |


## Аналіз сторінки `/some-map` (історична карта)

**Реалізація:** інтерактивна **Leaflet 1.9.4** (custom-code embed), не iframe стороннього сервісу і не Webflow-функція.
- **Leaflet** — з CDN `unpkg.com`; **тайли** (план Вінниці 1945) — з `https://gyborg.github.io/map/tiles/{z}/{x}/{y}.png` (окремий зовнішній проєкт на GitHub Pages, як `archive.*`).
- **12 маркерів** ведуть на сторінки `map/…` — тепер локальні, лінкуються відносно.

**Чи переживе перенос:** ТАК — від бекенду Webflow не залежить. Працюватиме, доки живі `unpkg.com` і `gyborg.github.io`.
**Ризик:** карта зав'язана на ці зовнішні сервіси; якщо стануть недоступні — не покаже тайли (сторінки `map/…` лишаться робочими). Локалізувати тайли недоцільно (окремий картографічний проєкт).
