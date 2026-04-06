import streamlit as st
from utils.navegacao import mostrar_navegacao

st.set_page_config(
    page_title="Progresso",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

mostrar_navegacao()