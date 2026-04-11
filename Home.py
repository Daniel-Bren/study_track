import streamlit as st
from utils.navegacao import mostrar_navegacao

st.set_page_config(
    page_title="StudyTrack",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

mostrar_navegacao()
from utils.auth import carregar_sessao
# Restaura sessao do cookie se necessario
if "usuario" not in st.session_state or st.session_state["usuario"] is None:
    usuario = carregar_sessao()
    if usuario:
        st.session_state["usuario"] = usuario
    else:
        st.switch_page("pages/0_Login.py")

st.title("📚 StudyTrack")
st.subheader("Organize. Faça. Conquiste.")


st.markdown("""
### Bem vindo!

- 📅 **Grade de Estudos** — monte seu cronograma semanal
- 📋 **Edital Verticalizado** — acompanhe seus tópicos
- 📚 **Sessão** — Comece a sua sessão diária de estudos
""")