# Thiago's Pokéwereld

Kleine, speelse oefenspelletjes voor Thiago (5 jaar), in het Nederlands, voor op de iPad.

- **Tellen**: tel de Pokémon (tot 5, 10, 15, 20).
- **Sommen**: plus- en minsommen met Pokéballen.
- **Eerste klank**: met welke klank begint het woord? Met een letter van de week.
- **Woordjes lezen**: lees een klankzuiver woord en kies het plaatje.

Elk goed antwoord geeft een Pokébal; bij 5 ballen vangt hij een nieuwe Pokémon voor zijn Pokédex.
Op de pagina "Voortgang voor ouders" staan per dag en per spel de niveaus, wat makkelijk ging, wat nog lastig is,
de stemkeuze, de letter van de week en knoppen om de geschiedenis te wissen. Voortgang wordt op het apparaat zelf bewaard.

## Stem

De pagina gebruikt de Nederlandse stem van de iPad. Het mooiste is een "Verbeterde" stem:
Instellingen → Toegankelijkheid → Gesproken materiaal → Stemmen → Nederlands → Xander of Claire (Verbeterd) downloaden.

## Bestanden

- `index.html`: de site (gebouwd uit `app.html` met `python3 tools/build_pages.py`).
- `app.html`: dezelfde pagina zonder `<head>`, voor de Claude-versie.
- `schaak/`: Thiago's Schaakavontuur, te openen via https://jonneguyt.github.io/thiago/schaak/
- `img/`: Pokémon-plaatjes (officiële artwork via PokeAPI, alleen voor privégebruik).
- `voice.json`: optionele computerstem (Piper, stem nl rdh, CC0), gemaakt met `tools/make_voice.py`.
