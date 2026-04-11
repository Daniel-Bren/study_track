# utils/auth.py

import streamlit as st
from utils.supabase_client import get_supabase
import extra_streamlit_components as stx


def get_cookie_manager():
    """Retorna o gerenciador de cookies"""
    return stx.CookieManager()


def salvar_sessao(token):
    """
    Salva o token de sessão no cookie.

    Entrada: token → string com o token de autenticação
    Saída: nenhuma
    """
    cookie_manager = get_cookie_manager()
    cookie_manager.set(
        cookie="study_track_token",
        val=token,
        expires_at=None  # expira quando fechar o browser
    )


def carregar_sessao():
    """
    Tenta restaurar a sessão a partir do cookie salvo.
    Retorna o usuário se encontrar, None se não encontrar.
    """
    cookie_manager = get_cookie_manager()
    token = cookie_manager.get("study_track_token")

    if not token:
        return None

    try:
        supabase = get_supabase()
        resposta = supabase.auth.get_user(token)
        return resposta.user
    except:
        return None


def apagar_sessao():
    """
    Remove o cookie de sessão — usado no logout.
    """
    cookie_manager = get_cookie_manager()
    cookie_manager.delete("study_track_token")
    st.session_state["usuario"] = None

def verificar_sessao():
    """
    Verifica se o usuario esta logado.
    Se nao estiver, redireciona pro login.
    """
    if "usuario" not in st.session_state:
        st.session_state["usuario"] = None

    if st.session_state["usuario"] is None:
        usuario = carregar_sessao()
        if usuario:
            st.session_state["usuario"] = usuario
        else:
            st.switch_page("pages/0_Login.py")

def fazer_logout():
    """Remove a sessao do usuario"""
    try:
        supabase = get_supabase()
        supabase.auth.sign_out()
    except:
        pass
    apagar_sessao()
    st.switch_page("pages/0_Login.py")