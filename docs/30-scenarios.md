# 30 — Scénáře a akceptační kritéria

> Vlastník: organizátoři sovy • Stav: draft • Poslední revize: 2026-09-19

> Scénáře popisují chování z pohledu uživatele ve formátu **Given / When / Then**,
> ať se dají přímo přepsat na (akceptační) testy.
> ID: `SC-<OBLAST>-xx`, kde `<OBLAST>` je stejný prefix jako u požadavků
> (viz `docs/20-requirements.md`). Číslování je nezávislé v rámci každé oblasti.
> **ID se po vytvoření nemění ani nepřečísluje** (stejné pravidlo jako u US a FR).
> Každý scénář odkazuje na požadavek(y) `FR-…` / `NFR-…` a zdrojovou story `US-…`,
> které ověřuje. Termíny podle `docs/glossary.md`.
>
> Scénáře jsou akceptační kritéria, ne detailní testovací dokumentace — pokrývají hlavní
> (happy path) a nejdůležitější alternativní/chybové cesty zmíněné v poznámkách zdrojové US.
> Zbytek detailů (přesná pole formulářů, texty chyb apod.) nese zdrojová US — neduplikovat.

## Oblasti

Stejné prefixy jako u FR (`docs/20-requirements.md` § Oblasti) a NFR (`docs/20-requirements.md` § Kategorie (NFR)) — neduplikováno zde.

---

## Scénáře

### AUTH

#### SC-AUTH-01 — Úspěšné přihlášení
- **Ověřuje:** FR-AUTH-01 • **Story:** US-PUBLIC-05
- **Given** tým/organizátor má platný login a heslo v aktuálním ročníku a je nepřihlášený
- **When** zadá správný login a heslo do přihlašovacího formuláře
- **Then** je přihlášen a přesměrován do odpovídající role (TEAM/SPARE/ORG)

#### SC-AUTH-02 — Přihlášení se zamítne při chybném heslu
- **Ověřuje:** FR-AUTH-01 • **Story:** US-PUBLIC-05
- **Given** tým zadá existující login
- **When** zadá k němu nesprávné heslo
- **Then** přihlášení je odmítnuto se srozumitelnou chybou a uživatel zůstává nepřihlášený

#### SC-AUTH-03 — Reset zapomenutého hesla
- **Ověřuje:** FR-AUTH-02 • **Story:** US-PUBLIC-06
- **Given** nepřihlášený uživatel zná email registrovaného týmu
- **When** vyžádá reset hesla a klikne na odkaz z emailu do vypršení platnosti
- **Then** může nastavit nové heslo (2× zadané) a přihlásit se jím

#### SC-AUTH-04 — Odhlášení
- **Ověřuje:** FR-AUTH-03 • **Story:** US-TEAM-02
- **Given** uživatel je přihlášený
- **When** klikne na odhlásit
- **Then** relace končí a soukromé informace přestanou být dostupné

#### SC-AUTH-05 — Změna hesla invaliduje ostatní relace
- **Ověřuje:** FR-AUTH-04 • **Story:** US-TEAM-04
- **Given** přihlášený uživatel zná své stávající heslo a je přihlášený současně ve dvou prohlížečích
- **When** úspěšně změní heslo (zadá staré + nové, které se liší)
- **Then** aktuální relace zůstává platná, ostatní relace téhož účtu jsou zneplatněny

### ROCNIK

#### SC-ROCNIK-01 — Úprava parametrů ročníku
- **Ověřuje:** FR-ROCNIK-01 • **Story:** US-ORG-01
- **Given** organizátor edituje parametry aktuálního ročníku
- **When** zadá platné hodnoty splňující `reg-from < reg-to`, `payment-to < start-time`, `last-info < start-time`, `start-time < end-time`
- **Then** parametry se uloží

#### SC-ROCNIK-02 — Neplatné pořadí datumů se zamítne
- **Ověřuje:** FR-ROCNIK-01 • **Story:** US-ORG-01
- **Given** organizátor edituje parametry ročníku
- **When** zadá datumy porušující pravidlo pořadí (např. `reg-from > reg-to`)
- **Then** uložení je odmítnuto s vysvětlující chybou a žádná hodnota se nezmění

#### SC-ROCNIK-03 — Správa kategorií ročníku
- **Ověřuje:** FR-ROCNIK-02 • **Story:** US-ORG-01
- **Given** ročník má jednu kategorii
- **When** organizátor se pokusí odebrat poslední zbývající kategorii
- **Then** operace je odmítnuta (ve hře musí zůstat minimálně 1 kategorie)

