import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Aircraft accident and fatality analysis application",
    page_icon="✈️",
    layout="wide"
)

# Carregar/processar/tratar o conjunto de dados
def load_and_process_data():
    dataset = pd.read_csv("datasets/air_crashes_fatalities_1948_at_2007.csv", sep=';', encoding='latin-1', index_col=0)
    return dataset

# Link para o GitHub
st.sidebar.markdown("[GitHub Repository](https://github.com/gbaere)")

if "data" not in st.session_state:

    st.session_state["data"] = load_and_process_data()


else:





