import time
import pandas as pd
import streamlit as st
import custom.functions as custom
import custom.mapas as custom_mapas

st.set_page_config(
    page_title="Air accident investigation data analysis application",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)


def main():

    if "data" not in st.session_state:
        # Exibe a barra de progresso
        progress_bar = st.progress(0)

        # Simulando carregamento demorado
        for i in range(101):
            time.sleep(0.1)  # Simula um processo demorado
            progress_bar.progress(i)


if __name__ == "__main__":
    main()

    if "data" not in st.session_state:
        st.session_state.data = custom.load_and_process_data()
    else:
        dataset = st.session_state.data

        # Extraindo o ano
        years = dataset['Date'].apply(lambda x: pd.to_datetime(x, format='%d/%m/%Y', dayfirst=True).year)
        min_year = years.min()
        max_year = years.max()
        years_values = range(min_year, max_year + 1)
        # Sidebar filtro periodo
        year_filter = st.sidebar.select_slider('Escolha o periodo:', options=years_values, value=(min_year, max_year))

        # Sidebar filtro vitimas fatais
        min_fatalities = dataset.Fatalities.min()
        max_fatalities = dataset.Fatalities.max()
        fatalities_values = range(min_fatalities, max_fatalities + 1)
        fatalities_filter = st.sidebar.select_slider('Vitímas Fatais:', options=fatalities_values,
                                                     value=(min_fatalities, max_fatalities))

        # Obter a lista de tipos de investigação únicos
        unique_investigation_types = dataset["Investigation Type"].unique()
        default_investigation = unique_investigation_types[0]
        investigation_filter = st.sidebar.multiselect("Tipo de Ocorrência:", unique_investigation_types,
                                                      default=default_investigation)

        # Sidebar filtro localidade
        unique_country_types = sorted(dataset["Country"].dropna().unique())
        default_country = unique_country_types[0]
        country_filter = st.sidebar.selectbox(label="Escolha um local:",
                                              options=unique_country_types,
                                              index=unique_country_types.index(default_country))

        # Sidebar filtro tipo de aeronaves
        aircrafts = sorted(dataset["Aircraft Category"].unique())
        default_country = unique_investigation_types[0]
        # Filtrar valores vazios ou nulos e criar a lista de opções finais
        unique_aircraft_types = [value for value in aircrafts if pd.notna(value) and value != '']
        default_aircraft = unique_aircraft_types[0]
        aircraft_filter = st.sidebar.multiselect("Tipo de Aeronave:", unique_aircraft_types, default=default_aircraft)

        # Validandos os dados antes de filtrar

        if country_filter:
            country_condition = dataset["Country"] == country_filter
        else:
            country_condition = True  # Sem filtro de localidade

        if investigation_filter:
            investigation_condition = dataset["Investigation Type"].isin(investigation_filter)
        else:
            investigation_condition = True  # Sem filtro de investigação

        if aircraft_filter:
            aircraft_condition = dataset["Aircraft Category"].isin(aircraft_filter)
        else:
            aircraft_condition = True  # Sem filtro de categoria de aeronaves

        # Aplicando todas as condições de filtro
        year_condition = ((pd.DatetimeIndex(dataset['Date']).year >= year_filter[0]) &
                          (pd.DatetimeIndex(dataset['Date']).year <= year_filter[1]))

        fatalities_condition = ((dataset['Fatalities'] >= fatalities_filter[0]) &
                                (dataset['Fatalities'] <= fatalities_filter[1]))

        final_condition = year_condition & fatalities_condition & investigation_condition & aircraft_condition & country_condition

        if final_condition.any():
            dataset_filtered = dataset[final_condition]
        else:
            dataset_filtered = dataset.copy()

        st.write(dataset_filtered)

        if not dataset_filtered.empty:
            # Filtrar as linhas com Latitude e Longitude diferentes de 0, não vazias e não NaN
            dataset_filtered = dataset_filtered[
                ~(
                        (dataset_filtered['Latitude'] == "00.0") |
                        (dataset_filtered['Longitude'] == "00.0") |
                        dataset_filtered['Latitude'].isna() |
                        dataset_filtered['Longitude'].isna()
                )
            ]

        # Exibir o gráfico
        custom_mapas.analise_acidentes_plotly(dataset_filtered)

        custom_mapas.analise_fatalidade_e_lesoes(dataset_filtered)

        custom_mapas.analise_aeronaves(dataset_filtered)

        tab1, tab2 = st.tabs(["Fabricantes", "Detalhes"])

        with tab1:
            custom_mapas.analise_fabricante_aeronaves(dataset_filtered)
        with tab2:
            custom_mapas.analise_fabricante_aeronaves_detalhes_tabela(dataset_filtered)

        # Link para o GitHub
        st.sidebar.markdown("[GitHub Repository](https://github.com/gbaere)")