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

# Gráfico 2: Categoria administrativa (privado, público, filantrópico)
st.subheader(f"Distribuição por Categoria Administrativa - {estado}")
if "DS_CATEGORIA_UNIDADE" in df_estado.columns:
    categoria = df_estado["DS_CATEGORIA_UNIDADE"].value_counts().reset_index()
    fig2 = px.pie(categoria, names="index", values="DS_CATEGORIA_UNIDADE", title="Categoria da Unidade")
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("Coluna de categoria administrativa não está disponível neste dataset.")

