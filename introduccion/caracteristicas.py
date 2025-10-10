import streamlit as st
from os import path


def mostrar_md(archivo: str, directorio: str = "markdown") -> str:
    texto_ruta = path.join(directorio, archivo)
    with open(texto_ruta, encoding="utf-8") as t:
        texto = t.read()
    return texto


pares = {
    "Introduccion": "00_00_introduccion.md",
    "Características de la evaluación": "01_00_caracteristicas.md",
    "Referentes curriculares": "01_01_referentes.md",
    "Diseño de los instrumentos": "01_02_diseno.md",
}


st.markdown("# Características de la Evaluación Diagnóstica de los Aprendizajes de las Alumnas y los Alumnos de Educación Básica Ciclo Escolar 2024-2025")

for tab, ruta in zip(st.tabs(pares.keys()), pares.values()):
    with tab:
        st.markdown(mostrar_md(ruta))
