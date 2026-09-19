---
description: Pravidla pro tvorbu UI (šablony, statická JS/CSS, web routes, překlady)
---

# Pravidla pro UI

Načte se, když Claude sáhne na šablonu, statický soubor nebo `routes_*.py`.
Cíl: neřešit dokola stejné chyby. Souvisí s ADR-0003 (server-rendered + htmx),
ADR-0013 (žádná i18n vrstva — web je trvale jen český).


## 1. Tabulky

- **Řaditelné sloupce = sdílená komponenta, ne vlastní `<select>`:**
  - server-side řazení (přes routu, stránkované): makro
    `_sorting.html::sort_header(label, key, sort, dir, base)` — ukazuje
    ↑/↓ u aktivního sloupce. `base` je `"?…"` s ostatními filtry, aby šlo
    připojit `&sort=…&dir=…`.
- Čísla zarovnávej doprava (`text-end`); kde se číslice řadí pod sebe

## 2. České řazení

- Filesystem / seznamy v paměti: `dataset.service.czech_sort_key`
  (case-insensitive, česká abeceda: `č` za `c`, `ch` mezi `h` a `i`,
  diakritika vokálů splývá se základem).
- DB dotazy: `db/sorting.py::icu_collation(session, locale)`.
- Nikdy `sorted()` bez klíče na text, který uvidí uživatel.

## 3. Destruktivní / měnící akce (PRG)

- Vždy `POST`, nikdy mutace na `GET`.
- CSRF: appka má globálně zapnutý Flask-WTF `CSRFProtect` (`factory.py`). Formulář
  postavený přes `FlaskForm` má token automaticky; ručně psaný formulář (mimo
  `FlaskForm`) potřebuje `{{ csrf_token() }}` jako skryté pole.
- `confirm()` před smazáním / přesunem / zahozením.
- Po akci `redirect(url_for(..., flash="klic"), code=303)` zpět s flash parametrem
  v URL; routa si whitelistuje povolené klíče, šablona vykreslí lokalizovaný `alert`.
  Žádný stav v session jen kvůli flash — nepoužívat vestavěné `flask.flash()`.
