import os
import zipfile
import xml.etree.ElementTree as ET
import json
import collections
import sys

sys.stdout.reconfigure(encoding='utf-8')

dir_path = os.path.dirname(os.path.abspath(__file__))
odt_path = os.path.join(dir_path, '..', 'documentos da zona 41', 'CONTROLE_PRESENCA_MESARIOS_DIA_DA_ELEICAO.odt')

with zipfile.ZipFile(odt_path) as z:
    xml_content = z.read('content.xml')

root = ET.fromstring(xml_content)
ns = {'table': 'urn:oasis:names:tc:opendocument:xmlns:table:1.0', 'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0'}

table = root.find('.//table:table', ns)
rows = table.findall('.//table:table-row', ns)

mesarios_lista = []
current_local = ""
current_secao = ""

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
    
    if not row_texts:
        continue
    
    # Pular cabeçalho
    if "FUNÇÃO" in " ".join(row_texts) or "NOME DO MESÁRIO" in " ".join(row_texts):
        continue
    
    # Caso 1: tem nome de local na primeira coluna (ex: ['IEMA', '1', 'Presidente', 'JHONY...'])
    if len(row_texts) >= 4 and not row_texts[0].isdigit():
        current_local = row_texts[0]
        current_secao = row_texts[1]
        funcao = row_texts[2]
        nome = row_texts[3]
    # Caso 2: começa com o número da seção (ex: ['1', '1º Mesário', 'PABLO...'])
    elif len(row_texts) >= 3 and row_texts[0].isdigit():
        current_secao = row_texts[0]
        funcao = row_texts[1]
        nome = row_texts[2]
    # Caso 3: apenas função e nome (seção implícita)
    elif len(row_texts) >= 2 and any(f in row_texts[0] for f in ['Presidente', 'Mesário', 'Secretário']):
        funcao = row_texts[0]
        nome = row_texts[1]
    else:
        print(f"Linha {i} não mapeada: {row_texts}")
        continue
    
    mesarios_lista.append({
        "local": current_local,
        "secao": current_secao,
        "funcao": funcao,
        "nome": nome
    })

print(f"Total de mesários extraídos: {len(mesarios_lista)}")

# Validar que temos exatamente 94 seções e 4 mesários por seção
secoes_map = collections.defaultdict(list)
for m in mesarios_lista:
    secoes_map[m["secao"]].append(m)

print(f"Total de seções distintas: {len(secoes_map)}")
incompletas = {s: len(m) for s, m in secoes_map.items() if len(m) != 4}
if incompletas:
    print(f"ATENÇÃO: Seções que não têm 4 mesários: {incompletas}")
else:
    print("PERFEITO: Todas as 94 seções têm exatamente 4 mesários (94 x 4 = 376 mesários)!")

# Salvar mesarios_secoes_2026.json
out_file = os.path.join(dir_path, 'mesarios_secoes_2026.json')
with open(out_file, 'w', encoding='utf-8') as f:
    json.dump(mesarios_lista, f, ensure_ascii=False, indent=2)

print(f"Arquivo {out_file} atualizado com sucesso!")
