# ADR-0004 — Routování podle ročníku bez blueprintů na ročník

- **Status:** Návrh — čeká na diskuzi s druhým programátorem, není zatím závazné
- **Datum:** 2026-09-19
- **Souvisí s:** FR-ROCNIK-03, US-ORG-18, NFR-PERFORMANCE-02 (rychlost startu appky)

## Kontext

Dnešní implementace (`factory.py:54-73`) registruje pro každý existující ročník
samostatnou instanci blueprintů `main`/`team`/`forum`/`admin` s číselným `url_prefix`
(`main2024`, `team2024`, ...), plus jednu bezprefixovou pro aktuální rok a jednu
předregistrovanou pro rok následující. Rok se ve view funkcích zjišťuje zpětně
regexem z `request.blueprint` (`year/model.py:40-64`).

Problém: Werkzeug URL mapa se staví jednou při vytvoření Flask app a s `lazy-apps=true`
(`configs/uwsgi/docker_wsgi.ini`) se navíc staví znovu v každém ze 4 uwsgi workerů
zvlášť (app se po forku nesdílí). Nový ročník založený za běhu (`FR-ROCNIK-03`) proto
nedostane vlastní URL prefix, dokud appka nerestartuje — obchází se to jen
předregistrací "příštího roku", což řeší jen sekvenční případ, ne obecný problém.
Zároveň roste náklad na start appky lineárně s počtem ročníků (dnes ~20 × 4 blueprinty
× 4 uwsgi procesy).

## Zvažované varianty

1. **Zachovat současný stav** (blueprint na ročník) — bez zásahu do kódu, ale založení
   nového ročníku dál vyžaduje restart appky a start appky dál zdražuje s každým dalším
   ročníkem.
2. **Runtime mutace URL mapy** (přidávání pravidel za běhu bez restartu) — technicky
   možné v jednom procesu, ale nesynchronizuje se to mezi 4 uwsgi workery bez vlastního
   signalizačního mechanismu (typicky by stejně skončilo jako automatizovaný restart/reload
   workerů) — nahrazuje problém automatizací, neřeší ho koncepčně.
3. **Rok jako URL parametr** (`/<int:year>/...`), resolvovaný centrálně přes
   `url_value_preprocessor` nebo `before_request` do `g.year`; bezprefixová URL
   (aktuální ročník) přesměruje na `/<aktuální_rok>/...`.

## Rozhodnutí

Navrhována varianta 3, ale se statusem **Návrh** — zásah je napříč všemi controllery
(`team`, `forum`, `admin`, `page`), dotkne se dekorátoru `current_year_required`
(`team/utils.py:27-35`) a všech míst, která dnes čtou `request.blueprint`. Než se
potvrdí jako závazné rozhodnutí, je potřeba to probrat s druhým programátorem
(dopad na rozdělanou práci, časový odhad refaktoru).

## Důsledky (pokud se varianta 3 přijme)

- Nový ročník se v UI projeví okamžitě po založení, bez restartu appky.
- Odpadá O(počet ročníků) registrace blueprintů při startu/reloadu (rychlejší start,
  zvlášť násobeno `lazy-apps` × 4 procesy).
- `request.blueprint` přestává nést informaci o roce — všude, kde se dnes volá
  `get_year(request.blueprint)`, je potřeba přepsat na čtení `g.year`/URL parametru.
- Mění se URL struktura (routy dostávají explicitní `<int:year>` segment) — sladit
  s redesignem, není cílem zachovat 1:1 kompatibilitu se starými URL.
