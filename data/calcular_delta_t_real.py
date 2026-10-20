import json
import datetime
import sys

sys.stdout.reconfigure(encoding='utf-8')

# 1. Carregar dados de 2026 (1T)
with open('data/resultado_consolidado_1turno_2026.json', 'r', encoding='utf-8') as f:
    r26 = json.load(f)

# 2. Carregar dados de 2022 (BWEB TSE)
with open('data/dados_oficiais_tse_2022_ze041.json', 'r', encoding='utf-8') as f:
    d22 = json.load(f)

# 3. Carregar mestre para nomes de locais
with open('data/ze041_inteligencia_consolidada.json', 'r', encoding='utf-8') as f:
    master = json.load(f)

local_names = {}
for loc in master.get('locais', []):
    local_names[str(loc['num_local'])] = f"{loc['nome']} ({loc.get('bairro_povoado', '')})"

def parse_time(t_str):
    if not t_str: return None
    t_clean = t_str.split()[-1]
    parts = [int(p) for p in t_clean.split(':')]
    return datetime.timedelta(hours=parts[0], minutes=parts[1], seconds=parts[2])

print("================================================================================")
print("ANÁLISE DO TEMPO EMPÍRICO REAL DE TRANSPORTE (ENCERRAMENTO URNA -> TRANSMISSÃO)")
print("================================================================================")

# 2º Turno 2022
deltas_22 = {}
for sec in d22.get('segundo_turno', {}).get('secoes', []):
    t_enc = parse_time(sec.get('encerramento'))
    t_rec = parse_time(sec.get('bu_recebido'))
    if t_enc and t_rec:
        diff_m = (t_rec - t_enc).total_seconds() / 60.0
        loc = str(sec.get('local'))
        deltas_22.setdefault(loc, []).append({
            'secao': sec['secao'],
            'diff_m': diff_m,
            'enc': str(t_enc),
            'rec': str(t_rec)
        })

# 1º Turno 2026
deltas_26 = {}
secoes_26_map = r26.get('secoes', {})

# Para mapear secao -> local em 2026
sec_to_loc_26 = {}
for s_m in master.get('secoes', []):
    sec_to_loc_26[str(s_m['secao'])] = str(s_m['num_local'])

for s_num_str, s_info in secoes_26_map.items():
    t_enc = parse_time(s_info.get('encerramento'))
    t_rec = parse_time(s_info.get('recebido') or s_info.get('transmitido'))
    loc = sec_to_loc_26.get(s_num_str, 'Desconhecido')
    if t_enc and t_rec:
        diff_m = (t_rec - t_enc).total_seconds() / 60.0
        # Filtrar anomalias de retenção de mesários pós-encerramento
        deltas_26.setdefault(loc, []).append({
            'secao': s_num_str,
            'diff_m': diff_m,
            'enc': str(t_enc),
            'rec': str(t_rec)
        })

print("\n--- DELTAS EMPÍRICOS POR LOCAL (MEDIANA E MÉDIA EM MINUTOS) ---")
print(f"{'Local':<8} | {'Nome do Local':<40} | {'2T 2022 (Min-Med-Max)':<22} | {'1T 2026 (Mediana)':<18}")
print("-" * 95)

comparativo_locais = []

for loc_num in sorted(local_names.keys(), key=lambda x: int(x)):
    nome = local_names[loc_num][:40]
    d22_list = [x['diff_m'] for x in deltas_22.get(loc_num, [])]
    d26_list = [x['diff_m'] for x in deltas_26.get(loc_num, [])]

    d22_str = "--"
    d22_med = None
    if d22_list:
        d22_list.sort()
        d22_med = d22_list[len(d22_list)//2]
        d22_str = f"{min(d22_list):.0f}m - {d22_med:.0f}m - {max(d22_list):.0f}m"

    d26_str = "--"
    d26_med = None
    if d26_list:
        d26_list.sort()
        d26_med = d26_list[len(d26_list)//2]
        d26_str = f"{d26_med:.0f}m (min {min(d26_list):.0f}m)"

    comparativo_locais.append({
        'local_num': loc_num,
        'nome': nome,
        'med_22': d22_med,
        'med_26': d26_med
    })

    print(f"{loc_num:<8} | {nome:<40} | {d22_str:<22} | {d26_str:<18}")

print("\nExemplo Real Coque (Local 1570):")
if '1570' in deltas_22:
    for x in deltas_22['1570']:
        print(f"  2022 2T Seção {x['secao']}: Encerrou {x['enc']} -> Recebeu no Cartório {x['rec']} = Delta {x['diff_m']:.1f} min")

print("\nExemplo Real São Benedito (Local 1341):")
if '1341' in deltas_22:
    for x in deltas_22['1341']:
        print(f"  2022 2T Seção {x['secao']}: Encerrou {x['enc']} -> Recebeu no Cartório {x['rec']} = Delta {x['diff_m']:.1f} min")
