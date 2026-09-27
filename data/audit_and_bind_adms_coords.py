import os
import sys
import json
import docx

sys.stdout.reconfigure(encoding='utf-8')

dir_path = os.path.dirname(os.path.abspath(__file__))
docs_dir = os.path.join(dir_path, '..', 'documentos da zona 41')

# 1. Carregar Locais de Votação Oficiais (32 locais)
with open(os.path.join(dir_path, 'ze041_inteligencia_consolidada.json'), 'r', encoding='utf-8') as f:
    master = json.load(f)
locais = master['locais']

# 2. Ler CONTROLE DE PRESENÇA ADM DE PREDIO.docx
adm_file = os.path.join(docs_dir, 'CONTROLE DE PRESENÇA ADM DE PREDIO.docx')
doc_adm = docx.Document(adm_file)
adms_doc = []

for table in doc_adm.tables:
    for row in table.rows:
        cells = [c.text.strip().replace('\n', ' ') for c in row.cells]
        if cells and cells[0].isdigit():
            num = int(cells[0])
            nome = cells[1].strip()
            local_desc = cells[2].strip()
            adms_doc.append({
                "num": num,
                "nome": nome,
                "local_trabalho_doc": local_desc
            })

print(f"Total de Administradores no documento: {len(adms_doc)}")

# 3. Ler CONTROLE DE PRESENÇA DE COORDENADORES DE ACESSIBILIDADE.docx
coord_file = os.path.join(docs_dir, 'CONTROLE DE PRESENÇA DE COORDENADORES DE ACESSIBILIDADE.docx')
doc_coord = docx.Document(coord_file)
coords_doc = []

for table in doc_coord.tables:
    for row in table.rows:
        cells = [c.text.strip().replace('\n', ' ') for c in row.cells]
        if cells and cells[0].isdigit():
            num = int(cells[0])
            nome = cells[1].strip()
            local_desc = cells[2].strip()
            coords_doc.append({
                "num": num,
                "nome": nome,
                "local_trabalho_doc": local_desc
            })

print(f"Total de Coordenadores no documento: {len(coords_doc)}")

# 4. Mapeamento dos 32 locais com os administradores de forma exata e verificada
# Vamos comparar string a string para garantir vínculo 1 a 1 perfeito
def norm(s):
    import unicodedata
    return unicodedata.normalize('NFKD', s).encode('ASCII', 'ignore').decode('ASCII').lower().replace('.', '').replace('-', '').replace('/', '')

