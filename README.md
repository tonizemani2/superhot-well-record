# Superhot well record (v1)

The public record of what happened to the casing of 21 geothermal wells drilled into or near supercritical conditions, or instrumented while they heated: **7 failed, 10 intact, 2 never cycled, 2 still open**. Every row was read at source on 20 November 2026 and carries the documents that hold it. One well, IDDP-1, has a public record complete enough to analyse end to end; the last column of the table names the document that would complete each of the others.

## What is here

| File | What it is |
|---|---|
| `inventory.csv`, `inventory.json` | one row per well: field, maximum temperature and its basis, casing, connections, cement record, load history, outcome, mode, measured response, sources, completeness (0–5), next document |
| `MECHANISMS.md` | ten mechanism claims about these failures, each set against quotations from the primary literature, with a verdict |
| `link-check.json`, `check_links.py` | every source resolves; the checker and its dated result |
| `dataset.jsonld` | schema.org Dataset description |
| `llms.txt` | the numbers an answer engine may quote, with their label |
| `test_release.py` | `python3 -m unittest` — counts, a source on every row, the files agree |

## Completeness score

One point each for: casing sizes with wall and grade; connection type; cement record; thermal load history with temperatures and durations; outcome located by depth and mode.

## Three findings from the reading

1. IDDP-1 parted three couplings at 300, 356 and 505 m when it was quenched after ten months at 450 °C, and collapsed near 620 m in its first flow test (Kaldal 2019, video log). The depth "below 1,600 m" that circulates in reviews belongs to a cement void behind the anchor casing.
2. IDDP-2's casing damage at 2,307–2,380 m is described by two reviews as thermal stress and buckling of an uncemented section.
3. Kakkonda WD-1a and Venelle-2 reached 500 °C and were never produced or quenched: they are not casing-failure cases.

## Cite

See `CITATION.cff`. Data and text: CC BY 4.0. Code: MIT.

Corrections are welcome: a row is only as good as the document behind it. Contact toni@zemanium.com.
