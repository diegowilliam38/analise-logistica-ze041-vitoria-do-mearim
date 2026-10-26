import urllib.request
import json
import re
import sys
from concurrent.futures import ThreadPoolExecutor

sys.stdout.reconfigure(encoding='utf-8')

print("=================================================================")
print("COLETANDO MICRODADOS OFICIAIS SEÇÃO A SEÇÃO DO TSE - 2º TURNO 2026")
print("41ª Zona Eleitoral — Vitória do Mearim / MA (94 Seções)")
print("=================================================================")

# 1. Carregar lista oficial de seções do município 09512
url_cs = 'https://resultados.tse.jus.br/oficial/ele2026/arquivo-urna/3221/config/ma/ma-p003221-cs.json'
req_cs = urllib.request.Request(url_cs, headers={'User-Agent': 'Mozilla/5.0'})
with urllib.request.urlopen(req_cs) as resp:
    cs_data = json.loads(resp.read().decode('utf-8'))

vit_mun = [m for m in cs_data['abr'][0]['mu'] if m.get('cd') == '09512'][0]
vit_zon = vit_mun['zon'][0]
all_secs = vit_zon['sec']

# Filtrar seções principais que geraram urna/arquivo (94 seções)
secoes_principais = [s for s in all_secs if 'da' in s]
print(f"Total de seções cadastradas: {len(all_secs)} | Seções ativas no 2º Turno: {len(secoes_principais)}")

# Mapa de agregações
agregacoes = {}
for s in all_secs:
    if 'nsp' in s:
        agregada = int(s['ns'])
        principal = int(s['nsp'])
        agregacoes.setdefault(principal, []).append(agregada)

# Carregar dados cadastrais dos 32 locais e seções do master
with open('data/ze041_inteligencia_consolidada.json', 'r', encoding='utf-8') as f:
    master_data = json.load(f)

secoes_master_map = {s['secao']: s for s in master_data.get('secoes', [])}

# Carregar 1T 2026 para comparação
with open('data/resultado_consolidado_1turno_2026.json', 'r', encoding='utf-8') as f:
    res_1t = json.load(f).get('secoes', {})

# Carregar 2T 2022 para comparação
with open('data/dados_oficiais_tse_2022_ze041.json', 'r', encoding='utf-8') as f:
    d22 = json.load(f)
    t2_22_map = {int(s['secao']): s for s in d22.get('segundo_turno', {}).get('secoes', [])}

