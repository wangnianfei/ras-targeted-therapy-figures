# Figure legends

English legends are the submission version. The Chinese text is a proofing translation and is not for submission. Figure files carry no title and no Chinese text: everything that describes a figure lives here.

---

## Figure 1 | Pan-cancer distribution of RAS mutations

**a**, Proportion of samples carrying a *KRAS* mutation, by cancer type, segmented by allele (G12D, G12V, G12C, G12R, G13D, Q61X, other). **b**, **c**, The ten cancer types with the highest *NRAS* (**b**) and *HRAS* (**c**) mutation frequency. Numbers in parentheses are mutant samples over sequenced samples of that type. Data: MSK-IMPACT clinical sequencing cohort, 10,945 samples; an advanced-disease referral cohort, so the G12C share should not be extrapolated to East Asian populations.

Source data: data/01_cancer_type_distribution/ (cancer_type_kras_alleles.csv, codon_share.csv, cbioportal_sample_cancertype.json). Code: code/structure_figures.py, function fig4. Method: mutant samples per cancer type over all sequenced samples of that type; types with fewer than 10 samples suppressed.

**图 1　RAS 突变的泛癌种分布**　a，各癌种 *KRAS* 突变样本比例，按等位基因分段着色；b、c，*NRAS* 与 *HRAS* 突变频率居前十的癌种；括号内，突变样本数/该癌种样本数；数据来自 MSK-IMPACT，晚期病例富集，G12C 比例不宜外推至东亚人群。

---

## Figure 2 | The global landscape of RAS-related oncology trials, 2000-2026

**a**, Trials with at least one registered site, shaded by the number of trials per country; leader lines mark the eleven busiest countries. **b**, One sector per trial, grouped into seven tumour blocks with block size at the outer edge; four concentric tracks encode, from outside in, relation to RAS, highest phase, lead-sponsor class and recruitment status. **c**, Annual registrations by relation to RAS. Data from ClinicalTrials.gov (REST API v2): 1,182 interventional phase I-III oncology trials first posted between 2000 and 20 October 2026 (snapshot 2026-10-20). Trials registered only on ChiCTR or with the Chinese regulator are absent, so China's share is understated. Sector width is about 0.3 mm; the ring is read for composition, not for locating individual trials.

Source data: data/02_trial_atlas/trials_1182.csv (record level) and the derived tables. Code: code/fig2_world_map.R (panel a), code/fig2_trial_atlas.R (whole figure). Method: 3,210 records screened, 2,028 excluded, 1,182 retained; classification rules in docs/01_data_sources.md.

**图 2　RAS 相关肿瘤试验的全球格局（2000—2026）**　a，至少设有一个登记中心的试验，按各国试验数着色，引线为试验数前 11 位国家。b，每扇区一项试验，按瘤种分七块并标注例数；四条轨道由外向内依次为与 RAS 的关系、最高分期、申办方类别与招募状态。c，按与 RAS 关系分类的年度登记数。数据取自 ClinicalTrials.gov（REST API v2），2000 年至 2026 年首次登记的Ⅰ—Ⅲ期干预性肿瘤试验 1 182 项，截取日 2026 年 10 月 20 日；仅登记于 ChiCTR 或中国药监者未纳入。扇区宽约 0.3 mm，只读构成，不定位单项试验。

---

## Figure 3 | Nucleotide-binding elements of KRAS and isoform differences

**a**, KRAS-GDP (PDB 4OBE, 1.24 A): dark blue, P-loop (10-17); gold, switch I (30-38); brick, switch II (60-76); deep teal, G4/NKxD and G5/SAK; red, Gly12. **b**, Position-by-position comparison of the four isoforms; dark cells mark differing residues; the G domain differs by 4-12 residues and the HVR by 15-19. **c**, Alignment of residues 161-189; pale blue, Lys/Arg; deep teal, S-palmitoylated cysteine; orange-red, S-farnesylated cysteine.

Source data: data/03_kras_structure/ (pdb_entries.json, protein_structure_features.csv, variable_first_exons.csv). Code: code/structure_figures.py, function fig_s1; rendering by code/pymol/render_supplementary_pymol.pml. Method: chain A only; global alignment with match +1, mismatch 0, gap -1.

**图 3　KRAS 的核苷酸结合元件与亚型差异**　a，KRAS–GDP（PDB 4OBE，1.24 Å）；深蓝，P-loop（10–17）；琥珀，switch I（30–38）；砖红，switch II（60–76）；深青，G4/NKxD 与 G5/SAK；红色，Gly12。b，四个亚型逐位比较；深色，差异残基；G 结构域差 4–12 个残基，HVR 差 15–19 个。c，C 端 161–189 位比对；浅蓝，赖氨酸/精氨酸；深青，S-棕榈酰化半胱氨酸；橙红，S-法尼基化半胱氨酸。

---

## Figure 4 | The RAS signalling network and its druggable nodes

**a**, Receptor inputs drive nucleotide exchange through GRB2-SOS1 and tissue-restricted GEFs; SHP2 sustains KRAS regulability as both scaffold and phosphatase; GAPs catalyse GTP hydrolysis as the return step; active RAS signals through RAF-MEK-ERK, PI3K-AKT-mTORC1, RALGDS-RAL, PLCe and TIAM1. Red dashed edges, ERK negative feedback onto SOS1, RAF and receptors. Circle, approved drug class; square, clinical stage; triangle, preclinical only or abandoned. **b**, Four programmes established by sustained RAS signalling: metabolic reprogramming, macropinocytosis and autophagy, an immunosuppressive microenvironment, and senescence. Arrows show direction only, not flux.

Source data: none - curated from pathway reviews (see manuscript citations). Code: code/fig4_network.py. Method: manual curation; approval status as of 2026-10.

