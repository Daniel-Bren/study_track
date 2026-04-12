# utils/auth.py

import streamlit as st
from utils.supabase_client import get_supabase

def verificar_sessao():
    """
    Verifica se o usuario esta logado.
    Se nao estiver, redireciona pro login.
    """
    if "usuario" not in st.session_state:
        st.session_state["usuario"] = None

    if st.session_state["usuario"] is None:
        st.switch_page("pages/0_Login.py")

def carregar_sessao():
    """Retorna o usuario logado ou None"""
    if "usuario" in st.session_state:
        return st.session_state["usuario"]
    return None

def fazer_logout():
    """Remove a sessao do usuario"""
    try:
        supabase = get_supabase()
        supabase.auth.sign_out()
    except:
        pass
    st.session_state["usuario"] = None
    st.switch_page("pages/0_Login.py")

def is_admin():
    """
    Verifica se o usuario logado e administrador
    consultando o campo is_admin no Supabase.
    """
    if "usuario" not in st.session_state or not st.session_state["usuario"]:
        return False

    try:
        supabase = get_supabase()
        resposta = supabase.table("perfis") \
            .select("is_admin") \
            .eq("id", st.session_state["usuario"].id) \
            .execute()

        if resposta.data:
            return resposta.data[0]["is_admin"]
        return False
    except:
        return False