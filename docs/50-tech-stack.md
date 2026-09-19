# 50 — Technologický stack

> Vlastník: organizátoři sovy • Stav: draft • Poslední revize: 2026-09-19
> Souhrn zvolených technologií. Zdůvodnění je v ADR (`docs/adr/`).
> Verze podle `requirements.txt` (dnes nepinované — viz § Konvence a nástroje kvality).

## Přehled

| Vrstva | Technologie | Verze (orientačně) | ADR |
|--------|-------------|--------------------|-----|
| Jazyk | Python | `python:3-slim` (Dockerfile, nepinovaná minor verze) | — |
| Web framework | Flask | nepinováno | — |
| ORM | Flask-SQLAlchemy | nepinováno | — |
| DB driver | mysqlclient | nepinováno | — |
| Databáze | MariaDB | `mariadb:latest` (docker-compose) | — |
| Migrace schématu | Flask-Migrate (Alembic) | nová závislost | ADR-0001 |
| Fronta / asynchronní úlohy | RQ | nová závislost | ADR-0002 |
| Broker pro RQ | Redis | nová závislost | ADR-0002 |
| WSGI server | uwsgi | nepinováno (instaluje se zvlášť v `Dockerfile`, mimo `requirements.txt`) | — |
| Reverse proxy / TLS | nginx (`trafex/php-nginx` image) | dle image | — |
| Frontend — interaktivita | htmx | nová statická závislost (bez build kroku) | ADR-0003 |
| Frontend — existující | jQuery 3.6, Bootstrap (+ bootstrap-table, bootstrap-editable) | dle `hksova/static/js` | — |
| Šablony | Jinja2 (přes Flask) | nepinováno | — |
| Formuláře / CSRF | Flask-WTF | nepinováno | NFR-SECURITY-04 |
| Markdown editace | Flask-MDEditor + mistune | nepinováno | US-ORG-10 |
| QR kódy | flask-qrcode, qrcode | nepinováno | FR-SIFRY-01 |
| Hashování hesel | passlib (argon2) | nepinováno | NFR-SECURITY-01 |
| Validace emailu | email-validator | nepinováno | — |
| České řazení | czech-sort | nepinováno | NFR-USABILITY-03 |
| Stránkování | flask-paginate | nepinováno | NFR-PERFORMANCE-01 |
| Datum/čas | python-dateutil | nepinováno | — |
| HTTP klient | requests | nepinováno | FR-STATEK-01 (příprava dat pro Statek) |
| Kryptografie | cryptography | nepinováno | — |
| Admin DB nástroj (dev) | Adminer | `adminer:latest` | — |
| Kontejnerizace | Docker, Docker Compose | — | — |

**Poznámky:**
- `Pillow` je v `requirements.txt` zakomentovaný a v kódu se dnes nikde nepoužívá
  (žádný `import PIL`/`Image`). Než se implementuje vkládání loga do QR kódu
  (US-ORG-04 „Do středu QR kódu bude vložené logo hradecké sovy"), je potřeba ověřit,
  jestli to `qrcode` zvládne bez Pillow, nebo se závislost odkomentuje.
- Žádný balíček v `requirements.txt` nemá pinovanou verzi, stejně jako `python:3-slim`
  v `Dockerfile` nemá pinovanou minor verzi. TODO: rozhodnout před/během implementace
  přesné verze (např. `python:3.12-slim`, `Flask==3.x`), ať je build reprodukovatelný.

## Vývojové prostředí

- **Konfigurace dle prostředí:** `HKSOVA_CONFIG_DIR` (výchozí `configs/`) vybírá adresář,
  `default.py` se načte vždy, `HKSOVA_CONFIG` (cesta k souboru) se navrství přes
  `from_envvar` — v Dockeru ukazuje na `configs/docker.py` (z `configs/docker.py.sample`,
  gitignored, obsahuje produkční/lokální tajemství). Lokální vývoj bez Dockeru používá
  `configs/development.py` (`DEBUG=True`).
- **Spuštění bez Dockeru:** `run.py` (`flask_app.run("0.0.0.0")`) — jednoduchý dev server,
  bez uwsgi/nginx.
- **Spuštění v Dockeru:** `docker-compose.yml.sample` → zkopírovat na `docker-compose.yml`
  (spolu s `configs/docker.py.sample` → `configs/docker.py`). Služby: `database` (MariaDB),
  `website` (Flask+uwsgi), `adminer`, `nginx`; nově přibudou `redis` a `worker` (ADR-0002).
- **DB migrace (po zavedení ADR-0001):** `flask db upgrade` — potřeba zařadit do startovní
  sekvence kontejneru `website` (po `/wait`, před `uwsgi`), spustit jen jednou, ne z každého
  uwsgi workeru zvlášť.

## Konvence a nástroje kvality

- **Testy:** `CLAUDE.md` počítá s `tests/` (pytest + testcontainers), ale adresář ani
  žádná test konfigurace zatím v repu neexistuje — je potřeba založit od nuly jako
  součást redesignu (TODO).
- **Lint/formátování:** žádný nástroj (flake8/black/ruff/mypy apod.) zatím není v repu
  nakonfigurovaný. TODO: vybrat a zavést, než přibude víc nového kódu k psaní.
- **Kód anglicky, dokumentace česky, commit po logických celcích** — viz `CLAUDE.md`.

