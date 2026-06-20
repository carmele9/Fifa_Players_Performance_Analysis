import streamlit as st
import pandas as pd

from plots import (
    plot_nacionalidades_valor,
    plot_club_plantilla,
    plot_calidad_mercado,
    plot_15,
    plot_valor_pos,
    plot_riesgo_valor,
    plot_panorama,
    plot_heatmap
)

# ----------------------------
# CONFIGURACIÓN DE PÁGINA
# ----------------------------
st.set_page_config(
    page_title="Football Analytics Dashboard",
    layout="wide"
)

# ----------------------------
# CARGA DE DATOS
# ----------------------------
df = pd.read_csv("data/fifa_player.csv")

# ----------------------------
# TÍTULO
# ----------------------------
st.title("Football Player Analytics Dashboard")

st.markdown("""
Análisis exploratorio de jugadores basado en rendimiento, valor de mercado y factores de riesgo.  
            El objetivo es simular un sistema de scouting profesional.
""")

# ----------------------------
# SIDEBAR (FILTROS)
# ----------------------------
st.sidebar.header("Filtros")

positions = df["position"].unique()
clubs = df["club"].unique()
nationalities = df["nationality"].unique()

position_filter = st.sidebar.multiselect("Posición", positions, default=positions)
club_filter = st.sidebar.multiselect("Club", clubs, default=clubs)
nationality_filter = st.sidebar.multiselect("Nacionalidad", nationalities, default=nationalities)

age_min, age_max = st.sidebar.slider(
    "Edad",
    int(df["age"].min()),
    int(df["age"].max()),
    (20, 35)
)

# ----------------------------
# FILTRADO DEL DATASET
# ----------------------------
df_filtered = df[
    (df["position"].isin(position_filter)) &
    (df["club"].isin(club_filter)) &
    (df["nationality"].isin(nationality_filter)) &
    (df["age"].between(age_min, age_max))
]

# ----------------------------
# KPIs (RESUMEN EJECUTIVO)
# ----------------------------
st.subheader("Resumen General")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Jugadores", len(df_filtered))
col2.metric("Valor medio (€M)", round(df_filtered["market_value_million_eur"].mean(), 2))
col3.metric("Rating medio", round(df_filtered["overall_rating"].mean(), 2))
col4.metric("Goles totales", int(df_filtered["goals"].sum()))

# ----------------------------
# GRÁFICOS
# ----------------------------

st.divider()
st.header("Análisis por Nacionalidad")
st.plotly_chart(plot_nacionalidades_valor(df_filtered), use_container_width=True)

st.header("Valor de Plantilla por Club")
st.plotly_chart(plot_club_plantilla(df_filtered), use_container_width=True)

st.header("Relación Calidad vs Valor de Mercado")
st.plotly_chart(plot_calidad_mercado(df_filtered), use_container_width=True)

st.header("Top 15 Jugadores Más Valiosos")
st.plotly_chart(plot_15(df_filtered), use_container_width=True)

st.header("Valor de Mercado por Posición")
st.plotly_chart(plot_valor_pos(df_filtered), use_container_width=True)

st.header("Riesgo de Transferencia vs Valor")
st.plotly_chart(plot_riesgo_valor(df_filtered), use_container_width=True)

st.header("Panorama General del Mercado")
st.plotly_chart(plot_panorama(df_filtered), use_container_width=True)

st.header("Matriz de Correlación")
st.plotly_chart(plot_heatmap(df_filtered), use_container_width=True)

# ----------------------------
# FOOTER
# ----------------------------
st.markdown("---")
st.markdown("Proyecto de análisis de datos aplicado a scouting deportivo")