import folium
from folium import plugins
from streamlit_folium import folium_static


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

