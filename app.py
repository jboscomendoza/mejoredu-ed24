import streamlit as st

pages = {
    "1. Desarrollo": [
        st.Page("desarrollo_general.py", title="1.1 Resultados generales"),
        st.Page("desarrollo_comparativos.py", title="1.2 Comparativos"),
    ],
    "2. Puntajes": [
        st.Page("scores_general.py", title="2.1 Resultados generales"),
        st.Page("scores_comparativos.py", title="2.2 Comparativos"),
    ],
}

navigation = st.navigation(pages)
navigation.run()
