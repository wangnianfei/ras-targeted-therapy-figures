# Data sources, cut-off dates and inclusion rules

Every number in the figures can be traced to a file in data/. This document states where each file came from, when it was frozen, and what was excluded.

## 1. MSK-IMPACT clinical sequencing cohort (figures 1 and 7)

| Item | Value |
|---|---|
| Study | MSK-IMPACT Clinical Sequencing Cohort, msk_impact_2017 (Memorial Sloan Kettering, Nat Med 2017; PMID 28481359) |
| Access | cBioPortal REST API, molecular profile msk_impact_2017_mutations |
| Samples | 10,945 |
| Genes | KRAS, NRAS, HRAS (Entrez 3845, 4893, 3267) |
| Fields kept | sample ID, cancer type, Hugo symbol, protein change, mutation type, allele count |
| Cut-off | cohort snapshot as distributed by cBioPortal; no later refresh was pulled |

Rules applied:

- Only non-synonymous, non-silent calls were counted; synonymous and UTR calls were dropped.
- The denominator for a cancer type is the number of samples of that type in the cohort, not the number of mutations. A sample with two KRAS calls contributes once to the numerator.
- Allele classes are G12D, G12V, G12C, G12R, G13D, Q61X (Q61H/K/L/R) and Other.
- Cancer types with fewer than 10 sequenced samples were not plotted; this removes long tails without changing the ranking of the types shown.
- MSK-IMPACT is an advanced-disease, referral-enriched cohort. Proportions describe sequenced tumours and must not be read as population incidence. The G12C share in particular is higher than in East Asian series.

Files: cancer_type_kras_alleles.csv (per cancer type x allele counts), codon_share.csv (codon-level shares), cbioportal_sample_cancertype.json (sample to cancer type map).

## 2. ClinicalTrials.gov (figure 2)

| Item | Value |
|---|---|
| Interface | REST API v2, /api/v2/studies |
| Snapshot | 2026-10-20 (SNAPSHOT in code/01_fetch_ctgov.py); requests executed 2026-11-05 |
| Raw records retrieved | 3,210 unique NCT numbers |
| Excluded | 2,028 (see below) |
| Included | 1,182 |

Query construction: free-text terms covering RAS, KRAS, NRAS, HRAS and the common allele names, combined with oncology terms; restricted to study_type = INTERVENTIONAL and phases 1-3 (Early Phase 1, Phase 1, Phase 2, Phase 3). Records were de-duplicated on NCT number across all query variants. The exact term list ships as data/02_trial_atlas/search_terms.csv.

Exclusions, with counts as recorded in summary.json:

| Reason | n |
|---|---|
| RAS not referenced as a gene or target (e.g. renin-angiotensin system; or the string appears in neither title, summary, condition, keyword, eligibility nor outcome) | 1,907 |
| Phase outside I-III (not applicable) | 54 |
| Non-malignant RASopathy or non-oncology indication | 19 |
| Condition not oncological | 38 |
| Phase IV | 10 |

Relation to RAS - assigned per trial from the intervention description, eligibility criteria and summary, with manual adjudication of ambiguous cases:

- RAS-targeted (358): the agent binds RAS itself (G12C/G12D/G12V inhibitors, ON-state tri-complex, degraders).
- RAS-regulator (134): the agent acts on SOS1, SHP2 or farnesylation.
- RAS-biomarker-selected (639): RAS genotype governs eligibility or stratification but the drug does not act on RAS.
- RAS-mentioned (51): RAS named without meeting any of the above.

Geography: 1,097 of 1,182 trials list at least one site, giving 3,293 trial-country pairs across 72 countries. Hong Kong is merged into China for the map only; the record-level file keeps the original country string.

Known gaps: trials registered only on ChiCTR or with the Chinese regulator are absent (for example the sosimerasib phase 2 monotherapy study, ChiCTR2200059986), so China's share is understated. Registration practice also differs by sponsor type, which affects the sponsor-class track.

Files: trials_1182.csv (record level, one row per trial), tables 2-13 derivatives (country, phase, status, sponsor, target class, tumour type, year, crosswalk), summary.json (counts), search_terms.csv.

## 3. Protein structures (figures 3 and 5)

| PDB | Content | Resolution | Used for |
|---|---|---|---|
| 4OBE | KRAS-GDP, wild type | 1.24 A | figure 3a; reference state in figure 5a |
| 5VQ2 | KRAS-GTP | - | figure 5a (nucleotide exchange) |
| 4LDJ | KRAS G12C-GDP | - | figure 5b (drug-free state) |
| 6OIM | KRAS G12C-sotorasib | - | figure 5b, 5c (drug-bound state) |

Only chain A was used. Region definitions follow Vetter and Wittinghofer: P-loop 10-17, switch I 30-38, switch II 60-76, G4/NKxD and G5/SAK motifs. In figure 3b, KRAS4A, KRAS4B, NRAS and HRAS were compared by global pairwise alignment (match +1, mismatch 0, gap -1); the alignment is a project-local implementation, not a substitution-matrix aligner.

Metadata: data/03_kras_structure/pdb_entries.json, protein_structure_features.csv, visible_residues.csv, variable_first_exons.csv, prepared_meta.json.

## 4. Curated tables (no primary dataset)

Two tables and two panels are assembled from the literature and regulatory labels rather than from a database dump:

- Table 1 - 13 approved or pivotal RAS-targeted agents: target and modality, key readout, regulatory status. Status as of 2026-10.
- Table 2 - 7 phase III trials that changed practice: population, comparator, primary result, current status.
- Figure 4 - signalling network: nodes and edges curated from pathway reviews; drug-class annotations carry approval status as of 2026-10.
- Figure 8 - 9 resistance mechanisms x 5 combination strategies, with a three-level correspondence code (direct, partial, none); the two acquired-resistance detection rates (45%, 17/38; 74%, 25/34) come from the published cohorts discussed in the manuscript.

Each row carries its supporting citation in the manuscript text; the CSV files contain the same values used to draw the figures.

## 5. Snapshot summary

| Dataset | Frozen at | Notes |
|---|---|---|
| MSK-IMPACT | cohort release | no refresh |
| ClinicalTrials.gov | 2026-10-20 | API called 2026-11-05, snapshot date pinned |
| PDB | deposition | resolutions as deposited |
| Drug / trial / resistance tables | 2026-10 | literature and labels |
