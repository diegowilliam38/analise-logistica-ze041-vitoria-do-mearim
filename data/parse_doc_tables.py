import olefile
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

filepath = r'Dados de eleiçoes/Logistica da zona 41 atualizada_setembro_2026/VISTORIA DE ADH NO SABADO ACOMPANHANDO LOGISTICA E DOMINGO NO DIA DA VOTAÇÃO/CONTROLE DOS TÉCNICOS RESPONSÁVEIS PELA URNA.doc'

ole = olefile.OleFileIO(filepath)
data = ole.openstream('WordDocument').read()

# O texto no stream WordDocument começa por volta de um offset de texto
# Vamos procurar blocos de texto contendo "SERVIDOR RESPONSÁVEL"
pos = 0
found = []
for m in re.finditer(b'SERVIDOR', data):
    start = max(0, m.start() - 10)
    end = min(len(data), m.start() + 4000)
    chunk = data[start:end]
    # decodificar caracteres legíveis
    chars = []
    for b in chunk:
        if 32 <= b <= 126 or 160 <= b <= 255:
            chars.append(chr(b))
        elif b in (10, 13, 7): # 7 é célula de tabela do word
            chars.append('\n')
    text = ''.join(chars)
    found.append(text)

print(f"Encontradas {len(found)} ocorrências de SERVIDOR\n")
for i, f in enumerate(found):
    print(f"--- OCORRÊNCIA {i+1} ---")
    lines = [l.strip() for l in f.split('\n') if len(l.strip()) > 1]
    # Pegar até o próximo servidor ou 30 linhas
    for line in lines[:40]:
        print(line)
