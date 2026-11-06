# RAS-targeted therapy in cancer — figures, source data and code

Data, code and vector artwork for the review **“RAS 靶向治疗的化学与生物学”** (manuscript in preparation). Everything needed to regenerate the eight main figures and the two tables is in this repository.

- **8 figures**, each as vector **PDF** (typeset) and **SVG** (editable); no raster previews are shipped.
- **2 tables** as CSV.
- **Source data** for every panel, in figure order.
- **Code** that produced each figure, with the parameters used.

## Figure order

| # | File stem | What it shows | Data | Code |
|---|---|---|---|---|
| 1 | 01_cancer_type_distribution | Pan-cancer distribution of *KRAS*/*NRAS*/*HRAS* mutations | data/01_cancer_type_distribution/ | code/structure_figures.py (fig4) |
| 2 | 02_trial_atlas | Atlas of 1,182 RAS-related oncology trials, 2000–2026 | data/02_trial_atlas/ | code/fig2_world_map.R, code/fig2_trial_atlas.R |
| 3 | 03_kras_gdp_structure | KRAS nucleotide-binding elements and isoform differences | data/03_kras_structure/ | code/structure_figures.py (fig_s1), code/pymol/render_supplementary_pymol.pml |
| 4 | 04_signalling_network | RAS signalling network and druggable nodes | curated, no dataset | code/fig4_network.py |
| 5 | 05_conformational_switch | Conformational shift on nucleotide exchange and drug binding | data/03_kras_structure/, PDB | code/structure_figures.py (fig6), code/pymol/render_panelC_pymol.pml |
| 6 | 06_drug_class_swimlanes | Chemotypes of RAS-targeted drugs against development stage | data/06_drug_swimlanes/ | code/fig6_swimlanes.R |
| 7 | 07_mutation_distribution | Residue-level mutation spectrum of the three *RAS* genes | data/07_mutation_distribution/ | code/structure_figures.py (fig3) |
| 8 | 08_resistance_combination | Resistance mechanisms mapped onto combination strategies | data/08_resistance_combination/ | code/fig8_resistance.R |

File names are ordered by the manuscript figure number. The original drawing-project stems are kept in figures/README.md for traceability.

## Data at a glance

| Source | What | Cut-off |
|---|---|---|
| MSK-IMPACT 2017 (cBioPortal msk_impact_2017) | 10,945 sequenced samples; mutation calls for *KRAS*, *NRAS*, *HRAS* | cohort snapshot as distributed; no later refresh |
| ClinicalTrials.gov REST API v2 | 3,210 records screened → **1,182** interventional phase I–III oncology trials referencing *RAS* | snapshot **2026-10-20** |
| PDB | 4OBE (1.24 Å), 5VQ2, 4LDJ, 6OIM | as deposited |
| Literature / labels | drug table, phase III readouts, resistance matrix | as of **2026-10** |

Full details: docs/01_data_sources.md, docs/02_methods.md, and the per-figure legends in docs/03_figure_legends.md.

## Reproducing

    python3 code/fetch_cbioportal.py      # pulls mutation calls
    python3 code/prepare_cbioportal.py    # builds the tables in data/
    python3 code/structure_figures.py .
    pymol -cq code/pymol/render_supplementary_pymol.pml
    pymol -cq code/pymol/render_panelC_pymol.pml

    Rscript code/fig2_world_map.R .
    Rscript code/fig2_trial_atlas.R .

    python3 code/fig4_network.py .
    Rscript code/fig6_swimlanes.R .
    Rscript code/fig8_resistance.R .

Scripts take the repository root as their single argument and write to figures/.

## Conventions

- **Colour**: a ten-step clinical palette anchored on navy #1F3A5F, brick #A63A2E and teal #2A6F6F; ordinal variables use tints of one hue; *other*/*unknown* are neutral grey. A colour means the same thing in every figure.
- **Type**: Arial throughout, 6.5–9 pt in figures, panel letters 9 pt bold.
- **Size**: every canvas is 180 mm wide (A4 text width at 15 mm margins); figures are placed at 15–16 cm in the manuscript.
- **Vector**: PDF and SVG only. Molecular surfaces in figures 3 and 5 are 600 dpi images embedded in the vector file — PyMOL surfaces cannot be vectorised, and a cartoon-only rendering was rejected because it loses too much.

## Licence

Text, data and figures: **CC BY 4.0**. Code: **MIT**. See LICENSE.

## Contact

Correspondence: Wang Nianfei. Please open an issue for data or code questions.
