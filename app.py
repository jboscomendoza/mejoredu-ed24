import streamlit as st

pages = {
    "Desarrollo": [
        st.Page("desarrollo_general.py", title="Resultados generales"),
        st.Page("desarrollo_comparativos.py", title="Comparativos"),
    ],
    "Puntajes": [st.Page("scores_general.py", title="Resultados generales")],
}

navigation = st.navigation(pages)
navigation.run()
