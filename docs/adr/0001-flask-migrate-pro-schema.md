# ADR-0001 — Flask-Migrate (Alembic) pro správu schématu databáze

- **Status:** Přijato
- **Datum:** 2026-09-19
- **Souvisí s:** NFR-COMPATIBILITY-01, FR-ROCNIK-01, FR-ROCNIK-03

## Kontext

Schéma databáze je dnes spravováno ručně přes SQL dumpy v `database/` (`database.sql`,
`2025_statek-puzzle-model.sql`), generované z Adminera a aplikované manuálně. Nejde tak
reprodukovat historii změn schématu, ani spolehlivě dostat dvě prostředí (dev/docker/prod)
do stejného stavu. Modelová vrstva už je plně na Flask-SQLAlchemy (`db.Model` ve všech
modulech), což je nutný předpoklad pro nástroj, který dokáže diffy generovat automaticky
z ORM modelů.

## Zvažované varianty

1. **Zůstat u ručních SQL dumpů** — žádná nová závislost, ale bez verzované historie
   schématu a s rizikem rozjetých prostředí.
2. **Alembic přímo** — plná kontrola nad migracemi, ale bez integrace na Flask konfiguraci a CLI.
3. **Flask-Migrate** (wrapper nad Alembicem, integrovaný s Flask-SQLAlchemy) — příkazy
   `flask db migrate` / `flask db upgrade`, autogenerace diffů z modelů, stejná konfigurace
   jako zbytek aplikace.

## Rozhodnutí

Flask-Migrate (varianta 3). Přímo staví na tom, co je v repu už zavedené (Flask-SQLAlchemy),
autogenerace snižuje riziko ručních chyb při psaní migrací a migrace lze verzovat v gitu
a spouštět jako součást startu kontejneru.

## Důsledky

- Nová závislost v `requirements.txt` (`Flask-Migrate`).
- `database/*.sql` dumpy přestávají být zdrojem pravdy — buď se zahodí, nebo se převedou
  na počáteční (baseline) migraci přes `flask db stamp`.
- Migrace je potřeba zařadit do startovní sekvence kontejneru (`/wait && flask db upgrade
  && uwsgi ...`); pozor na souběh více replik webu — migrace by měla běžet jen jednou,
  ne z každého uwsgi procesu/kontejneru zvlášť.
- Historické nekonzistence schématu mezi ročníky (NFR-COMPATIBILITY-01) se řeší jako
  běžná migrace dat, ne ad-hoc SQL skript.
