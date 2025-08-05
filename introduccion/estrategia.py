import streamlit as st
from os import path


def mostrar_md(archivo: str, directorio: str = "markdown") -> str:
    texto_ruta = path.join(directorio, archivo)
    with open(texto_ruta, encoding="utf-8") as t:
        texto = t.read()
    return texto


pares = {
    "Estrategia": "02_00_estrategia.md",
    "Muestra": "02_01_muestra.md",
    "Levantamiento": "02_02_levantamiento.md",
    "Sistemas": "02_03_sistemas.md",
    "Generacion de resultados": "02_04_generacion.md",
    "Devolución de resultados": "02_05_devolucion.md",
}

for tab, ruta in zip(st.tabs(pares.keys()), pares.values()):
    with tab:
        st.markdown(mostrar_md(ruta))