#### SC-ROCNIK-04 — Založení nového ročníku
- **Ověřuje:** FR-ROCNIK-03 • **Story:** US-ORG-18
- **Given** organizátor potvrdí založení nového ročníku
- **When** operace proběhne
- **Then** vznikne nový ročník s kopií stránek, menu a obecné diskuze předchozího ročníku a předchozí ročník se přepne do archivního režimu

#### SC-ROCNIK-06 — Založení nového ročníku smaže telefony z archivovaných ročníků
- **Ověřuje:** FR-ROCNIK-03, NFR-LEGAL-02 • **Story:** US-ORG-18
- **Given** stávající (dosud aktuální) ročník má u týmů vyplněná telefonní čísla
- **When** organizátor založí nový ročník
- **Then** telefonní čísla týmů ve ročníku, který se tím stal archivním, jsou z databáze smazána; jména týmů/hráčů a emaily zůstávají zachované

#### SC-ROCNIK-05 — Fáze ročníku se odvozuje z datumů
- **Ověřuje:** FR-ROCNIK-04 • **Story:** (zdroj: `00-vision.md` § Fáze ročníku)
- **Given** ročník má nastavené klíčové datumy (reg-from, reg-to, payment-to, last-info, start-time, end-time)
- **When** aktuální čas spadá do konkrétního intervalu mezi těmito datumy
- **Then** systém vyhodnotí odpovídající fázi (příprava/registrace/poslední informace/hra/ukončení/archiv) a podle ní řídí viditelnost stránek a funkcí

### NASTAVENI

#### SC-NASTAVENI-01 — Správa globálního nastavení
- **Ověřuje:** FR-NASTAVENI-01 • **Story:** US-ORG-02
- **Given** organizátor otevře přehled nastavení aplikace
- **When** upraví, přidá nebo smaže parametr (např. `base-url`, SMTP, platební účet, přístup na Statek)
- **Then** změna se projeví napříč ročníky (nastavení není vázané na konkrétní ročník)

### STANOVISTE

#### SC-STANOVISTE-01 — Správa pořadí a polohy stanovišť
- **Ověřuje:** FR-STANOVISTE-01 • **Story:** US-ORG-03
- **Given** organizátor spravuje stanoviště ročníku
- **When** přidá stanoviště, zadá jeho GPS polohu a upraví pořadí v trase
- **Then** trasa (spojnice mezi stanovišti na mapě) se přepočítá podle nového pořadí

#### SC-STANOVISTE-02 — Veřejné zobrazení trasy po skončení hry
- **Ověřuje:** FR-STANOVISTE-02 • **Story:** US-PUBLIC-13
- **Given** hra aktuálního ročníku skončila (nebo jde o archivní ročník)
- **When** návštěvník otevře stránku trasy
- **Then** vidí stanoviště na mapě propojená čarami, s podporou více kategorií (odlišené barvou)

#### SC-STANOVISTE-03 — Trasa není dostupná před koncem aktivní hry
- **Ověřuje:** FR-STANOVISTE-02 • **Story:** US-PUBLIC-13
- **Given** aktuální ročník ještě neskončil
- **When** návštěvník se pokusí zobrazit trasu aktuálního ročníku
- **Then** stránka trasu nezobrazí

### SIFRY

#### SC-SIFRY-01 — Správa šifry a generování QR kódu
- **Ověřuje:** FR-SIFRY-01 • **Story:** US-ORG-04
- **Given** organizátor vytvoří šifru a přiřadí ji ke stanovišti
- **When** uloží šifru
- **Then** vygeneruje se QR kód ve tvaru `https://seslost.cz/l/<kód>` s logem sovy a číselným označením stanoviště

#### SC-SIFRY-02 — Veřejné zobrazení šifry po skončení hry
- **Ověřuje:** FR-SIFRY-02 • **Story:** US-PUBLIC-12
- **Given** hra aktuálního ročníku skončila (nebo jde o archivní ročník)
- **When** návštěvník otevře stránku šifry
- **Then** vidí zadání a po rozkliknutí nápovědu a řešení, včetně odkazu na přidruženou sekci fóra

