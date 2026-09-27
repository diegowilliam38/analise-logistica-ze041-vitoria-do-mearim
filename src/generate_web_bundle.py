import os
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

project_root = r'C:\Users\Diego William\OneDrive\Área de Trabalho\AIOS-WORKSPACE\projects\analise-logistica-ze041-vitoria-do-mearim'
data_dir = os.path.join(project_root, 'data')
web_dir = os.path.join(project_root, 'web')
js_dir = os.path.join(web_dir, 'js')

# 1. Carregar Master Intelligence
with open(os.path.join(data_dir, 'ze041_inteligencia_consolidada.json'), 'r', encoding='utf-8') as f:
    master = json.load(f)

# 2. Carregar Diagnostico
with open(os.path.join(data_dir, 'diagnostico_risco_operacional.json'), 'r', encoding='utf-8') as f:
    diagnostico = json.load(f)

# 3. Carregar Serie Historica
with open(os.path.join(data_dir, 'serie_historica_2016_2026.json'), 'r', encoding='utf-8') as f:
    serie_historica = json.load(f)

# 4. Carregar Demografia
with open(os.path.join(data_dir, 'demografia_ze041.json'), 'r', encoding='utf-8') as f:
    demografia = json.load(f)

# 5. Carregar Rotas e Logística Zonal
with open(os.path.join(data_dir, 'rotas_logistica_2026.json'), 'r', encoding='utf-8') as f:
    logistica_rotas = json.load(f)

# 5.1 Carregar Logística Consolidada Oficial (7 Rotas Carga, 31 Mototáxis, 32 Adms, 11 Coord Acessibilidade)
with open(os.path.join(data_dir, 'logistica_consolidada_2026.json'), 'r', encoding='utf-8') as f:
    logistica_consolidada = json.load(f)

# 6. Carregar Escala Oficial de Vistoria de ADH (Sábado & Domingo)
with open(os.path.join(data_dir, 'escala_adh_tecnicos_2026.json'), 'r', encoding='utf-8') as f:
    escala_adh = json.load(f)

# 7. Carregar Mesários Oficiais por Seção (375 mesários nas 94 seções)
with open(os.path.join(data_dir, 'mesarios_secoes_2026.json'), 'r', encoding='utf-8') as f:
    mesarios_secoes = json.load(f)

bundle = {
    "master": master,
    "diagnostico": diagnostico,
    "serie_historica": serie_historica,
    "demografia": demografia,
    "logistica": logistica_rotas,
    "logistica_consolidada": logistica_consolidada,
    "escala_adh": escala_adh,
    "mesarios_secoes": mesarios_secoes
}

js_content = f"// Dataset Oficial de Inteligência da 41ª ZE - Vitória do Mearim/MA\nwindow.ZE041_DATA = {json.dumps(bundle, ensure_ascii=False, indent=2)};\n"

with open(os.path.join(js_dir, 'data-payload.js'), 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"Arquivo data-payload.js atualizado com sucesso!")
print(f"Tamanho do payload: {len(js_content)} caracteres")
