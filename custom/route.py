import folium
import plotly.graph_objs as go
import streamlit as st
import requests
from urllib.parse import quote
from folium import plugins
from streamlit_folium import folium_static

def format_location(location):
    return quote(location)

def get_coordinates(location):
    url = f"https://nominatim.openstreetmap.org/search?q={format_location(location)}&format=json"
    response = requests.get(url)
    data = response.json()

    if data:
        latitude = float(data[0]['lat'])
        longitude = float(data[0]['lon'])
        return latitude, longitude
    else:
        return None, None

def desenha_rota(data_frame):
    data_frame['Airport Name'] = data_frame['Airport Name'].str.strip()
    # Filtrar linhas com "Airport Name" igual a "Unknown"
    data_frame = data_frame[(data_frame['Airport Name'] != 'Unknown') & (data_frame['Airport Name'] != 'N/A')]
    # Adicionar colunas de Latitude e Longitude ao DataFrame
    data_frame['Latitude'] = data_frame['Airport Name'].apply(lambda name: get_coordinates(name)[0])
    data_frame['Longitude'] = data_frame['Airport Name'].apply(lambda name: get_coordinates(name)[1])

    # Criar uma figura de mapa Plotly
    fig = go.Figure()

    # Loop para adicionar marcadores e linhas para cada rota
    i = 0
    while i + 1 < len(data_frame):
        origin = data_frame.iloc[i]
        destination = data_frame.iloc[i + 1]

        fig.add_trace(go.Scattergeo(
            locationmode='USA-states',
            lon=[origin['Longitude'], destination['Longitude']],
            lat=[origin['Latitude'], destination['Latitude']],
            text=[origin['Airport Name'], destination['Airport Name']],
            mode='markers+lines',
            marker=dict(size=10, symbol='circle', color='blue'),
            line=dict(width=2, color='red'),
            name='Route {}'.format(i // 2 + 1)
        ))

        i += 2

    # Configurações de layout
    fig.update_layout(
        geo=dict(
            scope='world',
            showland=True,
        ),
        showlegend=True,
        legend_title_text='Legend',
        title='Flight Route Map',
    )

    # Exibir o mapa
    st.plotly_chart(fig, use_container_width=True)


def mostra_local(data_frame):

    data_frame.drop(data_frame[data_frame['Latitude'].astype(float) == 0].index, inplace=True)
    data_frame.drop(data_frame[data_frame['Longitude'].astype(float) == 0].index, inplace=True)

    # Corrigir formato das coordenadas
    data_frame['Latitude'] = data_frame['Latitude'].astype(float)
    data_frame['Longitude'] = data_frame['Longitude'].astype(float)

    mapa_ocorrencia = folium.Map([data_frame["Latitude"].mean(), data_frame["Longitude"].mean()],
                                 zoom_start=5, width="%100",
                                 height="%100")
    locations = list(zip(data_frame["Latitude"], data_frame["Longitude"]))

    popup_info = data_frame["Investigation Type"] + '<br>' + data_frame["Make"] + '<br>' + data_frame["Aircraft Category"] + '<br>' + data_frame["Country"]

    cluster = plugins.MarkerCluster(locations=locations,
                                    popups=popup_info.tolist())
    mapa_ocorrencia.add_child(cluster)
    folium_static(mapa_ocorrencia, height=300, width=1000)