#### SC-SIFRY-03 — Hodnocení šifry
- **Ověřuje:** FR-SIFRY-03 • **Story:** US-PUBLIC-12
- **Given** aktuální ročník skončil a šifra ještě nemá hodnocení od daného návštěvníka
- **When** návštěvník ohodnotí obtížnost a oblibu na stupnici 1–10
- **Then** hodnocení se uloží a zobrazí se v agregované statistice včetně počtu hlasujících

### TYM

#### SC-TYM-01 — Registrace do nenaplněné kapacity
- **Ověřuje:** FR-TYM-01 • **Story:** US-PUBLIC-04
- **Given** probíhá registrace a počet týmů je pod `max-teams`
- **When** návštěvník vyplní registrační formulář (vč. captcha a povinných souhlasů) s unikátním názvem a loginem
- **Then** tým vznikne v roli TEAM, dostane náhodný unikátní maskot a heslo je uloženo jako argon2 hash (NFR-SECURITY-01)

#### SC-TYM-02 — Registrace nad kapacitu vytvoří náhradníka
- **Ověřuje:** FR-TYM-01 • **Story:** US-PUBLIC-04
- **Given** počet týmů již dosáhl `max-teams`
- **When** návštěvník úspěšně vyplní registrační formulář
- **Then** tým vznikne v roli SPARE

#### SC-TYM-03 — Registrace se zamítne při duplicitě
- **Ověřuje:** FR-TYM-01 • **Story:** US-PUBLIC-04
- **Given** v aktuálním ročníku už existuje tým se stejným názvem nebo loginem
- **When** návštěvník odešle registrační formulář se stejným názvem/loginem
- **Then** formulář se zobrazí znovu s vyplněnými údaji a varováním o porušení unikátnosti

#### SC-TYM-04 — Veřejný přehled a statistiky týmů
- **Ověřuje:** FR-TYM-02 • **Story:** US-PUBLIC-07
- **Given** je zaregistrováno několik týmů, včetně jednoho smazaného
- **When** návštěvník otevře stránku týmů
- **Then** smazaný tým se nezobrazuje a statistiky (týmy, hráči, města) sedí na viditelné množině týmů

#### SC-TYM-05 — Zrušení účasti povýší náhradníka
- **Ověřuje:** FR-TYM-03 • **Story:** US-TEAM-03
- **Given** hrající tým zruší účast před začátkem hry a existuje alespoň jeden náhradník
- **When** zrušení je potvrzeno
- **Then** tým je označen jako smazaný, nejstarší náhradník je automaticky povýšen na TEAM a dostane o tom email

#### SC-TYM-06 — Zobrazení profilu s platebními údaji
- **Ověřuje:** FR-TYM-04 • **Story:** US-TEAM-05
- **Given** přihlášený tým nemá zaplaceno
- **When** otevře stránku „Údaje o týmu“
- **Then** vidí platební údaje včetně QR kódu pro platbu

#### SC-TYM-07 — Úprava údajů týmu s kontrolou unikátnosti loginu
- **Ověřuje:** FR-TYM-05 • **Story:** US-TEAM-06
- **Given** přihlášený tým edituje svůj profil před zahájením hry
- **When** změní login na hodnotu, kterou už používá jiný tým v ročníku
- **Then** změna je odmítnuta jako neunikátní

#### SC-TYM-08 — Náhradník nevidí platbu ani poslední informace
- **Ověřuje:** FR-TYM-06 • **Story:** US-SPARE-01
- **Given** přihlášený tým má roli SPARE
- **When** otevře „Údaje o týmu“ a hledá poslední informace
- **Then** platební údaje ani poslední informace se mu nezobrazí

#### SC-TYM-09 — Zaplacený tým vidí poslední informace
- **Ověřuje:** FR-TYM-07 • **Story:** US-TEAM_PAID-01
- **Given** hrající tým má zaplaceno a je dosaženo data `last-info`
- **When** tým otevře poslední informace
- **Then** obsah se zobrazí

#### SC-TYM-10 — Hromadná akce nad týmy
- **Ověřuje:** FR-TYM-08 • **Story:** US-ORG-05
- **Given** organizátor vybere v přehledu více týmů
- **When** spustí hromadnou akci „označit jako zaplaceno“
- **Then** všechny vybrané týmy mají nastaven příznak zaplaceno a filtrování/třídění tabulky zůstává zachováno

