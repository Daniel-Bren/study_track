import streamlit as st
from utils.navegacao import mostrar_navegacao

st.set_page_config(
    page_title="StudyTrack",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

mostrar_navegacao()

st.title("📚 StudyTrack")
st.subheader("Organize. Faça. Conquiste.")
st.markdown("---")

st.markdown("""
### Bem vindo!

- 📅 **Grade de Estudos** — monte seu cronograma semanal
- 📋 **Edital Verticalizado** — acompanhe seus tópicos
- 📊 **Progresso** — veja sua evolução
""")