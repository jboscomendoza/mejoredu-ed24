import streamlit as st
import polars as pl
import plot_helper as ph
from os import path
import plotly.graph_objects as go


@st.cache_data
def read_parquet_params(archivo: str, carpeta: str = "data"):
    parquet_data = pl.read_parquet(path.join(carpeta, archivo))
    return parquet_data


irt_params = read_parquet_params("irt_parametros.parquet")

nivel_grados = irt_params["nivel_grado"].unique(maintain_order=True)
umbrales = irt_params["umbral"].unique(maintain_order=True)

#### Page ####
st.title("Resultados de la evaluación diagnóstica 2024-2025 - Puntajes de IRT")

"""
A continuación, se presentan los puntajes de los estudiantes en la Evaluación Diagnósticas, obtenidos mediane Teoría de Respuesta al Ítem (TRI o IRT por sus siglas en inglés).

Para la estimación de estos puntajes se ha ajustado un modelo unidimensional de crédito parcial, de modo que se obtiene un único puntaje por estudiante para ambos EIA aplicados.
"""

sel_nivel_grado = st.selectbox("Grado", nivel_grados)

#### Resultados generales ####

st.markdown("## Resultados por grado")

irt_nivel = irt_params.filter(pl.col("nivel_grado") == sel_nivel_grado)

plot = go.Figure()
plot.add_hline(y=50, line_color=ph.SCR_COLOR)
for umbral in umbrales:
    irt_umbral = irt_nivel.filter(pl.col("umbral") == umbral)
    plot.add_trace(
        go.Scatter(
            name=umbral,
            x=irt_umbral["item"],
            y=irt_umbral["dificultad"],
            mode="markers+text",
            text=irt_umbral["dificultad"].round(2),
            textposition="top center",
            marker=dict(color=ph.DES_COLOR[umbral]),
        )
    )
plot.update_layout(
    height=500,
    xaxis_title="Item",
    xaxis_tickangle = 90,
    yaxis_title="Dificultad",
    margin=dict(t=30, b=10),
    legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="left", x=0),
)

st.plotly_chart(plot)