#### SC-TYM-11 — Editace týmu spustí přepočet náhradníků
- **Ověřuje:** FR-TYM-09 • **Story:** US-ORG-06
- **Given** organizátor označí hrající tým jako smazaný a existuje náhradník
- **When** změnu uloží
- **Then** proběhne automatický přepočet náhradníků a povýšený náhradník dostane email

### FORUM

#### SC-FORUM-01 — Přehled sekcí fóra
- **Ověřuje:** FR-FORUM-01 • **Story:** US-PUBLIC-08
- **Given** existují aktivní i neaktivní sekce fóra
- **When** návštěvník otevře přehled fóra
- **Then** vidí jen aktivní sekce seřazené podle pořadí, s časem posledního příspěvku

#### SC-FORUM-02 — Odeslání příspěvku
- **Ověřuje:** FR-FORUM-02 • **Story:** US-PUBLIC-09
- **Given** přihlášený tým otevře aktivní sekci fóra
- **When** odešle příspěvek s textem
- **Then** příspěvek se zobrazí nahoře seznamu (od nejmladšího) s jménem týmu a časem; org navíc vidí IP adresu odesílatele

#### SC-FORUM-03 — Sekce fóra vzniká automaticky se šifrou
- **Ověřuje:** FR-FORUM-03 • **Story:** US-ORG-07
- **Given** organizátor vytvoří novou šifru
- **When** šifra je uložena
- **Then** vznikne provázaná sekce fóra pojmenovaná podle šifry, nedostupná až do konce hry

#### SC-FORUM-04 — Moderace smaže cizí příspěvek
- **Ověřuje:** FR-FORUM-04 • **Story:** US-ORG-19
- **Given** v sekci fóra existuje nevhodný příspěvek týmu
- **When** organizátor příspěvek smaže
- **Then** příspěvek zmizí ze seznamu pro všechny role

### VYSLEDKY

#### SC-VYSLEDKY-01 — Zobrazení výsledků po synchronizaci ze Statku
- **Ověřuje:** FR-VYSLEDKY-01 • **Story:** US-PUBLIC-10
- **Given** hra skončila a výsledky byly synchronizovány ze Statku do interní databáze
- **When** návštěvník otevře stránku výsledků
- **Then** vidí výsledky z interní databáze (nezávisle na dlouhodobé dostupnosti Statku)

#### SC-VYSLEDKY-02 — Zobrazení reportáží
- **Ověřuje:** FR-VYSLEDKY-02 • **Story:** US-PUBLIC-11
- **Given** některé týmy vyplnily URL své reportáže
- **When** návštěvník po skončení hry otevře stránku reportáží
- **Then** vidí seznam odkazů na reportáže týmů (a orgů/fotek, pokud jsou vyplněné)

### STATEK

#### SC-STATEK-01 — Příprava dat pro Statek
- **Ověřuje:** FR-STATEK-01 • **Story:** US-ORG-17
- **Given** organizátor má kompletní data o týmech, stanovištích a šifrách aktuálního ročníku
- **When** spustí přípravu/export dat pro Statek
- **Then** vygenerují se podklady ve formátu, který Statek dokáže přijmout

### EXPORT

#### SC-EXPORT-01 — Export týmů do CSV
- **Ověřuje:** FR-EXPORT-01 • **Story:** US-ORG-16
- **Given** organizátor otevře export dat
- **When** spustí export týmů
- **Then** stáhne se CSV se jménem týmu, maskotem, telefonem a složením

### OBALKY

#### SC-OBALKY-01 — Generování PDF startovních obálek
- **Ověřuje:** FR-OBALKY-01 • **Story:** US-ORG-15
- **Given** organizátor upravil šablonu startovní obálky
- **When** spustí generování
- **Then** vytvoří se PDF s obálkami pro tisk odpovídající šabloně

### MASKOT

#### SC-MASKOT-01 — Správa seznamu maskotů
- **Ověřuje:** FR-MASKOT-01 • **Story:** US-ORG-08
- **Given** organizátor spravuje seznam maskotů ročníku
- **When** přidá nového maskota
- **Then** maskot je dostupný pro náhodné přiřazení při registraci a je unikátní v rámci ročníku

### EMAIL

#### SC-EMAIL-01 — Hromadný email vybrané skupině
- **Ověřuje:** FR-EMAIL-01 • **Story:** US-ORG-13
- **Given** organizátor vybere skupinu „Nezaplatili“ a zadá předmět a tělo emailu
- **When** rozešle email
- **Then** email dostanou jednotlivě jen týmy ve skupině, které nejsou smazané (odesílání běží asynchronně dle NFR-PERFORMANCE-03)

