# Spec Técnica 004: Engenharia de Dados & Vínculo de Presença Oficial

## 1. Arquitetura de Dados
* **Origem dos Dados:**
  - `CONTROLE_PRESENCA_MESARIOS_DIA_DA_ELEICAO.odt` -> XML parsing de 471 linhas da tabela com 376 mesários (94 seções x 4 mesários).
  - `CONTROLE DE PRESENÇA ADM DE PREDIO.docx` -> 32 administradores de prédio com vínculo de 100% aos 32 locais.
  - `CONTROLE DE PRESENÇA DE COORDENADORES DE ACESSIBILIDADE.docx` -> 11 coordenadores de acessibilidade.
  - `CONTROLE DOS TÉCNICOS RESPONSÁVEIS PELA URNA.doc` -> 7 fiscais de ADH.
* **Artefatos Gerados:**
  - `data/mesarios_secoes_2026.json` (376 mesários)
  - `data/apoio_logistico_oficial_32_locais.json` (32 locais com vínculo auditado de adms e coordenadores)
  - `data/logistica_consolidada_2026.json` (consolidação geral das 7 rotas, 31 motos e 32 adms)
  - `web/js/data-payload.js` (578 KB, bundle offline com todos os dados)

## 2. Matriz de Vínculo dos 32 Locais e Administradores de Prédio
| Num Local | Local de Votação Oficial | Povoado / Bairro | Administrador Oficial Convocado | Coord. Acessibilidade |
|:---:|:---|:---|:---|:---|
| 1015 | IEMA Pleno de Vitória do Mearim | MA-014, Povoado Jaguary | ISISLEA MARINHO SILVA | IVALDO SILVA MACIEL |
| 1023 | Colégio Municipal Ana Bogéa | Centro | JUCIENE PEREIRA BRUCE | MYRLLA RYANNE SILVA MACIEL |
| 1040 | CEMA Carlos Raimundo Figueiredo | Bairro Novo | LUCINEIDE GOMES CORRÊA | JEANE BATALHA GOMES |
| 1058 | Colégio Municipal Antônia Farias | Tapera | HIRES CRISTINA MACIEL REIS | GLEYCE MARCELLE MEDEIROS PERES |
| 1066 | J.I. Mons. Artur Gonçalves | Centro | EMILLY PEREIRA BRUCE | IANCA MICHELLY MARINHO MACIEL |
| 1074 | C.E. Cônego Eliud Nunes Arouche | Centro | DEIVIT BEZERRA MARINHO | BASYNGA FRANCO DA SILVA |
| 1082 | E.M. Maurícia Fernandes Jardim | Povoado Escondido | SAMIA ANDREIA MACIEL PEREIRA | — |
| 1090 | Colégio Municipal Hemetério Fernandes | Povoado Mato Grosso | ELBIANE DA CONCEIÇÃO FERREIRA | — |
| 1104 | Escola Municipal de Tirirical | Povoado Tirirical | JAQUELINE NUNES FONSECA | — |
| 1139 | Escola Municipal Deodato Santos | Povoado São Lourenço | VANAILDE LOPES PACHECO | — |
| 1147 | Escola Municipal Franklin Cantanhêde | Povoado São Lourenço | GEISIELMA FREITAS LOPES | — |
| 1155 | Escola Municipal Itelvino de Matos | Povoado Coque | DENILA DE MATOS RODRIGUES | ANA NAYLA MACIEL DA SILVA |
| 1163 | Escola Municipal Vila Falcão | Povoado Vila Falcão | CARLOS ALESSANDRO DE ALMEIDA SOARES | — |
| 1171 | Colégio Municipal Vila Nova | Povoado Vila Nova | ANDRESSA SANTOS TORRES | — |
| 1198 | Escola Municipal Nasser Assad | Povoado Coque | ANA ROSA RODRIGUES FALCAO | ANTONIA MARCIA SANTOS RODRIGUES |
| 1201 | Creche Comunitária de Coque | Povoado Coque | RAIZA FERREIRA VALE | — |
| 1210 | Escola Municipal Raimundo Bogéa | Povoado Coque | MORRAMES OLIVEIRA DA SILVA | — |
| 1228 | E.M. Francisco Xavier Correia | Povoado Jaguary | OCIANE DE BRITO ALVES | — |
| 1236 | Colégio Municipal Godofredo Maciel | Povoado São Felix | ARIADNE RIBEIRO CAMPELO | — |
| 1252 | Escola Municipal Izidoro de Jesus Lopes | Povoado Livramento | ADEMILDA COSTA DOS SANTOS | — |
| 1279 | Colégio Municipal José Carlos Mota Silva | Povoado Sumaúma do Japão | TEIZIANE DE JESUS ROCHA REIS | — |
| 1317 | Colégio Municipal José Ribamar Silva | Povoado Santa Rosa | ANGELA MARIA VALE ABREU | — |
| 1333 | Escola Municipal Paulo Maciel Neto | Povoado São Benedito | ELIENE DE JESUS BRITO | — |
| 1350 | Escola Municipal Abidão Rufino da Silva | Povoado Boca do Campo | DIEGO VIEIRA NEVES | — |
| 1392 | Escola Municipal de Juçaral | Povoado Juçaral das Margaridas | NERINILDO COELHO CARDOSO (Difícil Acesso) | (Suporte Adm / SF) |
| 1414 | Escola Municipal de Ipixuna | Povoado Ipixuna | ELIVANE CORREA COELHO | — |
| 1422 | E.M. Mamédio da Silva Sarmento | Povoado Jacaray | JOELMA CUTRIM COSTA | — |
| 1457 | CM Euzébio do Nascimento dos Reis | Povoado Juçaralzinho | RIAN SILVA MESQUITA | — |
| 1465 | U.E. Dr. Ribamar de Matos | Centro | SILVIANE VIEIRA SILVA COSTA | — |
| 1473 | Unidade Escolar Neuza da Cunha Costa | Bairro Novo | SELMA DE JESUS AMORIM VELEZ | KID DAVID PEREIRA CARDOSO |
| 1481 | U.E. Maria Graciana Pinto Costa | Vila Regina | MAURILIO LISBOA MOREIRA | CAMILA LEITE COSTA |
| 1490 | Escola Municipal Maria Celeste Barros | Bairro Novo | GIULIANNO PEREIRA DE SOUSA | MARIA BETANIA BARBOSA BATALHA |
