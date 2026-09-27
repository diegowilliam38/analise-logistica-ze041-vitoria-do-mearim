import os
import sys
import json
import math

sys.stdout.reconfigure(encoding='utf-8')

project_root = r'C:\Users\Diego William\OneDrive\Área de Trabalho\AIOS-WORKSPACE\projects\analise-logistica-ze041-vitoria-do-mearim'
data_dir = os.path.join(project_root, 'data')

# Coordenadas do Cartório Eleitoral da 41ª ZE (Ponto Zero de Saída e Retorno)
CARTORIO_GEO = {
    "nome": "Cartório Eleitoral da 41ª Zona (Vitória do Mearim / MA)",
    "endereco": "Travessa Antônio Filho da Costa, nº 12 – Bairro Campinas, Vitória do Mearim – MA",
    "lat": -3.46105,
    "lon": -44.87052
}

# Coordenadas Georreferenciadas dos 32 Locais de Votação
LOCAIS_GEO = {
    # Urbanos
    1015: {"lat": -3.46248, "lon": -44.86905, "maps_query": "IEMA Vitoria do Mearim MA"},
    1023: {"lat": -3.46320, "lon": -44.86850, "maps_query": "Colegio Municipal Ana Bogea Vitoria do Mearim MA"},
    1040: {"lat": -3.46180, "lon": -44.87120, "maps_query": "CEMA Carlos Raimundo Figueiredo Vitoria do Mearim MA"},
    1058: {"lat": -3.45600, "lon": -44.86450, "maps_query": "Escola Antonia Farias Puraqueu Vitoria do Mearim MA"},
    1066: {"lat": -3.45720, "lon": -44.86580, "maps_query": "Jardim de Infancia Mons Artur Goncalves Puraqueu Vitoria do Mearim MA"},
    1074: {"lat": -3.46450, "lon": -44.87350, "maps_query": "Centro Educacional Conego Eliud Manijituba Vitoria do Mearim MA"},
    1473: {"lat": -3.46800, "lon": -44.86200, "maps_query": "Unidade Escolar Neuza da Cunha Costa Itapui Tapera Vitoria do Mearim MA"},
    1481: {"lat": -3.45520, "lon": -44.86380, "maps_query": "Unidade Escolar Dr Ribamar de Matos Puraqueu Vitoria do Mearim MA"},
    1490: {"lat": -3.46550, "lon": -44.87480, "maps_query": "Escola Maria Celeste Barros Manijituba Vitoria do Mearim MA"},
    1627: {"lat": -3.47100, "lon": -44.86600, "maps_query": "Unidade Escolar Maria Graciana Pinto Costa Vila Regina Vitoria do Mearim MA"},

    # Rurais
    1104: {"lat": -3.49800, "lon": -44.84500, "maps_query": "Escola Francisco Xavier Correia Povoado Jaguary Vitoria do Mearim MA"},
    1112: {"lat": -3.41500, "lon": -44.81000, "maps_query": "Escola Deodato Santos Povoado Sao Lourenco Vitoria do Mearim MA"},
    1120: {"lat": -3.42500, "lon": -44.91200, "maps_query": "Escola Nasser Assad Povoado Coque BR-222 Vitoria do Mearim MA"},
    1287: {"lat": -3.38500, "lon": -44.78500, "maps_query": "Colegio Godofredo Maciel Povoado Sao Felix Vitoria do Mearim MA"},
    1309: {"lat": -3.37200, "lon": -44.76000, "maps_query": "Colegio Jose Ribamar Silva Povoado Santa Rosa Vitoria do Mearim MA"},
    1317: {"lat": -3.34500, "lon": -44.74000, "maps_query": "Escola Izidoro de Jesus Lopes Povoado Livramento Vitoria do Mearim MA"},
    1325: {"lat": -3.36000, "lon": -44.75000, "maps_query": "Colegio Jose Carlos Mota Silva Povoado Sumauma do Japao Vitoria do Mearim MA"},
    1341: {"lat": -3.33000, "lon": -44.72000, "maps_query": "Escola Paulo Maciel Neto Povoado Sao Benedito Vitoria do Mearim MA"},
    1368: {"lat": -3.42100, "lon": -44.91800, "maps_query": "Escola Itelvino de Matos Povoado Coque BR-222 Vitoria do Mearim MA"},
    1392: {"lat": -3.56000, "lon": -44.96000, "maps_query": "Escola Municipal de Jucaral Vitoria do Mearim MA"},
    1422: {"lat": -3.48500, "lon": -44.85500, "maps_query": "Escola Mamedio da Silva Sarmento Povoado Jacaray MA-014 Vitoria do Mearim MA"},
    1457: {"lat": -3.53500, "lon": -44.94500, "maps_query": "Colegio Euzebio do Nascimento Povoado Jucaralzinho Vitoria do Mearim MA"},
    1465: {"lat": -3.52000, "lon": -44.92000, "maps_query": "Colegio Municipal Vila Nova Povoado Vila Nova Vitoria do Mearim MA"},
    1503: {"lat": -3.47500, "lon": -44.82000, "maps_query": "Colegio Hemeterio Fernandes Povoado Mato Grosso Vitoria do Mearim MA"},
    1511: {"lat": -3.54000, "lon": -44.93500, "maps_query": "Escola Abidao Rufino da Silva Povoado Boca do Campo Vitoria do Mearim MA"},
    1554: {"lat": -3.42300, "lon": -44.91400, "maps_query": "Creche Comunitaria de Coque Povoado Coque Vitoria do Mearim MA"},
    1562: {"lat": -3.42700, "lon": -44.91600, "maps_query": "Escola Vila Falcao Povoado Coque Vitoria do Mearim MA"},
    1570: {"lat": -3.42900, "lon": -44.92000, "maps_query": "Escola Raimundo Bogea Povoado Coque Vitoria do Mearim MA"},
    1589: {"lat": -3.41800, "lon": -44.81500, "maps_query": "Escola Franklin Cantanhede Povoado Sao Lourenco Vitoria do Mearim MA"},
    1619: {"lat": -3.58500, "lon": -44.98000, "maps_query": "Escola Municipal de Ipixuna Povoado Ipixuna Vitoria do Mearim MA"},
    1635: {"lat": -3.50500, "lon": -44.89500, "maps_query": "Escola Municipal de Tirirical Povoado Tirirical Vitoria do Mearim MA"},
    1660: {"lat": -3.60500, "lon": -44.99500, "maps_query": "Escola Mauricia Fernandes Jardim Povoado Escondido Vitoria do Mearim MA"}
}

