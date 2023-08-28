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
        progress_bar = st.progress(0)
        for i in range(101):
            time.sleep(0.1)  # Simula um processo demorado
            st.session_state.data = custom.load_and_process_data()
            progress_bar.progress(i)


if __name__ == "__main__":
    main()

    if "data" in st.session_state:
        #if "dataset" not in locals():
        dataset, dataset_filtered = st.session_state.data, st.session_state.data

        # Extraindo o ano
        years = dataset['Date'].apply(lambda x: pd.to_datetime(x, format='%d/%m/%Y', dayfirst=True).year)
        min_year = years.min()
        max_year = years.max()
        years_values = range(min_year, max_year + 1)
        # Sidebar filtro periodo
        year_filter = st.sidebar.select_slider('Período:', options=years_values, value=(min_year, max_year))

        # Sidebar filtro vitimas fatais
        min_fatalities = dataset.Fatalities.min()
        max_fatalities = dataset.Fatalities.max()
        fatalities_values = range(min_fatalities, max_fatalities + 1)
        fatalities_filter = st.sidebar.select_slider('Mortes:', options=fatalities_values,
                                                     value=(min_fatalities, max_fatalities))

        # Obter a lista de tipos de investigação únicos
        unique_investigation_types = dataset["Investigation Type"].str.strip().unique()
        default_investigation = unique_investigation_types[0]
        investigation_filter = st.sidebar.multiselect("Ocorrência:", unique_investigation_types,
                                                      default=default_investigation)

        # Sidebar filtro localidade
        unique_country_types = sorted(dataset["Country"].str.strip().dropna().unique())
        default_country = unique_country_types[0]
        country_filter = st.sidebar.selectbox(label="Localidade:",
                                              options=unique_country_types,
                                              index=unique_country_types.index(default_country))

        # Sidebar filtro tipo de aeronaves
        aircrafts = sorted(dataset["Aircraft Category"].str.strip().unique())
        default_country = unique_investigation_types[0]
        # Filtrar valores vazios ou nulos e criar a lista de opções finais
        unique_aircraft_types = [value for value in aircrafts if pd.notna(value) and value != '']
        default_aircraft = unique_aircraft_types[0]
        aircraft_filter = st.sidebar.multiselect("Tipo de Aeronave:", unique_aircraft_types, default=default_aircraft)


        dataset_filtered = dataset_filtered[(dataset_filtered["Date"].dt.year >= year_filter[0]) &
                                            (dataset_filtered["Date"].dt.year <= year_filter[1])]

        dataset_filtered = dataset_filtered[(dataset_filtered["Fatalities"] >= fatalities_filter[0]) &
                                            (dataset_filtered["Fatalities"] <= fatalities_filter[1])]


        if country_filter:
            dataset_filtered = dataset_filtered[dataset_filtered["Country"].str.strip() == country_filter]

        if investigation_filter:
            dataset_filtered = dataset_filtered[dataset_filtered["Investigation Type"].str.strip().isin(investigation_filter)]

        if aircraft_filter:
            dataset_filtered = dataset_filtered[dataset_filtered["Aircraft Category"].str.strip().isin(aircraft_filter)]

        st.write("Tabela:", dataset_filtered)

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
        st.sidebar.markdown(f"Visitantes: {st.session_state.visit_count}")
