import streamlit as st

st.set_page_config(
    page_title="StudyTrack",
    page_icon="",
    layout="wide"
)

st.title("StudyTrack")
st.subheader("Seu edital verticalizado e grade de estudos em um só lugar.")

st.markdown("---")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label= "Disciplinas cadastradas", value="0")

with col2:
    st.metric(label="Tópicos estudados", value="0%")

with col3:
    st.metric(label="Horas esta semana", value="0h")

st.markdown("---")
st.info("Use o menu lateral para navegar entre as seções.")