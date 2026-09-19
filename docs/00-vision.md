# 00 — Vize a rozsah
> Vlastník: Organizátoři sovy • Stav: draft • Poslední revize: 2026-09-18

Projekt: Webová aplikace pro správu a organizaci šifrovací hry Hradecká sova. Aktuální verze se nachází na https://www.hksova.cz

Cílem projektu je navázat na předchozí verzi webové aplikace, provést její redesign, používat nové technologie a přidat/vylepšit funkcionalitu. Cílem je, aby se část administrativních úkonů prováděla automaticky v návaznosti na kritické datumy každého ročníku. 

> Navazuje: [10-user-stories.md](10-user-stories.md), [20-requirements.md](20-requirements.md), [glossary.md](glossary.md)


## Doménový kontext

Šifrovací hra je volnočasová aktivita, které se účastní týmy zpravidla o 1 až 5 hráčích. 

Hra se skládá z více stanovišť. Na každém stanovišti si tým vyzvedne zadání šifry, logické úlohy, která mu řekne, kde se nachází další stanoviště.

Na startu tým získá úvodní šifru a řešení jednotlivých šifer na stanovištích se dostane do cíle. Zde obdrží cílovou šifru, jejíž řešením je kód pro ukončení hry.

Ke každé šifře existuje nápověda, která týmu za určitou penalizaci poskytne nápovědu, jak pokračovat v luštění. 

Ke každé šifře existuje i řešení, které prozradí týmu umístění dalšího stanoviště. 

Hra probíhá jednou ročně a každý ročník má své unikátní nastavení: klíčová datumy, nové umístění stanovišť, nové šifry, ... 


## Problém

Proběhlo již asi 20 ročníků. Na začátku byly odlišné parametry hry (počet stanovišť, kategorie, systém nápověď a řešení). Webové stránky musí být uzpůsobeny, aby zpětně dokázaly příjmout data z proběhlých ročníků kvůli zobrazování archivovaných her.


## Cíl produktu

Výsledný produkt musí být kompatibilní i s původními hrami, ale hlavně má napomoci při organizaci hry.


## Klíčové pojmy

Stručně; závazné definice a anglické ekvivalenty jsou v [glossary.md](glossary.md).

## Fáze ročníku
Každý ročník je označený rokem, ve kterém probíhá. Během roku se mění je fáze a to v návaznosti na datumy specifikované při definici nového ročníku.

- Záložení ročníku: několik týdnů po ukončení předchozího ročníku organizátor založí nový ročník. Dojde ke zkopírování struktury předchozího ročníku. Část dat bude dostupná pouze organizátorům, část dat bude veřejně viditelná. Po založení ročníku organizátor nastavení klíčové datumy.
- Přípravy hry: během této fáze jsou dostupné obecné informace o ročníku. Organizátoři upravují stanoviště, šifry, pravidla, ... Probíhá správa týmů, rozesílání zvacích emailů apod.
- Zahájení registrace: Je otevřený formulář pro přihlášení týmu do hry. Navázáno na datum
- Ukončení registrace: Další týmy se již nemohou přihlásit. Navázáno na datum
- Zobrazení posledních informací: týmům, které jsou registrované a zaplatili se zobrazí připravené poslední informace, navázáno na datum
- Příprava před hrou: rozesílání emailů o nezaplacení, export dat do csv, statku, ....
- Zahájení hry: hra probíhá, z pohledu systému se nic neděje, 
- Ukončení hry: na stránkách se povolí zobrazení šifer, nápověď, řešení, trasy, výsledků. Toto je navázáno na přesný datum a čas.
- Archivace: Při vytvoření nového ročníku jsou všechny staré ročníky označeny za archivní. Týmy v nich již nemohou nic měnit (údaje o týmu, fórum atd.)

## Cíloví uživatelé

Závazný výčet rolí a jejich oprávnění je veden na jednom místě v [10-user-stories.md § Role](10-user-stories.md#role) (ORG, PUBLIC, TEAM, SPARE, TEAM_PAID).

## Rozsah (co produkt dělá)

Webová aplikace pro správu šifrovací hry Hradecká sova. Aplikace umožňuje přípravu hry, registraci týmů, komunikaci s týmy a zobrazování informací ke hře navázané na jednotlivé fáze ročníku. Detailní chování popisují stories v [10-user-stories.md](10-user-stories.md); zde jen shrnutí oblastí:

- **Veřejná prezentace** — informace o aktuálním i archivních ročnících, přehled přihlášených týmů se statistikami, výsledky a reportáže po skončení hry, zobrazení šifer/nápověd/řešení a trasy s mapou (aktuální i archiv).
- **Účet týmu** — registrace (vč. captcha), přihlášení, reset a změna hesla, správa údajů o týmu, zrušení účasti, přechod mezi rolemi TEAM/SPARE/TEAM_PAID (viz [10-user-stories.md § Role](10-user-stories.md#role)).
- **Fórum** — obecná diskuze i sekce provázané se šiframi, moderace.
- **Administrace ročníku** — parametry ročníku a kategorie, stanoviště a trasa, šifry/nápovědy/řešení, maskoti, stránky, média, menu.
- **Administrace týmů** — přehled a editace týmů, hromadné akce, export dat, příprava startovních obálek.
- **Komunikace** — hromadné a zvací emaily.
- **Integrace** — příprava/import dat pro externí systém Statek, synchronizace výsledků zpět do interní databáze.
- **Životní cyklus ročníku** — založení nového ročníku (kopie struktury), automatické řízení fází podle klíčových datumů, archivace předchozích ročníků.

Mimo rozsah (zatím neřešeno, viz TODO v jednotlivých dokumentech): přesný obsah stránky s posledními informacemi, automatizovaný import historických výsledků z archivu, přesný formát exportu/importu do Statku.

## Předpoklady a omezení

- UI je v češtině
- Webová aplikace je dostupná jak pro desktop, tak i pro mobil
