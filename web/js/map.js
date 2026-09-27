// ==========================================================================
// MAPA GEOESPACIAL INTERATIVO (LEAFLET + GOOGLE MAPS INTEGRATION)
// 41ª ZONA ELEITORAL — VITÓRIA DO MEARIM / MA
// ==========================================================================

window.initGeoMap = function(data) {
  const master = data.master;
  const logistica = data.logistica;
  const cartorio = logistica.cartorio_geo || { lat: -3.46105, lon: -44.87052, nome: "Cartório Eleitoral 41ª ZE" };

  const mapEl = document.getElementById('mapContainer');
  if (!mapEl) return;

  // Evitar reinicialização duplicada
  if (window._leafMap) {
    window._leafMap.remove();
  }

  // Inicializar Leaflet centrado em Vitória do Mearim
  const map = L.map('mapContainer', {
    center: [-3.475, -44.870],
    zoom: 11,
    zoomControl: true
  });
  window._leafMap = map;

  // Layer Dark do CartoDB (Visual de Centro de Comando)
  L.tileLayer('https://{s}.basemaps.cartocdn.com/rastertiles/voyager/{z}/{x}/{y}{r}.png', {
    attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> &copy; <a href="https://carto.com/attributions">CARTO</a>',
    subdomains: 'abcd',
    maxZoom: 19
  }).addTo(map);

  // 1. Marcador do Cartório Eleitoral (Ponto Zero)
  const cartorioIcon = L.divIcon({
    className: 'custom-cartorio-marker',
    html: `
      <div style="
        background: linear-gradient(135deg, #f59e0b, #b45309);
        width: 32px; height: 32px; border-radius: 50%;
        display: flex; align-items: center; justify-content: center;
        border: 2px solid #fff; box-shadow: 0 0 15px rgba(245, 158, 11, 0.8);
        color: #fff; font-size: 16px; font-weight: bold;
      ">⚖️</div>
    `,
    iconSize: [32, 32],
    iconAnchor: [16, 16]
  });

  const cartorioMarker = L.marker([cartorio.lat, cartorio.lon], { icon: cartorioIcon }).addTo(map);
  cartorioMarker.bindPopup(`
    <div class="popup-content">
      <div class="popup-title" style="color: var(--gold);">🏛️ Cartório da 41ª Zona Eleitoral</div>
      <div class="popup-meta">
        <strong>Sede Central da Junta Apuradora</strong><br>
        Travessa Antônio Filho da Costa, nº 12 – Bairro Campinas<br>
        <em>Ponto de partida das Vans e ponto de chegada dos 31 Mototáxis</em>
      </div>
      <a href="https://www.google.com/maps/search/?api=1&query=${cartorio.lat},${cartorio.lon}" target="_blank" class="btn-gmaps">
        📍 Ver no Google Maps
      </a>
    </div>
  `);

  // 2. Plotar os 32 Locais de Votação
  master.locais.forEach(loc => {
    if (!loc.geo) return;

    const isUrbano = (loc.area === 'URBANA');
    const isCritico = (loc.tem_votos_pos17 || loc.max_score_risco >= 50 || loc.num_local === 1392);

    let markerColor = isUrbano ? '#0284c7' : '#f97316';
    if (isCritico) markerColor = '#ef4444';

    const localIcon = L.divIcon({
      className: 'custom-local-marker',
      html: `
        <div style="
          background: ${markerColor};
          width: ${isCritico ? '24px' : '20px'};
          height: ${isCritico ? '24px' : '20px'};
          border-radius: 50%;
          border: 2px solid #fff;
          box-shadow: 0 0 ${isCritico ? '12px #ef4444' : '8px rgba(0,0,0,0.5)'};
          display: flex; align-items: center; justify-content: center;
          color: #fff; font-size: 10px; font-weight: bold;
        ">
          ${loc.num_local % 100}
        </div>
      `,
      iconSize: [24, 24],
      iconAnchor: [12, 12]
    });

    const marker = L.marker([loc.geo.lat, loc.geo.lon], { icon: localIcon }).addTo(map);

    // Traçar linha sutil conectando o Cartório ao Local
    const polyline = L.polyline([
      [cartorio.lat, cartorio.lon],
      [loc.geo.lat, loc.geo.lon]
    ], {
      color: isUrbano ? '#38bdf8' : (isCritico ? '#ef4444' : '#f97316'),
      weight: 1.5,
      opacity: 0.35,
      dashArray: '4, 6'
    }).addTo(map);

    // Popup Rico
    const popupHtml = `
      <div class="popup-content">
        <div class="popup-title">${loc.nome} (Cód. ${loc.num_local})</div>
        <div class="popup-meta">
          <strong>Referência:</strong> ${loc.bairro_povoado}<br>
          <strong>Endereço:</strong> ${loc.endereco}<br>
          <strong>Área:</strong> ${loc.area} &bull; <strong>Aptos:</strong> ${loc.total_aptos_2026.toLocaleString('pt-BR')}<br>
          <strong>Seções:</strong> ${loc.secoes.join(', ')} (${loc.total_secoes} mesas)<br>
          <hr style="border: 0; border-top: 1px solid rgba(255,255,255,0.08); margin: 6px 0;">
          📏 <strong>Distância Reta:</strong> ${loc.geo.distancia_reta_km} km<br>
          🚗 <strong>Distância Estimada Estrada:</strong> ~${loc.geo.distancia_rodoviaria_est_km} km<br>
          🏍️ <strong>Tempo Estimado Mototáxi:</strong> ${loc.geo.distancia_rodoviaria_est_km <= 3 ? '2 a 7 min' : Math.round(loc.geo.distancia_rodoviaria_est_km * 1.1) + ' min'}
        </div>
        <a href="${loc.geo.google_maps_route_url}" target="_blank" class="btn-gmaps">
          🗺️ Traçar Rota no Google Maps
        </a>
      </div>
    `;

    marker.bindPopup(popupHtml);
  });

  // Renderizar Tabela Comparativa de Distâncias
  renderComparativoDistancias(master.locais, logistica.rotas_mototaxis);
};