mapa_locais_adms = []
for l in locais:
    num_l = l['num_local']
    nome_l = l['nome']
    bairro_l = l['bairro_povoado']
    norm_l = norm(nome_l + ' ' + bairro_l)
    
    # Encontrar melhor match nos adms
    matched_adm = None
    for a in adms_doc:
        norm_a = norm(a['local_trabalho_doc'])
        # Casos especiais conhecidos:
        if "euzebio" in norm_l or "jucaralzinho" in norm_l:
            if "euzebio" in norm_a or "jucaralzinho" in norm_a:
                matched_adm = a
                break
        elif "jucaral" in norm_l:
            if "jucaral" in norm_a and "jucaralzinho" not in norm_a:
                matched_adm = a
                break
        elif "iema" in norm_l:
            if "instituto de educacao" in norm_a or "iema" in norm_a:
                matched_adm = a
                break
        elif "cema" in norm_l:
            if norm_a == "cema" or "carlos raimundo" in norm_a:
                matched_adm = a
                break
        elif "eliud" in norm_l:
            if "eliud" in norm_a:
                matched_adm = a
                break
        elif "ana bogea" in norm_l:
            if "ana bogea" in norm_a:
                matched_adm = a
                break
        elif "antonia farias" in norm_l:
            if "antonia farias" in norm_a:
                matched_adm = a
                break
        elif "dr ribamar" in norm_l or "doutor ribamar" in norm_l:
            if "ribamar de matos" in norm_a:
                matched_adm = a
                break
        elif "neuza" in norm_l:
            if "neuza" in norm_a:
                matched_adm = a
                break
        elif "celeste" in norm_l:
            if "celeste" in norm_a:
                matched_adm = a
                break
        elif "graciana" in norm_l:
            if "graciana" in norm_a:
                matched_adm = a
                break
        elif "mons" in norm_l or "artur" in norm_l:
            if "artur" in norm_a:
                matched_adm = a
                break
        elif "escondido" in norm_l or "mauricia" in norm_l:
            if "mauricia" in norm_a:
                matched_adm = a
                break
        elif "mato grosso" in norm_l or "hemeterio" in norm_l:
            if "hemeterio" in norm_a:
                matched_adm = a
                break
        elif "tirirical" in norm_l:
            if "tirirical" in norm_a:
                matched_adm = a
                break
        elif "deodato" in norm_l:
            if "deodato" in norm_a:
                matched_adm = a
                break
        elif "franklin" in norm_l:
            if "franklin" in norm_a:
                matched_adm = a
                break
        elif "itelvino" in norm_l:
            if "itelvino" in norm_a:
                matched_adm = a
                break
        elif "vila falcao" in norm_l:
            if "falcao" in norm_a:
                matched_adm = a
                break
        elif "vila nova" in norm_l:
            if "vila nova" in norm_a:
                matched_adm = a
                break
        elif "nasser" in norm_l:
            if "nasser" in norm_a:
                matched_adm = a
                break
        elif "creche" in norm_l:
            if "creche" in norm_a:
                matched_adm = a
                break
        elif "raimundo bogea" in norm_l:
            if "raimundo bogea" in norm_a:
                matched_adm = a
                break
        elif "jaguary" in norm_l or "francisco xavier" in norm_l:
            if "francisco xavier" in norm_a:
                matched_adm = a
                break
        elif "godofredo" in norm_l or "sao felix" in norm_l:
            if "godofredo" in norm_a:
                matched_adm = a
                break
        elif "livramento" in norm_l or "izidoro" in norm_l:
            if "izidoro" in norm_a:
                matched_adm = a
                break
        elif "sumauma" in norm_l or "mota silva" in norm_l:
            if "mota silva" in norm_a:
                matched_adm = a
                break
        elif "santa rosa" in norm_l or "jose ribamar" in norm_l:
            if "jose ribamar silva" in norm_a:
                matched_adm = a
                break
        elif "sao benedito" in norm_l or "paulo maciel" in norm_l:
            if "paulo maciel" in norm_a:
                matched_adm = a
                break
        elif "boca do campo" in norm_l or "abidao" in norm_l:
            if "abidao" in norm_a:
                matched_adm = a
                break
        elif "ipixuna" in norm_l:
            if "ipixuna" in norm_a:
                matched_adm = a
                break
        elif "jacaray" in norm_l or "mamedio" in norm_l:
            if "mamedio" in norm_a:
                matched_adm = a
                break

    # Match de coordenador de acessibilidade (se houver)
    matched_coord = None
    for c in coords_doc:
        norm_c = norm(c['local_trabalho_doc'])
        if "itelvino" in norm_l and "itelvino" in norm_c:
            matched_coord = c
        elif "nasser" in norm_l and "nasser" in norm_c:
            matched_coord = c
        elif "eliud" in norm_l and "eliud" in norm_c:
            matched_coord = c
        elif "graciana" in norm_l and "graciana" in norm_c:
            matched_coord = c
        elif "antonia farias" in norm_l and "antonia farias" in norm_c:
            matched_coord = c
        elif ("mons" in norm_l or "artur" in norm_l) and "artur" in norm_c:
            matched_coord = c
        elif "iema" in norm_l and ("instituto" in norm_c or "iema" in norm_c):
            matched_coord = c
        elif "cema" in norm_l and "cema" in norm_c:
            matched_coord = c
        elif "neuza" in norm_l and "neuza" in norm_c:
            matched_coord = c
        elif "celeste" in norm_l and "celeste" in norm_c:
            matched_coord = c
        elif "ana bogea" in norm_l and "ana bogea" in norm_c:
            matched_coord = c

    mapa_locais_adms.append({
        "num_local": num_l,
        "nome_local": nome_l,
        "bairro_povoado": bairro_l,
        "total_secoes": l['total_secoes'],
        "secoes": l['secoes'],
        "total_aptos_2026": l['total_aptos_2026'],
        "is_dificil_acesso": (num_l == 1392 or "juçaral" in norm_l),
        "administrador_predio": {
            "num": matched_adm['num'] if matched_adm else None,
            "nome": matched_adm['nome'] if matched_adm else "NÃO IDENTIFICADO",
            "local_doc": matched_adm['local_trabalho_doc'] if matched_adm else None
        },
        "coordenador_acessibilidade": {
            "num": matched_coord['num'] if matched_coord else None,
            "nome": matched_coord['nome'] if matched_coord else None,
            "local_doc": matched_coord['local_trabalho_doc'] if matched_coord else None
        } if matched_coord else None
    })

# Imprimir validação
print("\n=== VALIDAÇÃO DE VÍNCULO DOS 32 LOCAIS ===")
sem_adm = [x for x in mapa_locais_adms if x['administrador_predio']['nome'] == "NÃO IDENTIFICADO"]
if sem_adm:
    print(f"ATENÇÃO: {len(sem_adm)} locais sem Administrador:")
    for s in sem_adm:
        print(f"  Local {s['num_local']}: {s['nome_local']}")
else:
    print("SUCESSO ABSOLUTO: Todos os 32 locais possuem Administrador de Prédio oficial vinculado!")

adms_utilizados = set(x['administrador_predio']['num'] for x in mapa_locais_adms)
print(f"Total de Administradores únicos vinculados: {len(adms_utilizados)} de {len(adms_doc)}")

# Verificar Juçaral
jucaral = next(x for x in mapa_locais_adms if x['num_local'] == 1392)
print(f"\nLocal Difícil Acesso (Juçaral das Margaridas - Local 1392):")
print(f"  Nome: {jucaral['nome_local']}")
print(f"  Adm de Prédio: {jucaral['administrador_predio']['nome']}")
print(f"  Local no Doc: {jucaral['administrador_predio']['local_doc']}")

# Salvar o mapeamento auditado
with open(os.path.join(dir_path, 'apoio_logistico_oficial_32_locais.json'), 'w', encoding='utf-8') as f:
    json.dump(mapa_locais_adms, f, ensure_ascii=False, indent=2)

print("Arquivo apoio_logistico_oficial_32_locais.json salvo com sucesso!")
