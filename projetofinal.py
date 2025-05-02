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


