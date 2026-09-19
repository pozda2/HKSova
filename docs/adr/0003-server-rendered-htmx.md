# ADR-0003 — Server-rendered + htmx

- **Status:** Přijato
- **Datum:** 2026-09-19 (retroaktivní záznam — `.claude/rules/ui.md` se na toto
  rozhodnutí odkazovalo už dřív, ADR ale chyběl)
- **Souvisí s:** US-PUBLIC-07, US-ORG-05 (řaditelné/filtrovatelné tabulky),
  NFR-PERFORMANCE-03 (průběžné dotahování stavu)

## Kontext

Současná aplikace je server-rendered Jinja + jQuery + Bootstrap (bootstrap-table,
bootstrap-editable), bez htmx nebo jiné AJAX vrstvy. Redesign přidává nové interaktivní
potřeby: řaditelné a filtrovatelné tabulky napříč veřejnými i administračními stránkami,
průběžné dotahování stavu dlouhých operací (hromadné emaily, ADR-0002), formuláře
s validací bez plného reloadu. Otázka je, jestli přejít na SPA (React/Vue) s JSON API,
nebo zůstat server-rendered a interaktivitu jen doplnit.

## Zvažované varianty

1. **Plný přechod na SPA + REST/JSON API** — maximální interaktivita, ale kompletní
   přepis frontendu, dvojitá údržba stavu (klient i server), rozsah výrazně přesahující
   zbytek redesignu.
2. **Čistě server-rendered, jen plné reloady** — nejmenší změna, ale UX pro průběžné
   dotahování stavu (emaily) a interaktivní tabulky by bez JS šel řešit jen ošklivě
   (meta-refresh apod.).
3. **Server-rendered + htmx** — šablony zůstávají server-rendered (Jinja), htmx přidává
   AJAX-like chování (částečné překreslení, polling, formuláře bez plného reloadu) bez
   nutnosti stavět samostatnou API vrstvu nebo SPA framework.

## Rozhodnutí

Varianta 3 — server-rendered + htmx. Odpovídá velikosti týmu (žádný samostatný frontend
tým) i rozsahu appky, zachovává jednoduchost Jinja šablon a zároveň umožní věci jako
polling stavu asynchronní úlohy (ADR-0002) nebo sdílenou komponentu pro řazení tabulek
(`_sorting.html::sort_header`, viz `.claude/rules/ui.md` § Tabulky) bez psaní vlastního JS.

## Důsledky

- htmx se přidá jako statická JS závislost (žádný build step, žádný nový balíček
  v `requirements.txt`).
- jQuery/Bootstrap zůstávají pro zbytek UI; htmx se zavádí postupně v novém kódu, ne
  jako plošný refaktor starých šablon.
- Endpointy, které htmx volá, vrací HTML fragmenty, ne JSON — žádná samostatná REST/JSON
  API vrstva se nebuduje.
- Destruktivní/měnící akce přes htmx musí dál dodržet PRG a CSRF pravidla
  (`.claude/rules/ui.md` § 3).
