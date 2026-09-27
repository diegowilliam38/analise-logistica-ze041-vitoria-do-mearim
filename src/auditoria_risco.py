import os
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

project_root = r'C:\Users\Diego William\OneDrive\Área de Trabalho\AIOS-WORKSPACE\projects\analise-logistica-ze041-vitoria-do-mearim'
data_dir = os.path.join(project_root, 'data')

with open(os.path.join(data_dir, 'ze041_inteligencia_consolidada.json'), 'r', encoding='utf-8') as f:
    master = json.load(f)

secoes = master['secoes']
locais = master['locais']

# 1. Ranking de Gargalos de Horário (Votos pós-17h e Encerramento Tardio)
gargalos_horario = sorted([s for s in secoes if s['votos_pos_17h'] > 0 or s['tempo_medio_votacao_sec'] >= 40], 
                          key=lambda x: (x['votos_pos_17h'], x['tempo_medio_votacao_sec']), reverse=True)

# 2. Ranking de Lentidão na Habilitação e Biometria
gargalos_biometria = sorted(secoes, key=lambda x: (x['tempo_medio_habilitacao_sec'], -x['pct_biometria']), reverse=True)[:15]

# 3. Ranking de Falhas Operacionais de Mesários
falhas_mesarios = sorted([s for s in secoes if s['falhas_mesario']['total'] > 0], 
                         key=lambda x: x['falhas_mesario']['total'], reverse=True)

# 4. Ranking de Transmissão de BU (Logística Reversa Zonal)
atrasos_transmissao = sorted(secoes, key=lambda x: x['atraso_transmissao_min'], reverse=True)[:15]

# 5. Seções com Agregação e Carga Extrema (Aptos >= 300)
sobrecarga_agregacao = [s for s in secoes if s['tem_agregacao'] and s['aptos_2026'] >= 280]
sobrecarga_agregacao.sort(key=lambda x: x['aptos_2026'], reverse=True)

# 6. Plano de Alocação de Urnas de Contingência (MRV Reserva)
# Priorizar locais com histórico de falhas, muitas seções ou grande distância geográfica
locais_prioridade_urna = sorted(locais, key=lambda x: (x['tem_votos_pos17'], x['total_secoes'], x['atraso_transmissao_max']), reverse=True)

relatorio_diagnostico = {
    "gargalos_horario_filas": gargalos_horario,
    "gargalos_biometria": gargalos_biometria,
    "falhas_mesarios": falhas_mesarios,
    "atrasos_transmissao_bu": atrasos_transmissao,
    "secoes_sobrecarga_agregacao": sobrecarga_agregacao,
    "locais_prioridade_contingencia": locais_prioridade_urna[:12]
}

with open(os.path.join(data_dir, 'diagnostico_risco_operacional.json'), 'w', encoding='utf-8') as f:
    json.dump(relatorio_diagnostico, f, ensure_ascii=False, indent=2)

print("Diagnóstico de Risco Operacional gerado com sucesso!")
print(f"Seções com votos pós-17h ou votação lenta: {len(gargalos_horario)}")
print(f"Seções com falhas de mesários registradas: {len(falhas_mesarios)}")
print(f"Seções com sobrecarga de agregação: {len(sobrecarga_agregacao)}")
