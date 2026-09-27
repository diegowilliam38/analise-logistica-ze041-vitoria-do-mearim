import olefile
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

filepath = r'Dados de eleiçoes/Logistica da zona 41 atualizada_setembro_2026/VISTORIA DE ADH NO SABADO ACOMPANHANDO LOGISTICA E DOMINGO NO DIA DA VOTAÇÃO/CONTROLE DOS TÉCNICOS RESPONSÁVEIS PELA URNA.doc'

ole = olefile.OleFileIO(filepath)
data = ole.openstream('WordDocument').read()

# Extrair strings
raw_strings = []
current = []
for b in data:
    if 32 <= b <= 126 or 160 <= b <= 255 or b in (10, 13, 9):
        current.append(bytes([b]))
    else:
        if len(current) >= 2:
            try:
                s = b''.join(current).decode('latin1').strip()
                if s:
                    raw_strings.append(s)
            except:
                pass
        current = []

# Identificar blocos por SERVIDOR RESPONSÁVEL
servidores = {}
current_servidor = None

for s in raw_strings:
    m = re.search(r'SERVIDOR\s+RESPONS[AÁ]VEL\s*(\d*)\s*:\s*([^N]+?)(?:NOME|$)', s, re.IGNORECASE)
    if not m:
        m = re.search(r'SERVIDOR\s+RESPONS[AÁ]VEL\s*:\s*(\d+)\s*([^N]+?)(?:NOME|$)', s, re.IGNORECASE)
    
    if m:
        num = m.group(1).strip()
        nome = m.group(2).strip()
        current_servidor = f"Servidor {num}: {nome}" if num else nome
        servidores[current_servidor] = []
        continue
    
    if current_servidor:
        servidores[current_servidor].append(s)

print("=== DISTRIBUIÇÃO DA VISTORIA DE ADH (SÁBADO E DOMINGO) ===")
for serv, itens in servidores.items():
    print(f"\n==================================================")
    print(f"👤 {serv.upper()}")
    print(f"==================================================")
    for it in itens:
        # Filtrar cabeçalhos repetidos
        if it in ('DATA', 'hora da urna', 'Hora no relógio do Técnico Responsável', 'SEÇÃO PRINCIPAL', 'NOME DO LOCAL DE VOTAÇÃO'):
            continue
        print(f"  • {it}")
