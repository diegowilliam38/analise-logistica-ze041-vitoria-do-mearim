// ==========================================================================
// APLICAÇÃO COCKPIT ZE-041 - LÓGICA E INTERATIVIDADE (V2 - ROTAS & LOGÍSTICA)
// ==========================================================================

document.addEventListener('DOMContentLoaded', () => {
  const data = window.ZE041_DATA;
  if (!data) {
    console.error("Dados da 41ª ZE não encontrados em window.ZE041_DATA");
    return;
  }

  const master = data.master;
  const diag = data.diagnostico;
  const logistica = data.logistica;

  // 1. Inicializar Contadores do Topbar
  initCountdown();

  // 2. Inicializar KPIs
  renderKPIs(master.estatisticas_gerais);

  // 3. Inicializar Navegação por Abas
  setupTabs();

  // 4. Renderizar Tabela das 94 Seções
  let currentFilter = 'TODAS';
  let searchTerm = '';
  renderSecoesTable(master.secoes, currentFilter, searchTerm);

  // 5. Renderizar Tabela dos 32 Locais
  renderLocaisTable(master.locais);

  // 6. Renderizar Rankings de Diagnóstico Forense
  renderGargalosTable(diag.gargalos_horario_filas);
  renderFalhasTable(diag.falhas_mesarios);
  renderTransmissaoTable(diag.atrasos_transmissao_bu);

  // 7. Renderizar Rotas e Logística de Campo Oficial (7 Rotas Carga, 31 Motos, 32 Adms, 11 Coords, ADH)
  if (data.logistica_consolidada) {
    renderVansTable(data.logistica_consolidada.rotas_veiculos_carga);
    renderMotosTable(data.logistica_consolidada.rotas_mototaxis);
    renderApoioTable(data.logistica_consolidada.administradores_predio, data.logistica_consolidada.coordenadores_acessibilidade, master.locais, data.logistica_consolidada.apoio_logistico_32_locais);
  } else if (logistica) {
    renderVansTable(logistica.rotas_vans);
    renderMotosTable(logistica.rotas_mototaxis);
    renderApoioTableLegacy(logistica.apoio_logistico_locais);
  }
  if (data.escala_adh) {
    renderADHTable(data.escala_adh);
  }

  // 7.1 Inicializar Controle de Presença no Dia da Eleição
  initControlePresenca(data);

  // 7.2 Renderizar Dados Oficiais do 1º Turno & Estratégia do 2º Turno (2026)
  if (data.resultado_1turno) {
    renderSegundoTurno(data.resultado_1turno);
  }

  // 7.3 Inicializar Projeção Preditiva Oficial do 2º Turno (94 Seções)
  initPredicao2Turno();

  // 8. Renderizar Gráficos
  if (window.initDashboardCharts) {
    window.initDashboardCharts(data);
  }

  // 9. Eventos de Busca e Filtro
  const searchInput = document.getElementById('searchSecaoInput');
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      searchTerm = e.target.value.toLowerCase().trim();
      renderSecoesTable(master.secoes, currentFilter, searchTerm);
    });
  }

  const filterBtns = document.querySelectorAll('.filter-btn[data-filter]');
  filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      filterBtns.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      currentFilter = btn.getAttribute('data-filter');
      renderSecoesTable(master.secoes, currentFilter, searchTerm);
    });
  });

  // 10. Configurar Modal de Seção
  setupModal();
});

// -------------------------------------------------------------
// CONTADOR REGRESSIVO 04/10/2026
// -------------------------------------------------------------
function initCountdown() {
  const targetDate = new Date('2026-10-04T08:00:00-03:00').getTime();
  const el = document.getElementById('countdownDays');
  if (!el) return;

  function update() {
    const now = new Date().getTime();
    const diff = targetDate - now;
    if (diff <= 0) {
      el.innerText = "HOJE É DIA DE ELEIÇÃO!";
      return;
    }
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));
    const hours = Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
    el.innerText = `${days}d ${hours}h para o 1º Turno`;
  }
  update();
  setInterval(update, 60000);
}

// -------------------------------------------------------------
// RENDERIZAÇÃO DE KPIS
// -------------------------------------------------------------
function renderKPIs(eg) {
  setElText('kpiTotalAptos', eg.total_aptos_2026.toLocaleString('pt-BR'));
  setElText('kpiTotalLocais', eg.total_locais);
  setElText('kpiMetaLocais', `${eg.locais_urbanos} Urb / ${eg.locais_rurais} Rurais`);
  setElText('kpiTotalSecoes', eg.total_secoes_principais);
  setElText('kpiMetaSecoes', `${eg.secoes_urbanas} Urb / ${eg.secoes_rurais} Rurais (${eg.secoes_com_agregacao} agregadoras)`);
  setElText('kpiSecoesRiscoAlto', eg.secoes_risco_alto);
  setElText('kpiVotosPos17', `${eg.secoes_votos_pos17_2024} seções`);
  setElText('kpiTempoMedioVotacao', `${eg.tempo_medio_votacao_zonal_sec}s`);
  setElText('kpiBiometriaMedia', `${eg.media_pct_biometria_zonal}%`);
}

function setElText(id, text) {
  const el = document.getElementById(id);
  if (el) el.innerText = text;
}

// -------------------------------------------------------------
// NAVEGAÇÃO DE ABAS
// -------------------------------------------------------------
function setupTabs() {
  const tabBtns = document.querySelectorAll('.tab-btn');
  const tabContents = document.querySelectorAll('.tab-content');

  tabBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const target = btn.getAttribute('data-tab');
      tabBtns.forEach(b => b.classList.remove('active'));
      tabContents.forEach(c => c.classList.remove('active'));

      btn.classList.add('active');
      const targetContent = document.getElementById(target);
      if (targetContent) targetContent.classList.add('active');

      if (target === 'tab-mapa' && window.initGeoMap) {
        const data = window.ZE041_DATA;
        if (!window._leafMap) {
          window.initGeoMap(data);
        }
        setTimeout(() => {
          if (window._leafMap) {
            window._leafMap.invalidateSize();
          }
        }, 150);
      }
    });
  });
}