function renderComparativoDistancias(locais, rotasMotos) {
  const tbody = document.getElementById('distanciasTableBody');
  if (!tbody) return;

  tbody.innerHTML = locais.map(loc => {
    // Buscar rota moto correspondente por num_local
    const moto = rotasMotos.find(m => m.num_local === loc.num_local);
    
    let kmOficialTre = '--';
    let tempoOficial = '--';
    
    if (loc.num_local === 1392) {
      kmOficialTre = 'Suprimento Fundos';
      tempoOficial = 'Recolhe c/ Urna';
    } else if (moto) {
      kmOficialTre = `${moto.km_total} km`;
      tempoOficial = moto.tempo_estimado;
    } else {
      kmOficialTre = (loc.area === 'URBANA' ? '1,5 a 2,5 km' : '20 a 45 km');
      tempoOficial = (loc.area === 'URBANA' ? '00:05' : '00:35');
    }

    return `
      <tr>
        <td style="font-family: var(--font-mono); font-weight: 700;">${loc.num_local}</td>
        <td>
          <div style="font-weight: 600; color: #fff;">${loc.nome}</div>
          <div style="font-size: 0.75rem; color: var(--text-muted);">${loc.bairro_povoado} &bull; ${loc.endereco}</div>
        </td>
        <td><span class="badge ${loc.area === 'URBANA' ? 'badge-info' : 'badge-neutral'}">${loc.area}</span></td>
        <td style="font-family: var(--font-mono); color: var(--gold); font-weight: 600;" title="Quilometragem oficial com margem de segurança do roteiro de transporte">${kmOficialTre}</td>
        <td style="font-family: var(--font-mono); font-weight: 700; color: var(--blue-accent);">~${loc.geo ? loc.geo.distancia_rodoviaria_est_km : '--'} km</td>
        <td style="font-family: var(--font-mono); font-weight: 700; color: var(--status-success);">${tempoOficial}</td>
        <td>
          ${loc.geo ? `<a href="${loc.geo.google_maps_route_url}" target="_blank" class="badge badge-info" style="text-decoration: none; padding: 0.35rem 0.65rem; display: inline-flex; align-items: center; gap: 4px;">📍 Rota Maps</a>` : '--'}
        </td>
      </tr>
    `;
  }).join('');
}
