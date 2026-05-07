import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="COVID Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Dashboard COVID-19")
st.write("Análise global da COVID-19 com foco no Brasil")

# carregar base
BASE_DIR = Path(__file__).resolve().parent.parent
arquivo = BASE_DIR / "data" / "processed" / "covid_tratado.csv"

df = pd.read_csv(arquivo)

# -------------------------
# FILTRO
# -------------------------
st.sidebar.title("Filtros")

regioes = ["Todas"] + sorted(df["who_region"].unique().tolist())

regiao_escolhida = st.sidebar.selectbox(
    "Selecione a Região",
    regioes
)

if regiao_escolhida != "Todas":
    df_filtrado = df[df["who_region"] == regiao_escolhida]
else:
    df_filtrado = df.copy()

# -------------------------
# KPIs
# -------------------------
total_casos = df_filtrado["confirmed"].sum()
total_mortes = df_filtrado["deaths"].sum()
total_recuperados = df_filtrado["recovered"].sum()
total_ativos = df_filtrado["active"].sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Casos Confirmados", f"{total_casos:,.0f}")
col2.metric("Mortes", f"{total_mortes:,.0f}")
col3.metric("Recuperados", f"{total_recuperados:,.0f}")
col4.metric("Casos Ativos", f"{total_ativos:,.0f}")



if regiao_escolhida in ["Todas", "Americas"]:
    st.subheader("🇧🇷 Destaque: Brasil")

    brasil = df[df["country_region"] == "Brazil"]

    casos_br = int(brasil["confirmed"].iloc[0])
    mortes_br = int(brasil["deaths"].iloc[0])
    recuperados_br = int(brasil["recovered"].iloc[0])
    letalidade_br = float(brasil["letalidade"].iloc[0])

    b1, b2, b3, b4 = st.columns(4)

    b1.metric("Casos no Brasil", f"{casos_br:,}")
    b2.metric("Mortes no Brasil", f"{mortes_br:,}")
    b3.metric("Recuperados", f"{recuperados_br:,}")
    b4.metric("Letalidade", f"{letalidade_br:.2f}%")

st.subheader("🌍 Mapa Global de Casos")

fig_mapa = px.choropleth(
    df_filtrado,
    locations="country_region",
    locationmode="country names",
    color="confirmed",
    hover_name="country_region",
    hover_data={
        "confirmed": True,
        "deaths": True,
        "recovered": True,
        "active": True
    },
    title="Distribuição Global de Casos Confirmados",
    color_continuous_scale="Reds"
)

st.plotly_chart(fig_mapa, use_container_width=True)
metrica = st.selectbox(
    "Escolha a métrica do ranking",
    [
        "confirmed",
        "deaths",
        "recovered",
        "active",
        "letalidade",
        "taxa_recuperacao"
    ]
)

# -------------------------
# TOP 10
# -------------------------
top10 = df_filtrado.nlargest(10, metrica)

fig = px.bar(
    top10,
    x=metrica,
    y="country_region",
    orientation="h",
    title="Top 10 Países por Casos Confirmados"
)

fig.update_layout(yaxis={"categoryorder": "total ascending"})

st.plotly_chart(fig, use_container_width=True)

