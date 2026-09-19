# 40 — Architektura

> Vlastník: organizátoři sovy • Stav: draft • Poslední revize: 2026-09-19
> Vychází z nefunkčních požadavků (`docs/20-requirements.md`).
> Zásadní rozhodnutí se tu jen shrnují — odůvodnění je v ADR (`docs/adr/`).

## Přehled

Server-rendered webová aplikace v Pythonu (Flask), běžící v Dockeru za nginx, s daty
v MariaDB. Vrstva modelů je plně na Flask-SQLAlchemy (žádné syrové SQL). Redesign na
tomto základu staví a doplňuje čtyři věci, každá se zásadním zdůvodněním v ADR:

- databázové migrace přes Flask-Migrate/Alembic místo ručních SQL dumpů (ADR-0001),
- asynchronní úlohy (hromadné emaily) přes RQ + Redis (ADR-0002),
- interaktivitu na frontendu přes htmx nad stále server-rendered Jinja šablonami (ADR-0003),
- vědomě žádnou i18n vrstvu — web je a zůstane jen český (ADR-0013).

Navíc je v diskuzi (viz níže a ADR-0004, status Návrh) refaktor routování podle ročníku,
který by odstranil potřebu restartu appky při založení nového ročníku.

## Kontext (C4 – úroveň 1)

**Uživatelé:** Návštěvník webu (PUBLIC), Tým/Náhradník (TEAM/SPARE/TEAM_PAID),
Organizátor (ORG) — role viz `10-user-stories.md` § Role.

**Externí systémy:**
- **Statek** — externí aplikace zpracovávající průběh hry, výsledky, nápovědy a řešení
  během hry; tým se hlásí přes maskota (US-ORG-17, US-PUBLIC-10). Výsledky se po hře
  synchronizují zpět do interní databáze.
- **seslost.cz** — doména pro krátké QR odkazy na šifry (`https://seslost.cz/l/<kód>`,
  US-ORG-04). Zcela externí služba, mimo tento repozitář — zdrojové kódy k ní nemáme.
  Rozhraní (jak přesně `<kód>` mapovat na cílovou šifru/stanoviště) se doladí až při
  implementaci US-ORG-04.
- **SMTP server** — odchozí pošta (reset hesla, hromadné a zvací emaily); dnes Gmail
  nebo jiný SMTP dle nastavení ročníku (`email-smtp-*` v `settings`).
- **mapy.com** — ruční zdroj GPS souřadnic při zadávání stanovišť (US-ORG-03), není
  programová integrace.

Návštěvník/Tým/Organizátor přistupují do appky přes prohlížeč (HTTPS). Appka čte/zapisuje
do MariaDB, odesílá poštu přes SMTP, po hře čte výsledky ze Statku a generuje QR kódy
směřující na seslost.cz.

## Komponenty (C4 – úroveň 2)

| Komponenta | Technologie | Role |
|---|---|---|
| `nginx` | trafex/php-nginx | TLS terminace, reverse proxy na `website` (uwsgi_params), statický servis `/foto`, samostatný vhost na port 44443 pro `adminer` |
| `website` | Flask + uwsgi (4 procesy, `enable-threads`) | Aplikační vrstva — blueprinty `main`/`team`/`forum`/`admin`, registrované vícekrát podle ročníku (viz Klíčové toky) |
| `worker` *(nové, ADR-0002)* | RQ worker | Zpracování asynchronních úloh (hromadné emaily) |
| `redis` *(nové, ADR-0002)* | Redis | Fronta úloh + stav jobů pro `worker`/`website` |
| `database` | MariaDB | Perzistentní úložiště, schéma spravované přes Flask-Migrate (ADR-0001) |
| `adminer` | Adminer | Ruční správa DB (vývoj/ladění), zpřístupněný přes samostatný nginx vhost |

