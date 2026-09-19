# 10 — User stories

> Vlastník: orgové sovy • Stav: draft • Poslední revize: 2026-09-20

> Formát: *Jako [role] chci [akci], abych [přínos].*
> ID: `US-<ROLE>-xx`, kde `<ROLE>` je zkratka role (viz tabulka). Číslování je nezávislé v rámci každé role.
> **ID se po vytvoření nemění ani nepřečísluje.** Když se story přesune k jiné roli, ponechá si původní ID; prefix pak čti jako „kde vznikla", ne jako závaznou roli. Story přes více rolí zařaď pod její hlavní roli.
> Každá story má prioritu (MoSCoW: Must / Should / Could / Won't) a odkaz na požadavky (`FR-…`, případně `NFR-…` v `docs/20-requirements.md`).

## Role

| Role | Zkratka | Popis |
|------|---------|-------|
| **org** | ORG | Uživatel s plnými právy na administraci hry. V systému existuje jeden sdílený účet `org`, který používá cca 5 organizátorů se stejnými právy — nejde o samostatné účty. |
| **Návštěvník webu** | PUBLIC | Nepřihlášený uživatel. Zobrazení obecných informací o hře, přístup do minulých ročníků, během fáze registrace může registrovat tým. |
| **Registrovaný tým** | TEAM | Tým zaregistrovaný do aktuálního ročníku, zařazený mezi hrající (kapacita `max-teams` nebyla v době registrace naplněná). Může upravovat údaje o týmu, zobrazují se mu informace k platbě. |
| **Náhradník** | SPARE | Tým, který se zaregistroval až po naplnění kapacity `max-teams`. Má stejná práva jako TEAM, kromě zobrazení platebních údajů a posledních informací. |
| **Zaplacený tým** | TEAM_PAID | TEAM (nikoli SPARE), který zaplatil startovné. Navíc oproti TEAM může zobrazit poslední informace. |

### Přechody mezi rolemi

1. **Registrace** — podle aktuální naplněnosti hry (`max-teams`) se tým stane buď **TEAM**, nebo **SPARE**.
2. **Uvolnění místa** — zruší-li hrající tým účast, je nejstarší **SPARE** automaticky povýšen na **TEAM** (viz US-TEAM-03).
3. **Platba** — zaplacením startovného se z **TEAM** stává navíc **TEAM_PAID**. Platba je atribut týmu, ne náhrada role SPARE/TEAM — dokud je tým SPARE, platbu neřeší.

## Návštěvník webu

### US-PUBLIC-01 — Zobrazení webu

- **Jako** náhodný návštěvník webu
- **chci** získat informace o aktuálním ročníku
- **abych** mohl zvážit svoji účast
- **Priorita:** Must
- **Souvisí s požadavky:** FR-STRANKA-01
- **Poznámky:**
  - Uživateli se zobrazí stránky se základními informacemi o hře o aktuálním ročníku
  - Stránky jsou seřazeny podle menu daného ročníku
  - Zobrazují se pouze stránky, které jsou označeny jako aktivní a je u nich oprávnění kdokoliv
  - Úvodní stránka (/index) je proti současné implementaci dynamická — horní část se generuje z aktuálních dat ročníku v databázi (start a konec hry, registrace od–do, platba do, výše startovného), spodní část je upravitelný MD obsah. Je třeba vyřešit způsob zadávání údajů do horní části (makra v textu, nebo pevně generovaná horní část + MD dole).
  - Pozn.: dřívější samostatná story US-PUBLIC-02 (Informace o hře) byla sloučena sem, protože popisovala stejnou potřebu. ID `US-PUBLIC-02` zůstává neobsazené (nepřečíslováváme navazující stories).


### US-PUBLIC-03 — Zobrazení archivních ročníků

- **Jako** náhodný návštěvník webu
- **chci** získat informace o minulých ročnících
- **abych** mohl mít představu o náročnosti hry
- **Priorita:** Must
- **Souvisí s požadavky:** FR-STRANKA-02
- **Poznámky:**
  - V menu bude rozbalovací menu s vygenerovanými ročníky seřazenými sestupně 
  - V rámci archivního ročníku se budou zobrazovat všechny stránky označené za aktivní. Neuvažují se omezující pravidla na datumy
  - Menu bude platné podle nastavení menu daného ročníku

### US-PUBLIC-04 — Registrace
- **Jako** náhodný návštěvník webu
- **chci** se přihlásit na aktuální ročník
- **abych** mohl jít na Sovu
- **Priorita:** Must
- **Souvisí s požadavky:** FR-TYM-01, NFR-SECURITY-01, NFR-USABILITY-02, NFR-LEGAL-01
- **Poznámky:**
  - Formulář je aktivní pouze mezi datumy registrace od, registrace do včetně těchto datumu
  - Po skončení hry se formulář vůbec nezobrazuje v menu. Archivní ročníky také nezobrazují registraci.
  - Registrační formulář se nezobrazuje organizátorům a týmům, které jsou přihlášené na stránky
  - Mimo datumy se ne stránce zobrazuje pouze informace, od kdy do kdy běží registrace
  - Na registračním formuláři jsou položky Název týmu, Login, Heslo, Znovu heslo, email, Mobil. Tyto položky jsou povinné a lze případně dodatečně změnit.
  Další položky je URL týmu, a pak 5 možných hráčů s údaji Jméno hráče, Veřejné jméno hráče, Město a Věk. Jméno hráče je povinné, zbytek je volitelný.
  - Formulář obsahuje dva checkboxy Všichni hráči byli seznámeni a souhlasí s pravidly a charakterem hry. Všichni účastnici dávají souhlas se shromažďováním osobních údajů pro účel uspořádání hry a evidenci hráčů, výsledků. Které je nutné zaškrtnout před registrací.  
  - Heslo musí být alespoň 5 znaků.
  - Kontrola formuláře probíhá před odesláním v prohlížeči a pak i na serveru.
  - Jméno týmu a login musí být unikátní v rámci aktuální ročníku. Porušení unikátnosti se stránka zobrazí s varováním a vyplněnými informacemi.
  - Nově zařadíme pro registraci vyřešení captcha.
  - Formulář musí být čitelný i na mobilu.
  - Během registrace je týmu přiřazen náhodný unikátní maskot, který se již nebude měnit.
  - Heslo je uloženo v osolném hashi (argon2)

### US-PUBLIC-05 — Přihlášení
- **Jako** náhodný návštěvník webu
- **chci** se přihlásit pod svým loginem
- **abych** se dostal k informacím o svém týmu
- **Priorita:** Must
- **Souvisí s požadavky:** FR-AUTH-01
- **Poznámky:**
  - V aktivním ročníku se návštěvník webu může přihlásit svým loginem
  - Formulář obsahuje pole pro zadání loginu a hesla. Dole je odkaz na reset hesla.
  - V databázi je jeden uživatel org označený jako admin. Po jeho přihlášení se má přístup k administraci a to pro minulé ročníky.
  - Po přihlášení se návštěvník webu přesouvá do role TEAM nebo SPARE
  - Stránka je dostupná, pouze pokud je návštěvník nepřihlášený.

### US-PUBLIC-06 — Reset hesla
- **Jako** náhodný návštěvník webu
- **chci** obnovit zapomenuté heslo
- **abych** se dokázal přihlásit
- **Priorita:** Must
- **Souvisí s požadavky:** FR-AUTH-02
- **Poznámky:**
  - Platí pouze pro aktivní ročník
  - Formulář obsahuje pole pro zadání emailu
  - Na email se pošle dočasný odkaz vedoucí na formulář, kde jde zadat nové heslo. Heslo se zadává 2x.
  - Předpokládá se, že systém má správně nastavený poštovní server  
  - Stránka je dostupná, pouze pokud je návštěvník nepřihlášený.

### US-PUBLIC-07 — Týmy
- **Jako** náhodný návštěvník webu
- **chci** zobrazit přihlášené týmy
- **abych** se podíval na účastníky
- **Priorita:** Must
- **Souvisí s požadavky:** FR-TYM-02
- **Poznámky:**
  - Stránka je dostupná přes všechny fáze ročníku
  - Týmy se zobrazují v tabulce primárně seřazené podle datumu přihlášení
  - V tabulce se nezobrazují týmu označené jako smazané
  - Tabulka obsahuje sloupce: Název týmu, Hráči, Startovné, Stav.
  - Sloupec Hráči se vytvoří spojením Veřejných jmen hráčů oddělených čárkou. Pokud není pole vyplnění nahradí se za Anonymous
  - Sloupec startovné obsahuje hodnoty zaplaceno, nezaplaceno
  - Sloupec stav obsahuje hodnoty Hrající, Náhradníci
  - Tabulka lze třídit podle sloupců a jde i podle nich vyhledávat subřetezce
  - Po touto tabulkou je Statistika týmů, která obsahuje sloupce týmy a hráči. Na řádcích jsou Zaplaceno, Nezaplaceno, Náhradníci a Celkově
  - Níže je Statistika hráčů. Sloupce Průměrný věk, minimální věk, maximální věk. Řádky jsou Zaplaceno, Nezaplaceno, Náhradníci a Celkově. Pokud není vyplněný věk do statistiky se nepočítá.
  - Poslední je tabulka Statistika měst. Seřazeno podle počtu hráčů z daného města sestupně.
  - Nevyplněná města se vynechávají.
  - Seskupování se bere bez rozlišení velkých a malých písmen a bez diakritiky.
  - Statistika měst je opět tříditelná podle sloupců a je zde filtrování podle města.

### US-PUBLIC-08 — Fórum
- **Jako** náhodný návštěvník webu
- **chci** zobrazit různé sekce fóra
- **abych** mohl komunikovat s ostatními účastníky
- **Priorita:** Must
- **Souvisí s požadavky:** FR-FORUM-01
- **Poznámky:**
  - Na začátku se zobrazuje tabulka sekcí fora. Některé sekce nemusí být vždy aktivní. Typicky sekce navázané na šifry před ukončením hry.
  - Sekce jsou seřazený podle pořadí.
  - Vedle jména sekce se zobrazuje čas a datum posledního příspěvku.
  
### US-PUBLIC-09 — Sekce fóra
- **Jako** náhodný návštěvník webu
- **chci** zobrazit a zapsat text do nějaké sekce fóra
- **abych** mohl komunikovat s ostatními účastníky
- **Priorita:** Must
- **Souvisí s požadavky:** FR-FORUM-02
- **Poznámky:**
  - Nahoře stránky se zobrazuje formulář pro odeslání příspěvku.
  - Formulář obsahuje Kdo, které je převyplněné jménem týmu, pokud je tým přihlášený. Dále je text komentáře a tlačítko odeslat.
  - Níže jsou zobrazeny seřazeny příspěvky od nejmladšího k nejstaršímu.
  - Seznam příspěvků je stránkovaný.
  - V záhlaví příspěvku se zobrazuje autor a čas poslání
  - Pokud je přihlášen org, tak vidí i IP, adresu, odkud byl příspěvek zadán

### US-PUBLIC-10 — Výsledky
- **Jako** náhodný návštěvník webu
- **chci** zobrazit informace po hře
- **abych** věděl, jak to dopadlo
- **Priorita:** Must
- **Souvisí s požadavky:** FR-VYSLEDKY-01
- **Poznámky:**
   - Stránka je aktivní až po skončení hry a přetrvává i v archívu
  - Průběh hry, výsledky, nápovědy a řešení během hry zpracovává externí aplikace statek, kam se team hlásí přes maskota
  - Po hře bude dostupná stránka, na které budou odkazy na různé části statku jako pořadí, nasazení apod.
  - Protože jsou výsledky externě hostovány a není zaručena jejich dlouhodobá dostupnost, po hře dojde k jejich synchronizaci do interní databáze. 
  - Na této stránce se budou zobrazovat výsledky z interní databáze.
  - Poznámka, archivní ročníky nebyly zpracovány pomocí statku a výsledky jsou uchovány ve formě HTML stránek v archívu. Bude dobré vymyslet způsob jejich importu do databáze. Buď automaticky nebo ve správě přes formulář.
  - Historicky jsme měli i kategorie Pohoda a Výzva, které se lišily počtem šifer a samostatnými žebříčky. Možná v budoucnu se k tomu vrátíme, web by to měl podporovat. 

### US-PUBLIC-11 — Reportáže
- **Jako** náhodný návštěvník webu
- **chci** vidět reportáže týmů a hráčů
- **abych** si přečetl zážitky jiných
- **Priorita:** Must
- **Souvisí s požadavky:** FR-VYSLEDKY-02
- **Poznámky:**
 - Stránka je aktivní až po skončení hry a přetrvává i v archívu
 - Tým může vyplnit URL své reportáže
 - Stránka projde seznam týmů a nabídne odkazy na reportáže. Pozor na zadávání maligních odkazů. Je otázka jak to zjistit?
 - V nastavení ročníku přidáme parametry URL reportáže orgů a URL fotek na daný ročník. Pokud budou vyplněny, tak se zobrazí v samostatné kategorii Orgové.

### US-PUBLIC-12 — Šifry
- **Jako** náhodný návštěvník webu
- **chci** vidět šifry
- **abych** věděl, jak se šifra měla řešit a mohl ji ohodnotit
- **Priorita:** Must
- **Souvisí s požadavky:** FR-SIFRY-02, FR-SIFRY-03, NFR-SECURITY-02
- **Poznámky:**
  - Stránka je aktivní až po skončení hry a přetrvává i v archívu, ale bez možnosti vkládat komentáře do fóra a hodnotit šifru
  - V databázi pro každou šifru budou následující údaje a soubory: pdf zadání šifry, obrázky se zadáním šifry, text nápovědy (historicky bylo nápověd více), penalizace za nápovědu, někdy historicky má nápověda podobu obrázků, řešení šifry v pdf, řešení šifry v podobě obrázků a slovního popisu zadaného jako MD. 
  - V horní části stránky bude rozcestník na šifry daného ročníku. Rozcestník bude umožňovat přejít na předchozí a další šifru, ale třeba formou výběrového pole, přejít na libovolnou jinou šifru.
  - V horní části bude výběrové pole s ročníky seřazenými sestupně, aby se šlo rychle dostat na šifry z minulých ročníků
  - Proti současné podobě se bude zobrazovat zadání, pod ním bude schovaná nápověda a řešení, které se zobrazí kliknutím na nějaký ovládací prvek (tlačítko, div, ...)
  - Budou zde odkazy na stáhnutí pdf verzí zadání a řešení
  - Pod zadáním bude možnost hodnotit obtížnost a obliba. V aktuálním ročníku mohou i nepřihlášení týmy hodnotit na stupnici 1 až 10. V archivním ročníku se pouze zobrazuje statika. Bude dobré zobrazovat počet hlasujících.
  - Ke každé šifře je provázaná sekce fóra. Pod šifrou se zobrazuje pouze dané sekce s komentáři seřazenými sestupně. Vše viz US-PUBLIC-09
  - V aktuální ročníku tým může poslat komentář (US-PUBLIC-09)
  - Sekce fóra se bude vytvářet automaticky a aktivovat po hře.
  - Vstupní pole budou chráněny proti vkládání maligních řetězců (XSS, ...)
  - Zvážit možnost rozbalení mapy, kde bude vidět umístění stanoviště a trasy. Aktuální stanoviště by mohlo být zvýrazněno.
  - Pozor: v archivním režimu nesmí být možnost zobrazit šifry pro aktivní ročník, pokud ještě hra neskončila.

### US-PUBLIC-13 — Trasa
- **Jako** náhodný návštěvník webu
- **chci** vidět trasu šifry
- **abych** věděl, kudy šla cesta
- **Priorita:** Must
- **Souvisí s požadavky:** FR-STANOVISTE-02
- **Poznámky:**
  - Stránka je aktivní až po skončení hry a přetrvává i v archívu
  - V databázi je umístění stanovišť s GPS souřadnicemi
  - Zobrazení stanovišť na mapě a jejich propojení, aby se ukázala trasa
  - Pozor na možnost různých kategorií, které mohou mít jinou podobu trasy. Trasa výzvy byla stejná jako Pohody, pouze se v trase vnořil "pytlík" šifer označený písmeny. Např. Pohoda měla stanoviště 5, 6. Výzvy pak stanoviště 5, 5a, 5b, 5c, 6. Pytlík by mohl být znázorněn jinou barvou.
  - Kliknutím na stanoviště se otevře stránka s danou šifrou.
  - Checkbox, který povolí zakáže zobrazování spojovacích čar.
  - V horní části stránku bude výběrové pole s ostatními ročníky, pro rychlé přepnutí. Zvážit možnost, že na jedné mapě se zobrazí trasy za trasy z více ročníků. Například v podobě, že si zvolím ročník kliknu na přidat a v horní části se zobrazí barevná legenda s kříkem pro odebrání ročníku ze zobrazení. Jinými ročníky budou zobrazeny odlišnými barvami.
  - Pozor: v archivním režimu nesmí být možnost zobrazit trasu pro aktivní ročník, pokud ještě hra neskončila.
    
  
## Registrovaný tým

### US-TEAM-01 — Můj tým

- **Jako** přihlášený uživatel 
- **chci** vidět menu Můj tým
- **abych** mohl vidět a případně editovat své údaje
- **Priorita:** Must
- **Souvisí s požadavky:** FR-MENU-01
- **Poznámky:**
  - Zobrazení odkazů v menu na editaci údajů o týmu a zobrazení posledních informací a odhlášení, apod.

### US-TEAM-02 — Odhlášení

- **Jako** přihlášený uživatel 
- **chci** se odhlásit od stránek
- **abych** neviděl soukromé informace
- **Priorita:** Must
- **Souvisí s požadavky:** FR-AUTH-03
- **Poznámky:**  

### US-TEAM-03 — Zrušení registrace

- **Jako** přihlášený uživatel 
- **chci** se zrušit účast na hře
- **abych** se nemusel zúčastnit hry
- **Priorita:** Must
- **Souvisí s požadavky:** FR-TYM-03
- **Poznámky:**  
  - Stránka je dostupná jen do začátku hry. Když odstartuje hra, tým nemůže zrušit účast.
  - Zrušení je třeba potvrdit checkboxem
  - Po dokončení zrušení registrace dojde k případnému povolení prvního náhradníka.
  - Povolenému náhradníku se automaticky pošle email o změně jeho stavu.
  - Zrušení registrace se provádí nastavením příznaku smazané. Organizátoři mají přístup k informacím i o deaktivovaném týmu.

### US-TEAM-04 — Změna hesla

- **Jako** přihlášený uživatel 
- **chci** si kdykoli změnit heslo
- **abych** udržel svůj účet zabezpečený
- **Priorita:** Must
- **Souvisí s požadavky:** FR-AUTH-04
- **Poznámky:**
  - Vyžaduje zadání stávajícího hesla
  - Nové heslo se musí lišit od stávajícího
  - Po úspěšné změně se zneplatní ostatní relace téhož uživatele (aktuální zůstává)

### US-TEAM-05 — Údaje o týmu

- **Jako** přihlášený uživatel 
- **chci** zobrazit svůj profil
- **abych** viděl údaje o týmu a případně informace pro platbu
- **Priorita:** Must
- **Souvisí s požadavky:** FR-TYM-04
- **Poznámky:**
  - Stránka je aktivní pouze pro aktivní ročník
  - Stránka není určená pro orgy
  - Stránka obsahuje tabulku s informacemi o týmu: Název, maskot, Přihlášení do hry přes QR na seslost.cz, login, mobil, Složení, Veřejné složení, Zaplaceno a Stav
  - Pokud tým nemá zaplaceno, zobrazují se mu platební údaje včetně QR kódu.
  - Před zahájením hry je zde tlačítko vedoucí na formulář ke změně údajů o týmu.

### US-TEAM-06 — Změna údaje o týmu

- **Jako** přihlášený uživatel 
- **chci** modifikovat svůj profil
- **abych** aktualizoval složení týmu apod.
- **Priorita:** Must
- **Souvisí s požadavky:** FR-TYM-05
- **Poznámky:**
  - Stránka je aktivní pouze pro aktivní ročník a před zahájením hry
  - Stránka není určená pro orgy
  - Formulář vypadá podobně jako u registrace, ale již zde nejsou checkboxy a pole pro heslo. Navíc je zde pole na URL s reportáží.
  - Nově půjde změnit i login - jen se kontroluje unikátnost.

## Náhradníci — SPARE

Náhradník dědí všechny stories role TEAM ([Registrovaný tým](#registrovaný-tým)) beze změny, kromě výjimek popsaných v US-SPARE-01.

### US-SPARE-01 — Omezení oproti hrajícímu týmu

- **Jako** náhradník (SPARE)
- **chci** mít přístup ke stejným funkcím jako hrající tým
- **abych** mohl sledovat přípravu hry a byl připraven na případné povýšení
- **Priorita:** Must
- **Souvisí s požadavky:** FR-TYM-06
- **Poznámky:**
  - Platí všechny stories role TEAM (US-TEAM-01 až US-TEAM-06), kromě výjimek níže.
  - Na stránce „Údaje o týmu" (US-TEAM-05) se nezobrazují platební údaje ani QR kód pro platbu.
  - Nevidí stránku/sekci s posledními informacemi (US-TEAM_PAID-01) — ta je dostupná až po povýšení na TEAM a zaplacení.
  - Startovné se náhradníkovi neřeší, dokud není povýšen na TEAM (viz [Role → Přechody mezi rolemi](#přechody-mezi-rolemi)).

## Zaplacený tým — TEAM_PAID

### US-TEAM_PAID-01 — Poslední informace

- **Jako** zaplacený tým (TEAM_PAID)
- **chci** vidět poslední informace před hrou
- **abych** byl na start hry dobře připraven
- **Priorita:** Must
- **Souvisí s požadavky:** FR-TYM-07
- **Poznámky:**
  - Stránka/sekce se zpřístupní až po zaplacení startovného, ve fázi „Zobrazení posledních informací" (viz `00-vision.md`), tj. od data `last-info`.
  - Náhradníkům (SPARE) se nezobrazuje — přístup mají pouze hrající zaplacené týmy (role TEAM_PAID vyžaduje TEAM, ne SPARE).
  - TODO: upřesnit obsah a formát stránky (MD, odkaz, PDF?).

## Organizátor (ORG)
Pro níže uvedené scénáře platí tyto obecné požadavky:

 - Všechny níže uvedené scénáře se týkají pouze uživatele přihlášeného jako organizátor. Všem ostatním při zadání URL musí být odmítnut přístup.
 - Spravovat lze i archivní ročníky. Minimálně bude třeba provést import historických dat.
 - Správa bude mít zpravidla podobu přehledové tabulky, která půjde třídit a filtrovat podle sloupců. Třídění a filtrování by mělo přežít spuštění editačního formuláře, uložení/zrušení změny a návrat do přehledové tabulky.
 - Pokud bude mít přehledová tabulka více jak n záznamů, bude použito stránkování.
 - V tabulce půjde vybrat více položek (možnost i mít možnost vybrat všechny položky) a provést nad ní hromadnou akci.

### Správa ročníků

### US-ORG-01 — Správa ročníků

- **Jako** organizátor   
- **chci** upravovat parametry jednotlivých ročníků hry
- **abych** nastavil konkrétní podobu hry
- **Priorita:** Must
- **Souvisí s požadavky:** FR-ROCNIK-01, FR-ROCNIK-02
- **Poznámky:**
  - Aktuální tabulka year obsahuje pouze ročník. Přesuneme sem z nastavení parametry, které se týkají konkrétního ročníku.
  - Ročník bude obsahovat tyto informace: min-players, max-players, max-teams,  max-team-game-index,min-players-when-check-game-index, payment-price, payment-unit, reg-from, reg-to, payment-to, last-info, start-time, end-time. 
  - start-time a end-time se zadávají s přesností na minuty. Zbytek datumů je s přesností na dny.
  - min-players, max-players, max-teams, max-team-game-index, min-players-when-check-game-index, payment-price jsou čísla.
  - payment-price nemusí být zadaná při vytváření nového ročníku, může obsahovat NULL hodnotu. To se promítne do stránky /index a znemožní to generování QR kódu. Cena za hru se stanovuje po té, co jsou známy šifry a náklady na ně.
  - Kliknutím na edit se otevře formulář, kde půjde údaje upravit.
  - Pravidla pro datumy reg-from < reg-to, payment-to < start-time, last-info < start-time, start-time < end-time.
  - Pod tabulkou parametrů bude tabulka s kategoriemi. Standardně bude jedna kategorie Pohoda, ale půjde přidat nebo odebrat i další kategorie.
  - Ve hře musí být minimálně 1 kategorie. 
  - Ročníky nelze mazat.
  - Nový ročník se přidává přes samostatnou volbu v menu Nový ročník 

### US-ORG-02 — Správa nastavení
- **Jako** organizátor   
- **chci** upravovat parametry webové stránky
- **abych** nastavil chování aplikace
- **Priorita:** Must
- **Souvisí s požadavky:** FR-NASTAVENI-01
- **Poznámky:**
  - Jedná se o změnu proti současné implementaci, kdy nastavení je spojené s nastavením ročníků
  - Aktuálně se jedná o parametry 
    - base-url
    - Nastavení poštovního serveru: email-smtp-auth, email-smtp-from, email-smtp-password, email-smtp-port, email-smtp-server, email-smtp-user (zřejmě budeme přecházet na gmail.com)
    - účet pro platbu startovného pro generování QR: payment-account, payment-iban 
    - přístup na statek: trakar-login, trakar-token
  - Opět správa podobu přehledové tabulky
  - Parametry lze editovat, přidávat nové i mazat. 

### US-ORG-03 — Správa stanovišť
- **Jako** organizátor   
- **chci** spravovat umístění stanovišť v daném ročníku
- **abych** vytvořil trasu hry
- **Priorita:** Must
- **Souvisí s požadavky:** FR-STANOVISTE-01
- **Poznámky:**
  - Trasa se skládá z jednotlivých stanovišť, podle pořadí v tabulce. První stanoviště je start, poslední stanoviště je cíl.
  - Pokud má hra více kategorií, tak stanoviště mohu přiřadit jedné nebo více kategorií. Pokud má hra pouze jednu kategorii, automaticky se vyplňuje jedna kategorie.
  - U stanoviště mám tyto položky: pořadí, číselné značení šifry, název, přesný popis včetně upřesnítka, který se bude vracet jako řešení, upřesnítko, GPS souřadnice. Poloha stanoviště se zadává kliknutím do mapy nebo zadání souřadnic z mapy.com
  - Číselné značení šifry bude zpravidla číslo, ale v případě více kategorií to může být i číslo s písmenem.
  - Stanoviště lze přidávat, odebírat, editovat a měnit jejich pořadí v tabulce.
  - Pod tabulkou stanovišť se ukazují na mapě včetně propojovacích čar.
  - Pokud je více kategorií, tak se nejprve vykreslí propoje delší kategorie a pak přesní propoje kratší kategorie. Tím se zvýrazní "pytlík" stanovišť.
  - Ve spolupráci se správou šifer se pak na stanoviště přiřazují šifry. V tabulce stanovišť se mohou ukazovat již přiřazené šifry.
  - Trasa může vznikat nezávisle na šifrách. Zpravidla bude dříve trasa než budou známy všechny šifry.
  - V průběhu přípravy se může stát, že šifru přesuneme ze stanoviště na stanoviště.

### US-ORG-04 — Správa šifer
- **Jako** organizátor   
- **chci** spravovat šifry
- **abych** vytvořil hru
- **Priorita:** Must
- **Souvisí s požadavky:** FR-SIFRY-01
- **Poznámky:**
  - Základní informace o šifře jsou: Název, kód, poznámka orgů
  - Zadání šifry se skládá: pdf souboru a jednoho obrázku
  - Řešení šifry se skládá: pdf souboru a MD stránky, která může obsahovat více obrázků a případně informace, po jaké době je řešení zveřejněno v podobě počtu minut
  - Nápověda: Unifikovaný řetězec, počet trestných minut. Z historického hlediska, kdy se podávalo více nápověď, tak řetězec může být rozdělen do více řádků, které reprezentují jednotlivé nápovědy.
  - Na úvodní šifře z pravidla bývá nápověda vyvěšovaná po částech. V systému tedy bude možnost nápovědu vytvořit jako MD s možností vložit různé obrázky, komentáře apod.
  - Šifru lze přiřadit nějakému stanovišti. Na jednom stanovišti může být jen jedna šifra.
  - Číselné značení šifry, umístění, upřesnítko se přebírá ze stanoviště.
  - Pokud bude šifra přiřazená ke stanovišti, vygeneruje se pro ní QR kód. URL bude mít zpravidla podobu https://seslost.cz/l/kód. https://seslost.cz/l bych umístil do nastavení. Do středu QR kódu bude vložené logo hradecké sovy. Umístění souboru s logem zase bude v nastavení. Navíc v dolním pravém rohu bude drobně vykresleno číselné označení stanoviště.
  - S šifrou je spojené její hodnocení - obtížnost a líbí. Je třeba vyřešit, jak toto ukládat.
  - S šifrou je spojené fórum, při vytvoření šifry automaticky vzniká sekce fóra pojmenovaná podle jména šifry. V čase se jméno šifry může měnit, bude se měnit i jméno sekce fóra. Fórum bude zablokované. Automaticky se odblokuje až po skončení hry.

### US-ORG-05 —Správa týmů
- **Jako** organizátor   
- **chci** spravovat týmy
- **abych** viděl a upravoval jejich údaje
- **Priorita:** Must
- **Souvisí s požadavky:** FR-TYM-08
- **Poznámky:**
  - V tabulce se zobrazují týmy: id_týmu, KI index (Kuka index, viz `glossary.md`), Tým, Složení, Zaplaceno, Stav. Složení se poskládá z neveřejných jmen a dohledá se k nim KI index, pokud existuje. Tabulka lze určitě třídit a filtrovat.
  - Každý tým lze editovat spuštěním formuláře pro editaci.
  - Vedle týmu je tlačítko, které organizátora přepne do pohledu z týmu - proběhne vlastně login bez zadání hesla.
  - Jde označit více týmů najednou a provést s nimi hromadné akce (označit jako smazané, označit, že zaplatili)

### US-ORG-06 — Editace týmů
- **Jako** organizátor   
- **chci** upravovat údaje týmu
- **abych** upravoval jejich údaje
- **Priorita:** Must
- **Souvisí s požadavky:** FR-TYM-09
- **Poznámky:**
  - U týmu mohu upravovat údaje jméno, login, email, telefon, url na reportáž, web týmu a informace o hráčích.
  - Jména login, email musí být unikátní napříč aktuálním ročníkem. Email musí být unikátní, protože přes něj probíhá obnova hesla.
  - U týmu jde označit, že zaplatil. 
  - Org může manuálně označit tým, že je nebo není náhradník.
  - Org může označit tým, že je smazaný. Pak dojde k automatickému přepočtu náhradníků. Náhradník, který se stane hrajícím týmem o tomto dostane email.
  - Maskot nejde měnit, jen se zobrazuje.

### US-ORG-07 — Správa Fóra
- **Jako** organizátor   
- **chci** spravovat sekce fóra
- **abych** mohl řídit diskuzi na webu
- **Priorita:** Must
- **Souvisí s požadavky:** FR-FORUM-03
- **Poznámky:**
  - Tabulka obsahuje sekce fora - Pořadí, Název, viditelnost
  - Na začátku ročníku je automaticky vytvořena sekce Obecná diskuze, která je hned dostupná
  - S vytvářením šifer vznikají nové sekce fóra, ale ty jsou nedostupné. Aktivují se až po konci hry
  - Jde přidávat nové sekce, které nemusí mít návaznost na šifry
  - Sekce provázané se šiframi nejde smazat, mažou se automaticky se smazáním šifry.
  - Pokud se změní název šifry, změní se i název provázané sekce.
  - Hromadná akce na aktivaci nebo deaktivaci fóra.
  - Ve správně stránek lze ke stránce připnout sekci fóra.
  - Sekce lze editovat - jméno, pořadí, viditelnost.

### US-ORG-08 — Správa Maskotů
- **Jako** organizátor   
- **chci** upravovat seznam maskotů
- **abych** připravil dostatek unikátních maskotů pro hru
- **Priorita:** Must
- **Souvisí s požadavky:** FR-MASKOT-01
- **Poznámky:**
  - Tabulka obsahuje seznam maskotů, unikátních v rámci jednoho ročníku — napříč ročníky se duplicity mohou opakovat. Maskot je zpravidla podstatné hmotné jméno, které je krátké a neobsahuje diakritiku.
  - Maskot slouží pro identifikaci týmu během hry do externího systému statek.
  - Je možné vložit nového maskota.
  - Je možné upravit maskota.

### US-ORG-09 — Užitečné odkazy
- **Jako** organizátor 
- **chci** mít přehled o důležitých URL odkazech
- **abych** během hry mohl rychlé přecházet mezi různými systémy
- **Priorita:** Must
- **Souvisí s požadavky:** FR-STRANKA-04
- **Poznámky:**
  - Seznam odkazů musí být editovatelný. V aktuální podobě je pevně daný. Může to být třeba formou MD stránky.  

### US-ORG-10 — Správa Stránek
- **Jako** organizátor   
- **chci** spravovat stránky
- **abych** vytvářel obsah webu
- **Priorita:** Must
- **Souvisí s požadavky:** FR-STRANKA-03
- **Poznámky:**
  - Některé stránky jsou naprogramované a poskytují dynamický obsah. Ale web se skládá i ze statických stránek.
  - Tabulka obsahuje přehled statických stránek a umožňuje s nimi dělat hromadné operace - změna viditelnost, změna oprávnění.
  - Viditelnost je přepínač, který určuje, zda stránku vidí pouze organizátor nebo ji jiná role.
  - Přidáme ještě přepínač zobrazit pouze v Aktivním ročníku. Pokud je zapnutá, tak stránka bude pro běžné uživatele dostupná pouze v aktuálním ročníku.
  - Přístupová práva určují, pokud je stránka aktivní, která role ji má přístupnou.
  - Hierarchie rolí: organizátor, zaplatili, hrající, náhradníci, kdokoliv.
  - Stránku lze editovat. Nastavuje se její interní jméno, relativní část url, přístupová práva, stav, přiřazení k sekci fóra a hlavně její obsah. 
  - Obsah se zadává v podobě MD. Pro editaci se používá https://pandao.github.io/editor.md/. 
  - Po ukončení editace se stránka přesměruje na seznam stránek nebo přímo na stránku. 
  - Pokud je statická stránka zobrazena v roli org, nahoře má tlačítko Editovat, které přepíná do editačního režimu.
  - Pozor: stalo se, že do MD textu se dostaly nějaké nekompatibilní znaky, které shodily MD editor a pak nebyla možnost jak stránku opravit. Do tabulky bych přidal tlačítko nouzové editace, které stránku zobrazí pouze v klasickém formuláři. Půjde obsah opravit/promazat.

### US-ORG-11 — Správa Médií
- **Jako** organizátor   
- **chci** spravovat média ve složce static
- **abych** zpřístupnil na stránkách i netextový obsah
- **Priorita:** Must
- **Souvisí s požadavky:** FR-MEDIA-01, NFR-SECURITY-03
- **Poznámky:**
  - Stránka umožňuje navigaci ve složce static na disku
  - Org má možnost vytvářet nové složky.
  - Org má možnost mazat prázdné složky.
  - Org má možnost do složky nahrávat soubory jako pdf, obrázky apod.
  - Org má možnost soubor smazat.
  - Na soubory se bude odkazovat v rámci statických stránek.
  - Bezpečnostní požadavek: ve složce se mohou ještě před hrou objevit zadání šifer, řešení apod. Nesmí být možnost provést útok hádáním jména souboru a dostat se tak předčasně k zakázanému obsahu. Na druhou stranu ve složce musí být jasné, o jaké soubory se jedná. Není akceptovatelné, že by se jména souborů generovala náhodně a org musel v MD dohledávat náhodná jména souborů.
  
### US-ORG-12 — Správa Menu
- **Jako** organizátor   
- **chci** upravovat zobrazení menu
- **abych** organizovat stránky do hierarchické struktury.
- **Priorita:** Must
- **Souvisí s požadavky:** FR-MENU-01
- **Poznámky:**
  - Menu je automaticky generované na základě fáze hry a role uživatele.
  - Položky menu mohou být typu: Skupina, interní statická stránka, systémová stránka, která implementuje dynamickou stránku (registration, teams, login, ...) , externí odkaz. 
  - Pořadí položek lze měnit. 
  - Položky ve skupině Administrace jsou dostupné pouze pro orgy. Tato skupina bude vytvořena staticky přímo v programovém kódu.
  - Menu je unikátní pro každý ročník, protože může obsahovat různé stránky.
  - Pravidla jestli se položka v menu zobrazí:
     - statická stránka: je aktivní, odpovídá oprávnění stránky s rolí uživatele, je aktuální rok, pokud je to nastavená ná stránce. Org vidí stránku vždy.
     - dynamická stránka: teams, registration, login, results, ... zobrazování se řídí interními pravidly, které jsou navázané na fáze hry. Viz jednotlivé požadavky.
     - externí stránky: kdykoliv, zpravidla se nepoužívá.
  - Struktura menu má podobu seznamu. Položka skupina menu zahajuje skupinu a následující položky spadají do tohoto menu. Výjimku tvoří stránky označené v položce menu jako Samostatná položka mimo submenu.
  - Výskyt nové položky skupina zahajuje novou Skupinu.
  - Pokud skupina položek neobsahuje žádnou položku, která má povolené být zobrazena, skupina se nezobrazí.
  - Na konci seznamu se automaticky generovaná skupina Ročníky, která obsahuje odkazy na další ročník.

### US-ORG-13 — Emaily ročníku
- **Jako** organizátor   
- **chci** rozeslat hromadný email různým skupinám uživatelů
- **abych** je informoval o aktuálním ročníku
- **Priorita:** Must
- **Souvisí s požadavky:** FR-EMAIL-01, NFR-RELIABILITY-01
- **Poznámky:**
  - Systém bude používat poštovní server z nastavení
  - Org si může vybrat předpřipravené skupiny: Všichni, Zaplatili, Nezaplatili, Náhradníci. Ignorují se týmy označené za smazané.
  - Org bude moci zadat svůj vlastní seznam emailů
  - Org zadá předmět a tělo emailu. Půjde přiložit nějaký soubor jako posledni_info.pdf
  - Emaily se budou posílat jednotlivě, protože externí služby rozesílání na mnoho adres často zablokují jako spam. Pravděpodobně bude potřeba vyřešit asynchronní posílání emailů s nějakými logy. Je potřeba se dozvědět, že nějaká adresa není dostupná apod.

### US-ORG-14 —  Zvací email
- **Jako** organizátor   
- **chci** jednou ročně rozeslat zvací email na seznam emailů i z minulých let
- **abych** je pozval na hru
- **Priorita:** Must
- **Souvisí s požadavky:** FR-EMAIL-02
- **Poznámky:**
  - Potřebujeme mít databázi emailů napříč ročníky.
  - Aktuálně mám seznam platných adres, které potřebuji do tabulky naimportovat.
  - Tabulka se automaticky bude doplňovat emaily z aktuálního ročníku.
  - Tabulka musí být deduplikovaná (pozor na velikost písmen)
  - Zvací email se může rozesílat i během běžící registrace. Ze seznamu je třeba vynechat emaily teamů již přihlášených na aktuální ročník.
  - Seznam bude zastarávat a část emailů bude nedostupná. Pokud email nejde odeslat, bude ze seznamu odstraněn. Automaticky/ručně.
  - Na konec zvacího dopisu se bude přidat věta, že pokud nechce dostávat tyto emaily klikněte na subscription. To je třeba připravit.

### US-ORG-15 — Obálky
- **Jako** organizátor   
- **chci** upravit obsah startovních obálek a vytisknout je
- **abych** připravil startovní obálky
- **Priorita:** Must
- **Souvisí s požadavky:** FR-OBALKY-01
- **Poznámky:**
  - Proti stávající verzi potřebuji ve webovém prostředí mít možnost upravit vzor obálky.
  - Po té půjde vygenerovat pdf soubor s obálkami, jak je to nyní implementované.

### US-ORG-16 — Export dat
- **Jako** organizátor   
- **chci** exportovat údaje o týmu
- **abych** je nahrál do excelu
- **Priorita:** Must
- **Souvisí s požadavky:** FR-EXPORT-01
- **Poznámky:**
  - Vytvoření csv soubor s jménem týmu, maskotem, telefon a složením.

### US-ORG-17 — Statek
- **Jako** organizátor   
- **chci** mít možnosti připravit a importovat data o hře do statku
- **abych** připravil hru ve statku
- **Priorita:** Must
- **Souvisí s požadavky:** FR-STATEK-01
- **Poznámky:**
  - Příprava dat o týmech
  - Příprava dat o parametrech hry, šifrách a stanovištích
  - Přesný formát bude potřeba doladit.
  - Možná půjde i přímý export do statku.

### US-ORG-18 — Nový ročník
- **Jako** organizátor   
- **chci** vytvořit nový ročník
- **abych** začal připravovat hru
- **Priorita:** Must
- **Souvisí s požadavky:** FR-ROCNIK-03, NFR-LEGAL-02
- **Poznámky:**
 - Po ověření příkazu se založí nový ročník. V rámci operace ve formuláři budu pomoci upravit kopírované parametry hry.
 - Kopie aktuálního ročníku do nového ročníku
 - Kopie všech statických stránek, pokud najdu v obsahu aktuální rok, tak ho nahradím za příští rok. 
 - Kopie menu
 - Vytvoření a povolení obecné diskuze na fóru
 - Vytvoření nového ročníku automaticky přepíná aktuální ročník do archivního režimu
 - Retenční politika: při založení nového ročníku se ze všech ročníků, které se tím stávají archivními, smažou telefonní čísla týmů. Jména týmů/hráčů a emaily se naopak uchovávají trvale (viz `20-requirements.md` NFR-LEGAL-02).

### US-ORG-19 —  Editace příspěvku na fóru
- **Jako** organizátor   
- **chci** upravovat a mazat příspěvky na fóru
- **abych** moderoval diskuzi
- **Priorita:** Must
- **Souvisí s požadavky:** FR-FORUM-04
- **Poznámky:**
  - Chci mít možnost smazat libovolný příspěvek na fóru — svůj (org) i příspěvek týmu (spam, nevhodné chování apod.)
  - Chci mít možnost zpětně editovat svoje (org) příspěvky, protože dělám chyby.