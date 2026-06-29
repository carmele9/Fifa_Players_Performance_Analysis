import plotly.express as px
import numpy as np
import plotly.graph_objects as go

# Gráfico para ver las nacionalidades de los jugadores y su valor promedio en el mercado
def plot_nacionalidades_valor(df):
    nationality_df = (
        df.groupby("nationality")
        .agg(
            players=("player_name","count"),
            value=("market_value_million_eur","mean")
        )
        .sort_values("players", ascending=False)
    )

    fig = px.bar(
        nationality_df,
        x="players",
        y=nationality_df.index,
        orientation="h",
        color="value",
        color_continuous_scale="Viridis",
        title="Top Nacionalidades: número de jugadores y valor medio"
    )

    fig.update_layout(
        template="plotly_white",
        xaxis_title="Número de jugadores",
        yaxis_title="Nacionalidad",
        title_x=0.5
    )

    return fig

# Gráfico para ver clubes por valor total de plantilla
def plot_club_plantilla(df):
    club_values = (
        df.groupby("club")
        ["market_value_million_eur"]
        .sum()
        .sort_values(ascending=False)
    )

    club_values_df = club_values.reset_index()

    fig = px.bar(
        club_values_df,
        x="market_value_million_eur",
        y="club",
        orientation="h",
        color="market_value_million_eur",
        color_continuous_scale="Blues",
        title="Top Clubes por valor total de plantilla"
    )

    fig.update_layout(
        template="plotly_white",
        xaxis_title="Valor total (€ millones)",
        yaxis_title="Club",
        title_x=0.5
    )

    return fig


 # Top 15 jugadores más valiosos
def plot_15(df):
   
    top15 = (
        df.nlargest(15, "market_value_million_eur")
        .sort_values("market_value_million_eur")
    )

    fig = px.bar(
        top15,
        x="market_value_million_eur",
        y="player_name",
        orientation="h",
        color="goals",
        color_continuous_scale="Viridis",
        text="market_value_million_eur",
        hover_data={
            "age": True,
            "club": True,
            "position": True,
            "overall_rating": True,
            "goals": True,
            "market_value_million_eur": ":.1f"
        }
    )

    fig.update_traces(
        texttemplate="€%{x:.1f}M",
        textposition="outside"
    )

    fig.update_layout(
        title={
            "text": "Top 15 Jugadores Más Valiosos",
            "x": 0.5,
            "xanchor": "center"
        },
        xaxis_title="Valor de Mercado (€ Millones)",
        yaxis_title="",
        template="plotly_white",
        height=700,
        width=1200,
        coloraxis_colorbar=dict(
            title="Goles"
        )
    )

    return fig

# Valor Del Mercado según la Posición
def plot_valor_pos(df):
    fig = px.violin(
        df,
        x="position",
        y="market_value_million_eur",
        box=True,
        points="all",
        title="Valor Del Mercado según la Posición",
        color="position"
    )

    fig.update_layout(
        template="plotly_white",
        title_x=0.5,
        xaxis_title="",
        yaxis_title="Valor En El Mercado (€ Millones)",
        height=650,
        showlegend=False
    )
    return fig

# Relación Entre El Riesgo de Transferencia y Su Valor en El Mercado
def plot_riesgo_valor(df):
    risk_stats = (
        df.groupby("transfer_risk_level")["market_value_million_eur"]
        .mean()
        .reset_index()
    )

    fig = px.bar(
        risk_stats,
        x="transfer_risk_level",
        y="market_value_million_eur",
        color="market_value_million_eur",
        color_continuous_scale="Viridis",
        title="Valor Medio del Mercado por Riesgo de Transferencia"
    )

    fig.update_layout(
        template="plotly_white",
        title_x=0.5,
        xaxis_title="Riesgo de Transferencia",
        yaxis_title="Valor En El Mercado (€ Millones)",
        height=600
    )

    return fig

# Panorama Del Valor del Mercado del Jugador
def plot_panorama(df):
    fig = px.scatter(
        df,
        x="age",
        y="market_value_million_eur",
        color="position",
        size="overall_rating",
        hover_data={
            "club": True,
            "position": True,
            "overall_rating": True,
            "goals": True,
            "assists": True
        },
        opacity=0.7,
        title="Panorama Del Valor del Mercado del Jugador"
    )

    fig.update_layout(
        template="plotly_white",
        title_x=0.5,
        xaxis_title="Edad",
        yaxis_title="Valor En El Mercado (€ Millones)",
        height=750
    )
    return fig


# Heatmap: Matriz de Correlaciones
def plot_heatmap(df):
    numeric = df.select_dtypes(include="number")
    corr = numeric.corr()

    fig = go.Figure(
        data=go.Heatmap(
            z=corr.values,
            x=corr.columns,
            y=corr.columns,
            colorscale="RdBu",
            zmid=0,
            text=np.round(corr.values, 2),
            texttemplate="%{text}"
        )
    )

    fig.update_layout(
        title="Heatmap",
        title_x=0.5,
        template="plotly_white",
        height=700,
        width=800
    )
    return fig 