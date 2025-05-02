# Importação das bibliotecas necessárias
#venv\Scripts\activate.bat                                                                                                                                 
#venv\Scripts\activate.bat (cmd)
#python -m pip install plotly  python3 -m pip install plotly  

import streamlit as st
import pandas as pd
import plotly.express as px
import os
import datetime as dt


# Título do projeto
st.title("📊 Acesso à Saúde no Brasil")

st.markdown("""
#### Uma análise exploratória dos estabelecimentos de saúde cadastrados no CNES

A estrutura e a distribuição dos serviços de saúde no Brasil revelam muito sobre o acesso da população aos cuidados essenciais. 
Este painel analítico tem como objetivo visualizar os dados do Cadastro Nacional de Estabelecimentos de Saúde (CNES), destacando padrões por tipo de gestão, esfera administrativa e distribuição geográfica das unidades.
""")

# Storytelling de abertura
st.markdown("""
## 🎯 Objetivo do Projeto

Este painel interativo tem como objetivo apresentar, de maneira visual e acessível, a **distribuição dos estabelecimentos de saúde no Brasil** a partir dos dados públicos do CNES (Cadastro Nacional de Estabelecimentos de Saúde).  
A proposta é fornecer **insights relevantes** para gestores, pesquisadores e cidadãos, analisando aspectos como localização, esfera administrativa e tipo de gestão das unidades.

---
""")


# Caminho do arquivo CSV na mesma pasta
csv_file = "cnes_estabelecimentos2.csv"


df = pd.read_csv("cnes_estabelecimentos2.csv", sep=";", encoding="latin1", low_memory=False)


st.markdown("""
## 📥 Carregamento da Base de Dados

Os dados foram carregados com sucesso a partir do arquivo **`cnes_estabelecimentos2.csv`**, contendo informações sobre os estabelecimentos de saúde em todo o território nacional.
""")

# Exibe amostra dos dados
st.markdown("### 🔍 Primeiras linhas dos dados")

     # Exibe os dados carregados
st.markdown("### Dados de Vendas Carregados")
st.dataframe(df.head(5))

# Seleção de colunas principais
colunas_utilizadas = [
    "CNES", "NO_FANTASIA", "TP_UNIDADE", "DS_TIPO_UNIDADE", "CO_MUNICIPIO_GESTOR", 
    "NO_MUNICIPIO", "CO_UF", "NO_UF", "TP_ESTABELECIMENTO", "DS_TP_ESTABELECIMENTO",
    "TP_GESTAO", "DS_TP_GESTAO", "CO_CATEGORIA_UNIDADE", "DS_CATEGORIA_UNIDADE",
    "DS_ESFERA_ADMINISTRATIVA"
]

df = df[[col for col in colunas_utilizadas if col in df.columns]]

st.markdown("""
## 🧹 Tratamento e Preparação dos Dados

Selecionamos apenas as colunas mais relevantes da base original, como o tipo de unidade, esfera administrativa, estado e município.  
Também realizamos o mapeamento dos códigos de UF para siglas, facilitando a leitura dos gráficos.
""")


# Criação de dicionário de UFs
ufs = {
    12: 'AC', 27: 'AL', 13: 'AM', 16: 'AP', 29: 'BA', 23: 'CE',
    53: 'DF', 32: 'ES', 52: 'GO', 21: 'MA', 31: 'MG', 50: 'MS',
    51: 'MT', 15: 'PA', 25: 'PB', 26: 'PE', 22: 'PI', 41: 'PR',
    33: 'RJ', 24: 'RN', 43: 'RS', 11: 'RO', 14: 'RR', 42: 'SC',
    28: 'SE', 35: 'SP', 17: 'TO'
}
df['UF'] = df['CO_UF'].map(ufs)

# Filtro por estado
ufs_disponiveis = df["CO_UF"].dropna().unique()
estado = st.selectbox("Selecione um estado para análise", sorted(ufs_disponiveis))
df_estado = df[df["CO_UF"] == estado]


st.markdown("""
---
## 📊 Visualizações Interativas

A seguir, são apresentados diversos gráficos interativos que ilustram a distribuição das unidades de saúde, com base em diferentes critérios de agrupamento e análise.
""")


# Título da seção
st.header("Distribuição das Unidades por Estado")

# 1. Gráfico de barras
contagem_estados = df['UF'].value_counts().sort_index()
fig1 = px.bar(x=contagem_estados.index, y=contagem_estados.values,
              labels={'x': 'UF', 'y': 'Quantidade de Unidades'},
              title='Quantidade de Unidades por Estado')
st.plotly_chart(fig1)

# 2. Gráfico de pizza
fig2 = px.pie(values=contagem_estados.values, names=contagem_estados.index,
              title='Proporção de Unidades por Estado')
st.plotly_chart(fig2)

# 3. Gráfico de dispersão
fig3 = px.scatter(x=contagem_estados.index, y=contagem_estados.values,
                  labels={'x': 'UF', 'y': 'Quantidade de Unidades'},
                  title='Distribuição de Unidades por Estado')
st.plotly_chart(fig3)


st.markdown("""
## 🌡️ Mapa de Calor: Estado x Esfera Administrativa

Este mapa de calor cruza a **Unidade Federativa** com a **Esfera Administrativa** (Municipal, Estadual, Federal ou Privada), permitindo compreender como está distribuída a responsabilidade pela gestão das unidades em cada estado.
""")

# 4. Mapa de calor por Estado e Esfera Administrativa
if "DS_ESFERA_ADMINISTRATIVA" in df.columns:
    heatmap_data2 = df.groupby(["UF", "DS_ESFERA_ADMINISTRATIVA"]).size().reset_index(name='Quantidade')
    fig4 = px.density_heatmap(heatmap_data2, 
                              x="UF", y="DS_ESFERA_ADMINISTRATIVA", z="Quantidade", 
                              color_continuous_scale="Blues",
                              title="Mapa de Calor: Estado x Esfera Administrativa")
    st.plotly_chart(fig4)
else:
    st.warning("Coluna 'DS_ESFERA_ADMINISTRATIVA' não encontrada nos dados.")

    # Análise Final
st.markdown("""
## 🧾 Conclusões e Reflexões

- Os dados evidenciam uma concentração significativa de unidades em estados mais populosos, como São Paulo e Minas Gerais.
- A **esfera administrativa predominante** pode variar conforme a política pública local e o modelo de regionalização da saúde.
- Com base na distribuição por **tipo de gestão**, é possível avaliar se há predominância do SUS ou se existe maior atuação da iniciativa privada em determinadas regiões.
- O painel pode ser expandido futuramente para incluir indicadores de qualidade, capacidade de atendimento ou cruzamento com dados epidemiológicos regionais.

---
""")
