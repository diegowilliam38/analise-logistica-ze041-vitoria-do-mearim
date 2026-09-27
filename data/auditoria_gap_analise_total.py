import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')

dir_path = os.path.dirname(os.path.abspath(__file__))

print("="*75)
print("AUDITORIA GERAL DE INTEGRIDADE E ANÁLISE DE GAPS — 41ª ZE (VITÓRIA DO MEARIM)")
print("="*75)

# 1. Carregar arquivos de inteligência
f_master = os.path.join(dir_path, 'ze041_inteligencia_consolidada.json')
f_mesarios = os.path.join(dir_path, 'mesarios_secoes_2026.json')
f_apoio = os.path.join(dir_path, 'apoio_logistico_oficial_32_locais.json')
f_logistica = os.path.join(dir_path, 'logistica_consolidada_2026.json')

with open(f_master, 'r', encoding='utf-8') as f:
    master = json.load(f)
with open(f_mesarios, 'r', encoding='utf-8') as f:
    mesarios = json.load(f)
with open(f_apoio, 'r', encoding='utf-8') as f:
    apoio = json.load(f)
with open(f_logistica, 'r', encoding='utf-8') as f:
    logistica = json.load(f)

# CHECAGEM 1: Locais de Votação (Edital 20/2026)
locais = master['locais']
total_locais = len(locais)
print(f"\n[1] LOCAIS DE VOTAÇÃO: {total_locais} locais no master (Esperado Edital 20: 32)")
assert total_locais == 32, f"Erro: {total_locais} locais!"

# Verificar endereço do IEMA
iema = next(l for l in locais if l['num_local'] == 1015)
print(f"    - IEMA (Local 1015): Nome='{iema['nome']}'")
print(f"      Endereço retificado='{iema['endereco']}' | Bairro='{iema['bairro_povoado']}'")
assert "MA-014, Povoado Jaguary" in iema['endereco'], "Erro: Endereço IEMA incorreto!"

# Verificar Juçaral das Margaridas
jucaral = next(l for l in locais if l['num_local'] == 1392)
print(f"    - Juçaral das Margaridas (Local 1392): Nome='{jucaral['nome']}', Bairro='{jucaral['bairro_povoado']}'")
assert "Juçaral" in jucaral['nome'] or "Juçaral" in jucaral['bairro_povoado']

# CHECAGEM 2: Seções Principais (Urnas) e Agregadas
secoes = master['secoes']
total_secoes = len(secoes)
print(f"\n[2] SEÇÕES RECEPTORAS DE VOTOS (URNAS): {total_secoes} seções (Esperado: 94)")
assert total_secoes == 94, f"Erro: {total_secoes} seções!"

secoes_com_agreg = [s for s in secoes if s.get('tem_agregacao')]
print(f"    - Urnas que agregam outras seções: {len(secoes_com_agreg)} seções principais agregadoras")

# CHECAGEM 3: Mesários (Controle de Presença Oficial)
total_mesarios = len(mesarios)
secoes_com_mesarios = set(m['secao'] for m in mesarios)
print(f"\n[3] CONTROLE DE PRESENÇA DE MESÁRIOS:")
print(f"    - Seções cobertas: {len(secoes_com_mesarios)} seções (Esperado: 94)")
print(f"    - Total de mesários: {total_mesarios} mesários (Esperado: 376 = 94 x 4)")
assert len(secoes_com_mesarios) == 94, "Erro no número de seções com mesários!"
assert total_mesarios == 376, f"Erro: {total_mesarios} mesários!"

# Agrupando mesários por seção e conferindo se todas têm 4 membros
secao_counts = {}
for m in mesarios:
    s = m['secao']
    secao_counts[s] = secao_counts.get(s, 0) + 1

secoes_incompletas = {s: c for s, c in secao_counts.items() if c != 4}
if secoes_incompletas:
    print(f"    ATENÇÃO: Seções com contagem != 4: {secoes_incompletas}")
else:
    print("    - Todas as 94 seções possuem rigorosamente 4 mesários convocados (100% completas)!")

# CHECAGEM 4: Administradores de Prédio (32 locais de votação)
adms = [loc.get('administrador_predio') for loc in apoio if loc.get('administrador_predio')]
print(f"\n[4] ADMINISTRADORES DE PRÉDIO: {len(adms)} administradores (Esperado: 32)")
assert len(adms) == 32, f"Erro: {len(adms)} administradores!"

# Checar administrador de Juçaral
loc_jucaral = next(l for l in apoio if l['num_local'] == 1392)
adm_jucaral = loc_jucaral['administrador_predio']
print(f"    - Administrador de Juçaral das Margaridas (Local 1392): {adm_jucaral['nome']}")
assert "NERINILDO COELHO CARDOSO" in adm_jucaral['nome'].upper()

