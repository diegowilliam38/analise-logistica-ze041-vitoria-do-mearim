// ==========================================================================
// RENDERIZAÇÃO DE GRÁFICOS INTERATIVOS - CHART.JS (ZE-041)
// ==========================================================================

window.initDashboardCharts = function(data) {
  const master = data.master;
  const serie = data.serie_historica;
  const demo = data.demografia;
  const diag = data.diagnostico;

  // Configuração global de temas para Chart.js
  Chart.defaults.color = '#94a3b8';
  Chart.defaults.font.family = "'Inter', sans-serif";
  Chart.defaults.scale.grid.color = 'rgba(255, 255, 255, 0.05)';
  Chart.defaults.plugins.tooltip.backgroundColor = 'rgba(14, 22, 38, 0.95)';
  Chart.defaults.plugins.tooltip.titleColor = '#fff';
  Chart.defaults.plugins.tooltip.borderColor = 'rgba(56, 189, 248, 0.3)';
  Chart.defaults.plugins.tooltip.borderWidth = 1;
  Chart.defaults.plugins.tooltip.padding = 10;
  Chart.defaults.plugins.tooltip.cornerRadius = 8;

  // -------------------------------------------------------------
  // 1. Gráfico Histórico: Comparecimento vs Abstenção (2016-2026)
  // -------------------------------------------------------------
  const ctxHistorico = document.getElementById('chartHistorico');
  if (ctxHistorico) {
    new Chart(ctxHistorico, {
      type: 'line',
      data: {
        labels: serie.map(s => `${s.ano} (${s.tipo})`),
        datasets: [
          {
            label: 'Comparecimento (%)',
            data: serie.map(s => s.taxa_comparecimento_pct),
            borderColor: '#38bdf8',
            backgroundColor: 'rgba(56, 189, 248, 0.1)',
            fill: true,
            tension: 0.3,
            pointRadius: 5,
            pointBackgroundColor: '#0284c7',
            pointBorderColor: '#fff',
            pointBorderWidth: 2
          },
          {
            label: 'Abstenção (%)',
            data: serie.map(s => s.taxa_abstencao_pct),
            borderColor: '#f59e0b',
            backgroundColor: 'rgba(245, 158, 11, 0.05)',
            borderDash: [5, 5],
            fill: false,
            tension: 0.3,
            pointRadius: 5,
            pointBackgroundColor: '#f59e0b',
            pointBorderColor: '#fff',
            pointBorderWidth: 2
          }
        ]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'top', labels: { boxWidth: 12, font: { size: 11 } } },
          tooltip: {
            callbacks: {
              afterLabel: function(context) {
                const s = serie[context.dataIndex];
                return `Aptos: ${s.aptos.toLocaleString('pt-BR')} | Comparecimento: ${(s.comparecimento || s.comparecimento_projetado).toLocaleString('pt-BR')}`;
              }
            }
          }
        },
        scales: {
          y: { min: 0, max: 100, ticks: { callback: v => v + '%' } }
        }
      }
    });
  }

  // -------------------------------------------------------------
  // 2. Gráfico Donut: Distribuição de Risco das 94 Seções
  // -------------------------------------------------------------
  const ctxRisco = document.getElementById('chartRisco');
  if (ctxRisco) {
    const eg = master.estatisticas_gerais;
    new Chart(ctxRisco, {
      type: 'doughnut',
      data: {
        labels: ['Risco Alto (Atenção Máxima)', 'Risco Médio (Monitorar)', 'Risco Baixo (Estável)'],
        datasets: [{
          data: [eg.secoes_risco_alto, eg.secoes_risco_medio, eg.secoes_risco_baixo],
          backgroundColor: ['#ef4444', '#f59e0b', '#10b981'],
          borderWidth: 2,
          borderColor: '#141f36'
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'bottom', labels: { boxWidth: 12, padding: 15, font: { size: 11 } } }
        },
        cutout: '70%'
      }
    });
  }

  // -------------------------------------------------------------
  // 3. Gráfico Top Carga Eleitoral: Seções com Maior Eleitorado 2026
  // -------------------------------------------------------------
  const ctxCarga = document.getElementById('chartCarga');
  if (ctxCarga) {
    const topCarga = [...master.secoes].sort((a, b) => b.aptos_2026 - a.aptos_2026).slice(0, 10);
    new Chart(ctxCarga, {
      type: 'bar',
      data: {
        labels: topCarga.map(s => `Seção ${s.secao} (${s.bairro_povoado.replace('Povoado ', 'Pov. ')})`),
        datasets: [{
          label: 'Eleitores Aptos na Urna',
          data: topCarga.map(s => s.aptos_2026),
          backgroundColor: topCarga.map(s => s.tem_agregacao ? 'rgba(239, 68, 68, 0.85)' : 'rgba(56, 189, 248, 0.85)'),
          borderColor: topCarga.map(s => s.tem_agregacao ? '#ef4444' : '#38bdf8'),
          borderWidth: 1,
          borderRadius: 4
        }]
      },
      options: {
        indexAxis: 'y',
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: {
            callbacks: {
              afterLabel: function(ctx) {
                const s = topCarga[ctx.dataIndex];
                return `Local: ${s.nome_local}\nAgregação: ${s.secoes_agregadas}\nÁrea: ${s.area}`;
              }
            }
          }
        },
        scales: {
          x: { grid: { color: 'rgba(255, 255, 255, 0.05)' } }
        }
      }
    });
  }

  // -------------------------------------------------------------
  // 4. Gráfico Demografia: Faixa Etária
  // -------------------------------------------------------------
  const ctxIdade = document.getElementById('chartIdade');
  if (ctxIdade && demo.faixas_etarias) {
    new Chart(ctxIdade, {
      type: 'bar',
      data: {
        labels: demo.faixas_etarias.map(f => f.faixa),
        datasets: [{
          label: 'Eleitores (%)',
          data: demo.faixas_etarias.map(f => f.pct),
          backgroundColor: 'rgba(99, 102, 241, 0.8)',
          borderColor: '#818cf8',
          borderWidth: 1,
          borderRadius: 4
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: { legend: { display: false } },
        scales: {
          y: { ticks: { callback: v => v + '%' } }
        }
      }
    });
  }

  // -------------------------------------------------------------
  // 5. Gráfico Demografia: Escolaridade
  // -------------------------------------------------------------
  const ctxEscola = document.getElementById('chartEscola');
  if (ctxEscola && demo.escolaridade) {
    new Chart(ctxEscola, {
      type: 'doughnut',
      data: {
        labels: demo.escolaridade.map(e => e.grau),
        datasets: [{
          data: demo.escolaridade.map(e => e.pct),
          backgroundColor: [
            '#f59e0b', '#38bdf8', '#10b981', '#6366f1',
            '#ec4899', '#8b5cf6', '#14b8a6', '#94a3b8'
          ],
          borderWidth: 2,
          borderColor: '#141f36'
        }]
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { position: 'right', labels: { boxWidth: 10, font: { size: 10 } } }
        },
        cutout: '65%'
      }
    });
  }
};
