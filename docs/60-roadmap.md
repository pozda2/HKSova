# 60 — Implementační roadmapa

> Vlastník: organizátoři sovy • Stav: draft • Poslední revize: 2026-09-19
> Navazuje: `20-requirements.md`, `30-scenarios.md`, `40-architecture.md`, `50-tech-stack.md`, `docs/adr/`

Implementace postupuje po jednotlivých funkčních blocích, aby šlo chování aplikace
průběžně testovat, upřesňovat a ladit — ne jako jeden velký přepis najednou. Tři fáze
níže se realisticky prolínají po modulech, nečeká se, až je předchozí fáze hotová
úplně celá.

## Fáze 0 — Základ, než se sáhne na existující kód

Cíl: mít záchrannou síť a nástroje dřív, než začnou úpravy stávajícího kódu.

1. **Testy na existující chování.** Založit `tests/` (pytest + testcontainers dle
   `CLAUDE.md`), fixture pro Flask app + testcontainers MariaDB. První testy nepíšou
   proti user stories, ale proti **současnému** chování už napsaných modulů (`team`,
   `forum`, `menu`, `page`, `place`, `puzzle`, `settings`, `year`, `admin`) — bez toho
   nejde poznat, jestli další krok něco nerozbil.
2. **Alembic / Flask-Migrate** (ADR-0001). Baseline migrace z dnešního
   `database/database.sql`, zapojit `flask db upgrade` do startu kontejneru. Udělat
   dřív, než se začnou měnit modely — jinak se změny schématu blbě sledují zpětně.
3. **Pinování verzí** (`requirements.txt`, `python:3-slim` → konkrétní minor verze)
   a **základní lint/format** nástroj — ať CI/testy běží na reprodukovatelném
   prostředí od začátku (viz `50-tech-stack.md` § Konvence a nástroje kvality).
4. **Rozhodnout ADR-0004** (routing podle ročníku) s druhým programátorem. Blokující
   pro fázi 1 — pokud se přijme, dělá se *při* revizi jednotlivých modulů ve fázi 1,
   ne jako samostatný zásah navíc. Pokud se zamítne, revize modulů se bez něj obejde.

## Fáze 1 — Revize existujících bloků proti user stories

Nejdelší fáze, po funkčních oblastech (`20-requirements.md` § Oblasti), v pořadí podle
životního cyklu ročníku (`00-vision.md` § Fáze ročníku), ne abecedně:

1. **ROCNIK + NASTAVENI** — `year`/`settings` modely jsou základ, na kterém stojí
   všechno ostatní. Ověřit proti `FR-ROCNIK-01/02/03`, `FR-NASTAVENI-01`. Sem spadá
   i rozdělení nastavení ročníku vs. globálního nastavení (`US-ORG-02`).
2. **STANOVISTE + SIFRY** (`place`, `puzzle`) — nověji rozjetá funkcionalita
   (`2025_statek-puzzle-model.sql`), pravděpodobně nejblíž cílovému stavu; ověřit
   hlavně kategorie/pytlík (`FR-STANOVISTE-01/02`).
3. **TYM** — nejrizikovější blok: registrace, role TEAM/SPARE/TEAM_PAID a přechody
   mezi nimi (`FR-TYM-01` až `09`). Čekáme tu nejvíc rozdílů mezi napsaným a stories
   (pravidla o kapacitě, captcha, retenční politika telefonů — `NFR-LEGAL-02`).
4. **FORUM** — `FR-FORUM-01` až `04`, včetně automatického vzniku sekce se šifrou.
5. **STRANKA + MENU** — `page`, `menu`; menu je specifické (generování podle
   fáze/role, `FR-MENU-01`), zaslouží samostatnou pozornost.
6. **MASKOT, OBALKY, EXPORT** — menší, izolované bloky, na konci fáze 1.

U každého bloku: přečíst modul → porovnat s příslušnými `US-*`/`FR-*` → kde se to
rozchází, napsat/doplnit test (padající → oprava, TDD dle `CLAUDE.md`) → pokud se do
modulu promítá ADR-0004, udělat routing refaktor rovnou při té revizi, ne znovu později.

## Fáze 2 — Nová funkcionalita od nuly

Až je hotová fáze 1 (nebo aspoň blok, na kterém nová věc staví):

1. **RQ + Redis infrastruktura** (ADR-0002) — nová `worker`/`redis` služba
   v `docker-compose.yml`.
2. **FR-EMAIL-01/02** — skutečné odesílání (dnes je to jen generátor BCC seznamu, ne
   odesílač) + `NFR-RELIABILITY-01` / `NFR-PERFORMANCE-03`.
3. **htmx** (ADR-0003) — zavádět postupně tam, kde dává smysl (polling stavu emailu,
   řazení tabulek); přirozeně naváže na bod 2.
4. **FR-VYSLEDKY-01/02, FR-STATEK-01** — synchronizace výsledků ze Statku, reportáže.
   Z velké části nová práce, ne úprava stávajícího.
5. **NFR-LEGAL-02** — mazání telefonů při založení ročníku. Navazuje na `FR-ROCNIK-03`,
   který se řeší už ve fázi 1 — reálně může přibýt rovnou tam, místo čekání na fázi 2.

Hranice fáze 1 vs. 2 nebude vždy čistá — některé nové kousky logiky (jako bod 5) se
přirozeně nabalí na modul, který se zrovna reviduje ve fázi 1.