// -------------------------------------------------------------
// TABELA PRINCIPAL DAS 94 SEÇÕES
// -------------------------------------------------------------
function renderSecoesTable(secoes, filter, search) {
  const tbody = document.getElementById('secoesTableBody');
  if (!tbody) return;

  let filtered = secoes.filter(s => {
    if (filter === 'URBANA' && s.area !== 'URBANA') return false;
    if (filter === 'RURAL' && s.area !== 'RURAL') return false;
    if (filter === 'RISCO_ALTO' && s.nivel_risco !== 'ALTO') return false;
    if (filter === 'VOTOS_17' && s.votos_pos_17h === 0) return false;
    if (filter === 'AGREGADA' && !s.tem_agregacao) return false;
    if (filter === 'ACESSIVEL' && !s.has_ac) return false;

    if (search) {
      const secStr = s.secao.toString();
      const localStr = s.nome_local.toLowerCase();
      const bairroStr = s.bairro_povoado.toLowerCase();
      return secStr.includes(search) || localStr.includes(search) || bairroStr.includes(search);
    }
    return true;
  });

  const countBadge = document.getElementById('secoesCountBadge');
  if (countBadge) countBadge.innerText = `${filtered.length} de ${secoes.length}`;

  tbody.innerHTML = filtered.map(s => {
    const areaBadge = s.area === 'URBANA' 
      ? '<span class="badge badge-info">Urbana</span>' 
      : '<span class="badge badge-neutral">Rural</span>';

    const riscoBadge = `<span class="badge ${s.badge_class}">${s.nivel_risco}</span>`;
    
    const agregBadge = s.tem_agregacao 
      ? `<span class="badge badge-warning" title="Agregada: ${s.secoes_agregadas}">+ Sec ${s.secoes_agregadas}</span>`
      : '<span class="badge badge-neutral">Individual</span>';

    const votos17Badge = s.votos_pos_17h > 0
      ? `<span class="badge badge-danger" title="Filas graves no fechamento">${s.votos_pos_17h} votos pós-17h</span>`
      : `<span style="color: var(--text-dim); font-size: 0.8rem;">0</span>`;

    const acessPill = s.has_ac 
      ? '<span class="badge badge-success" title="Seção com Acessibilidade PCD">AC</span>' 
      : '<span style="color: var(--text-dim);">-</span>';

    return `
      <tr onclick="openSecaoModal(${s.secao})">
        <td style="font-family: var(--font-mono); font-weight: 700; color: #fff;">
          <strong>${s.secao}</strong>
        </td>
        <td>
          <div style="font-weight: 600; color: #fff;">${s.nome_local}</div>
          <div style="font-size: 0.75rem; color: var(--text-muted);">${s.bairro_povoado} &bull; ${s.endereco}</div>
        </td>
        <td>${areaBadge}</td>
        <td>${agregBadge}</td>
        <td style="font-family: var(--font-mono); font-weight: 600;">${s.aptos_2026}</td>
        <td>${acessPill}</td>
        <td style="font-family: var(--font-mono);">${s.tempo_medio_votacao_sec}s</td>
        <td>${votos17Badge}</td>
        <td style="font-family: var(--font-mono); font-size: 0.8rem;">${s.horario_bu_recebido ? s.horario_bu_recebido.split(' ')[1] : '--:--'}</td>
        <td>${riscoBadge}</td>
      </tr>
    `;
  }).join('');
}

// -------------------------------------------------------------
// TABELA DOS 32 LOCAIS DE VOTAÇÃO
// -------------------------------------------------------------
function renderLocaisTable(locais) {
  const tbody = document.getElementById('locaisTableBody');
  if (!tbody) return;

  tbody.innerHTML = locais.map(l => {
    const areaBadge = l.area === 'URBANA' 
      ? '<span class="badge badge-info">Urbana</span>' 
      : '<span class="badge badge-neutral">Rural</span>';

    const statusBadge = l.tem_votos_pos17
      ? '<span class="badge badge-danger">Alerta de Filas (Pós-17h)</span>'
      : (l.max_score_risco >= 40 
          ? '<span class="badge badge-warning">Atenção Logística</span>' 
          : '<span class="badge badge-success">Operação Normal</span>');

    return `
      <tr>
        <td style="font-family: var(--font-mono); font-weight: 700;">${l.num_local}</td>
        <td>
          <div style="font-weight: 600; color: #fff;">${l.nome}</div>
          <div style="font-size: 0.75rem; color: var(--text-muted);">${l.bairro_povoado} &bull; ${l.endereco}</div>
        </td>
        <td>${areaBadge}</td>
        <td style="font-family: var(--font-mono); font-weight: 600;">${l.total_secoes}</td>
        <td style="font-family: var(--font-mono); font-weight: 600;">${l.total_aptos_2026.toLocaleString('pt-BR')}</td>
        <td style="font-size: 0.8rem; color: var(--blue-accent);">Secs: ${l.secoes.join(', ')}</td>
        <td style="font-family: var(--font-mono);">${l.atraso_transmissao_max} min</td>
        <td>${statusBadge}</td>
      </tr>
    `;
  }).join('');
}

// -------------------------------------------------------------
// TABELAS DE DIAGNÓSTICO FORENSE
// -------------------------------------------------------------
function renderGargalosTable(gargalos) {
  const tbody = document.getElementById('gargalosTableBody');
  if (!tbody) return;

  tbody.innerHTML = gargalos.slice(0, 15).map(s => `
    <tr onclick="openSecaoModal(${s.secao})">
      <td style="font-family: var(--font-mono); font-weight: 700;">Sec ${s.secao}</td>
      <td><strong>${s.nome_local}</strong> (${s.bairro_povoado})</td>
      <td><span class="badge badge-danger">${s.votos_pos_17h} votos</span></td>
      <td style="font-family: var(--font-mono);">${s.tempo_medio_votacao_sec}s</td>
      <td style="font-family: var(--font-mono); font-size: 0.8rem;">${s.horario_encerramento || '--'}</td>
      <td style="color: var(--status-danger); font-weight: 600;">${s.secoes_agregadas}</td>
    </tr>
  `).join('');
}

function renderFalhasTable(falhas) {
  const tbody = document.getElementById('falhasTableBody');
  if (!tbody) return;

  tbody.innerHTML = falhas.slice(0, 15).map(s => `
    <tr onclick="openSecaoModal(${s.secao})">
      <td style="font-family: var(--font-mono); font-weight: 700;">Sec ${s.secao}</td>
      <td><strong>${s.nome_local}</strong></td>
      <td style="color: var(--status-warning); font-weight: 700;">${s.falhas_mesario.titulo_incorreto}</td>
      <td>${s.falhas_mesario.ja_votou}</td>
      <td>${s.falhas_mesario.suspenso}</td>
      <td style="font-weight: 700; color: #fff;">${s.falhas_mesario.total}</td>
    </tr>
  `).join('');
}

