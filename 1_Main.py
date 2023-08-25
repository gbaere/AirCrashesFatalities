import matplotlib.pyplot as plt
import pandas as pd
import requests
import seaborn as sns
import statsmodels.api as sm
import streamlit as st
import plotly.express as px


st.set_page_config(
    page_title="Aircraft accident and fatality analysis application",
    page_icon="✈️",
    layout="wide"
)


# Carregar/processar/tratar o conjunto de dados
def load_and_process_data():
    data = pd.read_csv("dataset/air_crashes_fatalities_1948_at_2007_cleaned_.csv", sep=';', encoding='latin-1', index_col=0)
    return data


def analise_acidentes_plotly(data_frame):
    # Convertendo a coluna Date para o formato de data
    data_frame['Date'] = pd.to_datetime(data_frame['Date'], format='%d/%m/%Y')

    # Transformando a coluna Date em ano
    data_frame['Crash.Year'] = data_frame['Date'].dt.year

    # Restante do código da função analise_acidentes
    grouped_data = data_frame.groupby('Crash.Year').agg(No_Of_Crashes=('Date', 'count'), No_Fatalities=('Fatalities', 'sum')).reset_index()

    # Criando o gráfico com Plotly Express
    fig = px.line(grouped_data, x='Crash.Year', y='No_Of_Crashes', title='Número de acidêntes ao longo do tempo',
                  labels={'Crash.Year': 'Ano', 'No_Of_Crashes': 'Numero de acidêntes'})

    # Adicionando a suavização (média)
    smoothed_data = grouped_data.rolling(window=5).mean()  # Janela de 5 anos para suavização
    fig.add_scatter(x=smoothed_data['Crash.Year'], y=smoothed_data['No_Of_Crashes'], mode='lines', name='Média suavizada',
                    line=dict(color='red'))

    fig.update_layout(height=500, width=1000)

    # Exibir o gráfico no Streamlit
    st.plotly_chart(fig)



# Função para formatar a localização para a URL da API do Mapbox
def format_location(location):
    if isinstance(location, str):
        formatted_name = location.replace(",", "")  # Remover vírgulas
        formatted_name = formatted_name.replace(" ", "%20")  # Substituir espaços por %20
        return formatted_name
    else:
        return ""


# Função para obter as coordenadas de uma cidade usando o Mapbox Geocoding API
def get_coordinates(location):
    if isinstance(location, str):
        url = f"https://nominatim.openstreetmap.org/search?q={format_location(location)}&format=json"
        st.write(url)
        response = requests.get(url)
        data = response.json()

        if data:
            latitude = float(data[0]['lat'])
            longitude = float(data[0]['lon'])
            return latitude, longitude
        else:
            return None, None
    else:
        return None, None


def transform_int(value):
    return int(value)


if "data" not in st.session_state:
    st.session_state["data"] = load_and_process_data()
else:
    dataset = st.session_state["data"]

    # Removendo as localidades vazias
    dataset = dataset.dropna(subset=['Location'])
    # só para garantir
    dataset = dataset[dataset['Location'].notna()]

    # Adicionar colunas de latitude e longitude ao DataFrame, pois o arquivo csv não possui essas informações
    #dataset["Latitude"], dataset["Longitude"] = zip(*dataset["Location"].apply(get_coordinates))

    # Filtrar cidades com coordenadas válidas
    #dataset = dataset.dropna(subset=["Latitude", "Longitude"])

    # Removendo as linhas com Fatalities igual a 0
    dataset = dataset[dataset['Fatalities'] != 0]

    # Criar um arquivo CSV a partir do DataFrame
    #dataset.to_csv('dataset/air_crashes_fatalities_1948_at_2007_clean.csv', index=False)

    # Extraindo o ano
    years = pd.DatetimeIndex(dataset['Date']).year
    min_year = years.min()
    max_year = years.max()
    years_values = range(min_year, max_year + 1)
    # Sidebar filtro periodo
    year_filter = st.sidebar.select_slider('Escolha o periodo:', options=years_values, value=(min_year, max_year))

    # Sidebar filtro vitimas
    min_fatalities = dataset.Fatalities.min()
    max_fatalities = dataset.Fatalities.max()
    fatalities_values = range(min_fatalities, max_fatalities + 1)
    fatalities_filter = st.sidebar.select_slider('Vitímas:', options=fatalities_values,
                                                 value=(min_fatalities, max_fatalities))


    dataset_filtered = dataset[(pd.DatetimeIndex(dataset['Date']).year >= year_filter[0]) &
                               (pd.DatetimeIndex(dataset['Date']).year <= year_filter[1]) &
                               (dataset['Fatalities'] >= fatalities_filter[0]) &
                               (dataset['Fatalities'] <= fatalities_filter[1])]

    st.write(dataset_filtered)

    # Exibir o gráfico
    analise_acidentes_plotly(dataset_filtered)



# Link para o GitHub
st.sidebar.markdown("[GitHub Repository](https://github.com/gbaere)")
