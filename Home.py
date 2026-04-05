import streamlit as st

st.set_page_config(
    page_title="StudyTrack",
    page_icon="📚",
    layout="wide"
)

st.title("📚 StudyTrack")
st.subheader("Organize. Faça. Conquiste.")
st.markdown("---")

st.markdown("""
### Bem vindo!

Use o menu lateral para navegar entre as seções:

- 📅 **Grade de Estudos** — monte seu cronograma semanal
- 📋 **Edital Verticalizado** — acompanhe seus tópicos
- 📊 **Progresso** — veja sua evolução
""")
