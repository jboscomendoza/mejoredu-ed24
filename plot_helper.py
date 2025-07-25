import polars as pl
import plotly.graph_objects as go

DES_COLOR = {
    "Sin evidencia": "#f6511d",
    "Requiere apoyo": "#ffb400",
    "En proceso": "#00a6ed",
    "Desarrollado": "#7fb800",
}
SCR_COLOR = "#4895ef"


def plot_bar(df: pl.DataFrame, grupo: str, columna: str, des_color: dict = DES_COLOR) -> go.Figure:
    n_grupos = len(df[grupo].unique())
    if n_grupos < 9:
        alto_base = 40 * n_grupos
    else:
        alto_base = 260
    alto_plot = (n_grupos * 20) + alto_base
    plot = go.Figure()
    plot.add_trace(go.Bar())
    for i in df[columna].unique(maintain_order=True):
        df_desarrollo = df.filter(pl.col(columna) == i)
        plot.add_trace(
            go.Bar(
                y=df_desarrollo[grupo],
                x=df_desarrollo["porcentaje"],
                orientation="h",
                name=i,
                text=df_desarrollo.select("porcentaje")
                .with_columns(pl.col("porcentaje") * 100)["porcentaje"]
                .round(2),
                marker=dict(color=des_color[i]),
            )
        )
    plot.update_layout(
        barmode="stack",
        xaxis=dict(tickformat=",.2%"),
        margin=dict(t=20, b=10),
        height=alto_plot,
    )
    return plot


def plot_scatter(df: pl.DataFrame, grupo: str, scr_color: str = SCR_COLOR) -> go.Figure:
    n_grupos = len(df[grupo].unique())
    if n_grupos < 9:
        alto_base = 35 * n_grupos
    else:
        alto_base = 160
    alto_plot = (n_grupos * 20) + alto_base
    plot = go.Figure()
    plot.add_trace(
        go.Scatter(
            x=df["puntaje"],
            y=df[grupo],
            orientation="h",
            mode="markers+text",
            text=df["puntaje"].round(2),
            textposition="middle right",
            marker=dict(color=scr_color),
        )
    )
    plot.update_layout(
        xaxis_range=[0, 20],
        margin=dict(t=20, b=10),
        height=alto_plot,
    )
    return plot
