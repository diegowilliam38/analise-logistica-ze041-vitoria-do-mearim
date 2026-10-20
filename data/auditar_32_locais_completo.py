import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

with open('data/ze041_inteligencia_consolidada.json', 'r', encoding='utf-8') as f:
    master = json.load(f)

with open('data/rotas_logistica_2026.json', 'r', encoding='utf-8') as f:
    rotas = json.load(f)

with open('data/logistica_consolidada_2026.json', 'r', encoding='utf-8') as f:
    log_cons = json.load(f)

print("=" * 110)
print(f"{'Nº':<5} | {'NOME DO LOCAL OFICIAL':<42} | {'BAIRRO / POVOADO':<26} | {'ÁREA':<7} | {'SEÇÕES'}")
print("=" * 110)

locais_list = sorted(master['locais'], key=lambda x: int(x['num_local']))
for l in locais_list:
    num = l['num_local']
    nome = l['nome']
    bairro = l.get('bairro_povoado', '')
    area = l.get('area', '')
    secs = l.get('secoes', [])
    print(f"{num:<5} | {nome:<42} | {bairro:<26} | {area:<7} | {secs}")

print("\n" + "=" * 110)
print("VERIFICAÇÃO DE ROTAS DE VAN / CARGA E MOTOTÁXIS OFICIAIS:")
print("=" * 110)
for r in rotas.get('rotas_vans', []):
    print(f"\nROTA {r['rota']} ({r['area']}): {r['qtd_locais']} locais, {r['qtd_urnas']} urnas | {r['km_total']} km")
    for loc in r['locais']:
        print(f"   - {loc}")

print("\n" + "=" * 110)
print("MOTOTÁXIS OFICIAIS (31 MOTOS) POR LOCAL:")
print("=" * 110)
for m in log_cons.get('mototaxis', []):
    print(f"Moto {m['moto_num']:<2}: {m['local_atendido']:<45} | Dist: {m['distancia_total']:<25} | Tempo: {m['tempo_estimado']}")
