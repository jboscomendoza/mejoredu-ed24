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


def get_especificacion(df: pl.DataFrame) -> str:
    contenido = df["pda"].unique()[0]
    pda = df["pda"].unique()[0]
    descriptor = df["descriptor"].unique()[0]
    criterio = df["criterio"].unique()[0]
    especificacion = f"""
                    **Contenido:** {contenido}\n
                    **PDA:** {pda}\n
                    **Descriptor:** {descriptor}\n
                    **Criterio:** {criterio}
                    """
    return especificacion


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

tab_ser, tab_sex, tab_ent = st.tabs(["Servicio", "Sexo", "Entidad"])

#### Resultados por servicio ####
with tab_ser:
    st.markdown("## Resultados por servicio")
    i_ser_sel = i_servicio.filter(pl.col("nivel_grado") == sel_nivel_grado)

    for campo in campos:
        st.markdown(f"### {campo}")
        i_ser_campo = i_ser_sel.filter(pl.col("campo") == campo)
        items = i_ser_campo.sort("item")["item"].unique(maintain_order=True)
        for i in items:
            st.markdown(f"**{i}**")
            i_ser_item = i_ser_campo.filter(pl.col("item") == i).sort("servicio", descending=True)
            plot_ser_campo = ph.plot_bar(i_ser_item, "servicio", "respuesta")
            st.plotly_chart(plot_ser_campo, key=f"i_servicio_{campo}_{i}")
            with st.expander("Ver especificaciones."):
                st.markdown(get_especificacion(i_ser_item))


#### Resultados por sexo ####
with tab_sex:
    st.markdown("## Resultados por sexo")
    i_sex_sel = i_sexo.filter(pl.col("nivel_grado") == sel_nivel_grado)

    for campo in campos:
        st.markdown(f"**{campo}**")
        i_sex_campo = i_sex_sel.filter(pl.col("campo") == campo)
        items = i_sex_campo.sort("item")["item"].unique(maintain_order=True)
        for i in items:
            st.markdown(i)
            i_sex_item = i_sex_campo.filter(pl.col("item") == i).sort("sexo", descending=True)
            plot_sex_campo = ph.plot_bar(i_sex_item, "sexo", "respuesta")
            st.plotly_chart(plot_sex_campo, key=f"i_sexo_{campo}_{i}")
            with st.expander("Ver especificaciones."):
                st.markdown(get_especificacion(i_sex_item))


#### Resultados por entidad ####
with tab_ent:
    st.markdown("## Resultados por entidad")
    i_ent_sel = i_entidad.filter(pl.col("nivel_grado") == sel_nivel_grado)
    for campo in campos:
        st.markdown(f"**{campo}**")
        i_ent_campo = i_ent_sel.filter(pl.col("campo") == campo)
        items = i_ent_campo.sort("item")["item"].unique(maintain_order=True)
        for i in items:
            st.markdown(i)
            i_ent_item = i_ent_campo.filter(pl.col("item") == i).sort("entidad", descending=True)
            plot_ent_campo = ph.plot_bar(i_ent_item, "entidad", "respuesta")
            st.plotly_chart(plot_ent_campo, key=f"i_entidad_{campo}_{i}")
            with st.expander("Ver especificaciones."):
                st.markdown(get_especificacion(i_ent_item))
