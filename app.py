import streamlit as st


desarrollo_general = st.Page(
    page="desarrollo/desarrollo_general.py",
    title="1.1 Resultados generales",
    icon="📗",
)
desarrollo_comparativos = st.Page(
    page="desarrollo/desarrollo_comparativos.py",
    title="1.2 Comparativos",
    icon="📗",
)
scores_general = st.Page(
    page="scores/scores_general.py",
    title="2.1 Resultados generales",
    icon="📘",
)
scores_comparativos = st.Page(
    page="scores/scores_comparativos.py", title="2.2 Comparativos", icon="📘"
)
items_general = st.Page(
    page="items/items_general.py", title="3.1 Resultados generales", icon="📙"
)
items_comparativos = st.Page(
    page="items/items_comparativos.py", title="3.2 Comparativos", icon="📙"
)

pages = {
    "1. Desarrollo": [
        desarrollo_general,
        desarrollo_comparativos,
    ],
    "2. Puntajes": [
        scores_general,
        scores_comparativos,
    ],
    "3. Items": [
        items_general,
        items_comparativos,
    ],
}

navigation = st.navigation(pages)
navigation.run()
