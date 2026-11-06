#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""三个 RAS 基因全部蛋白编码转录本的「第一外显子」（5′ 端那一个）。

用法: python3 -I 06_first_exons.py <root>
输出: <root>/数据/表8_可变第一外显子.csv

数据源与 `01_fetch.py` 同一条接口：Ensembl REST
    /lookup/id/<ENSG>?expand=1;content-type=application/json
（GRCh38；本次 2026-11-04 实取，基因坐标与 2026-10-20 那次逐位一致——KRAS
 12:25 205 246–25 326 473、HRAS 11:532 242–537 343、NRAS 1:114 704 468–114 716 775。）

为什么要这张表：图2a 原来只画「参考转录本从第一个到最后一个外显子」，于是轴题
只能写「距第一个外显子」，而基因座本身长得多（KRAS 121.2 kb，其中 75 kb 在参考
转录本上游）。把其余转录本的第一外显子摆到真实坐标上，轴题才可以是「距基因
5′ 端」，读者也才看得见 KRAS 那 121 kb 是怎么来的：最上游一个 70 bp 的第一外显子，
接着一段 81 kb 的内含子，然后才是共用的外显子群。

只取 `biotype == protein_coding`：NMD 与 retained_intron 的 5′ 端常在同一个启动子
区里重复出现，画上去只会加粗同一条竖线，不增加信息。

列：gene / transcript / biotype / exon_start / exon_end / exon_len / is_ref
    is_ref=1 表示该转录本就是 表1 里那四条参考转录本之一（KRAS4B ENST00000311936、
    KRAS4A ENST00000256078、HRAS ENST00000311189、NRAS ENST00000369535）。
"""
import csv
import json
import os
import sys
import time
import urllib.request

ROOT = sys.argv[1]
DATA = os.path.join(ROOT, '数据')
ENSG = {'KRAS': 'ENSG00000133703', 'HRAS': 'ENSG00000174775',
        'NRAS': 'ENSG00000213281'}
REF = {'ENST00000311936', 'ENST00000256078',
       'ENST00000311189', 'ENST00000369535'}
API = ('https://rest.ensembl.org/lookup/id/%s?expand=1;'
       'content-type=application/json')
UA = {'User-Agent': 'RAS-review-gene-structure/1.0 (academic use)',
      'Content-Type': 'application/json'}


def get(url, tries=4):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=90) as r:
                return json.loads(r.read().decode('utf-8'))
        except Exception as e:                      # noqa: BLE001
            if i == tries - 1:
                raise
            print('  重试 %d/%d：%s' % (i + 1, tries, e))
            time.sleep(2)


out = []
for gene, en in ENSG.items():
    d = get(API % en)
    assert d['display_name'] == gene, (gene, d['display_name'])
    assert d['assembly_name'] == 'GRCh38', d['assembly_name']
    strand = d['strand']
    assert strand == -1, '第一外显子的取法只对负链写过（%s 是 %d）' % (gene, strand)
    tx = [t for t in d['Transcript'] if t['biotype'] == 'protein_coding']
    for t in tx:
        ex = max(t['Exon'], key=lambda e: e['end'])     # 负链：坐标大的那端是 5′
        out.append({'gene': gene, 'transcript': t['id'],
                    'biotype': t['biotype'],
                    'exon_start': ex['start'], 'exon_end': ex['end'],
                    'exon_len': ex['end'] - ex['start'] + 1,
                    'is_ref': 1 if t['id'] in REF else 0})
    print('  %-5s 基因 %d–%d（%.1f kb）｜蛋白编码转录本 %d 条，第一外显子 %d 个'
          % (gene, d['start'], d['end'], (d['end'] - d['start']) / 1000,
             len(tx), len({(r['exon_start'], r['exon_end'])
                           for r in out if r['gene'] == gene})))

out.sort(key=lambda r: (list(ENSG).index(r['gene']), -r['exon_end'], r['transcript']))
path = os.path.join(DATA, '表8_可变第一外显子.csv')
with open(path, 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=['gene', 'transcript', 'biotype',
                                       'exon_start', 'exon_end', 'exon_len',
                                       'is_ref'])
    w.writeheader()
    w.writerows(out)
print('  ->', os.path.relpath(path, ROOT), len(out), '行')
