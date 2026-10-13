# Voynich-zwerm — Status & Hypotheses

**Datum:** 2026-10-13 · **Supervisor:** Claude Opus 5.5 · **Zwerm:** 1× Haiku 5.5, 2× Sonnet 5.5
**Branch:** `claude/voynich-subagents-hypotheses-593993`

> **Stand:** Golf 1 en Golf 2 afgerond. Zie onderaan voor de resultaten van Golf 2 en het bijgewerkte beeld.

## Wat is er gedaan (Golf 1)

| # | Agent | Opdracht | Rapport |
|---|---|---|---|
| 1 | Haiku | Claim-inventaris van README, rapporten en JSON's | [01_claim_inventory.md](01_claim_inventory.md) |
| 2 | Sonnet | Audit van de 3 Python-scripts | [02_code_audit.md](02_code_audit.md) |
| 3 | Sonnet | Blinde hermeting met eigen parser en nulmodellen | [03_remeasurement.md](03_remeasurement.md) + [scripts/](scripts/) |

## Kernconclusie

De **hoofdclaim van de map** — "Jaccard ≈ 0,02 = statistische onmogelijkheid, dus algoritmische generatie" — **is weerlegd**:

- Lage overlap tussen regels is normaal bij korte regels (~7 woorden) en een rijke woordenschat (71% van de woordtypes komt 1× voor).
- De echte waarde ligt juist **boven** toeval: 0,032 tegenover 0,012 (globaal geschud) en 0,025 (binnen het folio geschud). Opeenvolgende regels hangen dus *meer* samen, niet minder.
- De drempels en het "CONFIRMED"-oordeel in `quevedo_validation.py` zijn verzonnen; `voynich_linguistics.py` bevat hardcoded hypotheses en gebruikt alleen de top-50 woorden.

**Claim-telling:** 81 claims → 8 KEEP · 35 VERIFY · 38 DISCARD.

## Wat staat wél (resonerende basis, gerepliceerd op ZL3b én RF1b)

| Bevinding | Waarde | Tegen nulmodel |
|---|---|---|
| Conditionele tekenentropie h2 | 2,16 bits (Engels ≈ 3,3) | **Anomaal laag** |
| Regel als eenheid: begin- en eindtekens van regels | o.a. regel-finale *m* ≈ 15% | **≫100× permutatienul** |
| Alinea-beginwoord start met gallows (k/t/p/f) | 83% tegenover 6–9% elders | **Sterk** (alleen ZL3b) |
| Verschil Currier A/B, Davis-handen, secties | h2 1,8–2,3; andere topwoorden | **Sterk** |
| Slotgrammatica (prefix–gallows–ch/sh–e–suffix) | 66% van tokens (geschud: 11%) | Matig: grammatica handmatig, slechts 22% van types |
| Identieke en bijna-identieke buurwoorden | ×1,4 en ×1,5 boven nul | Zwak/matig |

## Hypotheses voor verdere toetsing

| ID | Hypothese | Toets | Wat het zou uitsluiten |
|---|---|---|---|
| **H1** | De lage h2 is (deels) een **artefact van de EVA-transcriptie**: *ch, sh, ii, iin, ee* zijn eigenlijk enkele tekens. | h2 en woordlengte herberekenen met alternatieve tekensets (Currier, v101-achtig); vergelijken met Latijn en Italiaans. | "Simpele substitutie van een Europese taal" als h2 laag blijft |
| **H2** | De **regel is een functionele eenheid** (schrijfconventie: afkortingen of opvulling aan het regeleinde; of een generator die per regel herstart). | Begin- en eindeffecten per hand en sectie; vergelijken met middeleeuwse Latijnse handschriften (afkortingsteken aan regeleinde). | Doorlopend proza zonder regelbewustzijn |
| **H3** | **Gallows aan het alinea-begin = opmaak of markering** (vergelijkbaar met rubricering of een initiaal), geen klankwaarde. | Werkt het effect alleen op het 1e teken, het 1e woord of de 1e regel? Ontdoe het woord van de gallows: wordt het dan een bekend woord? | Gallows als "gewone letter" |
| **H4** | **Currier A/B zijn dialecten of instellingen van één systeem**, niet twee talen. | Classificatie op woordvormen: sluit het beter aan op Davis-handen of op secties? Gedeelde stammen met verschillende affixen? | "Twee onafhankelijke talen" of "één homogene tekst" |
| **H5** | **Zelfkopiëren** (Timm & Schinner) verklaart de lokale gelijkenis. | Kwantitatieve voorspelling van het zelfkopieermodel (edit-afstand over afstand in regels) tegenover de gemeten ×1,5. | Zelfkopiëren als *hoofd*mechanisme, als het effect zo zwak blijft |
| **H6** | **Woorden hebben een gelaagde, data-gedreven structuur** (stam + affixen). | Grammatica automatisch leren (bijv. via minimum description length) in plaats van handmatig; dekking van types tegenover schud-nul. | Willekeurige letterreeksen of grillesysteem (Rugg), als de dekking hoog is |

## Wat het NIET is (voorlopige uitsluitingen)