#### SC-EMAIL-02 — Zvací email vynechá už přihlášené
- **Ověřuje:** FR-EMAIL-02 • **Story:** US-ORG-14
- **Given** databáze emailů napříč ročníky obsahuje i adresy týmů už přihlášených na aktuální ročník
- **When** organizátor rozešle zvací email
- **Then** už přihlášené týmy jsou ze zvacího seznamu vynechány a odeslané adresy jsou deduplikované

### STRANKA

#### SC-STRANKA-01 — Zobrazení aktivních stránek podle oprávnění
- **Ověřuje:** FR-STRANKA-01 • **Story:** US-PUBLIC-01
- **Given** existují stránky s různou viditelností a oprávněním
- **When** nepřihlášený návštěvník otevře web
- **Then** vidí jen aktivní stránky s oprávněním „kdokoliv“, seřazené podle menu ročníku

#### SC-STRANKA-02 — Archivní ročník bez datumových omezení
- **Ověřuje:** FR-STRANKA-02 • **Story:** US-PUBLIC-03
- **Given** návštěvník přepne na archivní ročník
- **When** otevře libovolnou jeho aktivní stránku
- **Then** stránka se zobrazí bez ohledu na to, jaká pravidla by platila v aktivním ročníku

#### SC-STRANKA-03 — Nouzová editace poškozené stránky
- **Ověřuje:** FR-STRANKA-03 • **Story:** US-ORG-10
- **Given** obsah stránky obsahuje znaky, které shodí standardní MD editor
- **When** organizátor použije tlačítko nouzové editace
- **Then** stránka se otevře v klasickém formuláři, kde jde obsah opravit nebo smazat

#### SC-STRANKA-04 — Správa užitečných odkazů
- **Ověřuje:** FR-STRANKA-04 • **Story:** US-ORG-09
- **Given** organizátor otevře stránku užitečných odkazů
- **When** přidá nový odkaz
- **Then** odkaz se objeví v přehledu pro rychlou navigaci během hry

### MEDIA

#### SC-MEDIA-01 — Needuhodnutelnost jména souboru
- **Ověřuje:** FR-MEDIA-01, NFR-SECURITY-03 • **Story:** US-ORG-11
- **Given** organizátor nahraje do médií neveřejný soubor (např. zadání šifry) před koncem hry
- **When** nepřihlášený uživatel zkusí uhodnout/sestavit URL souboru bez znalosti odkazu ze stránky
- **Then** soubor nejde uhodnutím najít, zatímco organizátor v administraci vidí jasný, čitelný název souboru

### MENU

#### SC-MENU-01 — Generování menu podle fáze a role
- **Ověřuje:** FR-MENU-01 • **Story:** US-ORG-12, US-TEAM-01
- **Given** stránka „Registrace“ je nastavená na zobrazení jen mezi `reg-from` a `reg-to`
- **When** nastane fáze mimo toto okno (např. po `reg-to`)
- **Then** položka registrace v menu zmizí; organizátor ji v menu vidí vždy

### SECURITY

#### SC-SECURITY-01 — Heslo je uložené jako hash
- **Ověřuje:** NFR-SECURITY-01 • **Story:** US-PUBLIC-04
- **Given** tým se zaregistruje s heslem
- **When** se podíváme do databáze na uložené heslo
- **Then** hodnota je argon2 hash, ne čitelné heslo

#### SC-SECURITY-02 — Pokus o XSS v příspěvku fóra
- **Ověřuje:** NFR-SECURITY-02 • **Story:** US-PUBLIC-12
- **Given** uživatel vloží do textu příspěvku/hodnocení skript (např. `<script>...</script>`)
- **When** příspěvek se zobrazí ostatním uživatelům
- **Then** skript se nespustí (obsah je escapovaný/sanitizovaný)

#### SC-SECURITY-03 — Neuhodnutelná cesta k neveřejnému médiu
- **Ověřuje:** NFR-SECURITY-03 • **Story:** US-ORG-11
- **Given** ve složce médií je neveřejný soubor před koncem hry
- **When** někdo zkusí přistoupit na odhadnutou/sekvenční URL
- **Then** přístup je odmítnut (soubor nejde najít bez znalosti skutečného odkazu)

