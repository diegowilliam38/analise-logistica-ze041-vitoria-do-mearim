import csv
import sys

sys.stdout.reconfigure(encoding='utf-8')

def check_arari_2022():
    for turno_file, nome in [('documentos da zona 41/bweb_2t_MA_311020221535.csv', '2º TURNO 2022'), ('documentos da zona 41/bweb_1t_MA_051020221321.csv', '1º TURNO 2022')]:
        secoes = {}
        with open(turno_file, 'r', encoding='latin1') as f:
            reader = csv.DictReader(f, delimiter=';')
            for row in reader:
                muni = row.get('NM_MUNICIPIO', '').strip().upper()
                if muni == 'ARARI':
                    sec = row.get('NR_SECAO')
                    if sec not in secoes:
                        secoes[sec] = {
                            'secao': sec,
                            'enc': row.get('DT_ENCERRAMENTO'),
                            'tx': row.get('DT_BU_RECEBIDO')
                        }
        if secoes:
            s_enc = sorted(secoes.values(), key=lambda x: str(x['enc']))
            s_tx = sorted(secoes.values(), key=lambda x: str(x['tx']))
            print(f"=== ARARI {nome} ===")
            print(f"Total de seções: {len(secoes)}")
            print(f"Primeiro encerramento: Seção {s_enc[0]['secao']} às {s_enc[0]['enc']}")
            print(f"Último encerramento: Seção {s_enc[-1]['secao']} às {s_enc[-1]['enc']}")
            print(f"Primeira transmissão: Seção {s_tx[0]['secao']} às {s_tx[0]['tx']}")
            print(f"Última transmissão: Seção {s_tx[-1]['secao']} às {s_tx[-1]['tx']}")
            print()

if __name__ == '__main__':
    check_arari_2022()