- **Niet aangetoond:** "lijn-onafhankelijkheid" of mechanische generatie op basis van Jaccard. De regels zijn juist iets *afhankelijker* dan bij toeval.
- **Waarschijnlijk geen** eenvoudige monoalfabetische substitutie van een Europese taal *in EVA-segmentatie* (te lage h2). Wordt hard na H1.
- **Niet homogeen:** de tekst gedraagt zich anders per hand en per sectie.

## Bekende beperkingen

- De enige offline natuurlijke-taalbasis was Engelse Python-documentatie. Er is **geen Latijnse, Italiaanse of Duitse basis**. Daarom zijn alleen de waarden ten opzichte van de schud-nul hard.
- 4% van de tokens (met `?` of `@`) is weggelaten.
- De paragraafmarkers ontbreken in RF1b, dus H3 rust op één transcriptie.

## Golf 2: resultaten (H1, H2, H3)

Jouw keuzes: baselines downloaden = ja · Golf 2 = H1 + H2/H3 · Zenodo = later beslissen · commit en PR = ja.

### H1: EVA-artefact? → **grotendeels weerlegd** ([04](04_H1_eva_segmentation.md))

| Conditie | h2 (bits) |
|---|---|
| Voynich EVA ruw (A / B) | 2,19 (2,18 / 2,00) |
| Voynich S1–S3 (ch/sh/gallows, ii/iin, ee als eenheid) | 2,26 – 2,43 |
| Latijn (Caesar) / Italiaans (Dante) / Duits (Faust) / Engels (Austen) | 3,29 / 3,10 / 3,14 / 3,28 |
| Eerlijke vergelijking: tekens samenvoegen bij beide, alfabet van ~35–42 | Voynich 2,59–2,84 tegenover talen 3,35–3,62 (kloof ≈ 0,75 bit) |
| Talen als verbose cipher (1 letter → 2 tekens) | 2,08–2,17, **gelijk aan Voynich**, maar woorden van 8–12 tekens (Voynich ≈ 5) |

- **Hard:** het is geen eenvoudige monoalfabetische substitutie van Latijn, Italiaans, Duits of Engels. De lage h2 is geen artefact van EVA.
- **Open:** verbose cipher, syllabarium, abjad of afgekorte tekst, en andere brontalen.

### H2: regel = functionele eenheid → **sterk ondersteund** ([05](05_H2H3_line_paragraph.md))

- Regel-finale *-m*: 15,3% tegenover 1,0% midden in de regel (×15,8; z = +51). In RF1b: 14,9%. Ook *-g* ×30.
- Regelbegin: *y* ×5,2, *p* ×7,2, *t* ×3,5; *c* juist ondervertegenwoordigd (×0,19).
- Het effect zit **alleen in het buitenste woord**, geldt op **elke** regel (niet alleen de eerste) en repliceert in A en B, bij handen 1–3 en in de grote secties. De sterkte verschilt: A ×6, B ×31.
- De woorden met *-m* zijn **gewone stammen** die midden in de regel op *-l*, *-r* of *-n* eindigen. Ze zijn niet ingekort. Hoe langer de regel, hoe vaker *-m* (10% → 25%).
- **Uitgesloten:** doorlopend proza dat alleen aan de kantlijn is afgebroken. **Open:** een schrijfconventie (een eindvariant van een letter, zoals de Latijnse eind-*-m*/*-ꝯ*) of een generator die per regel een toestand bijhoudt.

### H3: gallows aan het alinea-begin → **ondersteund als positiegebonden klasse; "geen klankwaarde" niet aangetoond**

- 82,7% tegenover een nulmodel van 8,0% (z = +79). In RF1b: 71%.
- Het gaat alleen om het **eerste woord** (bij woord 2 is het al 6,5%). Vooral **p** (54% tegenover 8% midden in de regel); *k* juist veel minder.
- De strip-toets zegt niets: zonder gallows matcht 70,4% een bestaand woord, tegenover 68,1% bij het nulmodel.

## Bijgewerkt beeld: wat het is en wat het NIET is

**Uitgesloten (hard):**
1. Een "Jaccard-anomalie" als bewijs voor mechanische generatie.
2. Eenvoudige letter-voor-letter-vervanging van Latijn, Italiaans, Duits of Engels.
3. Doorlopend proza dat zonder regelbewustzijn is afgebroken.
4. Een homogene tekst (A/B, handen en secties verschillen).

**Wel (robuust):** een systeem met lage voorspelbaarheid per teken, korte woorden, *positiegebonden varianten* (regel-eind, regel-begin, alinea-begin) en verschillende "dialecten" per hand.

**Sterkste kandidaat-families voor Golf 3:**
- **K1:** een verbose cipher of syllabarium **met afkortingen**. Dat verklaart de lage h2 én de korte woorden.
- **K2:** een **positiegebonden schrijfconventie** (eindvormen, zoals in Latijnse brevigrafie of Arabisch/Hebreeuws schrift).
- **K3:** een **generator met toestanden** (regel en alinea als reset).

## Open keuzes

1. Golf 3: welke kandidaat-familie toetsen?
2. Zenodo-record 18346527: nog steeds "later beslissen".
3. PR: de branch staat gepusht; de PR is nog niet aangemaakt (`gh` ontbreekt).
