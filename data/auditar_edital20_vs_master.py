import os
import sys
import json
import re

sys.stdout.reconfigure(encoding='utf-8')

dir_path = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(dir_path, 'edital_20_texto_completo.txt'), 'r', encoding='utf-8') as f:
    lines = [l.strip() for l in f.readlines()]

# Vamos parsear as seções do Edital 20
# No PDF do Edital 20, as linhas foram extraídas palavra por palavra em colunas estreitas
# Mas veja: o código do local aparece como um número de 4 dígitos (1015, 1023, 1040, etc.)
# E as seções principais aparecem em sequência!

# Vamos carregar nosso banco atual:
with open(os.path.join(dir_path, 'ze041_inteligencia_consolidada.json'), 'r', encoding='utf-8') as f:
    master = json.load(f)

locais_banco = {l['num_local']: l for l in master['locais']}
secoes_banco = {s['secao']: s for s in master['secoes']}

print(f"Total de Locais no Banco: {len(locais_banco)}")
print(f"Total de Seções no Banco: {len(secoes_banco)}")

# Vamos encontrar todos os locais de 4 dígitos mencionados no Edital 20
codigos_locais_edital = set()
for l in lines:
    if l.isdigit() and len(l) == 4 and int(l) in locais_banco:
        codigos_locais_edital.add(int(l))

print(f"Total de Locais de Votação oficiais identificados no Edital 20: {len(codigos_locais_edital)}")

diff_locais = set(locais_banco.keys()) - codigos_locais_edital
if diff_locais:
    print(f"Locais no banco que não foram achados no texto: {diff_locais}")
else:
    print("SUCESSO: Todos os 32 locais de votação constam expressamente no Edital nº 20/2026!")

# Vamos verificar o endereço do IEMA (1015)
# e de outros locais no texto
print("\n--- Verificação Textual do IEMA (Local 1015) no Edital 20 ---")
for idx, l in enumerate(lines):
    if l == "1015":
        snippet = " | ".join(lines[idx:idx+15])
        print(f"Ocorrência 1015: {snippet[:150]}")
        break

# Vamos verificar Juçaral (1392)
print("\n--- Verificação Textual de Juçaral (Local 1392) no Edital 20 ---")
for idx, l in enumerate(lines):
    if l == "1392":
        snippet = " | ".join(lines[idx:idx+18])
        print(f"Ocorrência 1392: {snippet[:160]}")
        break

# Vamos verificar a soma de seções do Edital 20
# Procurar números de seções
secoes_encontradas = set()
for s_num in secoes_banco.keys():
    # verificar se a seção s_num aparece no texto
    # para evitar falsos positivos com números comuns, procuramos a ocorrência exata
    pattern = rf'\b{s_num}\b'
    if re.search(pattern, "\n".join(lines)):
        secoes_encontradas.add(s_num)

print(f"\nTotal de seções do banco confirmadas textualmente no Edital 20: {len(secoes_encontradas)} de {len(secoes_banco)}")
faltantes = set(secoes_banco.keys()) - secoes_encontradas
if faltantes:
    print(f"Seções não encontradas: {faltantes}")
else:
    print("SUCESSO: Todas as 94 seções principais confirmadas no Edital nº 20/2026!")

# Conferir as 11 seções agregadas
agregadas_banco = [s for s in master['secoes'] if s['secoes_agregadas'] != "Nenhuma"]
print(f"\nTotal de seções agregadoras no banco: {len(agregadas_banco)}")
for s in agregadas_banco:
    print(f"  Seção Principal {s['secao']} (Local {s['num_local']}: {s['nome_local']}) <- Agrega: {s['secoes_agregadas']} | Total Aptos: {s['aptos_2026']}")
