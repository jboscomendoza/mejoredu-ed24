import streamlit as st
import polars as pl
import plot_helper as ph
from os import path

COL_TABLA = ["contenido", "pda", "descriptor", "criterio"]

@st.cache_data
def read_parquet_data(archivo: str) -> pl.DataFrame:
    parquet_data = pl.read_parquet(path.join("data", archivo)).with_columns(
        nivel_grado=(
            pl.col("nivel").cast(pl.String) + " - " + pl.col("grado").cast(pl.String)
        )
    )
    return parquet_data


i_nacional = read_parquet_data("i_nac.parquet")
i_entidad  = read_parquet_data("i_ent.parquet")
i_servicio = read_parquet_data("i_ser.parquet")
i_sexo     = read_parquet_data("i_sex.parquet")

campos    = i_nacional.sort("campo")["campo"].unique(maintain_order=True)
entidades = i_entidad["entidad"].unique(maintain_order=True)
servicios = i_servicio["servicio"].unique(maintain_order=True)
sexos     = i_sexo["sexo"].unique(maintain_order=True)
nivel_grados = i_nacional["nivel_grado"].unique(maintain_order=True)

#### Page ####
st.title("Resultados de la evaluación diagnóstica 2024-2025")

sel_nivel_grado = st.selectbox("Grado", nivel_grados)

tab_nac, tab_ser, tab_sex, tab_ent = st.tabs(["Nacional", "Servicio", "Sexo", "Entidad"])

#### Resultados nacionales ####
with tab_nac:
    st.markdown("## Resultados nacionales")
    i_nac_grado = i_nacional.filter(pl.col("nivel_grado") == sel_nivel_grado)

    for campo in campos:
        st.markdown(f"**{campo}**")
        p_nac_campo = i_nac_grado.filter(pl.col("campo") == campo).sort("item", descending=True)
        plot_nac_campo = ph.plot_bar(p_nac_campo, "item", "respuesta")
        st.plotly_chart(plot_nac_campo, key=f"p_nacional_{campo}")
        items = p_nac_campo.select("item").sort("item", descending=False).unique(maintain_order=True).to_series()
        for i in items:
            p_nac_item = (
                p_nac_campo.filter(pl.col("item") == i)
                .select(COL_TABLA)
                .unique(maintain_order=False)
                .rename(str.title)
                .transpose(
                    include_header=True, header_name=i, column_names=[""]
                )
                .to_pandas()
                .set_index(i)
            )
            st.dataframe(p_nac_item)

#### Resultados por servicio ####
with tab_ser:
    st.markdown("## Resultados por servicio")
    if sel_nivel_grado.find("Secundaria") == -1:
        servicios = servicios[0:3]
    
    sel_servicio = st.selectbox("Servicio", servicios)
    i_ser_sel = i_servicio.filter(
        pl.col("servicio") == sel_servicio,
        pl.col("nivel_grado") == sel_nivel_grado,
        )
    
    for campo in campos:
        st.markdown(f"**{campo}**")
        i_ser_campo = i_ser_sel.filter(pl.col("campo") == campo)
        plot_ser_campo = ph.plot_bar(i_ser_campo, "item", "respuesta")
        st.plotly_chart(plot_ser_campo, key=f"i_servicio_{campo}")

#### Resultados por sexo ####
with tab_sex:
    st.markdown("## Resultados por sexo")
    
    sel_sexo = st.selectbox("sexo", sexos)
    i_sex_sel = i_sexo.filter(
        pl.col("sexo") == sel_sexo,
        pl.col("nivel_grado") == sel_nivel_grado,
        )
    
    for campo in campos:
        st.markdown(f"**{campo}**")
        i_sex_campo = i_sex_sel.filter(pl.col("campo") == campo)
        plot_sex_campo = ph.plot_bar(i_sex_campo, "item", "respuesta")
        st.plotly_chart(plot_sex_campo, key=f"i_sexo_{campo}")

#### Resultados por sexo ####
with tab_ent:
    st.markdown("## Resultados por entidad")
    
    sel_entidad= st.selectbox("Entidad", entidades)
    i_ent_sel = i_entidad.filter(
        pl.col("entidad") == sel_entidad,
        pl.col("nivel_grado") == sel_nivel_grado,
        )
    
    for campo in campos:
        st.markdown(f"**{campo}**")
        i_ent_campo = i_ent_sel.filter(pl.col("campo") == campo)
        plot_ent_campo = ph.plot_bar(i_ent_campo, "item", "respuesta")
        st.plotly_chart(plot_ent_campo, key=f"i_entidad_{campo}")