# ADR-0002 — RQ + Redis pro asynchronní úlohy

- **Status:** Přijato
- **Datum:** 2026-09-19
- **Souvisí s:** NFR-PERFORMANCE-03, NFR-RELIABILITY-01, FR-EMAIL-01, FR-EMAIL-02

## Kontext

Hromadné emaily dnes fakticky neexistují jako serverová funkce — `admin/controller.py`
jen připraví BCC seznam po 40 adresách pro ruční vložení do emailového klienta
organizátora. Nové požadavky (`FR-EMAIL-01`, `FR-EMAIL-02`, `NFR-PERFORMANCE-03`)
vyžadují skutečné asynchronní odesílání s průběžně dotahovaným stavem na stránce, bez
blokování requestu, s logováním neúspěšných adres (`NFR-RELIABILITY-01`). V repu dnes
není žádná fronta ani background-worker infrastruktura (žádný Celery/RQ/APScheduler/Redis),
odesílání jediného emailu (reset hesla) běží synchronně přes `smtplib`.

## Zvažované varianty

1. **Vlákno uvnitř uwsgi procesu** — bez nové infrastruktury, ale křehké: uwsgi běží
   víc procesů (`processes=4` v `docker_wsgi.ini`), stav vlákna nepřežije restart/reload
   a špatně se sdílí mezi requestem, co úlohu spustil, a requestem, co se ptá na stav.
2. **APScheduler v procesu** — podobné omezení jako vlákno, navíc riziko duplicitního
   spuštění při více procesech/replikách webu.
3. **Celery + Redis/RabbitMQ** — robustní a featurní (retry politiky, periodické úlohy,
   monitoring), ale provozně těžké (broker + worker + případně beat) vzhledem k rozsahu
   potřeby (hromadné emaily řádově párkrát za ročník).
4. **RQ (Redis Queue) + Redis** — jednoduchá fronta nad Redisem, lehká integrace s Flask,
   samostatný `rq worker` proces, stav úlohy dostupný přes Redis nezávisle na uwsgi
   procesu (přežije reload/restart webu).

## Rozhodnutí

RQ + Redis (varianta 4). Poměr jednoduchosti k robustnosti nejlépe sedí na velikost
provozu — self-hosted server, jednotky hromadných úloh za ročník, ne kontinuální zátěž.
Redis navíc může posloužit i jinde (cache, rate-limiting), pokud bude potřeba později.

## Důsledky

- Nové služby v `docker-compose.yml`: `redis` a `worker` (spouští `rq worker`).
- Nové závislosti: `rq`, `redis`.
- Endpoint pro spuštění hromadného emailu vrátí ihned `job_id`; stránka jej pollingem
  (htmx, viz ADR-0003) dotazuje na stav/průběh — naplňuje `NFR-PERFORMANCE-03`.
- Je potřeba řešit restart/monitoring worker procesu (uwsgi dnes řeší start skrz `/wait`,
  worker potřebuje vlastní healthcheck/restart politiku v `docker-compose.yml`).
- Neúspěšné odeslání jednotlivého emailu (`NFR-RELIABILITY-01`) se zaloguje jako výsledek
  konkrétního jobu, nezastaví celou frontu.
