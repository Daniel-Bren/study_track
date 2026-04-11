import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.supabase_client import get_supabase

st.set_page_config(
    page_title="Login — StudyTrack",
    page_icon="🔐",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Esconde navegacao
st.markdown("""
    <style>
        [data-testid="stSidebarNav"] {display: none;}
    </style>
""", unsafe_allow_html=True)

st.title("📚 StudyTrack")
st.subheader("Comece sua sessão de estudos agora!")
st.markdown("---")

# Inicializa session_state
if "usuario" not in st.session_state:
    st.session_state["usuario"] = None

# Se já está logado, redireciona
if st.session_state["usuario"]:
    st.switch_page("Home.py")

# Abas de login e cadastro
aba = st.radio(
    label="",
    options=["🔑 Entrar", "📝 Cadastrar"],
    horizontal=True
)
supabase = get_supabase()

# ---- LOGIN ----
if aba == "🔑 Entrar":
    with st.form("form_login"):
        email = st.text_input("Email")
        senha = st.text_input("Senha", type="password")
        botao = st.form_submit_button("Entrar")

        if botao:
            if email == "" or senha == "":
                st.error("Preencha todos os campos!")
            else:
                try:
                    resposta = supabase.auth.sign_in_with_password({
                        "email": email,
                        "password": senha
                    })
                    st.session_state["usuario"] = resposta.user
                    # Salva o token no cookie
                    from utils.auth import salvar_sessao

                    salvar_sessao(resposta.session.access_token)
                    st.success("Login realizado com sucesso!")
                    st.switch_page("Home.py")
                except Exception as e:
                    st.error("Email ou senha incorretos!")

# ---- CADASTRO ----
if aba == "📝 Cadastrar":
    with st.form("form_cadastro"):
        nome = st.text_input("Nome completo")
        email = st.text_input("Email")
        senha = st.text_input("Senha", type="password")
        senha2 = st.text_input("Confirme a senha", type="password")
        botao = st.form_submit_button("Cadastrar")

        if botao:
            if nome == "" or email == "" or senha == "":
                st.error("Preencha todos os campos!")
            elif senha != senha2:
                st.error("As senhas não coincidem!")
            else:
                try:
                    resposta = supabase.auth.sign_up({
                        "email": email,
                        "password": senha,
                        "options": {"data": {"nome": nome}}
                    })
                    st.success("Conta criada! Verifique seu email para confirmar.")
                except Exception as e:
                    st.error(f"Erro ao cadastrar: {e}")