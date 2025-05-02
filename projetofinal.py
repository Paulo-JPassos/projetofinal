# Importação das bibliotecas necessárias
#venv\Scripts\activate.bat                                                                                                                                 
#venv\Scripts\activate.bat (cmd)
#python -m pip install plotly  python3 -m pip install plotly  

import streamlit as st
import pandas as pd
import plotly.express as px
import os
import datetime as dt

# Título do dashboard
st.title("Acesso a saúde no Brasil")

# Caminho do arquivo CSV na mesma pasta
csv_file = "cnes_estabelecimentos.csv"


df = pd.read_csv("cnes_estabelecimentos.csv", sep=";", encoding="latin1", low_memory=False)


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

# Gráfico 1: Tipos de unidade no estado
st.subheader(f"Distribuição por Tipo de Unidade - {estado}")
tipo_unidade = df_estado["DS_TIPO_UNIDADE"].value_counts().reset_index()
fig1 = px.bar(tipo_unidade, x="index", y="DS_TIPO_UNIDADE", labels={"index": "Tipo", "DS_TIPO_UNIDADE": "Quantidade"}, color="index")
st.plotly_chart(fig1, use_container_width=True)
