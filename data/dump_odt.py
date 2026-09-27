import os
import zipfile
import xml.etree.ElementTree as ET
import json
import collections

dir_path = os.path.dirname(os.path.abspath(__file__))
odt_path = os.path.join(dir_path, '..', 'documentos da zona 41', 'CONTROLE_PRESENCA_MESARIOS_DIA_DA_ELEICAO.odt')

with zipfile.ZipFile(odt_path) as z:
    xml_content = z.read('content.xml')

root = ET.fromstring(xml_content)
ns = {'table': 'urn:oasis:names:tc:opendocument:xmlns:table:1.0', 'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0'}

table = root.find('.//table:table', ns)
rows = table.findall('.//table:table-row', ns)

print(f"Total de linhas no ODT: {len(rows)}")

linhas_extraidas = []
for i, r in enumerate(rows):
    cells = r.findall('.//table:table-cell', ns)
    row_texts = []
    for c in cells:
        repeat = c.get(f"{{{ns['table']}}}number-columns-repeated")
        rep_count = min(int(repeat), 5) if repeat else 1
        ps = [p.text for p in c.findall('.//text:p', ns) if p.text]
        txt = " ".join(ps).strip()
        for _ in range(rep_count):
            row_texts.append(txt)
    
    # Remover colunas vazias à direita
    while row_texts and not row_texts[-1]:
        row_texts.pop()
    
    if row_texts:
        linhas_extraidas.append((i, row_texts))

print(f"Linhas com conteúdo: {len(linhas_extraidas)}")

# Imprimir as linhas para arquivo de texto para análise detalhada
with open(os.path.join(dir_path, 'dump_linhas_odt.txt'), 'w', encoding='utf-8') as f:
    for idx, (i, r) in enumerate(linhas_extraidas):
        f.write(f"L{i:03d} (col={len(r)}): {r}\n")

print("Dump salvo em dump_linhas_odt.txt!")
