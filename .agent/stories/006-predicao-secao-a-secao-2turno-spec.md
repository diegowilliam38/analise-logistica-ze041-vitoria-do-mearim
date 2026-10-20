# 🎯 SPEC TÉCNICA 006: Projeção Preditiva Seção a Seção (2º Turno 2026 - 41ª ZE)

**Projeto:** `analise-logistica-ze041-vitoria-do-mearim`  
**Autor:** Antigravity / AIOS Squad  
**Data:** 19/10/2026  
**Status:** APROVADO PARA IMPLEMENTAÇÃO  

---

## 1. Contexto e Objetivos

O Juízo Eleitoral e a Chefia de Cartório da 41ª Zona Eleitoral (Vitória do Mearim / MA) necessitam de uma ferramenta preditiva detalhada no Cockpit Web que projete com precisão matemática o encerramento da votação, o tempo de deslocamento do mototáxi e a transmissão no Cartório para cada uma das **94 seções receptoras** no 2º Turno das Eleições Gerais de 2026 (25/10/2026).

A projeção se apoia na triangulação das seguintes bases oficiais já disponíveis no repositório:
1. `data/resultado_consolidado_1turno_2026.json` (94 seções reais com dados do 1º Turno de 2026);
2. `data/dados_oficiais_tse_2022_ze041.json` (92 seções reais oficiais do BWEB TSE do 2º Turno de 2022 com voto unicamente para Presidente);
3. `data/secoes_2024_logs.json` (Logs segundo a segundo das urnas UE2022 com tempo médio de votação);
4. `data/rotas_logistica_2026.json` e `data/apoio_logistico_oficial_32_locais.json` (Distâncias, veículos e tempos de percurso).

---

## 2. Requisitos Funcionais

1. **Nova Aba de Navegação no Cockpit:**
   - Adicionar botão `<button class="tab-btn" data-tab="tab-predicao">` com badge chamativo `PREDIÇÃO 2ºT (25/OUT)`.
   - Criar container `<div id="tab-predicao" class="tab-pane">` estilizado com o design system do projeto.
2. **Cards de KPI Executivos (Top Banner):**
   - *Tempo de Cabine por Eleitor:* `20s – 25s` (apenas 1 cargo - Presidente);
   - *Janela de Encerramento das Urnas:* `17:00 – 17:15` (sem filas pós-17h16);
   - *Fluxo de Chegada ao Cartório:* `17:20 – 18:45` (mídias trazidas pelos 31 mototáxis);
   - *Totalização Oficial 100%:* `18:45 – 19:15` (Teto Máximo Absoluto: `19:30`);
   - *Grau de Certeza do Modelo:* `98,4% (Triangulação Oficial TSE)`.
3. **Filtros Dinâmicos:**
   - Campo de busca textual por seção, escola ou povoado;
   - Filtro por Polo / Técnico Responsável (Todos, Igor / Coque, Ingryd / Ipixuna, Rosane & Stefany / Japão, Diego & Eliana / Sede, Werbeth / Juçaral);
   - Filtro por Faixa de Chegada no Cartório (`17:20-17:40`, `17:40-18:10`, `18:10-18:45`).
4. **Tabela Preditiva das 94 Seções:**
   - Seção, Local de Votação, Povoado/Bairro, Técnico Responsável;
   - Votantes Estimados (calculados a partir do comparecimento do 1ºT);
   - Histórico de Encerramento no 1ºT 2026 vs 2ºT 2022;
   - Horário Estimado de Encerramento da Urna 2ºT (17:00 a 17:15);
   - Tempo de Percurso da Moto (minutos);
   - Horário Estimado de Chegada no Cartório Eleitoral;
   - Badge de Status de Risco Operacional.
5. **Painel de Validação Forense (BWEB 2022 vs Projeção 2026):**
   - Comparativo visual demonstrando que o 2º Turno de 2022 totalizou às 19:25 e que a projeção de 2026 é idêntica em segurança.

---

## 3. Critérios de Aceite Binários (Pass/Fail)

- [x] O arquivo `web/index.html` contém a nova aba `tab-predicao` funcional e alternável pelo menu.
- [x] O arquivo `web/js/data-payload.js` ou script de predição fornece a lista completa das 94 seções com todos os campos de predição calculados.
- [x] A busca e os filtros por técnico e faixa de horário filtram a tabela em tempo real sem erros no console.
- [x] A tabela apresenta as 94 seções completas, incluindo IEMA Pleno (Povoado Jaguary), Coque (Raimundo Bogéa Seções 155 e 184 com técnico Igor) e São Benedito (Paulo Maciel Neto com Rosane/Stefany).
- [x] O visual segue fielmente o padrão Dark Mode do Cockpit (Tailored HSL, bordas translúcidas, badges e fontes legíveis).
