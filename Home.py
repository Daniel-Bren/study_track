import streamlit as st
import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.navegacao import mostrar_navegacao
from utils.auth import verificar_sessao
from utils.data_manager import (
    carregar_editais_usuario_db,
    carregar_grade_db,
    get_edital_ativo
)

st.set_page_config(
    page_title="StudyTrack",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

mostrar_navegacao()
verificar_sessao()

# Carrega dados
usuario = carregar_editais_usuario_db()
edital_ativo = get_edital_ativo()

if edital_ativo not in usuario and len(usuario) > 0:
    edital_ativo = list(usuario.keys())[0]

# ---- CABEÇALHO ----
col_titulo, col_edital = st.columns([3, 1])

with col_titulo:
    st.title("📚 StudyTrack")
    st.caption("Organize. Faça. Conquiste.")

with col_edital:
    if edital_ativo:
        st.markdown(
            f"<div style='background:#1a1a2e; color:white; padding:8px 14px; "
            f"border-radius:10px; font-size:13px; margin-top:16px; text-align:center;'>"
            f"📌 <b>{edital_ativo}</b></div>",
            unsafe_allow_html=True
        )

st.markdown("---")

# ---- CARDS DAS ABAS ----
c1, c2, c3 = st.columns(3)

with c1:
    st.markdown("""
    <div style='background:var(--color-background-secondary); padding:20px; 
                border-radius:12px; border:1px solid var(--color-border-tertiary);
                min-height:140px;'>
        <div style='font-size:28px;'>📅</div>
        <div style='font-weight:500; font-size:16px; margin:8px 0 4px;'>Grade de Estudos</div>
        <div style='font-size:13px; color:var(--color-text-secondary);'>
            Monte seu cronograma semanal. Defina quais disciplinas estudar em cada dia da semana.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/1_Grade_de_Estudos.py", label="Abrir Grade →")

with c2:
    st.markdown("""
    <div style='background:var(--color-background-secondary); padding:20px; 
                border-radius:12px; border:1px solid var(--color-border-tertiary);
                min-height:140px;'>
        <div style='font-size:28px;'>📋</div>
        <div style='font-weight:500; font-size:16px; margin:8px 0 4px;'>Edital Verticalizado</div>
        <div style='font-size:13px; color:var(--color-text-secondary);'>
            Acompanhe tópicos e subtópicos do seu edital. Marque o que já estudou.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/2_Edital_Verticalizado.py", label="Abrir Edital →")

with c3:
    st.markdown("""
    <div style='background:var(--color-background-secondary); padding:20px; 
                border-radius:12px; border:1px solid var(--color-border-tertiary);
                min-height:140px;'>
        <div style='font-size:28px;'>⏱️</div>
        <div style='font-weight:500; font-size:16px; margin:8px 0 4px;'>Sessão de Estudo</div>
        <div style='font-size:13px; color:var(--color-text-secondary);'>
            Inicie sua sessão diária. Use o cronômetro ou temporizador para medir seu tempo.
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/3_Sessao_de_Estudo.py", label="Iniciar Sessão →")

st.markdown("---")

# ---- PROGRESSO ----
if len(usuario) > 0 and edital_ativo and edital_ativo in usuario:
    disciplinas = usuario[edital_ativo].get("disciplinas", {})

    if len(disciplinas) > 0:
        total_geral = 0
        estudados_geral = 0

        for topicos in disciplinas.values():
            for subtopicos in topicos.values():
                for feito in subtopicos.values():
                    total_geral += 1
                    if feito:
                        estudados_geral += 1

        percentual_geral = estudados_geral / total_geral if total_geral > 0 else 0

        col_p1, col_p2, col_p3 = st.columns([2, 1, 1])
        with col_p1:
            st.caption(f"📊 Progresso — {edital_ativo}")
            st.progress(percentual_geral)
        with col_p2:
            st.metric("Concluídos", f"{estudados_geral}/{total_geral}")
        with col_p3:
            st.metric("Progresso", f"{int(percentual_geral * 100)}%")