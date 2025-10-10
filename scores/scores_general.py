import streamlit as st
import polars as pl
import plot_helper as ph
from os import path


@st.cache_data
def read_parquet_data(archivo: str):
    parquet_data = pl.read_parquet(path.join("data", archivo)).with_columns(
        nivel_grado=(
            pl.col("nivel").cast(pl.String) + " - " + pl.col("grado").cast(pl.String)
        )
    )
    return parquet_data


s_nacional = read_parquet_data("s_nac.parquet")
s_entidad = read_parquet_data("s_ent.parquet")
s_servicio = read_parquet_data("s_ser.parquet")
s_sexo = read_parquet_data("s_sex.parquet")

campos = s_nacional["campo"].unique(maintain_order=True)
entidades = s_entidad["entidad"].unique(maintain_order=True)
servicios = s_servicio["servicio"].unique(maintain_order=True)
sexos = s_sexo["sexo"].unique(maintain_order=True)

#### Page ####
st.title("Resultados de la evaluación diagnóstica 2024-2025 - Puntajes de los estudiantes")

"""
En esta evaluación, las y los estudiantes fueron evaluados por sus propios docentes apoyándose con rúbricas en las cuales se establecieron criterios de valoración.

Cada criterio de valoración tenía cuatro niveles de desarrollo en los cuales se podían situar las respuestas de los estudiantes en las consignas de evaluación:

* Sin evidencia
* Requiere apoyo
* En proceso
* Desarrollado

A cada valoración corresponde un puntaje ponderado de acuerdo a la complejidad del proceso de aprendizaje evaluado. El máximo puntaje posible para un estudiante, a partir de sus respuesta a los EIAs aplicados, es de **20 puntos**.

A continuación, se presentan los puntajes promedio de los estudiantes.
"""

tab_nac, tab_ser, tab_sex, tab_ent = st.tabs(
    ["Nacional", "Servicio", "Sexo", "Entidad"]
)

#### Resultados nacionales ####
with tab_nac:
    st.markdown("## Resultados nacionales")

    for campo in campos:
        st.markdown(f"### {campo}")
        s_nac_campo = s_nacional.filter(pl.col("campo") == campo).sort(
            "nivel_grado", descending=True
        )
        plot_nac_campo = ph.plot_scatter(s_nac_campo, "nivel_grado")
        st.plotly_chart(plot_nac_campo, key=f"s_nacional_{campo}")

#### Resultados por servicio ####
with tab_ser:
    st.markdown("## Resultados por servicio")

    sel_servicio = st.selectbox("Servicio", servicios)
    s_ser_sel = s_servicio.filter(pl.col("servicio") == sel_servicio)

    for campo in campos:
        st.markdown(f"### {campo}")
        s_ser_campo = s_ser_sel.filter(pl.col("campo") == campo).sort(
            "nivel_grado", descending=True
        )
        plot_ser_campo = ph.plot_scatter(s_ser_campo, "nivel_grado")
        st.plotly_chart(plot_ser_campo, key=f"s_servicio_{campo}")


#### Resultados por sexo ####
with tab_sex:
    st.markdown("## Resultados por sexo")

    sel_sexo = st.selectbox("Sexo", sexos)
    s_sex_sel = s_sexo.filter(pl.col("sexo") == sel_sexo)

    for campo in campos:
        st.markdown(f"### {campo}")
        s_sex_campo = s_sex_sel.filter(pl.col("campo") == campo).sort(
            "nivel_grado", descending=True
        )
        plot_sex_campo = ph.plot_scatter(s_sex_campo, "nivel_grado")
        st.plotly_chart(plot_sex_campo, key=f"s_sexo_{campo}")


#### Resultados por entidad ####
with tab_ent:
    st.markdown("## Resultados por entidad")

    sel_entidad = st.selectbox("Entidad", entidades)
    s_ent_sel = s_entidad.filter(pl.col("entidad") == sel_entidad)

    for campo in campos:
        st.markdown(f"### {campo}")
        s_ent_campo = s_ent_sel.filter(pl.col("campo") == campo).sort(
            "nivel_grado", descending=True
        )
        plot_ent_campo = ph.plot_scatter(s_ent_campo, "nivel_grado")
        st.plotly_chart(plot_ent_campo, key=f"s_entidad_{campo}")
