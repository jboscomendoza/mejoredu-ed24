import polars as pl
import plotly.graph_objects as go

DES_COLOR = {
    "Sin evidencia": "#f6511d",
    "Requiere apoyo": "#ffb400",
    "En proceso": "#00a6ed",
    "Desarrollado": "#7fb800",
}

def plot_bar(df: pl.DataFrame, grupo:str, des_color:dict=DES_COLOR) -> go.Figure:
    n_grupos = len(df[grupo].unique())
    alto_plot = (n_grupos * 25) + 150
    plot = go.Figure()
    plot.add_trace(go.Bar())
    for desarrollo in df["desarrollo"].unique(maintain_order=True):
        df_desarrollo = df.filter(pl.col("desarrollo") == desarrollo)
        plot.add_trace(
            go.Bar(
                y=df_desarrollo[grupo],
                x=df_desarrollo["porcentaje"],
                orientation="h",
                name=desarrollo,
                text=df_desarrollo.select("porcentaje").with_columns(pl.col("porcentaje") * 100)["porcentaje"].round(2),
                marker=dict(color=des_color[desarrollo]),
            )
        )
    plot.update_layout(
        barmode="stack",
        xaxis=dict(tickformat=",.2%"),
        margin=dict(l=5, t=20),
        height=alto_plot,
    )
    return plot