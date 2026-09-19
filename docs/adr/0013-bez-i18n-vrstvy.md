# ADR-0013 — Bez i18n vrstvy (čeština napevno)

- **Status:** Přijato
- **Datum:** 2026-09-19
- **Souvisí s:** NFR-USABILITY-01

## Kontext

Hradecká sova je česká hra, cílená výhradně na české publikum. `NFR-USABILITY-01`
požaduje, aby bylo UI v češtině. Otázka byla, jestli přesto zavést i18n vrstvu
(Flask-Babel + `.po` soubory) pro budoucí rozšiřitelnost na další jazyk, nebo texty
držet natvrdo v šablonách a kódu jako dosud.

## Zvažované varianty

1. **Žádná i18n vrstva** — čeština napevno v šablonách, flash zprávách a kódu
   (současný stav appky). Nejjednodušší, žádná nová závislost ani boilerplate.
2. **Flask-Babel + `.po` soubory** i bez plánu na druhý jazyk — přidává infrastrukturu
   a extra krok do vývoje (extrakce/kompilace `.po`) bez reálného důvodu.

## Rozhodnutí

Varianta 1 — žádná i18n vrstva. Web je a zůstane jednojazyčný (organizátor to potvrdil
explicitně), investice do i18n frameworku by byla čistě spekulativní příprava na
scénář, který je vyloučený.

## Důsledky

- Žádná nová závislost (Flask-Babel se nezavádí).
- Texty zůstávají přímo v šablonách a kódu; konzistenci formulací je potřeba hlídat
  ručně/code review, ne přes centrální `.po` soubor.
- `.claude/rules/ui.md` dřív zmiňoval spouštění pravidla při dotyku na `.po` soubor —
  to je teď needůvodněné, protože žádné `.po` soubory v projektu nevzniknou; odstraněno
  z pravidla společně s tímto ADR.