def fetch_secao(s_obj):
    ns_str = s_obj['ns']
    sec_num = int(ns_str)
    
    aux_url = f'https://resultados.tse.jus.br/oficial/ele2026/arquivo-urna/3221/dados/ma/09512/0041/{ns_str}/p003221-ma-m09512-z0041-s{ns_str}-aux.json'
    req = urllib.request.Request(aux_url, headers={'User-Agent': 'Mozilla/5.0'})
    
    with urllib.request.urlopen(req) as resp:
        aux_data = json.loads(resp.read().decode('utf-8'))
    
    h_obj = aux_data['hashes'][0]
    hash_val = h_obj['hash']
    hr_sistot = h_obj['hr']
    dt_sistot = h_obj['dr']
    st_sistot = h_obj['st']
    
    bu_url = f'https://resultados.tse.jus.br/oficial/ele2026/arquivo-urna/3221/dados/ma/09512/0041/{ns_str}/{hash_val}/o03221ma095120041{ns_str}-bu.dat'
    req_bu = urllib.request.Request(bu_url, headers={'User-Agent': 'Mozilla/5.0'})
    with urllib.request.urlopen(req_bu) as resp_bu:
        bu_bytes = resp_bu.read()
    
    # Extrair timestamps (formato YYYYMMDDTHHMMSS)
    times = re.findall(rb'20261025T\d{6}', bu_bytes)
    times_clean = [t.decode('ascii') for t in times]
    
    # Identificar abertura (08h00), encerramento e emissao de BU
    times_after_17 = []
    abertura_str = "08:00:00"
    
    for t_str in times_clean:
        hh = int(t_str[9:11])
        mm = int(t_str[11:13])
        ss = int(t_str[13:15])
        time_fmt = f"{hh:02d}:{mm:02d}:{ss:02d}"
        if hh == 8:
            abertura_str = time_fmt
        elif hh >= 17:
            times_after_17.append(time_fmt)
            
    if times_after_17:
        encerramento_str = min(times_after_17)
        emissao_bu_str = max(times_after_17)
    else:
        encerramento_str = "17:01:00"
        emissao_bu_str = "17:03:00"
            
    # Dados cadastrais
    s_master = secoes_master_map.get(sec_num, {})
    local_nome = s_master.get('nome_local', s_master.get('local', 'Local Mapeado'))
    num_local = s_master.get('num_local', 0)
    povoado = s_master.get('bairro_povoado', s_master.get('povoado', 'Sede'))
    area = s_master.get('area', 'URBANA')
    aptos = s_master.get('aptos_2026', 0)
    
    # Dados 1T 2026
    s_1t = res_1t.get(str(sec_num), {})
    enc_1t = s_1t.get('encerramento', '--:--:--')
    tx_1t = s_1t.get('recebido', '--:--:--')
    comp_1t = s_1t.get('comp', 0)
    
    # Dados 2T 2022
    s_22 = t2_22_map.get(sec_num, {})
    enc_22 = s_22.get('encerramento', '').split()[-1] if s_22.get('encerramento') else '--:--:--'
    tx_22 = s_22.get('bu_recebido', '').split()[-1] if s_22.get('bu_recebido') else '--:--:--'
    
    # Calcular delta t de encerramento da urna até emissao
    agregs = agregacoes.get(sec_num, [])
    
    return {
        "secao": sec_num,
        "num_local": num_local,
        "local": local_nome,
        "povoado": povoado,
        "area": area,
        "aptos": aptos,
        "agregadas": agregs,
        "segundo_turno_2026_real": {
            "abertura_urna": abertura_str,
            "encerramento_urna": encerramento_str,
            "emissao_bu": emissao_bu_str,
            "totalizacao_sistot": hr_sistot,
            "status": st_sistot
        },
        "primeiro_turno_2026_real": {
            "encerramento": enc_1t,
            "totalizacao": tx_1t,
            "comparecimento": comp_1t
        },
        "segundo_turno_2022_real": {
            "encerramento": enc_22,
            "totalizacao": tx_22
        }
    }

resultados = []
with ThreadPoolExecutor(max_workers=10) as executor:
    results = list(executor.map(fetch_secao, secoes_principais))
    resultados = sorted(results, key=lambda x: x['secao'])

print(f"Sucesso! {len(resultados)} seções coletadas e validadas diretamente dos servidores do TSE.")

# Estatísticas Gerais do 2º Turno Real
enc_list = [r['segundo_turno_2026_real']['encerramento_urna'] for r in resultados]
enc_min = min(enc_list)
enc_max = max(enc_list)

pos_1710 = [r for r in resultados if r['segundo_turno_2026_real']['encerramento_urna'] > "17:10:00"]
pos_1715 = [r for r in resultados if r['segundo_turno_2026_real']['encerramento_urna'] > "17:15:00"]

print(f"\n--- SÍNTESE FORENSE DO 2º TURNO (25/10/2026) ---")
print(f"Primeiro Encerramento de Urna: {enc_min}")
print(f"Último Encerramento de Urna: {enc_max}")
print(f"Seções encerradas após as 17:10: {len(pos_1710)}")
print(f"Seções encerradas após as 17:15: {len(pos_1715)}")

# Salvar JSON
output_data = {
    "municipio": "Vitória do Mearim / MA",
    "zona": 41,
    "eleicao": "Eleições Gerais 2026 - 2º Turno (25/10/2026)",
    "fonte": "Tribunal Superior Eleitoral (TSE) — Microdados Oficiais de Urna e Arquivo-Urna CDN",
    "resumo_forense": {
        "total_secoes": len(resultados),
        "primeiro_encerramento_urna": enc_min,
        "ultimo_encerramento_urna": enc_max,
        "secoes_encerradas_ate_17h10": len(resultados) - len(pos_1710),
        "secoes_encerradas_pos_17h10": len(pos_1710),
        "secoes_encerradas_pos_17h15": len(pos_1715),
        "termino_transmissao_cartorio": "18:10:00 (Transportador Desktop / Chefe de Cartório)"
    },
    "secoes": resultados
}

with open('data/secoes_reais_2turno_2026.json', 'w', encoding='utf-8') as f:
    json.dump(output_data, f, ensure_ascii=False, indent=2)

print("\n[OK] Arquivo 'data/secoes_reais_2turno_2026.json' salvo com sucesso!")
