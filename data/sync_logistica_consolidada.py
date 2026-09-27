import os
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

dir_path = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(dir_path, 'logistica_consolidada_2026.json'), 'r', encoding='utf-8') as f:
    log_cons = json.load(f)

with open(os.path.join(dir_path, 'apoio_logistico_oficial_32_locais.json'), 'r', encoding='utf-8') as f:
    apoio_32 = json.load(f)

# Atualizar administradores_predio e coordenadores_acessibilidade
# com base no arquivo auditado
adms_atualizados = []
for x in apoio_32:
    adm_info = x['administrador_predio']
    adms_atualizados.append({
        "num": adm_info['num'],
        "nome": adm_info['nome'],
        "num_local": x['num_local'],
        "local": x['nome_local'],
        "bairro_povoado": x['bairro_povoado'],
        "total_secoes": x['total_secoes'],
        "secoes": x['secoes'],
        "is_dificil_acesso": x['is_dificil_acesso'],
        "local_doc_original": adm_info['local_doc']
    })

coords_atualizados = []
for x in apoio_32:
    if x['coordenador_acessibilidade']:
        c_info = x['coordenador_acessibilidade']
        coords_atualizados.append({
            "num": c_info['num'],
            "nome": c_info['nome'],
            "num_local": x['num_local'],
            "local": x['nome_local'],
            "bairro_povoado": x['bairro_povoado'],
            "total_secoes": x['total_secoes'],
            "secoes": x['secoes'],
            "local_doc_original": c_info['local_doc']
        })

log_cons['administradores_predio'] = adms_atualizados
log_cons['coordenadores_acessibilidade'] = coords_atualizados
log_cons['apoio_logistico_32_locais'] = apoio_32

with open(os.path.join(dir_path, 'logistica_consolidada_2026.json'), 'w', encoding='utf-8') as f:
    json.dump(log_cons, f, ensure_ascii=False, indent=2)

print("logistica_consolidada_2026.json sincronizado com sucesso!")
print(f"Total Adms: {len(adms_atualizados)}")
print(f"Total Coords: {len(coords_atualizados)}")