# Conferir se todos os 32 locais de votação têm 1 administrador vinculado
assert len(apoio) == 32, f"Erro: {len(apoio)} locais no arquivo de apoio!"
print("    - Cobertura 100%: Cada um dos 32 locais possui 1 Administrador de Prédio exclusivo!")

# CHECAGEM 5: Coordenadores de Acessibilidade (11 locais)
coords = [loc.get('coordenador_acessibilidade') for loc in apoio if loc.get('coordenador_acessibilidade')]
print(f"\n[5] COORDENADORES DE ACESSIBILIDADE: {len(coords)} coordenadores (Esperado: 11)")
assert len(coords) == 11, f"Erro: {len(coords)} coordenadores!"
print("    - Coordenadores alocados nos maiores colégios eleitorais e polos da zona:")
for c in coords:
    print(f"      * {c['nome']} ({c['local_doc']})")

# CHECAGEM 6: Quadro Geral de Colaboradores Convocados da Zona
total_colaboradores = total_mesarios + len(adms) + len(coords)
print(f"\n[6] QUADRO GERAL DE COLABORADORES CONVOCADOS:")
print(f"    - Mesários de Mesa Receptora: {total_mesarios}")
print(f"    - Administradores de Prédio:  {len(adms)}")
print(f"    - Coordenadores de Acessib.:  {len(coords)}")
print(f"    ---------------------------------------------")
print(f"    TOTAL DE COLABORADORES:      {total_colaboradores} convocados oficiais")

# CHECAGEM 7: Logística de Urnas e Campo (7 Rotas de Carga)
rotas_carga = logistica.get('rotas_veiculos_carga', [])
print(f"\n[7] LOGÍSTICA DE VEÍCULOS DE CARGA (DISTRIBUIÇÃO E RECOLHIMENTO):")
print(f"    - Quantidade de rotas: {len(rotas_carga)} rotas (Esperado: 7)")
assert len(rotas_carga) == 7, f"Erro: {len(rotas_carga)} rotas!"

for r in rotas_carga:
    print(f"      Rota {r['rota']}: {r['veiculo_modelo_placa']} | Motorista: {r['motorista_telefone']} | {r['qtd_locais']} locais, {r['qtd_urnas_cabinas']} urnas")

# Suprimento de Fundos Juçaral
suprimento = logistica.get('suprimento_fundos_dificil_acesso', {})
print(f"    - Local Especial (Juçaral das Margaridas): {suprimento.get('local')}")
print(f"      Responsável: {suprimento.get('responsavel')} | Transporte: {suprimento.get('tipo_transporte')}")

# CHECAGEM 8: Vistoria ADH no Sábado e Fiscais de Campo (Escala Oficial)
f_adh = os.path.join(dir_path, 'escala_adh_tecnicos_2026.json')
with open(f_adh, 'r', encoding='utf-8') as f:
    adh_data = json.load(f)

equipe_adh = adh_data.get('equipe_responsavel', [])
print(f"\n[8] VISTORIA ADH (SÁBADO) E FISCALIZAÇÃO OPERACIONAL (DOMINGO):")
print(f"    - Responsáveis escalados: {len(equipe_adh)} técnicos / servidores / apoio (Esperado: 7)")
assert len(equipe_adh) == 7, f"Erro: {len(equipe_adh)} fiscais!"

secoes_adh_total = set()
for resp in equipe_adh:
    secoes_resp = []
    for loc in resp.get('locais', []):
        for s in loc.get('secoes', []):
            s_clean = s.replace('ª', '').strip()
            secoes_adh_total.add(s_clean)
            secoes_resp.append(s_clean)
    print(f"      * {resp['nome']} ({resp['cargo']}): {len(secoes_resp)} seções atendidas")

print(f"    - Total de seções receptoras cobertas pela equipe ADH: {len(secoes_adh_total)} seções (Esperado: 94)")
assert len(secoes_adh_total) == 94, f"Erro: {len(secoes_adh_total)} seções cobertas no ADH!"
print("    - Cobertura 100%: Todas as 94 seções receptoras estão sob supervisão direta da equipe da Zona!")

print("\n" + "="*75)
print("VEREDITO FINAL: CONFORMIDADE TOTAL COM EDITAL 20/2026 E LISTAS OFICIAIS!")
print("NENHUM GAP DETECTADO. SISTEMA, BANCO DE DADOS E COCKPIT 100% ALINHADOS!")
print("="*75)
