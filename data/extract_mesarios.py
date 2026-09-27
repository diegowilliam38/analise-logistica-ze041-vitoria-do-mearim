import zipfile
import xml.etree.ElementTree as ET
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

odt_path = r'projects/analise-logistica-ze041-vitoria-do-mearim/documentos da zona 41/CONTROLE_PRESENCA_MESARIOS_DIA_DA_ELEICAO.odt'
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
    if i == 0:
        continue # cabeçalho
    cells = r.findall('.//table:table-cell', ns)
    texts = []
    for c in cells:
        # Se a celula tiver repetição de colunas
        repeat = c.get(f"{{{ns['table']}}}number-columns-repeated")
        rep_count = int(repeat) if repeat else 1
        ps = [p.text for p in c.findall('.//text:p', ns) if p.text]
        cell_str = ' '.join(ps).strip()
        for _ in range(rep_count):
            texts.append(cell_str)
    
    # Remover células vazias do final além da assinatura
    texts = [t for t in texts if t != None]
    
    if len(texts) >= 4:
        # Se tem 5 ou mais elementos, o primeiro é o local
        if len(texts) >= 5 and texts[0] and not texts[0].isdigit():
            current_local = texts[0]
            current_secao = texts[1]
            funcao = texts[2]
            nome = texts[3]
        elif texts[0].isdigit():
            current_secao = texts[0]
            funcao = texts[1]
            nome = texts[2]
        else:
            # Caso seja cabeçalho de local no meio
            continue
        
        if nome and funcao:
            mesarios_lista.append({
                "local": current_local,
                "secao": current_secao,
                "funcao": funcao,
                "nome": nome
            })

print(f"Total de mesários extraídos: {len(mesarios_lista)}")

with open(r'projects/analise-logistica-ze041-vitoria-do-mearim/data/mesarios_secoes_2026.json', 'w', encoding='utf-8') as f:
    json.dump(mesarios_lista, f, ensure_ascii=False, indent=2)

# Exibir resumo por local
secoes_distintas = set(m['secao'] for m in mesarios_lista)
locais_distintos = set(m['local'] for m in mesarios_lista)
print(f"Total de Seções cobertas: {len(secoes_distintas)}")
print(f"Total de Locais cobertos: {len(locais_distintos)}")
print(f"Amostra dos 3 primeiros:")
for m in mesarios_lista[:3]:
    print(m)
