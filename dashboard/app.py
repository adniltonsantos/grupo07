import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import base64

def get_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

st.set_page_config(
    page_title="COVID Dashboard",
    page_icon="📊",
    layout="wide"
)

# CSS personalizado
BASE_DIR = Path(__file__).resolve().parent.parent
background_path = BASE_DIR / "images" / "background.jpg"

background_image = get_base64(background_path)

st.markdown(f"""
<style>

/* Fundo com imagem */
.stApp {{
    background-image:
        linear-gradient(
            rgba(245,247,250,0.90),
            rgba(245,247,250,0.90)
        ),
        url("data:image/jpg;base64,{background_image}");

    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}

/* Área principal */
.main {{
    background-color: transparent;
}}

/* Cards KPI */
div[data-testid="metric-container"] {{
    background: rgba(255,255,255,0.98);
    border: 2px solid #cbd5e1;
    padding: 25px;
    border-radius: 20px;
    box-shadow: 0 6px 16px rgba(0,0,0,0.12);
    text-align: center;
    transition: 0.3s ease-in-out;
}}

/* efeito hover */
div[data-testid="metric-container"]:hover {{
    transform: translateY(-3px);
    box-shadow: 0 10px 24px rgba(0,0,0,0.18);
}}

/* Títulos */
h1 {{
    color: #0f172a;
    font-weight: 700;
}}

h2, h3 {{
    color: #1e293b;
}}

/* Sidebar */
section[data-testid="stSidebar"] {{
    background-color: rgba(255,255,255,0.96);
    border-right: 1px solid #d9e2ec;
}}

</style>
""", unsafe_allow_html=True)

# carregar base
BASE_DIR = Path(__file__).resolve().parent.parent
arquivo = BASE_DIR / "data" / "processed" / "covid_tratado.csv"

df = pd.read_csv(arquivo)

# -------------------------
# FILTRO
# -------------------------
st.sidebar.title("Filtros")

# -------------------------
# IDIOMA
# -------------------------

idioma = st.sidebar.selectbox(
    "🌍 Idioma / Language",
    ["Português", "English", "Español", "Русский", "中文"]
)
# -------------------------
# TRADUÇÕES
# -------------------------

translations = {
    "Português": {
        "titulo": "📊 Dashboard COVID-19",
        "subtitulo": "Análise Global da COVID-19",
        "filtros": "Filtros",
        "regiao": "Selecione a Região",
        "casos": "Casos Confirmados",
        "mortes": "Mortes",
        "recuperados": "Recuperados",
        "ativos": "Casos Ativos",
        "brasil": "🇧🇷 Destaque: Brasil",
        "casos_br": "Casos no Brasil",
        "mortes_br": "Mortes no Brasil",
        "recuperados_br": "Recuperados",
        "letalidade": "Letalidade",
        "mapa": "🌍 Mapa Global de Casos",
        "ranking": "Escolha a métrica do ranking",
        "top10": "Top 10 Países por"
    },

    "English": {
        "titulo": "📊 COVID-19 Dashboard",
        "subtitulo": "Global COVID-19 Analysis",
        "filtros": "Filters",
        "regiao": "Select Region",
        "casos": "Confirmed Cases",
        "mortes": "Deaths",
        "recuperados": "Recovered",
        "ativos": "Active Cases",
        "brasil": "🇧🇷 Brazil Highlights",
        "casos_br": "Cases in Brazil",
        "mortes_br": "Deaths in Brazil",
        "recuperados_br": "Recovered",
        "letalidade": "Fatality Rate",
        "mapa": "🌍 Global Cases Map",
        "ranking": "Choose ranking metric",
        "top10": "Top 10 Countries by"
    },

    "Español": {
        "titulo": "📊 Dashboard COVID-19",
        "subtitulo": "Análisis Global del COVID-19",
        "filtros": "Filtros",
        "regiao": "Seleccionar Región",
        "casos": "Casos Confirmados",
        "mortes": "Muertes",
        "recuperados": "Recuperados",
        "ativos": "Casos Activos",
        "brasil": "🇧🇷 Destaque: Brasil",
        "casos_br": "Casos en Brasil",
        "mortes_br": "Muertes en Brasil",
        "recuperados_br": "Recuperados",
        "letalidade": "Tasa de Mortalidad",
        "mapa": "🌍 Mapa Global de Casos",
        "ranking": "Elegir métrica del ranking",
        "top10": "Top 10 Países por"
    },

    "Русский": {
        "titulo": "📊 Панель COVID-19",
        "subtitulo": "Глобальный анализ COVID-19",
        "filtros": "Фильтры",
        "regiao": "Выберите регион",
        "casos": "Подтвержденные случаи",
        "mortes": "Смерти",
        "recuperados": "Выздоровевшие",
        "ativos": "Активные случаи",
        "brasil": "🇧🇷 Бразилия",
        "casos_br": "Случаи в Бразилии",
        "mortes_br": "Смерти в Бразилии",
        "recuperados_br": "Выздоровевшие",
        "letalidade": "Летальность",
        "mapa": "🌍 Глобальная карта случаев",
        "ranking": "Выберите метрику",
        "top10": "Топ 10 стран по"
    },

    "中文": {
        "titulo": "📊 COVID-19 仪表板",
        "subtitulo": "全球 COVID-19 分析",
        "filtros": "筛选",
        "regiao": "选择地区",
        "casos": "确诊病例",
        "mortes": "死亡人数",
        "recuperados": "康复人数",
        "ativos": "现存病例",
        "brasil": "🇧🇷 巴西亮点",
        "casos_br": "巴西病例",
        "mortes_br": "巴西死亡",
        "recuperados_br": "康复人数",
        "letalidade": "死亡率",
        "mapa": "🌍 全球病例地图",
        "ranking": "选择排名指标",
        "top10": "前10国家"
    }
}

