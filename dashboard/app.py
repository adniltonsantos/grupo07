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
.block-container {{
    background: rgba(255,255,255,0.97);
    border-radius: 20px;
    padding: 2rem 3rem !important;
    box-shadow: 0 4px 24px rgba(15,23,42,0.08);
    margin-top: 1rem;
}}
.header-block {{
    background: rgba(255,255,255,0.97);
    border-radius: 16px;
    padding: 24px 32px 20px 32px;
    margin-bottom: 8px;
    box-shadow: 0 2px 12px rgba(15,23,42,0.10);
    border-left: 5px solid #2563eb;
}}
.header-block h1 {{
    color: #0f172a !important;
    font-size: 2.1rem !important;
    font-weight: 800 !important;
    margin: 0 0 4px 0 !important;
    line-height: 1.2 !important;
}}
.header-block p {{
    color: #475569 !important;
    font-size: 1.05rem !important;
    margin: 0 !important;
}}
.section-header {{
    background: rgba(255,255,255,0.93);
    border-left: 5px solid #0ea5e9;
    border-radius: 0 12px 12px 0;
    padding: 12px 20px;
    margin: 24px 0 12px 0;
    box-shadow: 0 1px 6px rgba(15,23,42,0.07);
}}
.section-header h2 {{
    color: #0f172a !important;
    font-size: 1.35rem !important;
    font-weight: 700 !important;
    margin: 0 !important;
}}
.section-header.brasil {{ border-left-color: #16a34a; }}
div[data-testid="metric-container"] {{
    background: #ffffff !important;
    border: 1.5px solid #bfdbfe;
    padding: 24px 20px;
    border-radius: 16px;
    box-shadow: 0 4px 20px rgba(15,23,42,0.10), 0 1px 4px rgba(15,23,42,0.06);
    text-align: center;
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}}
div[data-testid="metric-container"]:hover {{
    transform: translateY(-4px);
    box-shadow: 0 12px 28px rgba(15,23,42,0.16), 0 2px 6px rgba(15,23,42,0.08);
}}
[data-testid="stMetricLabel"], [data-testid="stMetricLabel"] * {{
    color: #475569 !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    text-transform: uppercase !important;
    letter-spacing: 0.04em !important;
}}
[data-testid="stMetricValue"], [data-testid="stMetricValue"] * {{
    color: #0f172a !important;
    font-size: 1.8rem !important;
    font-weight: 800 !important;
}}
section[data-testid="stSidebar"] {{
    background-color: rgba(255,255,255,0.97);
    border-right: 1px solid #d9e2ec;
}}
/* Brasil KPI cards com acento verde */
.brasil-kpis div[data-testid="metric-container"] {{
    border-color: #bbf7d0;
}}
/* Hint caption abaixo dos KPIs */
.kpi-caption {{
    color: #94a3b8;
    font-size: 0.78rem;
    margin: -6px 0 18px 2px;
    letter-spacing: 0.02em;
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
st.markdown(
    f'<div class="header-block"><h1>{t["titulo"]}</h1><p>{t["subtitulo"]}</p></div>',
    unsafe_allow_html=True,
)

# -------------------------
# ABAS PRINCIPAIS
# -------------------------
show_brasil_tab = regiao_escolhida in [todas_label, "Americas"]

if show_brasil_tab:
    tab_global, tab_ranking, tab_brasil = st.tabs([
        t["aba_global"],
        t["aba_ranking"],
        t["aba_brasil"],
    ])
else:
    tab_global, tab_ranking = st.tabs([
        t["aba_global"],
        t["aba_ranking"],
    ])
    tab_brasil = None

# =========================================================
# ABA 1 — VISÃO GLOBAL
# =========================================================
with tab_global:
    # KPIs globais
    col1, col2, col3, col4 = st.columns(4)
    col1.metric(t["casos"],       f"{df_filtrado['confirmed'].sum():,.0f}")
    col2.metric(t["mortes"],      f"{df_filtrado['deaths'].sum():,.0f}")
    col3.metric(t["recuperados"], f"{df_filtrado['recovered'].sum():,.0f}")
    col4.metric(t["ativos"],      f"{df_filtrado['active'].sum():,.0f}")

    st.divider()

    # Mapa coroplético
    st.markdown(
        f'<div class="section-header"><h2>{t["mapa"]}</h2></div>',
        unsafe_allow_html=True,
    )

    fig_mapa = px.choropleth(
        df_filtrado,
        locations="iso_alpha",
        locationmode="ISO-3",
        color="confirmed",
        hover_name="country_region",
        hover_data={
            "confirmed": True,
            "deaths": True,
            "recovered": True,
            "active": True,
            "iso_alpha": False,
        },
        labels={
            "confirmed": t["casos"],
            "deaths": t["mortes"],
            "recovered": t["recuperados"],
            "active": t["ativos"],
        },
        title=t["titulo_mapa"],
        color_continuous_scale="Reds",
    )
    fig_mapa.update_layout(paper_bgcolor="#f7f9fc", plot_bgcolor="#f7f9fc", height=600)
    st.plotly_chart(fig_mapa, use_container_width=True)

# =========================================================
# ABA 2 — RANKING
# =========================================================
with tab_ranking:
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

# =========================================================
# ABA 3 — BRASIL (só aparece quando região inclui Brasil)
# =========================================================
if tab_brasil is not None:
    with tab_brasil:
        brasil = df[df["country_region"] == "Brazil"].iloc[0]

        st.markdown(
            f'<div class="section-header brasil"><h2>{t["brasil"]}</h2></div>',
            unsafe_allow_html=True,
        )

        # Linha 1 — casos e mortes
        with st.container():
            st.markdown('<div class="brasil-kpis">', unsafe_allow_html=True)
            b1, b2, b3, b4 = st.columns(4)
            b1.metric(t["casos_br"],      f"{int(brasil['confirmed']):,}")
            b2.metric(t["mortes_br"],     f"{int(brasil['deaths']):,}")
            b3.metric(t["recuperados_br"],f"{int(brasil['recovered']):,}")
            b4.metric(t["letalidade"],    f"{float(brasil['letalidade']):.2f}%")
            st.markdown("</div>", unsafe_allow_html=True)

        st.divider()

        # Gráfico de comparação Brasil vs. mundo (pie simples)
        confirmados_mundo = int(df["confirmed"].sum())
        confirmados_brasil = int(brasil["confirmed"])
        outros = confirmados_mundo - confirmados_brasil

        label_brasil_pie = "Brasil"
        label_outros_pie = t.get("aba_global", "Outros")

        fig_pie = px.pie(
            values=[confirmados_brasil, outros],
            names=[label_brasil_pie, label_outros_pie],
            title=f"{t['casos_br']} vs. {t['casos']}",
            color_discrete_sequence=["#16a34a", "#bfdbfe"],
            hole=0.45,
        )
        fig_pie.update_layout(paper_bgcolor="#f7f9fc")
        st.plotly_chart(fig_pie, use_container_width=True)
