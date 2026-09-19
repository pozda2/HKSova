# CLAUDE.md

## Co projekt je

Webová aplikace pro správu šifrovací hry Hradecká sova.

Zdroje pravdy (čti je, než začneš plánovat):
- Vize a rozsah: `docs/00-vision.md`
- User stories: `docs/10-user-stories.md`
- Požadavky (FR/NFR): `docs/20-requirements.md`
- Scénáře / akceptační kritéria: `docs/30-scenarios.md`
- Architektura: `docs/40-architecture.md`
- Zvolený stack: `docs/50-tech-stack.md`
- Rozhodnutí: `docs/adr/`

## Mapa adresáře

- `tests/` — testy (pytest + testcontainers)
- `docs/` — analytická dokumentace (Markdown)
- `.claude/` — konfigurace Claude Code (rules, commands, agents, skills)


## Konvence

- **Veškerý kód anglicky**: názvy proměnných, funkcí, komentáře, chybové hlášky,
  názvy souborů a commit messages jsou anglicky — i když je diskuze česky.
- Dokumentace v `docs/` je česky.
- Commit po jednotlivých logických celcích, popisná zpráva.
- Každé zásadní technické rozhodnutí = jeden nový ADR v `docs/adr/`.
- Požadavky, stories a scénáře mají ID (`FR-01`, `US-01`, `SC-01`) — odkazuj na ně
  v commitech, testech a ADR.

## Pracovní postup

1. **Explore** — nejdřív přečti relevantní soubory a popiš současný stav. Žádné úpravy.
2. **Plan** — v plan mode (2× Shift+Tab) navrhni plán. Počkej na moje schválení.
3. **Implement** — implementuj po jedné feature/story. Kde to jde, TDD (nejdřív padající test).
4. **Test** - k funkcím vytvářej unit a další testy
4. **Verify** — spusť testy a lint. **Commity si dělám sám** — Claude necommituje, dokud to výslovně neřeknu.

## Čemu se vyhnout

<!-- Doplňuj průběžně věci, které Claude opakovaně dělá špatně.
     Tip: během práce začni zprávu znakem '#' a Claude si sem instrukci zapíše sám. -->
- **Deprecated API.** Nepoužívej funkce/parametry označené knihovnou za deprecated —
  najdi a použij aktuální náhradu. Skutečnou deprecation ověř (varování za běhu,
  dokumentace), neřiď se jen domněnkou z IDE.