t = translations[idioma]

st.title(t["titulo"])
st.write(t["subtitulo"])

regioes = ["Todas"] + sorted(df["who_region"].unique().tolist())

regiao_escolhida = st.sidebar.selectbox(
    t["regiao"],
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

col1.metric(t["casos"], f"{total_casos:,.0f}")
col2.metric(t["mortes"], f"{total_mortes:,.0f}")
col3.metric(t["recuperados"], f"{total_recuperados:,.0f}")
col4.metric(t["ativos"], f"{total_ativos:,.0f}")

# -------------------------
# BRASIL
# -------------------------
if regiao_escolhida in ["Todas", "Americas"]:
    st.subheader(t["brasil"])

    brasil = df[df["country_region"] == "Brazil"]

    casos_br = int(brasil["confirmed"].iloc[0])
    mortes_br = int(brasil["deaths"].iloc[0])
    recuperados_br = int(brasil["recovered"].iloc[0])
    letalidade_br = float(brasil["letalidade"].iloc[0])

    b1, b2, b3, b4 = st.columns(4)

    b1.metric(t["casos_br"], f"{casos_br:,}")
    b2.metric(t["mortes_br"], f"{mortes_br:,}")
    b3.metric(t["recuperados_br"], f"{recuperados_br:,}")
    b4.metric(t["letalidade"], f"{letalidade_br:.2f}%")

# -------------------------
# MAPA
# -------------------------
st.subheader(t["mapa"])

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

fig_mapa.update_layout(
    paper_bgcolor="#f7f9fc",
    plot_bgcolor="#f7f9fc"
)

st.plotly_chart(fig_mapa, width="stretch")

# -------------------------
# RANKING
# -------------------------
metricas = {
    "Casos Confirmados": "confirmed",
    "Mortes": "deaths",
    "Recuperados": "recovered",
    "Casos Ativos": "active",
    "Letalidade (%)": "letalidade",
    "Taxa de Recuperação (%)": "taxa_recuperacao"
}

metrica_label = st.selectbox(
    t["ranking"],
    list(metricas.keys())
)

metrica = metricas[metrica_label]

top10 = df_filtrado.nlargest(10, metrica)

fig = px.bar(
    top10,
    x=metrica,
    y="country_region",
    orientation="h",
    title=f"Top 10 Países por {metrica_label}"
)

fig.update_layout(
    yaxis={"categoryorder": "total ascending"},
    paper_bgcolor="#f7f9fc",
    plot_bgcolor="#ffffff"
)

st.plotly_chart(fig, width="stretch")