function renderTransmissaoTable(atrasos) {
  const tbody = document.getElementById('transmissaoTableBody');
  if (!tbody) return;

  tbody.innerHTML = atrasos.map(s => `
    <tr onclick="openSecaoModal(${s.secao})">
      <td style="font-family: var(--font-mono); font-weight: 700;">Sec ${s.secao}</td>
      <td><strong>${s.nome_local}</strong> (${s.bairro_povoado})</td>
      <td><span class="badge badge-neutral">${s.area}</span></td>
      <td style="font-family: var(--font-mono);">${s.horario_encerramento ? s.horario_encerramento.split(' ')[1] : '--'}</td>
      <td style="font-family: var(--font-mono); color: var(--gold);">${s.horario_bu_recebido ? s.horario_bu_recebido.split(' ')[1] : '--'}</td>
      <td style="font-family: var(--font-mono); font-weight: 700; color: var(--status-danger);">${s.atraso_transmissao_min} min</td>
    </tr>
  `).join('');
}

// -------------------------------------------------------------
// TABELAS DE LOGÍSTICA DE CAMPO (7 ROTAS CARGA, 31 MOTOS & APOIO)
// -------------------------------------------------------------
function renderVansTable(rotasCarga) {
  const tbody = document.getElementById('vansTableBody');
  if (!tbody || !rotasCarga) return;

  tbody.innerHTML = rotasCarga.map(v => {
    return `
      <tr>
        <td style="font-family: var(--font-mono); font-weight: 800; color: var(--gold); font-size: 0.95rem;">Rota ${v.rota}</td>
        <td style="font-weight: 700; color: #fff;">
          ${v.veiculo_modelo_placa}
        </td>
        <td style="color: #38bdf8; font-weight: 600; font-family: var(--font-mono); font-size: 0.82rem;">
          ${v.motorista_telefone}
        </td>
        <td><span class="badge ${v.area === 'Urbana' ? 'badge-info' : 'badge-neutral'}">${v.area}</span></td>
        <td style="font-weight: 700; font-family: var(--font-mono); text-align: center;">${v.qtd_locais}</td>
        <td style="font-weight: 800; color: #fff; font-family: var(--font-mono); text-align: center; color: var(--gold);">${v.qtd_urnas_cabinas}</td>
        <td style="font-size: 0.78rem; color: var(--text-muted); line-height: 1.4; max-width: 300px;">
          ${v.itinerario}
        </td>
        <td style="font-family: var(--font-mono); font-size: 0.8rem; color: #cbd5e1;">${v.distancia_total}</td>
        <td style="font-family: var(--font-mono); font-weight: 700; color: var(--blue-accent); font-size: 0.85rem;">${v.tempo_estimado}</td>
      </tr>
    `;
  }).join('');
}

function renderMotosTable(rotasMotos) {
  const tbody = document.getElementById('motosTableBody');
  if (!tbody || !rotasMotos) return;

  tbody.innerHTML = rotasMotos.map(m => {
    return `
      <tr>
        <td style="font-family: var(--font-mono); font-weight: 800; color: var(--blue-accent);">Moto ${m.moto_num || m.rota}</td>
        <td style="font-weight: 700; color: #fff;">
          ${m.condutor_telefone || m.condutor || '--'}
        </td>
        <td style="font-size: 0.8rem; color: #94a3b8; font-family: var(--font-mono);">
          ${m.veiculo_placa_ano || m.placa || '--'}
        </td>
        <td style="font-weight: 600; color: #cbd5e1; font-size: 0.82rem;">
          ${m.local_atendido || m.local || '--'}
        </td>
        <td><span class="badge ${(m.area || '').includes('Urbana') ? 'badge-info' : 'badge-neutral'}">${m.area || 'Rural'}</span></td>
        <td style="font-family: var(--font-mono); font-weight: 800; color: var(--gold); text-align: center;">${m.qtd_urnas || m.qtd_midias || 1} MR</td>
        <td style="font-family: var(--font-mono); font-size: 0.8rem;">${m.distancia_total || m.km_total || '--'}</td>
        <td style="font-family: var(--font-mono); font-weight: 700; color: var(--status-success);">${m.tempo_estimado || '--'}</td>
      </tr>
    `;
  }).join('');
}

function renderApoioTable(adms, coords, locais, apoioAuditado) {
  const tbody = document.getElementById('apoioTableBody');
  if (!tbody) return;

  const lista = apoioAuditado || locais.map(l => ({
    num_local: l.num_local,
    nome_local: l.nome,
    bairro_povoado: l.bairro_povoado,
    total_secoes: l.total_secoes,
    total_aptos_2026: l.total_aptos_2026,
    is_dificil_acesso: (l.num_local === 1392),
    administrador_predio: adms.find(a => a.num_local === l.num_local) || { nome: 'ADMINISTRADOR DESIGNADO' },
    coordenador_acessibilidade: coords.find(c => c.num_local === l.num_local)
  }));

  tbody.innerHTML = lista.map(item => {
    const isJucaral = item.is_dificil_acesso || (item.num_local === 1392);
    const admNome = item.administrador_predio ? item.administrador_predio.nome : 'ADMINISTRADOR DESIGNADO';
    const coordNome = item.coordenador_acessibilidade ? item.coordenador_acessibilidade.nome : null;

    const localBadge = isJucaral 
      ? `<span class="badge" style="background:#ef4444; color:#fff; font-weight:700; font-size:0.68rem; margin-left:6px;">⚠️ DIFÍCIL ACESSO (JUÇARAL DAS MARGARIDAS)</span>`
      : '';

    const coordHtml = coordNome 
      ? `<strong style="color: #38bdf8;">${coordNome}</strong>`
      : `<span style="color: var(--text-dim); font-size: 0.75rem;">(Suporte via Adm de Prédio)</span>`;

    const missaoHtml = isJucaral
      ? `<span style="color: #f87171; font-weight:600;">Recepção sábado e recolhimento unificado domingo via Suprimento de Fundos (Werbeth Silva Dutra)</span>`
      : `<strong>07h00:</strong> Apoio Zerésima | <strong>17h00:</strong> Portão & Guarda | <strong>Entrega:</strong> ${item.total_secoes} MR ao Mototáxi`;

    return `
      <tr style="${isJucaral ? 'background: rgba(239, 68, 68, 0.08); border-left: 3px solid #ef4444;' : ''}">
        <td style="font-family: var(--font-mono); font-weight: 700; color: #fff;">${item.num_local}</td>
        <td>
          <div style="font-weight: 600; color: #fff; display: flex; align-items: center; flex-wrap: wrap;">
            ${item.nome_local} ${localBadge}
          </div>
          <div style="font-size: 0.72rem; color: var(--text-muted);">${item.bairro_povoado} &bull; ${item.total_secoes} seções (${(item.total_aptos_2026 || 0).toLocaleString('pt-BR')} aptos)</div>
        </td>
        <td style="color: var(--gold); font-weight: 700;">${admNome}</td>
        <td>${coordHtml}</td>
        <td style="font-size: 0.75rem; color: #cbd5e1; line-height: 1.4;">
          ${missaoHtml}
        </td>
      </tr>
    `;
  }).join('');
}

