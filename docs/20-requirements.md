# 20 — Požadavky

> Vlastník: organizátoři • Stav: draft • Poslední revize: 2026-09-19
>

> Funkční (FR) = co systém dělá. Nefunkční (NFR) = jak dobře to dělá.
> ID: `FR-<OBLAST>-xx` / `NFR-<KATEGORIE>-xx`, číslování nezávislé v rámci oblasti.
> **ID se po vytvoření nemění ani nepřečísluje** (stejné pravidlo jako u US). Zaniklé ID (sloučení/přeřazení) zůstává neobsazené.
> Každý FR: priorita (MoSCoW), zdrojová US (nebo `Zdroj:` u požadavků bez jedné konkrétní US, typicky odvozených z `00-vision.md` nebo `.claude/rules/`), ověřitelnost — scénář(e) `SC-…` v `docs/30-scenarios.md`.
> Priorita FR vychází z priority zdrojové US; při konfliktu více zdrojů platí nejvyšší.
>
> **Priorita v tomto draftu:** vše je Must. Horizont je ~půl roku, velká část funkcionality je z předchozí verze převzatelná po kontrole a cílem je pokrýt všechny user stories (viz `10-user-stories.md`) — nejde o výběr MVP podmnožiny. Should/Could/Won't se použije až pro nově navržené nápady nad rámec současných stories.

## Oblasti

| Prefix | Oblast |
|--------|--------|
|AUTH| Přihlašování |
|ROCNIK| Základní parametry ročníku a jeho životní cyklus |
|NASTAVENI| Nastavení aplikace (napříč ročníky) |
|STANOVISTE| Správa stanoviště |
|SIFRY| Správa šifer, nápověď a řešení |
|TYM| Správa týmů |
|FORUM| Správa fóra |
|VYSLEDKY| Výsledky a reportáže po hře |
|STATEK| Integrace s externím systémem Statek |
|EXPORT| Export dat|
|OBALKY|Příprava a tisk startovních obálek|
|MASKOT|Správa maskotů |
|EMAIL| Hromadné rozesílání emailů|
|STRANKA|Správa stránek|
|MEDIA| Správa médií (soubory, obrázky) |
|MENU| Správa menu|


---

## Funkční požadavky

> Formát: `**Priorita:**` • `**Zdrojová US:**` (viz `10-user-stories.md`) • `**Ověřitelnost:**` (SC-… v `30-scenarios.md`, zatím TODO — scénáře nejsou napsané). Popis je stručný, detaily nese zdrojová US — neduplikovat.

### AUTH — Přihlašování

#### FR-AUTH-01 — Přihlášení
- **Priorita:** Must • **Zdrojová US:** US-PUBLIC-05 • **Ověřitelnost:** SC-AUTH-01, SC-AUTH-02

Registrovaný uživatel (TEAM/SPARE) i organizátor se přihlásí loginem a heslem; po přihlášení je přesměrován do odpovídající role.

#### FR-AUTH-02 — Reset hesla
- **Priorita:** Must • **Zdrojová US:** US-PUBLIC-06 • **Ověřitelnost:** SC-AUTH-03

Nepřihlášený uživatel si přes email vyžádá dočasný odkaz pro nastavení nového hesla.

#### FR-AUTH-03 — Odhlášení
- **Priorita:** Must • **Zdrojová US:** US-TEAM-02 • **Ověřitelnost:** SC-AUTH-04

Přihlášený uživatel ukončí svou relaci.

#### FR-AUTH-04 — Změna hesla
- **Priorita:** Must • **Zdrojová US:** US-TEAM-04 • **Ověřitelnost:** SC-AUTH-05

Přihlášený uživatel si sám změní heslo po ověření stávajícího; ostatní relace téhož účtu se zneplatní.