Modulová struktura appky uvnitř `website` (`hksova/<modul>/`): `admin`, `forum`, `menu`,
`page`, `place`, `puzzle`, `settings`, `team`, `year` — moduly s routami mají
`controller.py` + `model.py` + `form.py` (a někdy `utils.py`), moduly `menu`/`place`/
`puzzle`/`settings`/`year` jsou jen modely konzumované ostatními.

## Datový model (hrubě)

Entity odpovídající modulům/tabulkám (`db.Model` třídy, vazby přes cizí klíče):

- `year` — ročník a jeho parametry (viz `20-requirements.md` FR-ROCNIK-01).
- `team`, `player` — tým a jeho hráči.
- `place`, `puzzle` — stanoviště (`place`) a šifra (`puzzle`), `puzzle` má FK na `year`
  i `place`; `place` má SQLAlchemy relationship na `Puzzle`.
- `forum`, `forum_section` — příspěvky a sekce fóra.
- `page` — statické stránky (obsah v MD).
- `menu` — položky menu, unikátní na ročník.
- `mascot` — seznam maskotů.
- `setting` — klíč/hodnota nastavení, per-ročník i globální (viz `NFR` vs `FR-NASTAVENI-01`).

Přesné sloupce a vazby (PK/FK, datové typy) patří do budoucí migrace (ADR-0001), ne
do prózy tady — zdroj pravdy pro aktuální stav je `database/database.sql` do doby,
než ho nahradí verzovaná historie migrací.

## Klíčové toky

### Směrování podle ročníku

`factory.py` neřeší aktuální ročník jako parametr requestu uvnitř jedné sady rout.
Místo toho **registruje stejné blueprinty vícekrát** — jednou bez prefixu pro aktuální
ročník, a pak znovu s prefixem `/<rok>` pro každý existující ročník i pro rok následující
(`main<rok>`, `team<rok>`, `forum<rok>`, `admin<rok>`). Archivní ročník (`US-PUBLIC-03`)
je tak vlastně jiná instance téhož blueprintu na jiné URL, ne runtime přepínač. To je
potřeba mít na paměti při každé změně routování — přidání routy platí pro všechny
registrace najednou, ale chování uvnitř ní se často větví podle toho, jestli jde
o aktuální nebo archivní ročník.

Autor (jeden z programátorů) tenhle vzor sám označuje za provizorní pokus, který je
v některých situacích neohrabaný — typicky založení nového ročníku dnes vyžaduje
restart appky, protože URL mapa se pro daný ročník nezaregistruje za běhu. Padl návrh
přejít na rok jako URL parametr místo N kopií blueprintu (viz `docs/adr/0004-rocnik-jako-url-parametr.md`,
**status Návrh** — čeká na shodu s druhým programátorem, není zatím závazné).

### Registrace týmu

Návštěvník → `POST /register` (`team.controller`) → validace formuláře (Flask-WTF) →
kontrola kapacity `max-teams` → zápis přes SQLAlchemy (`Team`, `Player`) → přiřazení
náhodného maskota → heslo hashováno (argon2/passlib) → podle kapacity role TEAM/SPARE
(`FR-TYM-01`).

### Asynchronní hromadný email (nově, ADR-0002)

Organizátor spustí rozeslání → `admin.controller` naplní RQ frontu (`redis`) jedním
jobem na email → vrátí se ihned s `job_id`, request se neblokuje → `worker` zpracovává
frontu, pro každý email loguje úspěch/neúspěch (`NFR-RELIABILITY-01`) → stránka pomocí
htmx pollingu (ADR-0003) dotahuje průběh/stav jobu z Redisu (`NFR-PERFORMANCE-03`).

### Přihlášení — rizikové místo výkonu

`FR-AUTH-01` — v minulé verzi bylo přihlašování opakovaně pomalé (viz `NFR-PERFORMANCE-02`).
Při implementaci nové verze je potřeba ověřit, kde přesně čas mizí (SMTP timeout u
navazujících operací, DB dotazy bez indexu, hashování hesla) a scénář `SC-PERFORMANCE-02`
zahrnout do zátěžového/manuálního testování jako prioritní.

