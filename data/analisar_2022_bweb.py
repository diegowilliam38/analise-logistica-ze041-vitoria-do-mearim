import csv
import sys
import json

sys.stdout.reconfigure(encoding='utf-8')

def process():
    print("==================================================")
    print("ANÁLISE COMPARATIVA OFICIAL BWEB TSE 2022 (ZE-041)")
    print("Vitória do Mearim / MA - 1º e 2º Turno")
    print("==================================================")

    # 1º Turno
    secoes_1t = {}
    with open('documentos da zona 41/bweb_1t_MA_051020221321.csv', 'r', encoding='latin1') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            zona = row.get('NR_ZONA', '').strip()
            if zona == '41':
                muni = row.get('NM_MUNICIPIO', '').strip().upper()
                if 'VITÓRIA' in muni or 'VITORIA' in muni:
                    secao = row.get('NR_SECAO')
                    if secao not in secoes_1t:
                        secoes_1t[secao] = {
                            'secao': secao,
                            'local': row.get('NR_LOCAL_VOTACAO'),
                            'muni': muni,
                            'zona': zona,
                            'aptos': int(row.get('QT_APTOS', 0)),
                            'comp': int(row.get('QT_COMPARECIMENTO', 0)),
                            'abst': int(row.get('QT_ABSTENCOES', 0)),
                            'abertura': row.get('DT_ABERTURA'),
                            'encerramento': row.get('DT_ENCERRAMENTO'),
                            'emissao_bu': row.get('DT_EMISSAO_BU'),
                            'bu_recebido': row.get('DT_BU_RECEBIDO')
                        }

    # 2º Turno
    secoes_2t = {}
    with open('documentos da zona 41/bweb_2t_MA_311020221535.csv', 'r', encoding='latin1') as f:
        reader = csv.DictReader(f, delimiter=';')
        for row in reader:
            zona = row.get('NR_ZONA', '').strip()
            if zona == '41':
                muni = row.get('NM_MUNICIPIO', '').strip().upper()
                if 'VITÓRIA' in muni or 'VITORIA' in muni:
                    secao = row.get('NR_SECAO')
                    if secao not in secoes_2t:
                        secoes_2t[secao] = {
                            'secao': secao,
                            'local': row.get('NR_LOCAL_VOTACAO'),
                            'muni': muni,
                            'zona': zona,
                            'aptos': int(row.get('QT_APTOS', 0)),
                            'comp': int(row.get('QT_COMPARECIMENTO', 0)),
                            'abst': int(row.get('QT_ABSTENCOES', 0)),
                            'abertura': row.get('DT_ABERTURA'),
                            'encerramento': row.get('DT_ENCERRAMENTO'),
                            'emissao_bu': row.get('DT_EMISSAO_BU'),
                            'bu_recebido': row.get('DT_BU_RECEBIDO')
                        }

    print(f"\n--- 1º TURNO 2022 (02/10/2022) ---")
    print(f"Total Seções: {len(secoes_1t)}")
    if secoes_1t:
        s_enc = sorted(secoes_1t.values(), key=lambda x: str(x['encerramento']))
        s_rec = sorted(secoes_1t.values(), key=lambda x: str(x['bu_recebido']))
        print(f"Primeiro Encerramento de Urna: Seção {s_enc[0]['secao']} às {s_enc[0]['encerramento']}")
        print(f"Último Encerramento de Urna: Seção {s_enc[-1]['secao']} às {s_enc[-1]['encerramento']}")
        print(f"Primeiro BU Recebido (Transmissão): Seção {s_rec[0]['secao']} às {s_rec[0]['bu_recebido']}")
        print(f"Último BU Recebido (Totalização): Seção {s_rec[-1]['secao']} às {s_rec[-1]['bu_recebido']}")

        pos_18 = [s for s in secoes_1t.values() if s['encerramento'] and s['encerramento'].split()[1] >= '18:00:00']
        print(f"Seções com encerramento pós-18h (filas): {len(pos_18)}")
        for s in pos_18:
            print(f"  - Seção {s['secao']} (Local {s['local']}): Encerrou às {s['encerramento']} | Transmitiu às {s['bu_recebido']}")

    print(f"\n--- 2º TURNO 2022 (30/10/2022) ---")
    print(f"Total Seções: {len(secoes_2t)}")
    if secoes_2t:
        s_enc2 = sorted(secoes_2t.values(), key=lambda x: str(x['encerramento']))
        s_rec2 = sorted(secoes_2t.values(), key=lambda x: str(x['bu_recebido']))
        print(f"Primeiro Encerramento de Urna: Seção {s_enc2[0]['secao']} às {s_enc2[0]['encerramento']}")
        print(f"Último Encerramento de Urna: Seção {s_enc2[-1]['secao']} às {s_enc2[-1]['encerramento']}")
        print(f"Primeiro BU Recebido (Transmissão): Seção {s_rec2[0]['secao']} às {s_rec2[0]['bu_recebido']}")
        print(f"Último BU Recebido (Totalização): Seção {s_rec2[-1]['secao']} às {s_rec2[-1]['bu_recebido']}")

        pos_18_2t = [s for s in secoes_2t.values() if s['encerramento'] and s['encerramento'].split()[1] >= '17:30:00']
        print(f"Seções com encerramento após 17:30: {len(pos_18_2t)}")

    # Salvar consolidado em JSON
    output_data = {
        'eleicao': 'Eleições Gerais 2022 - TSE',
        'zona': 41,
        'municipio': 'Vitória do Mearim',
        'primeiro_turno': {
            'data': '02/10/2022',
            'secoes_total': len(secoes_1t),
            'primeiro_encerramento': s_enc[0]['encerramento'] if secoes_1t else None,
            'ultimo_encerramento': s_enc[-1]['encerramento'] if secoes_1t else None,
            'primeira_transmissao': s_rec[0]['bu_recebido'] if secoes_1t else None,
            'ultima_transmissao': s_rec[-1]['bu_recebido'] if secoes_1t else None,
            'secoes': list(secoes_1t.values())
        },
        'segundo_turno': {
            'data': '30/10/2022',
            'secoes_total': len(secoes_2t),
            'primeiro_encerramento': s_enc2[0]['encerramento'] if secoes_2t else None,
            'ultimo_encerramento': s_enc2[-1]['encerramento'] if secoes_2t else None,
            'primeira_transmissao': s_rec2[0]['bu_recebido'] if secoes_2t else None,
            'ultima_transmissao': s_rec2[-1]['bu_recebido'] if secoes_2t else None,
            'secoes': list(secoes_2t.values())
        }
    }

    with open('data/dados_oficiais_tse_2022_ze041.json', 'w', encoding='utf-8') as f_out:
        json.dump(output_data, f_out, ensure_ascii=False, indent=2)

    print("\n[OK] Arquivo 'data/dados_oficiais_tse_2022_ze041.json' gerado com sucesso!")

if __name__ == '__main__':
    process()