def haversine_km(lat1, lon1, lat2, lon2):
    R = 6371.0 # Raio da Terra em km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return round(R * c, 2)

# Carregar intelligence
with open(os.path.join(data_dir, 'ze041_inteligencia_consolidada.json'), 'r', encoding='utf-8') as f:
    master = json.load(f)

# Atualizar cada local
for loc in master['locais']:
    nl = loc['num_local']
    geo = LOCAIS_GEO.get(nl, {"lat": -3.4610, "lon": -44.8705, "maps_query": loc['nome']})
    
    dist_reta = haversine_km(CARTORIO_GEO['lat'], CARTORIO_GEO['lon'], geo['lat'], geo['lon'])
    # Estimativa de trajeto rodoviário real (~1.3x a 1.4x a distância em linha reta)
    dist_est_rodoviaria = round(max(0.5, dist_reta * (1.35 if loc['area'] == 'RURAL' else 1.2)), 1)
    
    # URL de Rota no Google Maps
    google_maps_route_url = f"https://www.google.com/maps/dir/?api=1&origin={CARTORIO_GEO['lat']},{CARTORIO_GEO['lon']}&destination={geo['lat']},{geo['lon']}&travelmode=driving"
    google_maps_view_url = f"https://www.google.com/maps/search/?api=1&query={geo['lat']},{geo['lon']}"
    
    loc['geo'] = {
        "lat": geo['lat'],
        "lon": geo['lon'],
        "distancia_reta_km": dist_reta,
        "distancia_rodoviaria_est_km": dist_est_rodoviaria,
        "google_maps_route_url": google_maps_route_url,
        "google_maps_view_url": google_maps_view_url
    }

# Atualizar cada seção com a geo do seu local
for s in master['secoes']:
    nl = s['num_local']
    loc_ref = next((l for l in master['locais'] if l['num_local'] == nl), None)
    if loc_ref and 'geo' in loc_ref:
        s['geo'] = loc_ref['geo']

# Salvar master atualizada
with open(os.path.join(data_dir, 'ze041_inteligencia_consolidada.json'), 'w', encoding='utf-8') as f:
    json.dump(master, f, ensure_ascii=False, indent=2)

print("Dados georreferenciados injetados com sucesso em ze041_inteligencia_consolidada.json!")

# Atualizar também rotas_logistica_2026.json
with open(os.path.join(data_dir, 'rotas_logistica_2026.json'), 'r', encoding='utf-8') as f:
    rotas = json.load(f)

rotas['cartorio_geo'] = CARTORIO_GEO

with open(os.path.join(data_dir, 'rotas_logistica_2026.json'), 'w', encoding='utf-8') as f:
    json.dump(rotas, f, ensure_ascii=False, indent=2)

print("rotas_logistica_2026.json enriquecido com Cartório GEO!")
