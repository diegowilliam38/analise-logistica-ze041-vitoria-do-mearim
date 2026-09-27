import os
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

dir_path = os.path.dirname(os.path.abspath(__file__))

# 1. ze041_inteligencia_consolidada.json
f1 = os.path.join(dir_path, 'ze041_inteligencia_consolidada.json')
with open(f1, 'r', encoding='utf-8') as f:
    master = json.load(f)

# Atualizar nos locais
for loc in master['locais']:
    if loc['num_local'] == 1015:
        loc['endereco'] = "MA-014, Povoado Jaguary"
        loc['bairro_povoado'] = "Povoado Jaguary"
        print("IEMA atualizado em master['locais']")

# Atualizar nas seções do IEMA
for s in master['secoes']:
    if s['num_local'] == 1015:
        s['endereco'] = "MA-014, Povoado Jaguary"
        s['bairro_povoado'] = "Povoado Jaguary"

with open(f1, 'w', encoding='utf-8') as f:
    json.dump(master, f, ensure_ascii=False, indent=2)
print("ze041_inteligencia_consolidada.json salvo com sucesso!")

# 2. edital_2026_locais_secoes.json
f2 = os.path.join(dir_path, 'edital_2026_locais_secoes.json')
if os.path.exists(f2):
    with open(f2, 'r', encoding='utf-8') as f:
        ed26 = json.load(f)
    locais_list = ed26.get('locais', ed26) if isinstance(ed26, dict) else ed26
    for item in locais_list:
        if isinstance(item, dict):
            if str(item.get('num_local')) == '1015' or str(item.get('cod_local')) == '1015' or 'Instituto Estadual' in item.get('nome', '') or 'IEMA' in item.get('nome', ''):
                item['endereco'] = "MA-014, Povoado Jaguary"
    with open(f2, 'w', encoding='utf-8') as f:
        json.dump(ed26, f, ensure_ascii=False, indent=2)
    print("edital_2026_locais_secoes.json salvo!")

# 3. logistica_consolidada_2026.json
f3 = os.path.join(dir_path, 'logistica_consolidada_2026.json')
with open(f3, 'r', encoding='utf-8') as f:
    log_cons = json.load(f)

# Nas rotas de moto
for m in log_cons.get('rotas_mototaxis', []):
    if 'IEMA' in m.get('local_atendido', ''):
        m['local_atendido'] = "IEMA Pleno de Vitória do Mearim (MA-014, Povoado Jaguary)"

# Nas rotas de veículos
for v in log_cons.get('rotas_veiculos_carga', []):
    if 'IEMA' in v.get('itinerario', ''):
        v['itinerario'] = v['itinerario'].replace("IEMA Pleno de Vitória do Mearim", "IEMA Pleno (MA-014, Povoado Jaguary)")

with open(f3, 'w', encoding='utf-8') as f:
    json.dump(log_cons, f, ensure_ascii=False, indent=2)
print("logistica_consolidada_2026.json atualizado!")

# 4. apoio_logistico_oficial_32_locais.json
f4 = os.path.join(dir_path, 'apoio_logistico_oficial_32_locais.json')
if os.path.exists(f4):
    with open(f4, 'r', encoding='utf-8') as f:
        ap = json.load(f)
    for item in ap:
        if item.get('num_local') == 1015:
            item['bairro_povoado'] = "MA-014, Povoado Jaguary"
    with open(f4, 'w', encoding='utf-8') as f:
        json.dump(ap, f, ensure_ascii=False, indent=2)
    print("apoio_logistico_oficial_32_locais.json atualizado!")
