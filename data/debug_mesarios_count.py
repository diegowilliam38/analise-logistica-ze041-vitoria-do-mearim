import zipfile
import xml.etree.ElementTree as ET
import sys
import collections

sys.stdout.reconfigure(encoding='utf-8')

import os
dir_path = os.path.dirname(os.path.abspath(__file__))
odt_path = os.path.join(dir_path, '..', 'documentos da zona 41', 'CONTROLE_PRESENCA_MESARIOS_DIA_DA_ELEICAO.odt')
with zipfile.ZipFile(odt_path) as z:
    xml_content = z.read('content.xml')

root = ET.fromstring(xml_content)
ns = {'table': 'urn:oasis:names:tc:opendocument:xmlns:table:1.0', 'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0'}

table = root.find('.//table:table', ns)
rows = table.findall('.//table:table-row', ns)

print(f"Total de linhas na tabela ODT: {len(rows)}")

parsed_rows = []
for i, r in enumerate(rows):
    cells = r.findall('.//table:table-cell', ns)
    texts = []
    for c in cells:
        repeat = c.get(f"{{{ns['table']}}}number-columns-repeated")
        rep_count = int(repeat) if repeat else 1
        ps = [p.text for p in c.findall('.//text:p', ns) if p.text]
        cell_str = ' '.join(ps).strip()
        for _ in range(rep_count):
            texts.append(cell_str)
    
    # Pegar os textos não vazios
    non_empty = [t for t in texts if t]
    parsed_rows.append((i, non_empty, texts[:6]))

print("Amostra das 15 primeiras linhas:")
for i, ne, t in parsed_rows[:15]:
    print(f"Linha {i}: non_empty({len(ne)}) -> {ne}")

# Vamos agrupar por seção
current_local = ""
current_secao = ""
mesarios_por_secao = collections.defaultdict(list)

for i, ne, t in parsed_rows:
    if not ne:
        continue
    # Se a linha contem cabeçalho
    if "FUNÇÃO" in ne or "NOME DO MESÁRIO" in ne:
        continue
    
    # Identificar formato da linha
    # Coluna 0: Local (as vezes presente quando muda) ou Seção ou vazio
    # Vamos ver como as colunas sao dispostas
    c0 = t[0] if len(t) > 0 else ""
    c1 = t[1] if len(t) > 1 else ""
    c2 = t[2] if len(t) > 2 else ""
    c3 = t[3] if len(t) > 3 else ""
    c4 = t[4] if len(t) > 4 else ""
    
    # Verificar se c0 tem nome de local
    if c0 and not c0.isdigit() and ("ESCOLA" in c0 or "COLEGIO" in c0 or "CENTRO" in c0 or "UNIDADE" in c0 or "IEMA" in c0 or "CEMA" in c0 or "JARDIM" in c0 or "CRECHE" in c0 or "INSTITUTO" in c0):
        current_local = c0
    
    # Se c1 é digito (numero da secao)
    if c1.isdigit():
        current_secao = c1
        funcao = c2
        nome = c3
        mesarios_por_secao[(current_local, current_secao)].append((i, funcao, nome))
    elif c0.isdigit():
        current_secao = c0
        funcao = c1
        nome = c2
        mesarios_por_secao[(current_local, current_secao)].append((i, funcao, nome))
    else:
        # Pode ser linha onde local e secao estao vazios (mesma secao anterior)
        # Ex: c0="", c1="", c2=funcao, c3=nome
        if c2 in ["Presidente", "1º Mesário", "2º Mesário", "1º Secretário", "Secretário"]:
            funcao = c2
            nome = c3
            mesarios_por_secao[(current_local, current_secao)].append((i, funcao, nome))
        elif c1 in ["Presidente", "1º Mesário", "2º Mesário", "1º Secretário", "Secretário"]:
            funcao = c1
            nome = c2
            mesarios_por_secao[(current_local, current_secao)].append((i, funcao, nome))
        else:
            # linha não reconhecida
            pass

total_mesarios = sum(len(v) for v in mesarios_por_secao.values())
print(f"\nTotal de seções mapeadas: {len(mesarios_por_secao)}")
print(f"Total de mesários mapeados: {total_mesarios}")

print("\nSeções com quantidade DIFERENTE de 4 mesários:")
for (loc, sec), m_list in sorted(mesarios_por_secao.items(), key=lambda x: int(x[0][1]) if x[0][1].isdigit() else 999):
    if len(m_list) != 4:
        print(f"  Local: {loc} | Seção: {sec} -> {len(m_list)} mesários:")
        for r_id, func, n in m_list:
            print(f"     L{r_id}: {func} - {n}")