function renderApoioTableLegacy(apoioLocais) {
  const tbody = document.getElementById('apoioTableBody');
  if (!tbody || !apoioLocais) return;

  tbody.innerHTML = apoioLocais.map(a => `
    <tr>
      <td style="font-family: var(--font-mono); font-weight: 700;">${a.num_local}</td>
      <td style="font-weight: 600; color: #fff;">${a.nome_local}</td>
      <td style="color: var(--gold); font-weight: 600;">${a.adm}</td>
      <td style="color: #38bdf8;">${a.coord_acesso}</td>
      <td style="font-size: 0.75rem; color: #cbd5e1;">Apoio Zerésima 07h & Entrega ao Mototáxi 17h</td>
    </tr>
  `).join('');
}

// -------------------------------------------------------------
// MODAIS DE DETALHES DE SEÇÃO E MAPA HISTÓRICO
// -------------------------------------------------------------
function setupModal() {
  // Modal de Seção
  const overlaySecao = document.getElementById('secaoModalOverlay');
  const closeBtnSecao = document.getElementById('modalCloseBtn');
  if (overlaySecao && closeBtnSecao) {
    closeBtnSecao.addEventListener('click', () => overlaySecao.classList.remove('active'));
    overlaySecao.addEventListener('click', (e) => {
      if (e.target === overlaySecao) overlaySecao.classList.remove('active');
    });
  }

  // Modal do Mapa Histórico 2018
  const overlayMapa = document.getElementById('mapaHistoricoModalOverlay');
  const closeBtnMapa = document.getElementById('modalMapaCloseBtn');
  if (overlayMapa && closeBtnMapa) {
    closeBtnMapa.addEventListener('click', () => overlayMapa.classList.remove('active'));
    overlayMapa.addEventListener('click', (e) => {
      if (e.target === overlayMapa) overlayMapa.classList.remove('active');
    });
  }
}

window.openMapaHistoricoModal = function() {
  const overlay = document.getElementById('mapaHistoricoModalOverlay');
  if (overlay) overlay.classList.add('active');
};

window.openSecaoModal = function(secaoNum) {
  const data = window.ZE041_DATA;
  const s = data.master.secoes.find(x => x.secao === secaoNum);
  if (!s) return;

  const overlay = document.getElementById('secaoModalOverlay');
  if (!overlay) return;

  document.getElementById('modalSecaoTitle').innerText = `Seção Eleitoral nº ${s.secao}`;
  document.getElementById('modalSecaoSubtitle').innerText = `${s.nome_local} — ${s.bairro_povoado}`;

  document.getElementById('modalAptos').innerText = s.aptos_2026;
  document.getElementById('modalTempoVoto').innerText = `${s.tempo_medio_votacao_sec}s`;
  document.getElementById('modalBio').innerText = `${s.pct_biometria}%`;
  document.getElementById('modalAgreg').innerText = s.secoes_agregadas;
  document.getElementById('modalAcessibilidade').innerText = s.acessibilidade;
  document.getElementById('modalRisco').innerHTML = `<span class="badge ${s.badge_class}">${s.nivel_risco} (Score: ${s.score_risco})</span>`;

  document.getElementById('modalVotos17').innerText = `${s.votos_pos_17h} votos`;
  document.getElementById('modalHorarioEnc').innerText = s.horario_encerramento || '17:00';
  document.getElementById('modalHorarioBU').innerText = s.horario_bu_recebido || '19:00';
  document.getElementById('modalAtrasoBU').innerText = `${s.atraso_transmissao_min} minutos`;

  document.getElementById('modalFalhasMesario').innerText = `Tít. Incorreto: ${s.falhas_mesario.titulo_incorreto} | Já Votou: ${s.falhas_mesario.ja_votou} | Suspenso: ${s.falhas_mesario.suspenso} | Cancelada: ${s.falhas_mesario.hab_cancelada}`;
  document.getElementById('modalFalhasUrna').innerText = `Troca MV: ${s.falhas_urna.troca_mv} | Reinício: ${s.falhas_urna.reinicio} | Substituição: ${s.falhas_urna.substituicao}`;

  overlay.classList.add('active');
};

// -------------------------------------------------------------
// RENDERIZAÇÃO DA ESCALA OFICIAL DE ADH (SÁBADO & DOMINGO)
// -------------------------------------------------------------
function renderADHTable(escala) {
  const tbody = document.getElementById('adhTableBody');
  if (!tbody || !escala || !escala.equipe_responsavel) return;

  tbody.innerHTML = escala.equipe_responsavel.map(r => {
    const locaisStr = r.locais.map(l => `<strong>${l.nome.split('(')[0].trim()}</strong> <span style="color:var(--text-muted); font-size:0.75rem;">(${l.secoes.length} un)</span>`).join('<br>');
    const totalUrnas = r.locais.reduce((acc, l) => acc + l.secoes.length, 0);

    let badgeColor = '#38bdf8';
    if (r.id === 1) badgeColor = 'var(--gold)';
    else if (r.id === 2 || r.id === 4) badgeColor = '#c084fc';
    else if (r.id === 7) badgeColor = '#f87171';
    else badgeColor = '#10b981';

    return `
      <tr style="border-bottom: 1px solid rgba(255,255,255,0.05);">
        <td style="padding: 10px 12px; font-weight: 800; color: ${badgeColor}; font-size: 0.95rem;">${String(r.id).padStart(2, '0')}</td>
        <td style="padding: 10px 12px; font-weight: 700; color: #fff;">
          ${r.nome}
          <div style="font-size: 0.72rem; color: var(--text-muted); font-weight: 400;">${r.tipo}</div>
        </td>
        <td style="padding: 10px 12px; color: ${badgeColor}; font-weight: 600;">${r.cargo}</td>
        <td style="padding: 10px 12px; color: #cbd5e1; font-size: 0.8rem;">${r.polo}</td>
        <td style="padding: 10px 12px; font-size: 0.78rem; line-height: 1.5;">${locaisStr}</td>
        <td style="padding: 10px 12px; text-align: center; font-weight: 800; color: #fff; background: rgba(255,255,255,0.02);">${totalUrnas}</td>
        </td>
      </tr>
    `;
  }).join('');
}

