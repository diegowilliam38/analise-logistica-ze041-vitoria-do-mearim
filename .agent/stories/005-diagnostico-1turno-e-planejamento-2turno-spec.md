# Spec Técnica 005: Integração dos Dados Oficiais do 1º Turno & Cockpit do 2º Turno

## 1. Dados e Estruturas de Entrada
- **Arquivos Fonte:**
  - `documentos da zona 41/LOCAIS_1_TURNO_2026_VITORIA.pdf` (10 páginas do sistema Acompanha-E com dados de cada seção).
  - `documentos da zona 41/DADOS_1_TURNO_2026_VITORIA_MEARIM.pdf` (36 páginas com consolidação estadual do Maranhão).
- **Campos Mapeados por Seção:**
  - `local`: Nome do estabelecimento de ensino.
  - `aptos`: Quantidade de eleitores aptos oficiais (total: 24.458).
  - `comp`: Quantidade de eleitores votantes (total: 19.338 / 79,06%).
  - `abst`: Quantidade de abstenções (total: 5.345 / 21,85%).
  - `inicio`: Horário de emissão da zerésima e abertura da urna (08:00:01).
  - `encerramento`: Horário de encerramento da urna (17:00:00 a 19:52:31).
  - `transmitido`: Horário de leitura da mídia e envio no SISTOT centralizado no Cartório Eleitoral (sem pontos JE Connect externos).
  - `recebido`: Horário de processamento no SISTOT no Cartório.
  - `totalizado`: Horário de computação oficial pelo TSE.

## 2. Pipeline de Engenharia de Dados
- **Script de Processamento:** `data/consolidar_1turno_2026.py`
  - Gera: `data/resultado_consolidado_1turno_2026.json`
- **Script de Empacotamento Web:** `src/generate_web_bundle.py`
  - Injeta `window.ZE041_DATA.resultado_1turno` em `web/js/data-payload.js`.

## 3. Componentes da Interface Web
- **Arquivo `web/index.html`:**
  - Botão de navegação: `<button class="tab-btn" data-tab="tab-segundo-turno">` com badge dourada `DADOS REAIS`.
  - Seção: `<section id="tab-segundo-turno" class="tab-content">`
    - Bloco de 4 KPIs:
      - `#kpi1TComparecimento`: 19.338 (79,06%)
      - `#kpi1TPrimeiroEncerramento`: 17:00:00 (1º BU 17:42:45)
      - `#kpi1TUltimoEncerramento`: 19:52:31 (Mesárias se enrolaram no fechamento da urna - Seção 155)
      - `#kpi1TTotalizacao`: 20:55:14 (100% Apurado no Cartório Eleitoral)
    - Painel tático de 5 Ações Focais para o 2º Turno (`#gridAcoes2Turno`).
    - Tabela de Top Gargalos de Fila Pós-17h (`#tableGargalos1Turno`).
    - Painel de Casos de Sucesso (`#containerCasosSucesso`).
    - Tabela de Benchmarking Estadual (`#tableBenchmarking`).
    - Tabela Geral das 94 seções com campo de busca `#inputSearch1Turno` e contador `#badgeCount1Turno`.
- **Arquivo `web/js/app.js`:**
  - Função `renderSegundoTurno(res1T)` chamada no `DOMContentLoaded`.
  - Event listener de input para busca dinâmica e instantânea em memória.

## 4. Benchmarking Regional Oficial
| Município | ZE | Eleitores Aptos | Horário Totalização | Desempenho Relativo |
|---|---|---|---|---|
| Igarapé do Meio | 41ª ZE | 12.450 | 20:18:30 | Concluiu antes (polo menor) |
| Arari | 40ª ZE | 23.800 | 20:42:15 | Porte similar a Vitória |
| **Vitória do Mearim** | **41ª ZE** | **24.458** | **20:55:14** | **100% Apurado no Cartório antes das 21h** |
| São Bento | 61ª ZE | 34.100 | 21:11:30 | +16 min após Vitória |
| Pinheiro | 42ª ZE | 58.200 | 21:25:40 | +30 min após Vitória |
| Santa Helena | 83ª ZE | 28.400 | 21:30:15 | +35 min após Vitória |
| Matinha | 61ª ZE | 19.800 | 21:48:22 | +53 min após Vitória |
| Cantanhede | 44ª ZE | 17.900 | 21:55:10 | +1h após Vitória |
| Viana | 46ª ZE | 41.200 | 01:40:20 (05/10) | Madrugada seguinte (+4h45) |
| Cajari | 46ª ZE | 14.600 | 01:56:45 (05/10) | Madrugada seguinte (+5h01) |

## 5. Diretrizes Táticas Oficiais para o 2º Turno (25/10/2026)
1. **Redução Estrutural do Voto (Apenas 2 Cargos vs 6 Cargos):** No 2º Turno, o eleitor vota apenas para Presidente e/ou Governador (2 dígitos cada). Tempo médio de cabine cai de ~100s para ~18s (-78%). Elimina filas no final da tarde.
2. **Intervenção Seção 155 (EM Raimundo Bogéa - Coque):** O Administrador de Prédio e o Técnico de Apoio acompanharão o encerramento da urna diretamente às 17h para orientar o procedimento correto de emissão de BU, evitando o travamento procedural do 1º Turno (quando a Seção 184 fechou 17h15 e a 155 atrasou).
3. **Intervenção Seção 119 (Bairro Novo) & Polo CEMA:** Triagem de documentos e fila externa organizada por Administradores de Prédio e Coordenadores de Acessibilidade.
4. **Celeridade no Retorno dos Mototáxis:** Despacho expresso das mídias físicas de Ipixuna e Sumaúma diretamente para o Cartório Eleitoral.
5. **Meta ZE041:** Conclusão da última urna até 17h30, última mídia no Cartório às 18h45 e Totalização Oficial 100% no TSE às **19h15**.
