import os
import sys
import re
import json

sys.stdout.reconfigure(encoding='utf-8')

dir_path = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(dir_path, 'edital_20_texto_completo.txt'), 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Extrair locais e seções do texto do Edital 20
# Formato típico no PDF do TRE-MA:
# Local de Votação: 1015 - INSTITUTO DE EDUCAÇÃO, CIÊNCIA E TECNOLOGIA DO MARANHÃO - IEMA PLENO
# Endereço: MA-014, POVOADO JAGUARY
# Seções: 1, 2, 3, 19, 84, 188
# Seções agregadas: ...

print("=== PARSER DO EDITAL Nº 20/2026 ===")

# Expressões regulares para locais e seções
# Vamos buscar blocos de locais
# Padrões comuns: "Local de Votação: XXXX" ou "XXXX - NOME DO LOCAL"
linhas = text.split('\n')

locais_edital20 = []
curr_local = None

for l in linhas:
    l_str = l.strip()
    if not l_str or l_str.startswith('--- PAGINA'):
        continue
    
    # Detecção de cabeçalho de local
    # Ex: "1015 - INSTITUTO DE EDUCAÇÃO..." ou "Local de Votação: 1015"
    m_loc = re.search(r'(?:Local\s+de\s+Votação:\s*)?(\d{4})\s*[-–]\s*(.+)', l_str, re.IGNORECASE)
    if m_loc:
        num = int(m_loc.group(1))
        nome = m_loc.group(2).strip()
        curr_local = {
            "num_local": num,
            "nome": nome,
            "endereco": "",
            "linhas_secoes": []
        }
        locais_edital20.append(curr_local)
        continue
    
    if curr_local:
        if "Endereço:" in l_str or "Endereco:" in l_str:
            curr_local["endereco"] = l_str.replace("Endereço:", "").replace("Endereco:", "").strip()
        else:
            curr_local["linhas_secoes"].append(l_str)

print(f"Total de locais detectados no Edital 20: {len(locais_edital20)}")

# Se a regex pegou os 32 locais, vamos listar
for loc in locais_edital20:
    print(f"Local {loc['num_local']}: {loc['nome']} | End: {loc['endereco']}")
