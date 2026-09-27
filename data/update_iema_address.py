import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

# 1. Atualizar ze041_inteligencia_consolidada.json
path_intel = r'projects/analise-logistica-ze041-vitoria-do-mearim/data/ze041_inteligencia_consolidada.json'
with open(path_intel, 'r', encoding='utf-8') as f:
    intel = json.load(f)

# Atualizar endereço do IEMA (local 1015)
for loc in intel.get('locais', []):
    if loc.get('num_local') == 1015:
        loc['endereco'] = "MA-014, Povoado Jaguary"
        loc['bairro_povoado'] = "Povoado Jaguary (MA-014)"
        print("Atualizado local 1015 em locais!")

for sec in intel.get('secoes', []):
    if sec.get('num_local') == 1015:
        sec['endereco'] = "MA-014, Povoado Jaguary"
        sec['bairro_povoado'] = "Povoado Jaguary (MA-014)"

intel['edital_vigente'] = "Edital nº 20/2026 (Pós-2ª Vistoria)"

with open(path_intel, 'w', encoding='utf-8') as f:
    json.dump(intel, f, ensure_ascii=False, indent=2)

# 2. Atualizar edital_2026_locais_secoes.json
path_edital = r'projects/analise-logistica-ze041-vitoria-do-mearim/data/edital_2026_locais_secoes.json'
with open(path_edital, 'r', encoding='utf-8') as f:
    edital = json.load(f)

for loc in edital.get('locais', []):
    if loc.get('num_local') == '1015':
        loc['endereco'] = "MA-014, Povoado Jaguary"
        print("Atualizado local 1015 em edital_2026_locais_secoes.json!")

with open(path_edital, 'w', encoding='utf-8') as f:
    json.dump(edital, f, ensure_ascii=False, indent=2)

print("Endereço do IEMA atualizado com sucesso em todos os datasets!")
