import streamlit as st
import polars as pl
import plotly.graph_objects as go
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


p_nacional = read_parquet_data("p_nac.parquet")
p_entidad  = read_parquet_data("p_ent.parquet")
p_servicio = read_parquet_data("p_ser.parquet")
p_sexo     = read_parquet_data("p_sex.parquet")

campos    = p_nacional["campo"].unique(maintain_order=True)
entidades = p_entidad["entidad"].unique(maintain_order=True)
servicios = p_servicio["servicio"].unique(maintain_order=True)
sexos     = p_sexo["sexo"].unique(maintain_order=True)

#### Page ####
st.title("Resultados de la evaluación diagnóstica 2024-2025")

tab_nac, tab_ser, tab_sex, tab_ent = st.tabs(["Nacional", "Servicio", "Sexo", "Entidad"])

#### Resultados nacionales ####
with tab_nac:
    st.markdown("## Resultados nacionales")

    for campo in campos:
        st.markdown(f"**{campo}**")
        p_nac_campo = p_nacional.filter(pl.col("campo") == campo)
        plot_nac_campo = ph.plot_bar(p_nac_campo, "nivel_grado")
        st.plotly_chart(plot_nac_campo, key=f"p_nacional_{campo}")

#### Resultados por servicio ####
with tab_ser:
    st.markdown("## Resultados por servicio")

    sel_servicio= st.selectbox("Servicio", servicios)
    p_ser_sel = p_servicio.filter(pl.col("servicio") == sel_servicio)

    for campo in campos:
        st.markdown(f"**{campo}**")
        p_ser_campo = p_ser_sel.filter(pl.col("campo") == campo)
        plot_ser_campo = ph.plot_bar(p_ser_campo, "nivel_grado")
        st.plotly_chart(plot_ser_campo, key=f"p_servicio_{campo}")


#### Resultados por sexo ####
with tab_sex:
    st.markdown("## Resultados por sexo")

    sel_sexo = st.selectbox("Sexo", sexos)
    p_sex_sel = p_sexo.filter(pl.col("sexo") == sel_sexo)

    for campo in campos:
        st.markdown(f"**{campo}**")
        p_sex_campo = p_sex_sel.filter(pl.col("campo") == campo)
        plot_sex_campo = ph.plot_bar(p_sex_campo, "nivel_grado")
        st.plotly_chart(plot_sex_campo, key=f"p_sexo_{campo}")


#### Resultados por entidad ####
with tab_ent:
    st.markdown("## Resultados por entidad")

    sel_entidad = st.selectbox("Entidad", entidades)
    p_ent_sel = p_entidad.filter(pl.col("entidad") == sel_entidad)

    for campo in campos:
        st.markdown(f"**{campo}**")
        p_ent_campo = p_ent_sel.filter(pl.col("campo") == campo)
        plot_ent_campo = ph.plot_bar(p_ent_campo, "nivel_grado")
        st.plotly_chart(plot_ent_campo, key=f"p_entidad_{campo}")
