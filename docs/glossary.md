# Slovník pojmů

> Doménové pojmy a zkratky, ať jim Claude i lidé rozumí stejně.
> Používej tyto termíny konzistentně v celé dokumentaci i v kódu.

| Pojem (CZ) | Termín v kódu (EN) | Význam |
|------------|--------------------|--------|
| Ročník | `year` | Jedno vydání hry, označené rokem konání. Má vlastní fáze, stanoviště, šifry, týmy a nastavení (viz `00-vision.md` § Fáze ročníku). |
| Stanoviště | `location` | Místo v terénu s GPS souřadnicemi, kde tým vyzvedne zadání šifry. Trasa = seřazená posloupnost stanovišť; první je start, poslední cíl. |
| Šifra | `puzzle` | Logická úloha na stanovišti, jejíž vyřešení prozradí polohu dalšího stanoviště. |
| Nápověda | `hint` | Nápověda k šifře poskytnutá za penalizaci (trestné minuty). Historicky může jít o víc nápověd v pořadí (řetězec rozdělený do řádků). |
| Řešení | `solution` | Oficiální řešení šifry, zveřejněné až po skončení hry (případně s odloženým zveřejněním v minutách). |
| Pytlík | `bag` (pracovní název) | Skupina stanovišť navíc pro těžší kategorii, vložená mezi dvě stanoviště společné oběma kategoriím (např. 5, 5a, 5b, 5c, 6). TODO: ověřit ustálený název v kódu. |
| Kategorie | `category` | Varianta hry s vlastní trasou/žebříčkem v rámci jednoho ročníku (historicky např. Pohoda, Výzva). Ročník má vždy alespoň 1 kategorii. |
| Tým | `team` | Registrovaný účastník hry, 1–5 hráčů. Role TEAM/SPARE a atribut zaplaceno viz [10-user-stories.md § Role](10-user-stories.md#role). |
| Náhradník | `spare` | Tým zaregistrovaný po naplnění kapacity `max-teams`; role SPARE. Po uvolnění místa automaticky povýšen na TEAM. |
| Zaplacený tým | `team.paid` (atribut, ne samostatná entita) | TEAM, který zaplatil startovné; role TEAM_PAID. Neplést se SPARE — viz [10-user-stories.md § Role](10-user-stories.md#role). |
| Maskot | `mascot` | Krátké unikátní jméno (bez diakritiky) náhodně přiřazené týmu při registraci; slouží k identifikaci týmu v externím systému Statek. Unikátní jen v rámci jednoho ročníku, napříč ročníky se může opakovat. |
| Startovné | `payment-price` / `payment-unit` | Poplatek za účast týmu ve hře; výše se stanovuje až po vyčíslení nákladů na šifry, proto může být při založení ročníku nevyplněné (`NULL`). |
| Poslední informace | `last-info` | Souhrn informací zpřístupněný zaplaceným hrajícím týmům (TEAM_PAID) těsně před startem hry, od data `last-info`. |
| Fórum | `forum` | Diskuzní systém webu, členěný do sekcí. |
| Sekce fóra | `forum_section` | Jedna diskuzní sekce; může být obecná, nebo automaticky vytvořená a provázaná s konkrétní šifrou (odemyká se až po skončení hry). |
| Obálka | `envelope` | Startovní obálka pro tým, tisknutelná ve formě PDF podle upravitelné šablony. |
| KI index (Kuka index) | `ki_index` | Externí ukazatel herní síly hráče (Kuka index). Detaily výpočtu/zdroj: TODO — viz aktuální implementace. |
| Statek | `statek` (vlastní jméno, nepřekládá se) | Externí aplikace, která během hry zpracovává průběh, výsledky, nápovědy a řešení; tým se do ní hlásí přes maskota. |
| Trakar | `trakar` (vlastní jméno, nepřekládá se) | Přístupové údaje (`trakar-login`, `trakar-token`) pro autentizaci vůči Statku. TODO: upřesnit přesný vztah Trakar ↔ Statek (stejný systém, nebo samostatná autentizační služba?). |
