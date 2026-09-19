---
description: Pravidla pro psaní dokumentace v docs/
paths:
  - "docs/**/*.md"
---

# Pravidla pro dokumentaci

Toto pravidlo se načte jen když Claude sáhne na soubor v `docs/`.

- Dokumentace je česky; kódové identifikátory a příklady kódu anglicky.
- Zachovávej ID požadavků/stories/scénářů (`FR-xx`, `US-xx`, `SC-xx`, `NFR-xx`)
  a používej je pro křížové odkazy.
- Neduplikuj obsah mezi dokumenty — odkazuj.
- Zásadní technická rozhodnutí nepatří do prózy, ale do samostatného ADR.
- Nevyplněná místa označuj `TODO`, ať jsou dohledatelná.
