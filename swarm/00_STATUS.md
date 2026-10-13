# Voynich-zwerm — Status & Hypotheses

**Datum:** 2026-10-13 · **Supervisor:** Claude Opus 5.5 · **Zwerm:** 1× Haiku 5.5, 2× Sonnet 5.5
**Branch:** `claude/voynich-subagents-hypotheses-593993`

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

## Open keuzes (zie vragen in chat)

1. Mogen agents echte **vergelijkingsteksten downloaden** (Latijn, middeleeuws Italiaans, Duits)?
2. Welke **hypotheses** gaan in Golf 2?
3. Wat doen we met de gepubliceerde **Zenodo-record 18346527**, waarvan de kernclaim nu weerlegd is?
4. **Commit en PR** van `swarm/`?