**图 4　RAS 信号网络与可干预节点**　a，受体输入经 GRB2–SOS1 与组织限定性 GEF 驱动核苷酸交换；SHP2 以支架与磷酸酶两种作用维持 KRAS 的可调控性；GAP 催化 GTP 水解，构成回程反应；活化 RAS 经 RAF–MEK–ERK、PI3K–AKT–mTORC1、RALGDS–RAL、PLCε 与 TIAM1 分支输出；红色虚线，ERK 对 SOS1、RAF 与受体的负反馈。圆形，已获批药物类别；方形，临床阶段；三角形，仅前临床或已放弃。b，持续 RAS 信号建立的代谢重编程、巨胞饮与自噬、免疫抑制微环境与衰老屏障。箭头只示方向，不示信号通量。

---

## Figure 5 | Conformational displacement on nucleotide exchange and drug binding

**a**, **b**, Per-residue C-alpha deviation after superposition on the core G domain; **a**, KRAS-GDP (4OBE) versus KRAS-GTP (5VQ2); **b**, KRAS(G12C)-GDP (4LDJ) versus KRAS(G12C)-sotorasib (6OIM); shading marks P-loop, switch I and switch II. Displacement is confined to the switch regions; core-region RMSD is 0.71 and 0.88 A. **c**, The 6OIM complex; Cys12 in red.

Source data: PDB entries 4OBE, 5VQ2, 4LDJ, 6OIM; data/03_kras_structure/visible_residues.csv. Code: code/structure_figures.py, function fig6; code/pymol/render_panelC_pymol.pml. Method: least-squares fit on C-alpha atoms of residues 1-166 excluding switch I and II.

**图 5　核苷酸状态与药物结合引起的构象位移**　a、b，按 G 结构域核心叠合后的逐残基 Cα 偏差；a，KRAS–GDP（4OBE）对 KRAS–GTP（5VQ2）；b，KRAS(G12C)–GDP（4LDJ）对 KRAS(G12C)–sotorasib（6OIM）；阴影，P-loop、switch I、switch II。位移限于开关区；核心区 RMSD 0.71 与 0.88 Å。c，6OIM 复合物；红色，Cys12。

---

## Figure 6 | Chemotypes of RAS-targeted drugs against development stage

**a**, Six chemotypes: OFF-state covalent, non-covalent reversible, RAS(ON) tri-complex, degrader, upstream and immune, downstream combination; horizontal axis, development stage; diamond, approved; circle, clinical; triangle, preclinical; n, number of registered trials. **b**, Coverage of the six chemotypes across alleles and wild type. Data as of October 2026.

Source data: data/06_drug_swimlanes/ (图八_药物泳道.csv, 图八_等位基因覆盖.csv, 图八_试验命中.tsv, 图八_直接RAS候选.tsv). Code: code/fig6_swimlanes.R. Method: 60 compounds, 6 lanes, 8 approved, 50 clinical, 2 preclinical; 489 trials matched.

**图 6　RAS 靶向药物的化学类型与临床阶段**　a，六类化学：OFF 态共价、非共价可逆、RAS(ON) 三元复合物、降解剂、上游与免疫、下游通路联合；横轴，研发阶段；菱形，已获批；圆点，临床阶段；三角，前临床；n，登记试验数。b，六类化学对各等位基因及野生型的覆盖。数据截至 2026 年 10 月。

---

## Figure 7 | Residue-level mutation spectrum of the three RAS genes

**a**-**c**, Mutation sites and counts for *KRAS*, *NRAS* and *HRAS* in 10,945 MSK-IMPACT samples; stem height and dot area encode the number of mutated samples at that residue; diamonds, classical hotspot codons; bar beneath the axis, protein region. *KRAS* mutations concentrate at codon 12, with G12D, G12V and G12C together accounting for 1,286 cases (77%); *NRAS* and *HRAS* are dominated by Q61 (66% and 38%). Percentages are of mutation records and describe the sequenced cohort, not population incidence.

Source data: data/07_mutation_distribution/ (mutation_spectrum_MSK-IMPACT.csv, hotspot_codons.csv, cbioportal_mutations.json). Code: code/structure_figures.py, function fig3.

**图 7　三条 RAS 基因的位点级突变谱**　a–c，MSK-IMPACT 队列 10 945 份样本中 *KRAS*、*NRAS* 与 *HRAS* 的突变位点与频次；竖线高度与圆点面积，该残基的突变样本数；菱形，经典热点密码子；底部色条，蛋白区段。*KRAS* 的突变集中在密码子 12，G12D、G12V 与 G12C 合计 1 286 例，占 77%；NRAS 与 HRAS 以 Q61 为主，分别占 66% 与 38%。百分比按突变记录计，描述送检队列，不代表人群发病率。

---

## Figure 8 | Resistance mechanisms mapped onto combination strategies

**a**, Correspondence matrix between nine resistance mechanisms (rows) and five combination strategies (columns); dark, direct; light, partial; blank, none. **b**, Two acquired-resistance detection rates with denominators: 45% (17/38, mostly lung, monotherapy) and 74% (25/34, colorectal, doublet); the two are not interchangeable.

Source data: data/08_resistance_combination/ (图十一_耐药机制.csv, 图十一_联合逻辑.csv, 图十一_对应.csv, 图十一_矩阵.csv, 图十一_检出率.csv). Code: code/fig8_resistance.R. Method: two-reader coding with disagreements resolved against source papers.

**图 8　耐药机制与联合策略的对应**　a，九类耐药机制（行）与五条联合思路（列）的对应矩阵；深色，直接对应；浅色，部分对应；空白，无对应。b，两项获得性变异检出比例及分母：45%（17/38，肺癌为主，单药）与 74%（25/34，结直肠癌，双药）；二者不可互推。