// -------------------------------------------------------------
// CONTROLE DE PRESENÇA NO DIA DA ELEIÇÃO & ESCALAS OFICIAIS
// -------------------------------------------------------------
function initControlePresenca(data) {
  const tbody = document.getElementById('presencaTableBody');
  if (!tbody) return;

  const STORAGE_KEY = 'ze041_presenca_oficial_2026';
  let presencasGravadas = {};
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (raw) presencasGravadas = JSON.parse(raw);
  } catch (e) {
    console.error("Erro ao ler presenças do localStorage:", e);
  }

  // 1. Montar Lista Unificada de Convocados (425 registros oficiais)
  const convocados = [];

  // 1.1 Mesários (375)
  if (data.mesarios_secoes && Array.isArray(data.mesarios_secoes)) {
    data.mesarios_secoes.forEach((m, idx) => {
      const isPres = (m.funcao === 'Presidente');
      convocados.push({
        id: `mes_${m.secao}_${idx}`,
        nome: m.nome,
        funcao: m.funcao,
        tipo_papel: isPres ? 'PRESIDENTE' : 'MESARIO',
        badge_style: isPres ? 'background: rgba(245, 158, 11, 0.2); color: var(--gold); border: 1px solid rgba(245, 158, 11, 0.4);' : 'background: rgba(56, 189, 248, 0.15); color: #38bdf8; border: 1px solid rgba(56, 189, 248, 0.3);',
        secao: `Seção ${m.secao}`,
        local: m.local,
        diretriz: isPres ? '⚠️ Emitir Zerésima às 07h00 | Conduzir votação 08h-17h | Emitir BU às 17h00' : 'Identificação biométrica / Caderno de votação / Controle de fila'
      });
    });
  }

  // 1.2 Administradores de Prédio (32)
  if (data.logistica_consolidada && data.logistica_consolidada.administradores_predio) {
    data.logistica_consolidada.administradores_predio.forEach((adm, idx) => {
      convocados.push({
        id: `adm_${adm.num || idx}`,
        nome: adm.nome,
        funcao: 'Administrador de Prédio',
        tipo_papel: 'ADM_PREDIO',
        badge_style: 'background: rgba(168, 85, 247, 0.2); color: #c084fc; border: 1px solid rgba(168, 85, 247, 0.4);',
        secao: 'Geral do Prédio',
        local: adm.local,
        diretriz: '🔑 Abertura do prédio | Suporte Zerésima 07h | Trancar portão 17h | Entrega das mídias ao mototáxi'
      });
    });
  }

  // 1.3 Coordenadores de Acessibilidade (11)
  if (data.logistica_consolidada && data.logistica_consolidada.coordenadores_acessibilidade) {
    data.logistica_consolidada.coordenadores_acessibilidade.forEach((c, idx) => {
      convocados.push({
        id: `coord_${c.num || idx}`,
        nome: c.nome,
        funcao: 'Coordenador de Acessibilidade',
        tipo_papel: 'COORD_ACESSO',
        badge_style: 'background: rgba(16, 185, 129, 0.2); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.4);',
        secao: 'Acessibilidade / Portão',
        local: c.local,
        diretriz: '♿ Prioridade imediata a idosos/PCD | Desobstrução de corredores | Apoio às seções'
      });
    });
  }

  // 1.4 Técnicos de Urna & Fiscais de ADH (7)
  if (data.escala_adh && data.escala_adh.equipe_responsavel) {
    data.escala_adh.equipe_responsavel.forEach(t => {
      convocados.push({
        id: `tec_${t.id}`,
        nome: t.nome,
        funcao: `${t.cargo} (Fiscal ADH)`,
        tipo_papel: 'TECNICO_ADH',
        badge_style: 'background: rgba(239, 68, 68, 0.2); color: #f87171; border: 1px solid rgba(239, 68, 68, 0.4);',
        secao: `${t.locais.reduce((acc,l)=>acc+l.secoes.length, 0)} seções inspecionadas`,
        local: t.polo,
        diretriz: '⏱️ Vistoria ADH no sábado | Auditoria de zerésima 07h | Suporte volante domingo'
      });
    });
  }

  // Atualizar contadores estáticos
  const totalConvocados = convocados.length;
  const countTodosEl = document.getElementById('countRoleTodos');
  if (countTodosEl) countTodosEl.innerText = totalConvocados;

  // Estado dos Filtros
  let activeRole = 'TODOS';
  let onlyPending = false;
  let searchQuery = '';

  function salvarPresencas() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(presencasGravadas));
    } catch (e) {
      console.error("Erro ao salvar presenças no localStorage:", e);
    }
  }

  function atualizarKPIsPresenca() {
    const totalPresentes = Object.keys(presencasGravadas).length;
    const pct = totalConvocados > 0 ? ((totalPresentes / totalConvocados) * 100).toFixed(1) : 0;

    const kpiConfirmada = document.getElementById('kpiPresencaConfirmada');
    if (kpiConfirmada) kpiConfirmada.innerText = `${totalPresentes} / ${totalConvocados}`;

    const kpiPct = document.getElementById('kpiPresencaPct');
    if (kpiPct) kpiPct.innerText = `${pct}% presente`;
  }

  function renderPresencaList() {
    const q = searchQuery.toLowerCase().trim();

    const filtrados = convocados.filter(item => {
      // Filtro por Papel
      if (activeRole !== 'TODOS') {
        if (activeRole === 'MESARIO' && (item.tipo_papel !== 'MESARIO' && item.tipo_papel !== 'PRESIDENTE')) return false;
        if (activeRole === 'PRESIDENTE' && item.tipo_papel !== 'PRESIDENTE') return false;
        if (activeRole === 'ADM_PREDIO' && item.tipo_papel !== 'ADM_PREDIO') return false;
        if (activeRole === 'COORD_ACESSO' && item.tipo_papel !== 'COORD_ACESSO') return false;
        if (activeRole === 'TECNICO_ADH' && item.tipo_papel !== 'TECNICO_ADH') return false;
      }

      // Filtro por Apenas Pendentes
      const isPresente = !!presencasGravadas[item.id];
      if (onlyPending && isPresente) return false;

      // Filtro de Busca Textual
      if (q) {
        const matchNome = item.nome.toLowerCase().includes(q);
        const matchLocal = item.local.toLowerCase().includes(q);
        const matchSecao = item.secao.toLowerCase().includes(q) || item.secao.replace(/\D/g, '') === q;
        const matchFuncao = item.funcao.toLowerCase().includes(q);
        if (!matchNome && !matchLocal && !matchSecao && !matchFuncao) return false;
      }

      return true;
    });

    const badgeFiltered = document.getElementById('presencaFilteredBadge');
    if (badgeFiltered) badgeFiltered.innerText = `Exibindo ${filtrados.length} de ${totalConvocados} registros`;

    if (filtrados.length === 0) {
      tbody.innerHTML = `
        <tr>
          <td colspan="7" style="text-align: center; padding: 2rem; color: var(--text-muted);">
            Nenhum colaborador encontrado com os filtros selecionados.
          </td>
        </tr>
      `;
      atualizarKPIsPresenca();
      return;
    }

    tbody.innerHTML = filtrados.map(item => {
      const reg = presencasGravadas[item.id];
      const isChecked = !!reg;
      const horarioStr = reg ? reg.horario : '--:--';
      const rowBg = isChecked ? 'background: rgba(16, 185, 129, 0.05);' : '';

      return `
        <tr style="${rowBg} border-bottom: 1px solid rgba(255,255,255,0.04);">
          <td style="text-align: center; vertical-align: middle;">
            <input type="checkbox" class="presenca-checkbox" data-id="${item.id}" ${isChecked ? 'checked' : ''} 
              style="width: 18px; height: 18px; cursor: pointer; accent-color: #10b981;">
          </td>
          <td style="font-family: var(--font-mono); font-size: 0.8rem; color: ${isChecked ? '#10b981' : 'var(--text-dim)'}; font-weight: ${isChecked ? '700' : '400'};">
            ${horarioStr}
          </td>
          <td style="font-weight: 700; color: #fff;">
            ${item.nome}
          </td>
          <td>
            <span class="badge" style="${item.badge_style} font-size: 0.72rem; padding: 3px 8px; border-radius: 4px;">
              ${item.funcao}
            </span>
          </td>
          <td style="font-family: var(--font-mono); font-weight: 700; color: var(--gold);">
            ${item.secao}
          </td>
          <td>
            <div style="font-weight: 600; color: #cbd5e1; font-size: 0.82rem;">${item.local}</div>
          </td>
          <td style="font-size: 0.75rem; color: var(--text-muted); line-height: 1.35;">
            ${item.diretriz}
          </td>
        </tr>
      `;
    }).join('');

    // Adicionar eventos aos checkboxes
    const checkboxes = tbody.querySelectorAll('.presenca-checkbox');
    checkboxes.forEach(cb => {
      cb.addEventListener('change', (e) => {
        const id = e.target.getAttribute('data-id');
        if (e.target.checked) {
          const nowStr = new Date().toLocaleTimeString('pt-BR');
          presencasGravadas[id] = { presente: true, horario: nowStr };
        } else {
          delete presencasGravadas[id];
        }
        salvarPresencas();
        atualizarKPIsPresenca();
        renderPresencaList();
      });
    });

    atualizarKPIsPresenca();
  }

  // Configuração dos Eventos
  const searchInput = document.getElementById('presencaSearchInput');
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      searchQuery = e.target.value;
      renderPresencaList();
    });
  }

  const roleChips = document.querySelectorAll('[data-filter-role]');
  roleChips.forEach(chip => {
    chip.addEventListener('click', () => {
      roleChips.forEach(c => c.classList.remove('active'));
      chip.classList.add('active');
      activeRole = chip.getAttribute('data-filter-role');
      renderPresencaList();
    });
  });

  const pendingChip = document.querySelector('[data-filter-status="PENDENTES"]');
  if (pendingChip) {
    pendingChip.addEventListener('click', () => {
      onlyPending = !onlyPending;
      if (onlyPending) {
        pendingChip.classList.add('active');
        pendingChip.style.background = 'rgba(245, 158, 11, 0.2)';
      } else {
        pendingChip.classList.remove('active');
        pendingChip.style.background = 'transparent';
      }
      renderPresencaList();
    });
  }

  const btnMarcarTodos = document.getElementById('btnMarcarPresentesVisiveis');
  if (btnMarcarTodos) {
    btnMarcarTodos.addEventListener('click', () => {
      const checkboxes = tbody.querySelectorAll('.presenca-checkbox:not(:checked)');
      if (checkboxes.length === 0) {
        alert("Todos os colaboradores listados já estão com presença registrada!");
        return;
      }
      const nowStr = new Date().toLocaleTimeString('pt-BR');
      checkboxes.forEach(cb => {
        const id = cb.getAttribute('data-id');
        presencasGravadas[id] = { presente: true, horario: nowStr };
      });
      salvarPresencas();
      renderPresencaList();
    });
  }

  const btnLimpar = document.getElementById('btnLimparPresencas');
  if (btnLimpar) {
    btnLimpar.addEventListener('click', () => {
      if (confirm("Tem certeza que deseja zerar todas as marcações de presença salvas?")) {
        presencasGravadas = {};
        salvarPresencas();
        renderPresencaList();
      }
    });
  }

  const btnExportarCSV = document.getElementById('btnExportarPresencaCSV');
  if (btnExportarCSV) {
    btnExportarCSV.addEventListener('click', () => {
      const cabecalho = ['Nome do Convocado', 'Cargo / Função', 'Seção Eleitoral', 'Local de Votação', 'Situação Presença', 'Horário de Registro'];
      const linhas = convocados.map(item => {
        const reg = presencasGravadas[item.id];
        const status = reg ? 'PRESENTE' : 'PENDENTE / AUSENTE';
        const hora = reg ? reg.horario : '--:--';
        return [
          `"${item.nome.replace(/"/g, '""')}"`,
          `"${item.funcao.replace(/"/g, '""')}"`,
          `"${item.secao.replace(/"/g, '""')}"`,
          `"${item.local.replace(/"/g, '""')}"`,
          `"${status}"`,
          `"${hora}"`
        ].join(';');
      });

      const csvContent = '\uFEFF' + [cabecalho.join(';'), ...linhas].join('\r\n');
      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.setAttribute('href', url);
      link.setAttribute('download', `Frequencia_Oficial_Eleicoes_2026_ZE041_${new Date().toISOString().slice(0,10)}.csv`);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(url);
    });
  }

  // Render inicial
  renderPresencaList();
}

