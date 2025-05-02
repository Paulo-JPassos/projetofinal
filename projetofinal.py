# Importação das bibliotecas necessárias
#venv\Scripts\activate.bat                                                                                                                                 
#venv\Scripts\activate.bat (cmd)
#python -m pip install plotly  python3 -m pip install plotly  

import streamlit as st
import pandas as pd
import plotly.express as px
import datetime as dt

# Título do dashboard
st.title("Acesso a saúde no Brasil")

# Caminho do arquivo CSV na mesma pasta
csv_file = "cnes_estabelecimentos2.csv"


df = pd.read_csv("cnes_estabelecimentos2.csv", sep=";", encoding="latin1", low_memory=False)


st.markdown("### Até aqui importamos as bibliotecas e subimos o arquivo CSV e verificamos se ele existe no projeto")

     # Exibe os dados carregados
st.markdown("### Dados de Vendas Carregados")
st.dataframe(df.head(10))

# Seleção de colunas principais
colunas_utilizadas = [
    "CNES", "NO_FANTASIA", "TP_UNIDADE", "DS_TIPO_UNIDADE", "CO_MUNICIPIO_GESTOR", 
    "NO_MUNICIPIO", "CO_UF", "NO_UF", "TP_ESTABELECIMENTO", "DS_TP_ESTABELECIMENTO",
    "TP_GESTAO", "DS_TP_GESTAO", "CO_CATEGORIA_UNIDADE", "DS_CATEGORIA_UNIDADE"
]

df = df[[col for col in colunas_utilizadas if col in df.columns]]

# Filtro por estado
ufs = df["CO_UF"].dropna().unique()
estado = st.selectbox("Selecione um estado para análise", sorted(ufs))

df_estado = df[df["CO_UF"] == estado]

# Criação de dicionário de UFs
ufs = {
    12: 'AC', 27: 'AL', 13: 'AM', 16: 'AP', 29: 'BA', 23: 'CE',
    53: 'DF', 32: 'ES', 52: 'GO', 21: 'MA', 31: 'MG', 50: 'MS',
    51: 'MT', 15: 'PA', 25: 'PB', 26: 'PE', 22: 'PI', 41: 'PR',
    33: 'RJ', 24: 'RN', 43: 'RS', 11: 'RO', 14: 'RR', 42: 'SC',
    28: 'SE', 35: 'SP', 17: 'TO'
}

df['UF'] = df['CO_UF'].map(ufs)

# Título da seção
st.header("Distribuição das Unidades por Estado")

# 1. Gráfico de barras - Contagem de unidades por estado
contagem_estados = df['UF'].value_counts().sort_index()
fig1 = px.bar(x=contagem_estados.index, y=contagem_estados.values,
              labels={'x': 'UF', 'y': 'Quantidade de Unidades'},
              title='Quantidade de Unidades por Estado')
st.plotly_chart(fig1)

# 2. Gráfico de pizza - Proporção de unidades por estado
fig2 = px.pie(values=contagem_estados.values, names=contagem_estados.index,
              title='Proporção de Unidades por Estado')
st.plotly_chart(fig2)


# 3. Gráfico de dispersão - Quantidade de unidades por estado
fig3 = px.scatter(x=contagem_estados.index, y=contagem_estados.values,
                  labels={'x': 'UF', 'y': 'Quantidade de Unidades'},
                  title='Distribuição de Unidades por Estado')
st.plotly_chart(fig3)
