---
name: setup-progress
description: Zet het automatische voortgangslog (PROGRESS.md) op voor het huidige project, zodat de Stop-hook na elke werksessie een entry met urenschatting kan wegschrijven. Gebruik bij projectstart, of wanneer een bestaand project nog geen PROGRESS.md heeft.
---

Stel het automatische voortgangslog-systeem in voor het huidige project.

Doe het volgende:

1. Controleer of `PROGRESS.md` al bestaat in de huidige werkdirectory.
   - Zo ja: vertel de gebruiker dat het systeem al actief is en stop hier.
   - Zo nee: check ook 1-2 levels omhoog (`../PROGRESS.md`, `../../PROGRESS.md`) — sommige multi-deployment projecten consolideren één centrale PROGRESS.md in de projectroot met H2-headers `## YYYY-MM-DD — <deployment> — <onderwerp>` per deployment. Als zo'n centrale file bestaat: vraag de gebruiker of ze bijdragen aan die centrale log (aanbevolen) of alsnog een lokale per-deployment PROGRESS.md willen. Geen dubbele bestanden aanmaken zonder bevestiging.
   - Als er nergens een PROGRESS.md is: maak het bestand aan in CWD met onderstaande inhoud (vervang {projectnaam}
     door de naam van de huidige map):

```
# Voortgangslog — {projectnaam}

Automatisch bijgehouden door Claude Code na elke werksessie.

---
```

2. Meld de gebruiker het volgende (beknopt, in het Nederlands):
   - PROGRESS.md is aangemaakt
   - Na elke sessie waarbij bestanden worden gewijzigd, wordt automatisch een
     entry toegevoegd, gegroepeerd per week
   - Voor een bi-weekly rapport: open PROGRESS.md en kopieer de afgelopen 2 weken