// -------------------------------------------------------------
// RENDERIZAÇÃO DO 1º TURNO REAL & ESTRATÉGIA DO 2º TURNO (2026)
// -------------------------------------------------------------
function renderSegundoTurno(res1T) {
  if (!res1T) return;

  const est = res1T.estatisticas_oficiais_tse;
  if (est) {
    setElText('kpi1TComparecimento', `${est.comparecimento.toLocaleString('pt-BR')}`);
    setElText('kpi1TPrimeiroEncerramento', est.primeiro_encerramento_urna.split(' ')[1] || "17:00:00");
    setElText('kpi1TUltimoEncerramento', est.ultimo_encerramento_urna.split(' ')[1] || "19:52:31");
    setElText('kpi1TTotalizacao', est.ultima_totalizacao.split(' ')[1] || "20:55:14");
  }

  // 1. Ações Focais do 2º Turno
  const gridAcoes = document.getElementById('gridAcoes2Turno');
  if (gridAcoes && res1T.diretrizes_estrategicas_2turno && res1T.diretrizes_estrategicas_2turno.acoes_focais) {
    gridAcoes.innerHTML = res1T.diretrizes_estrategicas_2turno.acoes_focais.map((ac, idx) => `
      <div style="background: rgba(15, 23, 42, 0.7); border-radius: 8px; padding: 12px; border: 1px solid rgba(255,255,255,0.08); border-left: 3px solid #f59e0b;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;">
          <span style="font-size: 0.82rem; font-weight: 800; color: #fff;">${idx + 1}. ${ac.alvo}</span>
          <span class="badge badge-warning" style="font-size: 0.7rem;">${ac.responsavel}</span>
        </div>
        <div style="font-size: 0.76rem; color: #f87171; margin-bottom: 4px;">
          <strong>1ºT:</strong> ${ac.problema_1turno}
        </div>
        <div style="font-size: 0.78rem; color: #e2e8f0; line-height: 1.35;">
          <strong>Ação 2ºT:</strong> ${ac.acao_2turno}
        </div>
      </div>
    `).join('');
  }

  // 2. Tabela de Gargalos de Filas Pós-17h
  const tbodyGargalos = document.getElementById('tbodyGargalos1Turno');
  if (tbodyGargalos && res1T.top_gargalos_filas_pos17h) {
    tbodyGargalos.innerHTML = res1T.top_gargalos_filas_pos17h.map(g => {
      let badgeStyle = "badge-danger";
      let esperaTxt = `${g.espera_minutos} min`;
      if (g.espera_minutos >= 120) esperaTxt = `2h${g.espera_minutos - 120}m de fila`;
      else if (g.espera_minutos >= 60) esperaTxt = `1h${g.espera_minutos - 60}m de fila`;

      return `
        <tr>
          <td style="text-align: center; font-weight: 800; color: var(--gold); font-size: 0.95rem;">${g.secao}</td>
          <td style="font-weight: 600; color: #fff;">${g.local}</td>
          <td><span style="color: var(--text-muted); font-size: 0.8rem;">${g.povoado}</span></td>
          <td style="text-align: center; font-family: monospace; font-weight: 700; color: #f87171;">${g.encerramento}</td>
          <td style="text-align: center;"><span class="badge ${badgeStyle}">${esperaTxt}</span></td>
          <td style="font-size: 0.8rem; color: #cbd5e1;">${g.motivo}</td>
        </tr>
      `;
    }).join('');
  }

  // 3. Casos de Sucesso
  const containerSucesso = document.getElementById('containerCasosSucesso');
  if (containerSucesso && res1T.casos_sucesso_pontualidade) {
    containerSucesso.innerHTML = res1T.casos_sucesso_pontualidade.map(cs => `
      <div style="background: rgba(16, 185, 129, 0.08); border: 1px solid rgba(16, 185, 129, 0.2); border-radius: 6px; padding: 10px;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 4px;">
          <strong style="color: #10b981; font-size: 0.82rem;">${cs.local}</strong>
          <span style="font-family: monospace; font-size: 0.75rem; color: #6ee7b7; font-weight: 700;">
            ${cs.encerramento ? `Enc: ${cs.encerramento}` : `Enc. Médio: ${cs.encerramento_medio}`}
          </span>
        </div>
        <div style="font-size: 0.76rem; color: #cbd5e1; line-height: 1.35;">
          ${cs.destaque}
        </div>
      </div>
    `).join('');
  }

  // 4. Benchmarking Regional
  const tbodyBench = document.getElementById('tbodyBenchmarking');
  if (tbodyBench && res1T.benchmarking_regional_maranhao) {
    tbodyBench.innerHTML = res1T.benchmarking_regional_maranhao.map(b => {
      const isVit = b.municipio.includes('Vitória do Mearim');
      const isCritico = b.status === 'Crítico';
      const rowStyle = isVit ? 'background: rgba(245, 158, 11, 0.12); font-weight: 800;' : '';
      const badgeCls = isVit ? 'badge-gold' : (isCritico ? 'badge-danger' : (b.status === 'Totalizado antes' ? 'badge-success' : 'badge-info'));
      return `
        <tr style="${rowStyle}">
          <td><strong>${b.municipio}</strong> <span style="font-size:0.7rem; color:var(--text-muted);">(ZE ${b.zona})</span></td>
          <td style="text-align: right; font-family: monospace;">${b.aptos.toLocaleString('pt-BR')}</td>
          <td style="text-align: center; font-family: monospace; color: ${isCritico ? '#f87171' : (isVit ? 'var(--gold)' : '#38bdf8')}; font-weight: 700;">${b.totalizacao}</td>
          <td><span class="badge ${badgeCls}" style="font-size: 0.68rem;">${b.comparativo}</span></td>
        </tr>
      `;
    }).join('');
  }

  // 5. Tabela Completa das 94 Seções
  const tbodySecoes1T = document.getElementById('tbodyTodasSecoes1Turno');
  const inputSearch = document.getElementById('inputSearch1Turno');
  const badgeCount = document.getElementById('badgeCount1Turno');

  if (tbodySecoes1T && res1T.secoes) {
    const secoesArr = Object.entries(res1T.secoes).map(([num, s]) => ({ num: parseInt(num), ...s }));
    secoesArr.sort((a, b) => a.num - b.num);

    function renderSecoes1TList(termo) {
      const filtradas = secoesArr.filter(s => {
        if (!termo) return true;
        const txt = `secao ${s.num} ${s.local}`.toLowerCase();
        return txt.includes(termo);
      });

      if (badgeCount) badgeCount.innerText = `${filtradas.length} de 94 seções`;

      tbodySecoes1T.innerHTML = filtradas.map(s => {
        const pctComp = s.aptos > 0 ? ((s.comp / s.aptos) * 100).toFixed(1) : 0;
        
        let statusTag = '<span class="badge badge-success" style="font-size:0.7rem;">Normal (&lt;17h10)</span>';
        if (s.encerramento >= '19:00:00') {
          statusTag = '<span class="badge badge-danger" style="font-size:0.7rem;">Crítico (&gt;19h)</span>';
        } else if (s.encerramento >= '18:00:00') {
          statusTag = '<span class="badge badge-warning" style="font-size:0.7rem;">Fila (&gt;18h)</span>';
        } else if (s.encerramento >= '17:15:00') {
          statusTag = '<span class="badge badge-info" style="font-size:0.7rem;">Moderado (&gt;17h15)</span>';
        }

        return `
          <tr>
            <td style="text-align: center; font-weight: 800; color: var(--gold);">${s.num}</td>
            <td style="font-weight: 600; color: #fff;">${s.local}</td>
            <td style="text-align: center; font-family: monospace;">${s.aptos}</td>
            <td style="text-align: center; font-family: monospace; color: #38bdf8;">${s.comp}</td>
            <td style="text-align: center; font-family: monospace; font-size: 0.8rem;">${pctComp}%</td>
            <td style="text-align: center; font-family: monospace; font-size: 0.8rem; color: var(--text-muted);">${s.inicio || '08:00:01'}</td>
            <td style="text-align: center; font-family: monospace; font-weight: 700; color: ${s.encerramento >= '18:00:00' ? '#f87171' : '#10b981'};">${s.encerramento}</td>
            <td style="text-align: center; font-family: monospace; font-size: 0.8rem;">${s.transmitido || '--:--:--'}</td>
            <td style="text-align: center; font-family: monospace; font-size: 0.8rem;">${s.recebido || '--:--:--'}</td>
            <td style="text-align: center; font-family: monospace; font-size: 0.8rem; color: #38bdf8;">${s.totalizado || '--:--:--'}</td>
            <td style="text-align: center;">${statusTag}</td>
          </tr>
        `;
      }).join('');
    }

    if (inputSearch) {
      inputSearch.addEventListener('input', (e) => {
        renderSecoes1TList(e.target.value.toLowerCase().trim());
      });
    }

    renderSecoes1TList('');
  }
}

