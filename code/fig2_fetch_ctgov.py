#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Harvest every RAS-related interventional trial registered on ClinicalTrials.gov.

Strategy (two complementary sweeps, union then de-duplicated by NCT ID):
  A. biomarker/gene sweep  -- any record whose text mentions KRAS / NRAS / HRAS /
     "RAS mutation" / "RAS pathway" ... , i.e. trials that *select* on RAS status.
  B. agent sweep           -- explicit names of RAS-directed and RAS-regulator
     drugs, so that a trial which never spells out the gene is still captured.

Raw API payloads are kept under 数据/raw/ so every downstream number is traceable.

Usage: python3 01_fetch_ctgov.py <root>
"""
import json, os, sys, time, urllib.parse, urllib.request

ROOT = sys.argv[1] if len(sys.argv) > 1 else os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, '数据', 'raw')
os.makedirs(RAW, exist_ok=True)

API = 'https://clinicaltrials.gov/api/v2/studies'
FIELDS = ','.join([
    'NCTId', 'OrgStudyId', 'BriefTitle', 'OfficialTitle', 'Acronym', 'BriefSummary',
    'OverallStatus', 'WhyStopped', 'StudyType', 'Phase',
    'EnrollmentCount', 'EnrollmentType',
    'StartDate', 'PrimaryCompletionDate', 'CompletionDate',
    'StudyFirstPostDate', 'LastUpdatePostDate', 'ResultsFirstPostDate',
    'LeadSponsorName', 'LeadSponsorClass', 'CollaboratorName',
    'Condition', 'InterventionType', 'InterventionName',
    'DesignAllocation', 'DesignPrimaryPurpose', 'DesignInterventionModel',
    'LocationFacility', 'LocationCity', 'LocationState', 'LocationCountry',
    # RAS is very often named only in the eligibility criteria or the keywords;
    # these three fields are what makes the recall of the gene sweep usable.
    'EligibilityCriteria', 'Keyword', 'PrimaryOutcomeMeasure', 'SecondaryOutcomeMeasure',
])

# ---- sweep A: gene / biomarker vocabulary ---------------------------------
GENE_TERMS = [
    'KRAS', 'NRAS', 'HRAS', 'KRAS G12C', 'KRAS G12D', 'KRAS G12V', 'KRAS G13D',
    'KRAS Q61', 'NRAS Q61', 'HRAS Q61',
    '"RAS mutation"', '"RAS mutant"', '"RAS wild-type"', '"RAS wild type"',
    '"pan-RAS"', '"RAS pathway"', '"RAS inhibitor"', '"RAS ON inhibitor"',
    '"RAS GTPase"', '"RASopathy"',
    # 2026-11-05 召回审计补：原词表只收单数、连字符与写全的写法，漏掉了
    # 「RAS Mutations」「RAS/MAPK Mutation-Positive」这类复数与组合写法。
    # 24 项符合同一分层定义的试验因此整批落在语料之外（见 4.7 段四的审计段）。
    '"RAS mutations"', '"RAS mutant"', '"RAS-mutant"', '"RAS/MAPK"',
    '"RAS wildtype"', '"RAS alteration"', '"RAS-altered"',
    '"RAS positive"', '"RAS-positive"',
]

# ---- sweep B: RAS-directed agents and RAS-regulator agents ----------------
AGENTS_RAS = [
    # KRAS G12C (covalent, OFF-state)
    'sotorasib', 'AMG 510', 'adagrasib', 'MRTX849', 'divarasib', 'GDC-6036',
    'olomorasib', 'LY3537982', 'glecirasib', 'JAB-21822', 'fulzerasib', 'IBI351',
    'garsorasib', 'D-1553', 'opnurasib', 'JDQ443', 'MK-1084', 'HRS-4642',
    'BI 1823911', 'ERAS-3490', 'JMKX1899', 'GFH925', 'YL-15293', 'SY-5933',
    # KRAS G12D / G12V / multi
    'MRTX1133', 'HRS-4642', 'ASP3082', 'RMC-9805', 'zoldonrasib', 'INCB161734',
    'ERAS-4001', 'QTX3034', 'TSN1611', 'BBO-8520', 'VS-7375', 'GFH375',
    'ELI-002', 'mRNA-5671', 'ASP2453',
    # RAS(ON) multi-selective / pan-RAS
    'RMC-6236', 'daraxonrasib', 'RMC-6291', 'elironrasib', 'ADT-007',
    'BI 2865', 'pan-KRAS',
    # HRAS and farnesylation
    'tipifarnib', 'lonafarnib', 'salirasib',
    # RAS regulators and effectors used as RAS-directed strategies
    'SOS1 inhibitor', 'BI 1701963', 'MRTX0902', 'TNO155', 'SHP2 inhibitor',
    'RMC-4630', 'JAB-3312', 'RLY-1971', 'migoprotafib', 'ERAS-601',
    # ---- 2026-11-05：词表与图9／表1 的药物集合对齐（59 个药的通用名与代号全部入表），
    # 另补三篇综述点名、而登记页从不出现 RAS 的代号（LUNA18／AUBE00）与本轮审计新查到的
    # HRS-7058、HRS-7172、HRS-2329、S241656。身份证据见 4.7 与证据卡。
    'sosimerasib', 'HBI-2438', 'JMKX001899', 'calderasib', 'D3S-001',
    'HS-10370', 'ZG19018', 'GEC255', 'HYP-2090PTSA', 'QTX3544',
    'DN022150', 'QLC1101', 'RMC-5127', 'GFH276', 'setidegrasib',
    'LY4066434', 'BGB-53038', 'JAB-23E73', 'ZG2001', 'FMC-376',
    'ARV-806', 'siG12D-LODER', 'iExosome', 'BI-2865', 'sitneprotafib',
    'vociprotafib', 'batoprotafib', 'BBP-398', 'R115777', 'SCH66336',
    'GI-4000', 'TG01', 'V941', 'LUNA18', 'AUBE00',
    'HRS-7058', 'HRS-7172', 'HRS-2329', 'S241656',
]

HEAD = {'User-Agent': 'RAS-review-harvest/1.0 (academic literature survey)'}


def get(params, tries=4):
    url = API + '?' + urllib.parse.urlencode(params)
    for k in range(tries):
        try:
            req = urllib.request.Request(url, headers=HEAD)
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.load(r)
        except Exception as e:                        # noqa: BLE001
            if k == tries - 1:
                raise
            print('    retry %d (%s)' % (k + 1, type(e).__name__))
            time.sleep(2 + 3 * k)


def sweep(expr, label, extra=None):
    """Page through one Essie query, return {nctId: study}."""
    out, token, page = {}, None, 0
    while True:
        p = {'query.term': expr, 'fields': FIELDS, 'pageSize': 1000,
             'countTotal': 'true', 'filter.overallStatus': ''}
        p.pop('filter.overallStatus')
        if extra:
            p.update(extra)
        if token:
            p['pageToken'] = token
        d = get(p)
        page += 1
        for s in d.get('studies', []):
            nid = s['protocolSection']['identificationModule']['nctId']
            out[nid] = s
        token = d.get('nextPageToken')
        if not token:
            print('  %-28s total=%-5s kept=%-5d (%d page(s))'
                  % (label, d.get('totalCount', '?'), len(out), page))
            return out
        time.sleep(0.3)


def main():
    studies, prov = {}, {}

    print('sweep A -- gene / biomarker vocabulary')
    expr_a = ' OR '.join(GENE_TERMS)
    a = sweep(expr_a, 'all RAS vocabulary', {'filter.advanced': 'AREA[StudyType]INTERVENTIONAL'})
    for k, v in a.items():
        studies[k] = v
        prov.setdefault(k, []).append('gene')

    print('sweep B -- RAS-directed agents (one query per agent)')
    hit_by_agent = {}
    for ag in sorted(set(AGENTS_RAS)):
        q = 'AREA[InterventionName]"%s" OR AREA[InterventionOtherName]"%s"' % (ag, ag)
        try:
            r = sweep(q, ag, {'filter.advanced': 'AREA[StudyType]INTERVENTIONAL'})
        except Exception as e:                        # noqa: BLE001
            print('    !! %s failed: %s' % (ag, e))
            continue
        hit_by_agent[ag] = sorted(r)
        for k, v in r.items():
            studies.setdefault(k, v)
            prov.setdefault(k, []).append('agent:' + ag)
        time.sleep(0.2)

    # ---- snapshot: the manuscript is dated to a fixed cut-off, so records first
    # posted after it are dropped here (they are not "excluded", they are out of
    # scope).  Without this the counts drift every time the harvest is re-run.
    SNAPSHOT = '2026-10-20'
    def posted(s):
        d = ((s['protocolSection'].get('statusModule') or {})
             .get('studyFirstPostDateStruct') or {}).get('date', '') or ''
        return d[:10] if len(d) >= 10 else (d + '-01' if len(d) == 7 else '')
    late = [k for k, v in studies.items() if posted(v) > SNAPSHOT]
    for k in late:
        studies.pop(k, None)
    print('  snapshot %s: dropped %d record(s) first posted after the cut-off' % (SNAPSHOT, len(late)))

    print('\nunion: %d interventional studies' % len(studies))
    with open(os.path.join(RAW, 'studies_raw.json'), 'w') as f:
        json.dump({'fetched': time.strftime('%Y-%m-%dT%H:%M:%S'),
                   'api': 'ClinicalTrials.gov REST API v2',
                   'sweep_gene_expression': expr_a,
                   'agents_queried': sorted(set(AGENTS_RAS)),
                   'provenance': prov,
                   'agent_hits': hit_by_agent,
                   'studies': studies}, f, ensure_ascii=False)
    print('raw ->', os.path.join(RAW, 'studies_raw.json'))


if __name__ == '__main__':
    main()