#### SC-SECURITY-04 — Destruktivní akce bez CSRF tokenu je odmítnuta
- **Ověřuje:** NFR-SECURITY-04 • **Story:** (zdroj: `.claude/rules/ui.md`, ADR-0003)
- **Given** přihlášený organizátor má otevřený formulář na smazání záznamu
- **When** je odeslán POST požadavek bez platného CSRF tokenu
- **Then** požadavek je odmítnut a záznam zůstává nezměněný

### USABILITY

#### SC-USABILITY-01 — UI je v češtině
- **Ověřuje:** NFR-USABILITY-01 • **Story:** (zdroj: `00-vision.md`)
- **Given** libovolná stránka aplikace
- **When** ji otevře uživatel bez změny jazyka
- **Then** veškerý text rozhraní je česky

#### SC-USABILITY-02 — Registrační formulář na mobilu
- **Ověřuje:** NFR-USABILITY-02 • **Story:** US-PUBLIC-04
- **Given** návštěvník otevře registrační formulář na mobilním zařízení
- **When** vyplňuje a odesílá formulář
- **Then** všechna pole jsou čitelná a ovladatelná bez nutnosti zoomovat/scrollovat vodorovně

#### SC-USABILITY-03 — České řazení tabulky
- **Ověřuje:** NFR-USABILITY-03 • **Story:** (zdroj: `.claude/rules/ui.md`)
- **Given** tabulka obsahuje jména se znaky „ch“, „č“ a diakritikou
- **When** uživatel seřadí sloupec se jmény
- **Then** pořadí odpovídá české abecedě (case-insensitive, „ch“ mezi „h“ a „i“), ne ASCII pořadí

### COMPATIBILITY

#### SC-COMPATIBILITY-01 — Zobrazení historického ročníku s odlišnými parametry
- **Ověřuje:** NFR-COMPATIBILITY-01 • **Story:** (zdroj: `00-vision.md` § Problém)
- **Given** archivní ročník má jiný počet stanovišť/kategorií/systém nápověd než aktuální ročník
- **When** návštěvník otevře jeho archivní stránky
- **Then** data se zobrazí korektně bez chyb způsobených odlišnou historickou strukturou

### RELIABILITY

#### SC-RELIABILITY-01 — Hromadný email pokračuje při nedoručitelné adrese
- **Ověřuje:** NFR-RELIABILITY-01 • **Story:** US-ORG-13
- **Given** v seznamu příjemců hromadného emailu je jedna neplatná adresa
- **When** rozesílání proběhne
- **Then** ostatním adresátům email dorazí, chyba u neplatné adresy se zaloguje a rozesílání se kvůli ní nezastaví

### LEGAL

#### SC-LEGAL-01 — Registrace bez souhlasu je odmítnuta
- **Ověřuje:** NFR-LEGAL-01 • **Story:** US-PUBLIC-04
- **Given** návštěvník vyplní registrační formulář
- **When** neodškrtne souhlas se zpracováním osobních údajů
- **Then** registrace je odmítnuta a formulář vyžaduje zaškrtnutí souhlasu

#### SC-LEGAL-02 — Retenční politika osobních údajů
- **Ověřuje:** NFR-LEGAL-02 • **Story:** (zdroj: zadání organizátora, US-ORG-18)
- **Given** databáze obsahuje týmy z aktuálního i starších (archivních) ročníků s telefonními čísly
- **When** se zkontroluje uložená data po založení nového ročníku
- **Then** telefonní čísla existují jen u týmů právě zakládaného (nyní aktuálního) ročníku, zatímco jména týmů/hráčů a emaily zůstávají dostupné napříč všemi ročníky

### PERFORMANCE

#### SC-PERFORMANCE-01 — Výchozí a volitelná velikost stránky
- **Ověřuje:** NFR-PERFORMANCE-01 • **Story:** (zdroj: `10-user-stories.md` § Organizátor)
- **Given** uživatel otevře přehledovou tabulku poprvé
- **When** nezmění nastavení stránkování
- **Then** tabulka zobrazuje 50 záznamů na stránku; uživatel může velikost stránky změnit

#### SC-PERFORMANCE-02 — Odezva stránky do 1 vteřiny
- **Ověřuje:** NFR-PERFORMANCE-02 • **Story:** (zdroj: zadání organizátora)
- **Given** běžný request (např. přihlášení nebo zobrazení stránky) za standardní zátěže
- **When** je požadavek odeslán
- **Then** odpověď dorazí do 1 vteřiny