// -------------------------------------------------------------
// 7.3 PROJEÇÃO PREDITIVA SEÇÃO A SEÇÃO - 2º TURNO (25/10/2026)
// -------------------------------------------------------------
function initPredicao2Turno() {
  const pData = window.PREDICAO_2TURNO_DATA;
  if (!pData || !pData.secoes_predicao) {
    console.warn("Dados de predição do 2º turno não encontrados em window.PREDICAO_2TURNO_DATA");
    return;
  }

  const secoes = pData.secoes_predicao;
  const tbody = document.getElementById('tbodyPredicao2Turno');
  const searchInput = document.getElementById('searchPredicao');
  const filterPolo = document.getElementById('filterPredicaoPolo');
  const filterFaixa = document.getElementById('filterPredicaoFaixa');
  const countBadge = document.getElementById('countPredicaoVisiveis');

  if (!tbody) return;

  function renderRows() {
    const q = searchInput ? searchInput.value.toLowerCase().trim() : '';
    const poloSel = filterPolo ? filterPolo.value : 'TODOS';
    const faixaSel = filterFaixa ? filterFaixa.value : 'TODAS';

    const filtradas = secoes.filter(s => {
      // 1. Filtro busca textual
      if (q) {
        const txt = `${s.secao} ${s.local_nome} ${s.bairro_povoado} ${s.tecnico_responsavel} ${s.mototaxi_responsavel}`.toLowerCase();
        if (!txt.includes(q)) return false;
      }
      // 2. Filtro polo / técnico
      if (poloSel !== 'TODOS' && s.tecnico_responsavel !== poloSel) {
        return false;
      }
      // 3. Filtro faixa de onda
      if (faixaSel !== 'TODAS' && !s.predicao_2t_2026.faixa_onda.startsWith(faixaSel)) {
        return false;
      }
      return true;
    });

    if (countBadge) {
      countBadge.innerText = filtradas.length;
    }

    if (filtradas.length === 0) {
      tbody.innerHTML = `<tr><td colspan="12" style="text-align:center; padding: 2.5rem; color: #94a3b8;">Nenhuma seção encontrada com os filtros selecionados.</td></tr>`;
      return;
    }

    tbody.innerHTML = filtradas.map(s => {
      const pred = s.predicao_2t_2026;
      const h1t = s.historico_1t_2026;
      const h22 = s.historico_2t_2022;

      let badgeColor = pred.cor_badge || '#10b981';
      let statusHtml = `
        <span class="badge" style="background: ${badgeColor}; color: #022c22; font-weight: 700; font-size: 0.7rem; padding: 3px 8px; border-radius: 4px;">${pred.status_badge}</span>
        <div style="font-size: 0.72rem; color: #94a3b8; margin-top: 3px; line-height: 1.25;">${pred.justificativa}</div>
      `;

      return `
        <tr>
          <td style="text-align: center; font-weight: 800; color: var(--gold); font-size: 0.95rem;">${s.secao}</td>
          <td>
            <div style="font-weight: 700; color: #fff;">${s.local_nome}</div>
            <div style="font-size: 0.75rem; color: #38bdf8; margin-top: 2px;">🏍️ ${s.mototaxi_responsavel}</div>
          </td>
          <td>
            <span style="color: #cbd5e1; font-size: 0.82rem; font-weight: 600;">${s.bairro_povoado || 'Sede'}</span>
            <div style="font-size: 0.7rem; color: #64748b;">${s.tipo_via}</div>
          </td>
          <td>
            <div style="font-weight: 600; color: #e2e8f0;">${s.tecnico_responsavel}</div>
            <div style="font-size: 0.72rem; color: #94a3b8;">${s.polo_logistico}</div>
          </td>
          <td style="text-align: center; font-family: monospace;">
            <strong style="color: #fff; font-size: 0.88rem;">${s.votantes_estimados}</strong>
            <span style="font-size: 0.7rem; color: #64748b;">/${s.aptos}</span>
          </td>
          <td style="text-align: center; font-family: monospace; font-size: 0.8rem; color: ${h1t.encerramento >= '18:00:00' ? '#f87171' : '#cbd5e1'};">
            ${h1t.encerramento}
          </td>
          <td style="text-align: center; font-family: monospace; font-size: 0.8rem; color: #38bdf8;">
            ${h22.encerramento || '--:--:--'}
          </td>
          <td style="text-align: center; font-family: monospace; font-weight: 700; color: #10b981; font-size: 0.88rem; background: rgba(16, 185, 129, 0.08);">
            ${pred.encerramento_urna}
          </td>
          <td style="text-align: center; font-family: monospace; font-size: 0.88rem; font-weight: 700; color: #38bdf8; background: rgba(56, 189, 248, 0.08);">
            +${s.delta_t_chegada_cartorio_min || pred.delta_t_chegada_min || s.delta_t_empirico_total_min || 0} min
            <div style="font-size: 0.68rem; color: #94a3b8; font-weight: 400;">(${s.tempo_deslocamento_estrada_min}m estrada)</div>
          </td>
          <td style="text-align: center; font-family: monospace; font-weight: 800; color: #fbbf24; font-size: 0.9rem; background: rgba(251, 191, 36, 0.08);" title="Momento exato da entrega na Zona Eleitoral p/ Transportador Desktop">
            ${pred.chegada_cartorio}
          </td>
          <td style="text-align: center; font-family: monospace; font-weight: 800; color: var(--gold); font-size: 0.9rem;" title="Transmissão no SISTOT após leitura pelo Chefe de Cartório">
            ${pred.transmissao_sistot}
          </td>
          <td>${statusHtml}</td>
        </tr>
      `;
    }).join('');
  }

  if (searchInput) searchInput.addEventListener('input', renderRows);
  if (filterPolo) filterPolo.addEventListener('change', renderRows);
  if (filterFaixa) filterFaixa.addEventListener('change', renderRows);

  renderRows();
}

