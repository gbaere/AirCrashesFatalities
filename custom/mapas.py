import pandas as pd
import plotly.express as px
import streamlit as st


def analise_acidentes_plotly(data_frame):
    data_frame['Date'] = pd.to_datetime(data_frame['Date'], format='%d/%m/%Y')
    data_frame['ANO'] = data_frame['Date'].dt.year
    data_frame['INVESTIGATION'] = data_frame["Investigation Type"].str.strip()

    grouped_data = data_frame.groupby(['ANO', 'INVESTIGATION'])['INVESTIGATION'].count().unstack(fill_value=0).reset_index()

    # Criando o gráfico com Plotly Express
    fig = px.line(grouped_data,
                  x='ANO',
                  y=grouped_data.columns[1:],  # Colunas que representam os tipos de investigação
                  title='Ocorrências',
                  labels={'value': 'QUANTIDADE'})

    fig.update_xaxes(
        dtick="M12",  # Intervalo de 12 meses (1 ano)
        tickformat="%b %Y"  # Formato: Mês Ano com quatro dígitos
    )

    st.plotly_chart(fig, use_container_width=True)


def analise_fatalidade_e_lesoes(data_frame):
    # Convertendo a coluna Date para o formato de data
    data_frame['Date'] = pd.to_datetime(data_frame['Date'], format='%d/%m/%Y')

    # Transformando a coluna Date em ano
    data_frame['Crash.Year'] = data_frame['Date'].dt.year

    # Agregar os novos dados de lesões e sem ferimentos
    grouped_data = data_frame.groupby('Crash.Year').agg(
        Mortos=('Fatalities', 'sum'),
        FerimentoGrave=('Total Serious Injuries', 'sum'),
        FerimentoLeve=('Total Minor Injuries', 'sum'),
        SemFerimentos=('Total Uninjured', 'sum')
    ).reset_index()

    # Criando o gráfico de barras empilhadas com Plotly Express
    fig = px.bar(grouped_data, x='Crash.Year', y=['Mortos', 'FerimentoGrave', 'FerimentoLeve', 'SemFerimentos'],
                 title='Fatalidades e Lesões',
                 labels={'Crash.Year': 'Ano', 'value': 'Número de Pessoas'},
                 color_discrete_map={
                     'Mortos': 'red',
                     'FerimentoGrave': 'orange',
                     'FerimentoLeve': 'yellow',
                     'SemFerimentos': 'green'
                 })

    # Atualizar as etiquetas de texto das barras
    fig.update_traces(texttemplate='%{y}', textposition='inside')  # Exibe os valores de y nas barras

    fig.update_layout(barmode='stack')  # Modo de empilhamento das barras
    st.plotly_chart(fig, use_container_width=True)


def analise_aeronaves(data_frame):
    # Convertendo a coluna Date para o formato de data
    data_frame['Date'] = pd.to_datetime(data_frame['Date'], format='%d/%m/%Y')
    # Transformando a coluna Date em ano
    data_frame['Crash.Year'] = data_frame['Date'].dt.year

    # Contando os tipos de Aircraft Category por ano
    grouped_data = data_frame.groupby(['Crash.Year', 'Aircraft Category'])['Aircraft Category'].count().unstack(fill_value=0).reset_index()

    # Reformatar o DataFrame para o formato apropriado para o gráfico de barras empilhadas
    stacked_data = pd.melt(grouped_data, id_vars='Crash.Year', value_vars=grouped_data.columns[1:], var_name='Aircraft Category', value_name='Count')

    fig = px.bar(stacked_data,
                 x='Crash.Year', y='Count', color='Aircraft Category',
                 title='Distribuição de tipos de aeronaves envolvidas no período',
                 labels={'Crash.Year': 'Ano', 'Count': 'Quantidade', 'Aircraft Category': 'Categoria de Aeronave'})

    fig.update_layout(barmode='stack')  # Barras empilhadas
    st.plotly_chart(fig, use_container_width=True)



def analise_fabricante_aeronaves(data_frame):
    # Convertendo a coluna Date para o formato de data
    data_frame['Date'] = pd.to_datetime(data_frame['Date'], format='%d/%m/%Y')
    # Transformando a coluna Date em ano
    data_frame['Crash.Year'] = data_frame['Date'].dt.year

    # Contando os tipos de Aircraft Category por ano
    grouped_data = data_frame.groupby(['Crash.Year', 'Make'])['Make'].count().unstack(fill_value=0).reset_index()

    # Reformatar o DataFrame para o formato apropriado para o gráfico de barras empilhadas
    stacked_data = pd.melt(grouped_data, id_vars='Crash.Year', value_vars=grouped_data.columns[1:], var_name='Make', value_name='Count')

    # Calcular as porcentagens
    total_per_year = stacked_data.groupby('Crash.Year')['Count'].transform('sum')
    stacked_data['Percentage'] = (stacked_data['Count'] / total_per_year) * 100

    fig = px.bar(stacked_data,
                 x='Crash.Year', y='Count', color='Make',
                 title='Distribuição de fabricantes das aeronaves envolvidas no período',
                 labels={'Crash.Year': 'Ano', 'Count': 'Quantidade', 'Make': 'Fabricante/Modelo'})

    fig.update_layout(barmode='stack')  # Barras empilhadas
    st.plotly_chart(fig, use_container_width=True)


def format_cell_value(x):
    count = x['Count']
    percentage = x['Percentage']
    return f"Count: {count} ({percentage:.2f}%)"

def analise_fabricante_aeronaves_detalhes_tabela(data_frame):
    # Convertendo a coluna Date para o formato de data
    data_frame['Date'] = pd.to_datetime(data_frame['Date'], format='%d/%m/%Y')
    # Transformando a coluna Date em ano
    data_frame['ANO'] = data_frame['Date'].dt.year

    data_frame['ANO'] = data_frame['ANO'].astype(str)

    # Contando os tipos de Aircraft Category por ano e fabricante
    grouped_data = data_frame.groupby(['ANO', 'Make'])['Make'].count().unstack(fill_value=0).reset_index()

    # Criando a matriz de ano x fabricante
    year_make_matrix = grouped_data.set_index('ANO')  # Usar 'Crash.Year' como índice

    # Criando um DataFrame para armazenar as porcentagens
    percentage_data = year_make_matrix.copy()
    years = year_make_matrix.columns

    # Adicionando a coluna total_acidentes_ano
    total_acidentes_ano = year_make_matrix.sum(axis=1)
    year_make_matrix['total_acidentes_ano'] = total_acidentes_ano

    # Calculando porcentagens
    for year in years:
        percentage_data[year] = (year_make_matrix[year] / year_make_matrix['total_acidentes_ano']) * 100

    # Criando um DataFrame para armazenar os resultados formatados
    formatted_table = percentage_data.copy()

    for year in years:
        formatted_table[year] = formatted_table.apply(
            lambda row: f"{int(year_make_matrix[year][row.name])} ({percentage_data[year][row.name]:.1f}%)",
            axis=1
        )

    formatted_table.columns = [str(col).split('.')[0] for col in formatted_table.columns]


    return st.dataframe(formatted_table.style.set_properties(**{'background-color': 'black',
                           'color': 'lawngreen',
                           'border-color': 'white'}).apply(highlight_max), use_container_width=True)


# Aplicando cores alternadas usando o método styler
def highlight_odd_rows(row):
    if row.name % 2 == 0:
        return ['background-color: blue'] * len(row)
    else:
        return ['background-color: black'] * len(row)

def highlight_max(s):
    is_max = s == s.max()
    return ['background-color: blue; color: white' if v else '' for v in is_max]









