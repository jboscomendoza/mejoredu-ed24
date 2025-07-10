import streamlit as st
import polars as pl
import plotly.graph_objects as go
from os import path

DES_COLOR = {
    "Sin evidencia": "#f6511d",
    "Requiere apoyo": "#ffb400",
    "En proceso":"#00a6ed",
    "Desarrollado": "#7fb800",
}

@st.cache_data
def read_parquet_data(archivo: str):
    parquet_data = pl.read_parquet(path.join("data", archivo))
    return parquet_data


st.title("Resultados de la evaluación diagnóstica 2024-2025")

p_nacional = read_parquet_data("p_nac.parquet")
p_nacional = p_nacional.with_columns(
    nivel_grado=(
        pl.col("nivel").cast(pl.String) + " - " + pl.col("grado").cast(pl.String)
    )
)

campos = p_nacional["campo"].unique()
nivel_grado = p_nacional["nivel_grado"].unique()

for campo in campos:
    st.markdown(f"## {campo}")
    p_campo = p_nacional.filter(pl.col("campo") == campo)

    ploto = go.Figure()

    ploto.add_trace(go.Bar())
    for desarrollo in p_campo["desarrollo"].unique():
        p_desarrollo = p_campo.filter(pl.col("desarrollo") == desarrollo)
        ploto.add_trace(
            go.Bar(
                x=p_desarrollo["nivel_grado"],
                y=p_desarrollo["porcentaje"],
                name=desarrollo, 
                marker=dict(
                    color=DES_COLOR[desarrollo]
                )
        ))
    ploto.update_layout(
        barmode="stack",
        yaxis=dict(
            tickformat=",.2%"
        )
        )

    st.plotly_chart(ploto, key=f"nacional_{campo}")