#### SC-PERFORMANCE-03 — Asynchronní běh dlouhé operace
- **Ověřuje:** NFR-PERFORMANCE-03 • **Story:** US-ORG-13
- **Given** organizátor spustí hromadné rozeslání emailu velké skupině týmů
- **When** operace běží na pozadí
- **Then** stránka zůstává použitelná, request na spuštění se okamžitě vrátí a průběh/stav se průběžně dotahuje a zobrazuje

---

## Traceabilita FR/NFR → SC

| Požadavek | Scénář(e) |
|-----------|-----------|
| FR-AUTH-01 | SC-AUTH-01, SC-AUTH-02 |
| FR-AUTH-02 | SC-AUTH-03 |
| FR-AUTH-03 | SC-AUTH-04 |
| FR-AUTH-04 | SC-AUTH-05 |
| FR-ROCNIK-01 | SC-ROCNIK-01, SC-ROCNIK-02 |
| FR-ROCNIK-02 | SC-ROCNIK-03 |
| FR-ROCNIK-03 | SC-ROCNIK-04, SC-ROCNIK-06 |
| FR-ROCNIK-04 | SC-ROCNIK-05 |
| FR-NASTAVENI-01 | SC-NASTAVENI-01 |
| FR-STANOVISTE-01 | SC-STANOVISTE-01 |
| FR-STANOVISTE-02 | SC-STANOVISTE-02, SC-STANOVISTE-03 |
| FR-SIFRY-01 | SC-SIFRY-01 |
| FR-SIFRY-02 | SC-SIFRY-02 |
| FR-SIFRY-03 | SC-SIFRY-03 |
| FR-TYM-01 | SC-TYM-01, SC-TYM-02, SC-TYM-03 |
| FR-TYM-02 | SC-TYM-04 |
| FR-TYM-03 | SC-TYM-05 |
| FR-TYM-04 | SC-TYM-06 |
| FR-TYM-05 | SC-TYM-07 |
| FR-TYM-06 | SC-TYM-08 |
| FR-TYM-07 | SC-TYM-09 |
| FR-TYM-08 | SC-TYM-10 |
| FR-TYM-09 | SC-TYM-11 |
| FR-FORUM-01 | SC-FORUM-01 |
| FR-FORUM-02 | SC-FORUM-02 |
| FR-FORUM-03 | SC-FORUM-03 |
| FR-FORUM-04 | SC-FORUM-04 |
| FR-VYSLEDKY-01 | SC-VYSLEDKY-01 |
| FR-VYSLEDKY-02 | SC-VYSLEDKY-02 |
| FR-STATEK-01 | SC-STATEK-01 |
| FR-EXPORT-01 | SC-EXPORT-01 |
| FR-OBALKY-01 | SC-OBALKY-01 |
| FR-MASKOT-01 | SC-MASKOT-01 |
| FR-EMAIL-01 | SC-EMAIL-01 |
| FR-EMAIL-02 | SC-EMAIL-02 |
| FR-STRANKA-01 | SC-STRANKA-01 |
| FR-STRANKA-02 | SC-STRANKA-02 |
| FR-STRANKA-03 | SC-STRANKA-03 |
| FR-STRANKA-04 | SC-STRANKA-04 |
| FR-MEDIA-01 | SC-MEDIA-01 |
| FR-MENU-01 | SC-MENU-01 |
| NFR-SECURITY-01 | SC-SECURITY-01 |
| NFR-SECURITY-02 | SC-SECURITY-02 |
| NFR-SECURITY-03 | SC-SECURITY-03, SC-MEDIA-01 |
| NFR-SECURITY-04 | SC-SECURITY-04 |
| NFR-USABILITY-01 | SC-USABILITY-01 |
| NFR-USABILITY-02 | SC-USABILITY-02 |
| NFR-USABILITY-03 | SC-USABILITY-03 |
| NFR-COMPATIBILITY-01 | SC-COMPATIBILITY-01 |
| NFR-RELIABILITY-01 | SC-RELIABILITY-01 |
| NFR-LEGAL-01 | SC-LEGAL-01 |
| NFR-LEGAL-02 | SC-LEGAL-02 |
| NFR-PERFORMANCE-01 | SC-PERFORMANCE-01 |
| NFR-PERFORMANCE-02 | SC-PERFORMANCE-02 |
| NFR-PERFORMANCE-03 | SC-PERFORMANCE-03 |
