import json
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Escala Oficial dos 7 Responsáveis de ADH - Versão Final com Nomes Reais
escala_adh_oficial = {
    "ano_pleito": 2026,
    "zona": 41,
    "municipio": "VITÓRIA DO MEARIM / MA",
    "finalidade": "Vistoria de ADH (Data e Hora no Sábado) e Auditoria Operacional (Presença, Zerésima às 07h e Encerramento às 17h no Domingo)",
    "equipe_responsavel": [
        {
            "id": 1,
            "cargo": "Servidora Requisitada",
            "nome": "Eliana Silva",
            "tipo": "Servidora do Cartório / Requisitada",
            "polo": "Polo Sede 1 / IEMA / Eliud / Neuza / Celeste / CEMA / Jacaray / Jaguary",
            "locais": [
                {
                    "num_local": 1015,
                    "nome": "IEMA Pleno de Vitória do Mearim (MA-014, Povoado Jaguary)",
                    "secoes": ["01ª", "02ª", "03ª", "19ª", "84ª", "188ª"]
                },
                {
                    "num_local": 1074,
                    "nome": "Centro Educacional Cônego Eliud N. Arouche (Sede)",
                    "secoes": ["16ª", "17ª", "18ª", "93ª", "107ª", "159ª"]
                },
                {
                    "num_local": 1473,
                    "nome": "Unidade Escolar Neuza da Cunha Costa (Sede)",
                    "secoes": ["20ª", "21ª", "119ª", "185ª"]
                },
                {
                    "num_local": 1490,
                    "nome": "Escola Municipal Maria Celeste Barros",
                    "secoes": ["08ª", "121ª", "141ª", "146ª"]
                },
                {
                    "num_local": 1040,
                    "nome": "CEMA Carlos Raimundo Figueiredo",
                    "secoes": ["09ª", "10ª", "11ª", "80ª", "82ª", "148ª"]
                },
                {
                    "num_local": 1422,
                    "nome": "Escola Municipal Mamédio da Silva Sarmento (Jacaray)",
                    "secoes": ["104ª", "187ª"]
                },
                {
                    "num_local": 1104,
                    "nome": "Escola Municipal Francisco Xavier Correia (Jaguary)",
                    "secoes": ["22ª", "187ª"]
                }
            ],
            "total_urnas": 30
        },
        {
            "id": 2,
            "cargo": "Chefe de Cartório",
            "nome": "Diego William Pereira dos Santos",
            "tipo": "Chefe de Cartório Eleitoral — 41ª ZE",
            "polo": "Polo Sede 2 / Colégio Ana Bogéa / Mons. Artur / Antônia Farias / Dr. Ribamar",
            "locais": [
                {
                    "num_local": 1023,
                    "nome": "Colégio Municipal Ana Bogéa Gonçalves (Sede)",
                    "secoes": ["04ª", "05ª", "06ª", "07ª", "90ª", "94ª", "157ª"]
                },
                {
                    "num_local": 1066,
                    "nome": "Jardim de Infância Mons. Arthur Gonçalves (Sede)",
                    "secoes": ["14ª", "15ª", "103ª", "186ª"]
                },
                {
                    "num_local": 1058,
                    "nome": "Escola Municipal Antônia Farias (Sede)",
                    "secoes": ["12ª", "13ª", "83ª", "137ª", "183ª"]
                },
                {
                    "num_local": 1481,
                    "nome": "Unidade Escolar Dr. Ribamar de Matos (Sede)",
                    "secoes": ["92ª", "122ª", "145ª", "166ª", "173ª"]
                }
            ],
            "total_urnas": 21
        },
        {
            "id": 3,
            "cargo": "Técnica de Urna",
            "nome": "Stefany Pereira Bruce",
            "tipo": "Apoio Técnico Volante / Urnas de Contingência",
            "polo": "Polo Vicinal Norte Profundo (Sumaúma / Santa Rosa / São Benedito)",
            "locais": [
                {
                    "num_local": 1325,
                    "nome": "Colégio Municipal José Carlos Mota Silva (Sumaúma)",
                    "secoes": ["66ª", "81ª", "176ª"]
                },
                {
                    "num_local": 1309,
                    "nome": "Colégio Municipal José Ribamar Silva (Santa Rosa)",
                    "secoes": ["64ª", "65ª"]
                },
                {
                    "num_local": 1341,
                    "nome": "Escola Municipal Paulo Maciel Neto (São Benedito)",
                    "secoes": ["73ª", "89ª", "147ª"]
                }
            ],
            "total_urnas": 8
        },
        {
            "id": 4,
            "cargo": "Servidora Requisitada",
            "nome": "Rosane Praseres Nunes Dutra",
            "tipo": "Servidora do Cartório / Requisitada",
            "polo": "Polo Graciana / Mato Grosso / Tirirical / São Lourenço / São Félix / Livramento",
            "locais": [
                {
                    "num_local": 1627,
                    "nome": "Unidade Escolar Maria Graciana Pinto Costa (Sede)",
                    "secoes": ["105ª (150/170)", "161ª", "165ª", "182ª"]
                },
                {
                    "num_local": 1503,
                    "nome": "Colégio Municipal Hemetério Fernandes (Mato Grosso)",
                    "secoes": ["144ª", "178ª"]
                },
                {
                    "num_local": 1635,
                    "nome": "Colégio Municipal de Tirirical",
                    "secoes": ["162ª"]
                },
                {
                    "num_local": 1112,
                    "nome": "Escola Municipal Deodato Santos (São Lourenço)",
                    "secoes": ["23ª (24)"]
                },
                {
                    "num_local": 1589,
                    "nome": "Escola Municipal Franklin Cantanhêde (São Lourenço)",
                    "secoes": ["153ª (113/189)", "166ª"]
                },
                {
                    "num_local": 1287,
                    "nome": "Escola Municipal Godofredo Maciel (São Félix)",
                    "secoes": ["62ª", "68ª", "179ª"]
                },
                {
                    "num_local": 1317,
                    "nome": "Colégio Municipal Izidoro de Jesus Lopes (Livramento)",
                    "secoes": ["75ª (114/172)"]
                }
            ],
            "total_urnas": 14
        },
        {
            "id": 5,
            "cargo": "Técnico de Urna",
            "nome": "Igor Fonseca Moreira",
            "tipo": "Apoio Técnico Volante / Urnas de Contingência",
            "polo": "Polo Eixo BR-222 / Coque (Nasser Assad / Itelvino / Falcão / Creche)",
            "locais": [
                {
                    "num_local": 1120,
                    "nome": "Colégio Municipal Nasser Assad (Coque)",
                    "secoes": ["25ª", "26ª", "27ª", "28ª", "78ª", "85ª", "95ª"]
                },
                {
                    "num_local": 1368,
                    "nome": "Escola Municipal Itelvino de Matos (Coque)",
                    "secoes": ["29ª", "30ª", "108ª", "143ª", "177ª"]
                },
                {
                    "num_local": 1562,
                    "nome": "Escola Municipal Vila Falcão (Coque)",
                    "secoes": ["152ª", "164ª"]
                },
                {
                    "num_local": 1554,
                    "nome": "Creche Comunitária de Coque",
                    "secoes": ["173ª (154)"]
                }
            ],
            "total_urnas": 15
        },
        {
            "id": 6,
            "cargo": "Técnica de Urna",
            "nome": "Ingridy Fonseca Moreira",
            "tipo": "Apoio Técnico Volante / Urnas de Contingência",
            "polo": "Polo Sul / Bogéa / Boca do Campo / Juçaralzinho / Ipixuna / Escondido / Vila Nova",
            "locais": [
                {
                    "num_local": 1570,
                    "nome": "Colégio Municipal Raimundo Bogéa (Coque)",
                    "secoes": ["155ª (151)", "184ª"]
                },
                {
                    "num_local": 1511,
                    "nome": "Colégio Municipal Abidão Rufino da Silva (Boca do Campo)",
                    "secoes": ["142ª"]
                },
                {
                    "num_local": 1457,
                    "nome": "Colégio Municipal de Juçaralzinho",
                    "secoes": ["117ª"]
                },
                {
                    "num_local": 1619,
                    "nome": "Colégio Municipal de Ipixuna",
                    "secoes": ["160ª (175/180)"]
                },
                {
                    "num_local": 1465,
                    "nome": "Colégio Municipal Vila Nova",
                    "secoes": ["120ª (169)"]
                },
                {
                    "num_local": 1660,
                    "nome": "Escola Municipal Maurícia Fernandes Jardim (Escondido)",
                    "secoes": ["101ª (171/181)"]
                }
            ],
            "total_urnas": 7
        },
        {
            "id": 7,
            "cargo": "Responsável Suprimento de Fundos",
            "nome": "Werbeth Silva Dutra",
            "tipo": "Prestador de Serviço Especial / Transporte Dedicado",
            "polo": "Polo Difícil Acesso (Juçaral)",
            "locais": [
                {
                    "num_local": 1392,
                    "nome": "Escola Municipal de Juçaral",
                    "secoes": ["106ª (135)"]
                }
            ],
            "total_urnas": 1
        }
    ]
}

with open(r'projects/analise-logistica-ze041-vitoria-do-mearim/data/escala_adh_tecnicos_2026.json', 'w', encoding='utf-8') as f:
    json.dump(escala_adh_oficial, f, ensure_ascii=False, indent=2)

print("Escala Oficial de ADH atualizada com nomes oficiais com sucesso!")