> Bezpečné uložení hesla je nefunkční požadavek, viz [NFR-SECURITY-01](#nfr-security-01--ukládání-hesel) (dříve vedeno jako FR-AUTH-05 — ID zůstává neobsazené, viz pravidlo výše).

### ROCNIK — Základní parametry ročníku a jeho životní cyklus

#### FR-ROCNIK-01 — Parametry ročníku
- **Priorita:** Must • **Zdrojová US:** US-ORG-01 • **Ověřitelnost:** SC-ROCNIK-01, SC-ROCNIK-02

Organizátor spravuje parametry aktuálního ročníku (kapacity, datumy, cena) včetně validace závislostí mezi datumy.

#### FR-ROCNIK-02 — Kategorie hry
- **Priorita:** Must • **Zdrojová US:** US-ORG-01 • **Ověřitelnost:** SC-ROCNIK-03

Organizátor spravuje kategorie ročníku (min. 1), ke kterým se dále váží stanoviště a šifry.

#### FR-ROCNIK-03 — Založení nového ročníku
- **Priorita:** Must • **Zdrojová US:** US-ORG-18 • **Ověřitelnost:** SC-ROCNIK-04, SC-ROCNIK-06

Organizátor založí nový ročník zkopírováním struktury (stránky, menu, obecná diskuze) předchozího ročníku; předchozí ročník se tím přepne do archivního režimu. Zároveň se z týmů ve všech ročnících, které se tím stávají archivními, smažou telefonní čísla (retenční politika, viz NFR-LEGAL-02).

#### FR-ROCNIK-04 — Řízení fází ročníku podle datumů
- **Priorita:** Must • **Zdroj:** `00-vision.md` § Fáze ročníku • **Ověřitelnost:** SC-ROCNIK-05

Systém odvozuje aktuální fázi ročníku (příprava, registrace, poslední informace, hra, ukončení, archiv) z klíčových datumů a podle ní řídí viditelnost stránek a funkcí napříč ostatními FR.

### NASTAVENI — Nastavení aplikace

#### FR-NASTAVENI-01 — Správa nastavení aplikace
- **Priorita:** Must • **Zdrojová US:** US-ORG-02 • **Ověřitelnost:** SC-NASTAVENI-01

Organizátor spravuje parametry platné napříč ročníky (base-url, SMTP, platební účet, přístup na Statek) formou editovatelné přehledové tabulky klíč/hodnota.

### STANOVISTE — Správa stanoviště

#### FR-STANOVISTE-01 — Správa stanovišť a trasy
- **Priorita:** Must • **Zdrojová US:** US-ORG-03 • **Ověřitelnost:** SC-STANOVISTE-01

Organizátor spravuje pořadí, polohu (GPS) a přiřazení kategorií stanovišť v rámci ročníku; systém z nich sestavuje trasu a zobrazuje ji na mapě.

#### FR-STANOVISTE-02 — Veřejné zobrazení trasy
- **Priorita:** Must • **Zdrojová US:** US-PUBLIC-13 • **Ověřitelnost:** SC-STANOVISTE-02, SC-STANOVISTE-03

Návštěvník po skončení hry (i v archivu) zobrazí trasu na mapě včetně podpory více kategorií a přepínání mezi ročníky.

### SIFRY — Správa šifer, nápověď a řešení

#### FR-SIFRY-01 — Správa šifer
- **Priorita:** Must • **Zdrojová US:** US-ORG-04 • **Ověřitelnost:** SC-SIFRY-01

Organizátor spravuje zadání, nápovědu a řešení šifry včetně přiřazení ke stanovišti a generování QR kódu.

#### FR-SIFRY-02 — Veřejné zobrazení šifry
- **Priorita:** Must • **Zdrojová US:** US-PUBLIC-12 • **Ověřitelnost:** SC-SIFRY-02

Návštěvník po skončení hry (i v archivu) zobrazí zadání, nápovědu a řešení šifry a přidružené fórum.

#### FR-SIFRY-03 — Hodnocení šifry
- **Priorita:** Must • **Zdrojová US:** US-PUBLIC-12 • **Ověřitelnost:** SC-SIFRY-03

Návštěvník ohodnotí obtížnost a oblibu šifry na stupnici 1–10 v aktuálním ročníku; archivní ročník zobrazuje jen souhrnnou statistiku.

### TYM — Správa týmů

#### FR-TYM-01 — Registrace týmu
- **Priorita:** Must • **Zdrojová US:** US-PUBLIC-04 • **Ověřitelnost:** SC-TYM-01, SC-TYM-02, SC-TYM-03

Návštěvník zaregistruje tým do aktivního ročníku (validace, captcha, unikátní login/název, přiřazení maskota, zařazení TEAM/SPARE podle kapacity).

#### FR-TYM-02 — Veřejný přehled a statistiky týmů
- **Priorita:** Must • **Zdrojová US:** US-PUBLIC-07 • **Ověřitelnost:** SC-TYM-04

Návštěvník zobrazí tabulku přihlášených týmů a odvozené statistiky (týmy, hráči, města).

#### FR-TYM-03 — Zrušení účasti týmu
- **Priorita:** Must • **Zdrojová US:** US-TEAM-03 • **Ověřitelnost:** SC-TYM-05

Tým zruší svou účast do začátku hry; systém automaticky povýší nejstaršího náhradníka a informuje ho emailem.

#### FR-TYM-04 — Zobrazení profilu týmu
- **Priorita:** Must • **Zdrojová US:** US-TEAM-05 • **Ověřitelnost:** SC-TYM-06

Přihlášený tým zobrazí své údaje a (pokud nemá zaplaceno) platební údaje včetně QR kódu.

#### FR-TYM-05 — Úprava údajů týmu
- **Priorita:** Must • **Zdrojová US:** US-TEAM-06 • **Ověřitelnost:** SC-TYM-07

Přihlášený tým upraví své údaje (včetně loginu) do zahájení hry; unikátnost se validuje.

#### FR-TYM-06 — Omezení role SPARE
- **Priorita:** Must • **Zdrojová US:** US-SPARE-01 • **Ověřitelnost:** SC-TYM-08

Náhradník má stejná oprávnění jako TEAM kromě zobrazení platebních údajů a posledních informací.

#### FR-TYM-07 — Poslední informace pro TEAM_PAID
- **Priorita:** Must • **Zdrojová US:** US-TEAM_PAID-01 • **Ověřitelnost:** SC-TYM-09

Zaplacený hrající tým zobrazí poslední informace od data `last-info`.

#### FR-TYM-08 — Přehled týmů pro organizátora
- **Priorita:** Must • **Zdrojová US:** US-ORG-05 • **Ověřitelnost:** SC-TYM-10

Organizátor prochází, třídí a filtruje přehled všech týmů ročníku, provádí hromadné akce a přihlašuje se „za tým".

#### FR-TYM-09 — Editace týmu organizátorem
- **Priorita:** Must • **Zdrojová US:** US-ORG-06 • **Ověřitelnost:** SC-TYM-11

Organizátor edituje údaje libovolného týmu, mění stav zaplaceno/náhradník/smazáno; smazání spouští přepočet náhradníků.

### FORUM — Správa fóra

#### FR-FORUM-01 — Přehled sekcí fóra
- **Priorita:** Must • **Zdrojová US:** US-PUBLIC-08 • **Ověřitelnost:** SC-FORUM-01

Návštěvník zobrazí přehled dostupných sekcí fóra seřazených podle pořadí.

#### FR-FORUM-02 — Zobrazení a psaní příspěvků
- **Priorita:** Must • **Zdrojová US:** US-PUBLIC-09 • **Ověřitelnost:** SC-FORUM-02

Návštěvník/tým čte stránkovaný seznam příspěvků sekce a odešle nový příspěvek; org navíc vidí IP adresu odesílatele.

#### FR-FORUM-03 — Správa sekcí fóra
- **Priorita:** Must • **Zdrojová US:** US-ORG-07 • **Ověřitelnost:** SC-FORUM-03

Organizátor spravuje sekce fóra (vznik, pořadí, viditelnost, provázání se šifrou nebo stránkou).

#### FR-FORUM-04 — Moderace příspěvků
- **Priorita:** Must • **Zdrojová US:** US-ORG-19 • **Ověřitelnost:** SC-FORUM-04

Organizátor maže libovolný příspěvek a edituje vlastní příspěvky.

### VYSLEDKY — Výsledky a reportáže po hře

#### FR-VYSLEDKY-01 — Zobrazení výsledků hry
- **Priorita:** Must • **Zdrojová US:** US-PUBLIC-10 • **Ověřitelnost:** SC-VYSLEDKY-01

Návštěvník po skončení hry (i v archivu) zobrazí výsledky synchronizované z externího systému Statek do interní databáze.

#### FR-VYSLEDKY-02 — Reportáže týmů
- **Priorita:** Must • **Zdrojová US:** US-PUBLIC-11 • **Ověřitelnost:** SC-VYSLEDKY-02

Návštěvník po skončení hry (i v archivu) zobrazí odkazy na reportáže týmů a orgů, které tým/org sám vyplnil.

### STATEK — Integrace s externím systémem Statek

#### FR-STATEK-01 — Příprava a import dat do Statku
- **Priorita:** Must • **Zdrojová US:** US-ORG-17 • **Ověřitelnost:** SC-STATEK-01

Organizátor připraví/importuje data o týmech, parametrech hry, šifrách a stanovištích pro externí systém Statek.

### EXPORT — Export dat

#### FR-EXPORT-01 — Export dat o týmech
- **Priorita:** Must • **Zdrojová US:** US-ORG-16 • **Ověřitelnost:** SC-EXPORT-01

Organizátor exportuje údaje o týmech do CSV.

### OBALKY — Příprava a tisk startovních obálek

#### FR-OBALKY-01 — Startovní obálky
- **Priorita:** Must • **Zdrojová US:** US-ORG-15 • **Ověřitelnost:** SC-OBALKY-01

Organizátor upraví šablonu startovní obálky a vygeneruje PDF k tisku.

### MASKOT — Správa maskotů

#### FR-MASKOT-01 — Správa maskotů
- **Priorita:** Must • **Zdrojová US:** US-ORG-08 • **Ověřitelnost:** SC-MASKOT-01

Organizátor spravuje seznam maskotů dostupných pro přiřazení týmům v rámci ročníku.

### EMAIL — Hromadné rozesílání emailů

#### FR-EMAIL-01 — Hromadný email ročníku
- **Priorita:** Must • **Zdrojová US:** US-ORG-13 • **Ověřitelnost:** SC-EMAIL-01

Organizátor rozešle email vybrané skupině týmů (nebo vlastnímu seznamu adres) aktuálního ročníku, jednotlivě a s logováním.

#### FR-EMAIL-02 — Zvací email
- **Priorita:** Must • **Zdrojová US:** US-ORG-14 • **Ověřitelnost:** SC-EMAIL-02

Organizátor rozešle zvací email na deduplikovanou databázi emailů napříč ročníky, s vynecháním již přihlášených týmů a možností odhlášení z odběru.

### STRANKA — Správa stránek

#### FR-STRANKA-01 — Zobrazení statických stránek
- **Priorita:** Must • **Zdrojová US:** US-PUBLIC-01 • **Ověřitelnost:** SC-STRANKA-01

Návštěvník zobrazí aktivní stránky ročníku, na které má oprávnění, včetně dynamické úvodní stránky napojené na data ročníku.

#### FR-STRANKA-02 — Zobrazení archivních ročníků
- **Priorita:** Must • **Zdrojová US:** US-PUBLIC-03 • **Ověřitelnost:** SC-STRANKA-02

Návštěvník přepne na archivní ročník a zobrazí jeho aktivní stránky bez omezení datumy.

#### FR-STRANKA-03 — Správa stránek
- **Priorita:** Must • **Zdrojová US:** US-ORG-10 • **Ověřitelnost:** SC-STRANKA-03

Organizátor spravuje statické stránky (obsah v MD, viditelnost, oprávnění, provázání s fórem) včetně nouzové editace při poškození obsahu.

#### FR-STRANKA-04 — Užitečné odkazy
- **Priorita:** Must • **Zdrojová US:** US-ORG-09 • **Ověřitelnost:** SC-STRANKA-04

Organizátor spravuje editovatelný přehled důležitých URL odkazů pro rychlou navigaci během hry.

### MEDIA — Správa médií

#### FR-MEDIA-01 — Správa médií
- **Priorita:** Must • **Zdrojová US:** US-ORG-11 • **Ověřitelnost:** SC-MEDIA-01

Organizátor spravuje soubory (nahrávání, mazání, složky) v úložišti médií tak, aby nešlo uhodnout název souboru a předčasně se dostat k neveřejnému obsahu.

### MENU — Správa menu

#### FR-MENU-01 — Generování menu
- **Priorita:** Must • **Zdrojová US:** US-ORG-12, US-TEAM-01 • **Ověřitelnost:** SC-MENU-01

Systém generuje menu ročníku ze seznamu položek podle fáze hry a role uživatele; organizátor spravuje pořadí a strukturu položek.

## Kategorie (NFR)

| Prefix | Kategorie |
|--------|-----------|
|SECURITY| Bezpečnost |
|USABILITY| Použitelnost |
|COMPATIBILITY| Kompatibilita a historická data |
|RELIABILITY| Spolehlivost |
|LEGAL| Legislativa a ochrana osobních údajů |
|PERFORMANCE| Výkon a škálovatelnost |

## Nefunkční požadavky

> Vytaženo z poznámek roztroušených po `10-user-stories.md`, `00-vision.md` a `.claude/rules/`, aby bezpečnostní/UX/výkonnostní požadavky, které se týkají víc než jedné FR, žily na jednom místě místo opakování v poznámkách (viz `.claude/rules/docs.md`).

### SECURITY — Bezpečnost

#### NFR-SECURITY-01 — Ukládání hesel
- **Priorita:** Must • **Zdrojová US:** US-PUBLIC-04 • **Ověřitelnost:** SC-SECURITY-01

Heslo se ukládá jako osolený hash (argon2), nikdy v čitelné podobě.

#### NFR-SECURITY-02 — Ochrana proti XSS
- **Priorita:** Must • **Zdrojová US:** US-PUBLIC-12 • **Ověřitelnost:** SC-SECURITY-02

Veškerý uživatelský vstup zobrazovaný dalším uživatelům (fórum, komentáře, hodnocení šifer apod.) je ošetřen proti vkládání škodlivého obsahu (XSS).

#### NFR-SECURITY-03 — Needuhodnutelné názvy souborů v médiích
- **Priorita:** Must • **Zdrojová US:** US-ORG-11 • **Ověřitelnost:** SC-SECURITY-03, SC-MEDIA-01

Adresářová struktura/pojmenování souborů v úložišti médií nesmí umožnit uhodnutím URL předčasný přístup k neveřejnému obsahu (zadání/řešení šifer před koncem hry), a zároveň musí zůstat pro organizátora čitelné a spravovatelné (ne náhodně generovaná jména).

#### NFR-SECURITY-04 — Ochrana destruktivních a stav měnících akcí
- **Priorita:** Must • **Zdroj:** `.claude/rules/ui.md` (ADR-0003) • **Ověřitelnost:** SC-SECURITY-04

Všechny destruktivní/měnící akce jdou přes POST s CSRF ochranou, destruktivní akce vyžadují potvrzení a po dokončení následuje redirect (PRG vzor).

### USABILITY — Použitelnost

#### NFR-USABILITY-01 — Jazyk uživatelského rozhraní
- **Priorita:** Must • **Zdroj:** `00-vision.md` § Předpoklady a omezení • **Ověřitelnost:** SC-USABILITY-01

Veškeré uživatelské rozhraní je v češtině.

#### NFR-USABILITY-02 — Responzivita pro desktop i mobil
- **Priorita:** Must • **Zdroj:** `00-vision.md` § Předpoklady a omezení; **Zdrojová US:** US-PUBLIC-04 • **Ověřitelnost:** SC-USABILITY-02

Aplikace včetně formulářů (např. registrace) je plně použitelná jak na desktopu, tak na mobilu.

#### NFR-USABILITY-03 — České řazení textů
- **Priorita:** Must • **Zdroj:** `.claude/rules/ui.md` • **Ověřitelnost:** SC-USABILITY-03

Řazení textových sloupců viditelných uživateli respektuje českou abecedu (case-insensitive, „ch“ mezi „h“ a „i“, diakritika vokálů splývá se základem) — nikdy prosté `sorted()` bez klíče.

### COMPATIBILITY — Kompatibilita a historická data

#### NFR-COMPATIBILITY-01 — Zpětná kompatibilita s historickými ročníky
- **Priorita:** Must • **Zdroj:** `00-vision.md` § Problém • **Ověřitelnost:** SC-COMPATIBILITY-01

Systém musí umět přijmout a zobrazit data z cca 20 proběhlých ročníků, které měly odlišné parametry hry (počet stanovišť, kategorie, systém nápověd a řešení).

### RELIABILITY — Spolehlivost

#### NFR-RELIABILITY-01 — Doručitelnost hromadných emailů
- **Priorita:** Must • **Zdrojová US:** US-ORG-13 • **Ověřitelnost:** SC-RELIABILITY-01

Hromadné emaily se odesílají jednotlivě (ne jako jeden broadcast), s logováním a možností zjistit nedoručitelné adresy — kvůli riziku, že poštovní služba označí hromadné rozesílání za spam. Asynchronní běh a průběžné zobrazení stavu viz NFR-PERFORMANCE-03.

### LEGAL — Legislativa a ochrana osobních údajů

#### NFR-LEGAL-01 — Souhlas se zpracováním osobních údajů
- **Priorita:** Must • **Zdrojová US:** US-PUBLIC-04 • **Ověřitelnost:** SC-LEGAL-01

Registrace vyžaduje explicitní souhlas všech účastníků se zpracováním osobních údajů pro účely organizace hry a evidence hráčů/výsledků; systém uchovává dohledatelně obsah a čas udělení souhlasu.

#### NFR-LEGAL-02 — Retenční politika osobních údajů
- **Priorita:** Must • **Zdroj:** zadání organizátora • **Ověřitelnost:** SC-LEGAL-02

Jména týmů a hráčů (vč. veřejných jmen) se uchovávají trvale kvůli historii výsledků a archivaci proběhlých ročníků. Emailové adresy se uchovávají napříč ročníky kvůli zvacím emailům (FR-EMAIL-02). Telefonní čísla se naopak trvale neuchovávají — při založení nového ročníku (FR-ROCNIK-03) se smažou z týmů ve všech ročnících, které se tím stávají archivními.

### PERFORMANCE — Výkon a škálovatelnost

#### NFR-PERFORMANCE-01 — Stránkování přehledových tabulek
- **Priorita:** Must • **Zdroj:** `10-user-stories.md` § Organizátor (obecné požadavky) • **Ověřitelnost:** SC-PERFORMANCE-01

Přehledové tabulky (veřejné i administrační) se stránkují. Velikost stránky je uživatelsky volitelná, výchozí hodnota je 50 záznamů.

#### NFR-PERFORMANCE-02 — Doba odezvy stránky
- **Priorita:** Must • **Zdroj:** zadání organizátora • **Ověřitelnost:** SC-PERFORMANCE-02

Doba odezvy webové stránky (běžný request/response, bez dlouhotrvajících operací dle NFR-PERFORMANCE-03) je cílově 1 vteřina. Zvláštní pozornost je potřeba věnovat přihlášení (FR-AUTH-01) — v minulé verzi bylo přihlašování opakovaně pomalé, jde tedy o známé rizikové místo, které je potřeba při implementaci a testování ověřit obzvlášť pečlivě.

#### NFR-PERFORMANCE-03 — Asynchronní zpracování dlouhotrvajících operací
- **Priorita:** Must • **Zdroj:** zadání organizátora • **Ověřitelnost:** SC-PERFORMANCE-03

Operace, které nelze dokončit v rámci cílové doby odezvy (NFR-PERFORMANCE-02) — typicky hromadné rozesílání emailů (US-ORG-13, US-ORG-14) — běží na pozadí asynchronně; stránka průběžně (pollingem/AJAX) dotahuje a zobrazuje aktuální stav/průběh, request na spuštění operace se nezablokuje.
