# Analysis methods, figure by figure

Software: Python 3.11 (numpy, pandas, matplotlib, Biopython), R 4.6.2 (ggplot2, sf, rnaturalearth, patchwork), PyMOL 3.x, LibreOffice 25 for PDF conversion. Figures are drawn at final size; no post-hoc scaling of type.

## Figure 1 - Pan-cancer distribution of RAS mutations

Input: MSK-IMPACT mutation calls (10,945 samples). For each cancer type the numerator is the number of samples carrying at least one non-synonymous KRAS (panel a), NRAS (b) or HRAS (c) call; the denominator is the number of samples of that type in the cohort. Within a bar, mutations are split into G12D, G12V, G12C, G12R, G13D, Q61X and Other. Types are ordered by mutant proportion; the top 15 (a) and top 10 (b, c) are shown, with types under 10 samples suppressed. Labels give n/N and the percentage. Stacked bars, no smoothing.

## Figure 2 - Atlas of 1,182 trials

Screening and classification are described in 01_data_sources.md. Drawing:

- Panel a: choropleth of trials with at least one registered site, classed by count (>100, 51-100, 26-50, 11-25, 6-10, 2-5, 1, 0); eleven leader lines for the busiest countries; Hong Kong merged into China for the map.
- Panel b: one sector per trial (1,182 sectors), grouped into seven tumour blocks sized at the outer edge; four concentric tracks from outside in encode relation to RAS, highest phase, lead-sponsor class and recruitment status. Sector width is about 0.3 mm, so the ring is a composition device: it supports reading the joint distribution of tracks, not locating an individual trial.
- Panel c: annual registrations stacked by relation to RAS; 2026 is truncated at the snapshot date.

Sanity checks are built into the script (stopifnot): 1,182 sectors, seven tumour blocks summing to 1,182, four relation levels summing to 1,182, five status levels including Not yet recruiting (a level silently dropped in an early version, 71 trials).

## Figure 3 - KRAS structure and isoform differences

Panel a: chain A of 4OBE (KRAS-GDP, 1.24 A) rendered in PyMOL; cartoon coloured by region (P-loop 10-17, switch I 30-38, switch II 60-76, G4/NKxD, G5/SAK), Gly12 as red spheres; GDP and Mg2+ as sticks/spheres. Panel b: global pairwise alignment of the four isoforms (KRAS4A, KRAS4B, NRAS, HRAS) with match +1, mismatch 0, gap -1; per-position differences are marked against KRAS4B; the G domain differs by 4-12 residues and the HVR by 15-19. Panel c: alignment of residues 161-189, with Lys/Arg, S-palmitoylated Cys and S-farnesylated Cys highlighted.

## Figure 4 - Signalling network

Curated, not computed. Nodes and edges were assembled from pathway reviews; receptor inputs feed GRB2-SOS1 and tissue-restricted GEFs, SHP2 acts as both scaffold and phosphatase, GAPs catalyse the return hydrolysis step, and active RAS drives RAF-MEK-ERK, PI3K-AKT-mTORC1, RALGDS-RAL, PLCe and TIAM1 outputs. Dashed red edges are ERK negative feedback onto SOS1, RAF and receptors. Marker shape encodes approval status (circle approved class, square clinical stage, triangle preclinical or abandoned). Panel b lists four consequence programmes (metabolic reprogramming, macropinocytosis and autophagy, immunosuppressive microenvironment, senescence). Arrows show direction only, not flux.

## Figure 5 - Conformational displacement

Structures were superposed on the core G-domain C-alpha atoms (residues 1-166, switch I and II excluded) by least squares; per-residue C-alpha distance is plotted for 4OBE versus 5VQ2 (a) and 4LDJ versus 6OIM (b). Shaded bands mark P-loop, switch I and switch II. Core RMSD is 0.71 A (a) and 0.88 A (b); displacement is confined to the switch regions. Panel c shows the 6OIM complex with Cys12 in red.

## Figure 6 - Chemotypes against development stage

The drug table (60 compounds) records chemotype class, highest phase reached, approval status and the number of registered trials in the 1,182-trial set. Six chemotypes are plotted as swimlanes against stage; symbol shape encodes approval (diamond), clinical (circle) or preclinical (triangle). Panel b is a binary coverage matrix of the six chemotypes against KRAS G12C/G12D/G12V/G12R/G13D, NRAS, HRAS and wild type. Counts: 60 drugs, 6 lanes, 8 approved, 50 clinical, 2 preclinical; 489 trials matched.

## Figure 7 - Residue-level mutation spectrum

Per-residue counts of non-synonymous calls in the 10,945-sample cohort for KRAS (a), NRAS (b) and HRAS (c). Stem height and dot area both encode the number of mutated samples at that residue; diamonds mark classical hotspot codons; the bar under each axis shows protein regions (P-loop, switch I, switch II, G4, G5, HVR). Percentages are of mutation records within that gene, not of patients. KRAS: 1,670 mutations, G12D/G12V/G12C 1,286 (77%), G13D/G13C/G13V 161 (10%). NRAS: 252 mutations, Q61 167 (66%). HRAS: 101 mutations, Q61 38 (38%).

## Figure 8 - Resistance mechanisms and combination strategies

The matrix has nine mechanism rows and five strategy columns; each cell is coded direct, partial or none by two readers, with disagreements resolved against the source papers. Panel b plots two acquired-resistance detection rates with their denominators: 45% (17/38, mostly lung, monotherapy) and 74% (25/34, colorectal, doublet). The two are not interchangeable: different tumour context, different drug combinations, different assays.

## Tables 1 and 2

Built from publications and regulatory labels, one row per agent or trial, status as of 2026-10. Table 1 columns: drug, target and modality, key readout, status. Table 2 columns: trial, population, comparator, primary result, current status. Both are exported as CSV in data/tables/ and typeset as three-line tables in the manuscript.
