import streamlit as st
import plotly.express as px

from data import BASE_DIR, load_data, get_base64
from translations import TRANSLATIONS

st.set_page_config(page_title="COVID Dashboard", page_icon="📊", layout="wide")

background_image = get_base64(BASE_DIR / "images" / "background.jpg")

st.markdown(f"""
<style>
.stApp {{
    background-image:
        linear-gradient(rgba(245,247,250,0.90), rgba(245,247,250,0.90)),
        url("data:image/jpg;base64,{background_image}");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}}
.main {{ background-color: transparent; }}
div[data-testid="metric-container"] {{
    background: rgba(255,255,255,0.98);
    border: 2px solid #cbd5e1;
    padding: 25px;
    border-radius: 20px;
    box-shadow: 0 6px 16px rgba(0,0,0,0.12);
    text-align: center;
    transition: 0.3s ease-in-out;
}}
div[data-testid="metric-container"]:hover {{
    transform: translateY(-3px);
    box-shadow: 0 10px 24px rgba(0,0,0,0.18);
}}
h1 {{ color: #0f172a; font-weight: 700; }}
h2, h3 {{ color: #1e293b; }}
section[data-testid="stSidebar"] {{
    background-color: rgba(255,255,255,0.96);
    border-right: 1px solid #d9e2ec;
}}
</style>
""", unsafe_allow_html=True)

df = load_data()

# -------------------------
# SIDEBAR
# -------------------------
idioma = st.sidebar.selectbox("🌍 Idioma / Language", list(TRANSLATIONS.keys()))
t = TRANSLATIONS[idioma]

st.sidebar.title(t["filtros"])

todas_label = t["todas"]
regioes = [todas_label] + sorted(df["who_region"].unique().tolist())
regiao_escolhida = st.sidebar.selectbox(t["regiao"], regioes)

# -------------------------
# FILTRO
# -------------------------
if regiao_escolhida != todas_label:
    df_filtrado = df[df["who_region"] == regiao_escolhida]
else:
    df_filtrado = df.copy()

# -------------------------
# CABEÇALHO
# -------------------------
st.title(t["titulo"])
st.write(t["subtitulo"])

# -------------------------
# KPIs
# -------------------------
col1, col2, col3, col4 = st.columns(4)
col1.metric(t["casos"],      f"{df_filtrado['confirmed'].sum():,.0f}")
col2.metric(t["mortes"],     f"{df_filtrado['deaths'].sum():,.0f}")
col3.metric(t["recuperados"],f"{df_filtrado['recovered'].sum():,.0f}")
col4.metric(t["ativos"],     f"{df_filtrado['active'].sum():,.0f}")

# -------------------------
# BRASIL
# -------------------------
if regiao_escolhida in [todas_label, "Americas"]:
    st.subheader(t["brasil"])
    brasil = df[df["country_region"] == "Brazil"].iloc[0]
    b1, b2, b3, b4 = st.columns(4)
    b1.metric(t["casos_br"],     f"{int(brasil['confirmed']):,}")
    b2.metric(t["mortes_br"],    f"{int(brasil['deaths']):,}")
    b3.metric(t["recuperados_br"],f"{int(brasil['recovered']):,}")
    b4.metric(t["letalidade"],   f"{float(brasil['letalidade']):.2f}%")

# -------------------------
# MAPA
# -------------------------
st.subheader(t["mapa"])

fig_mapa = px.choropleth(
    df_filtrado,
    locations="iso_alpha",
    locationmode="ISO-3",
    color="confirmed",
    hover_name="country_region",
    hover_data={"confirmed": True, "deaths": True, "recovered": True, "active": True, "iso_alpha": False},
    labels={"confirmed": t["casos"], "deaths": t["mortes"], "recovered": t["recuperados"], "active": t["ativos"]},
    title=t["titulo_mapa"],
    color_continuous_scale="Reds",
)
fig_mapa.update_layout(paper_bgcolor="#f7f9fc", plot_bgcolor="#f7f9fc")
st.plotly_chart(fig_mapa, use_container_width=True)

# -------------------------
# RANKING
# -------------------------
metricas = t["metricas"]
metrica_label = st.selectbox(t["ranking"], list(metricas.values()))
metrica = next(k for k, v in metricas.items() if v == metrica_label)

top10 = df_filtrado.nlargest(10, metrica)

fig_ranking = px.bar(
    top10,
    x=metrica,
    y="country_region",
    orientation="h",
    title=f"{t['top10']} {metrica_label}",
    labels={metrica: metrica_label, "country_region": ""},
)
fig_ranking.update_layout(
    yaxis={"categoryorder": "total ascending"},
    paper_bgcolor="#f7f9fc",
    plot_bgcolor="#ffffff",
)
st.plotly_chart(fig_ranking, use_container_width=True)
