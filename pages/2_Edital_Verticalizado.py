import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.data_manager import (
    carregar_editais_plataforma,
    carregar_editais_usuario,
    salvar_editais_usuario,
    adicionar_edital_plataforma
)
from utils.navegacao import mostrar_navegacao

st.set_page_config(
    page_title="Edital Verticalizado",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="collapsed"
)

mostrar_navegacao()

# Carrega os dois tipos de edital
plataforma = carregar_editais_plataforma()
usuario    = carregar_editais_usuario()

# ---- SEÇÃO 1: Editais da plataforma ----
st.subheader("Editais disponíveis na plataforma")

if len(plataforma) == 0:
    st.info("Nenhum edital disponível na plataforma ainda.")
else:
    edital_selecionado = st.selectbox(
        label="Selecione um edital:",
        options=list(plataforma.keys())
    )

    if st.button("Utilizar este edital"):
        resultado = adicionar_edital_plataforma(edital_selecionado)
        if resultado:
            st.success(f"Edital '{edital_selecionado}' adicionado aos seus editais!")
            st.rerun()
        else:
            st.warning("Você já adicionou este edital!")

st.markdown("---")

# ---- SEÇÃO 2: Adicionar edital manualmente ----
with st.expander("Não encontrou seu edital? Adicione manualmente"):
    with st.form("form_edital_manual"):
        nome_edital = st.text_input("Nome do edital (ex: PCCE 2024)")
        botao = st.form_submit_button("Adicionar")

        if botao:
            if nome_edital == "":
                st.error("Digite um nome para o edital!")
            elif nome_edital in usuario:
                st.warning("Você já possui um edital com esse nome!")
            else:
                usuario[nome_edital] = {"disciplinas": {}}
                salvar_editais_usuario(usuario)
                st.success(f"Edital '{nome_edital}' adicionado com sucesso!")
                st.rerun()

st.markdown("---")

# ---- SEÇÃO 3: Meus editais ----
st.subheader("Meus Editais")

if len(usuario) == 0:
    st.info("Você ainda não adicionou nenhum edital.")
else:
    edital_escolhido = st.selectbox(
        label="Selecione um edital para estudar:",
        options=list(usuario.keys()),
        key="selectbox_usuario"
    )

    disciplinas = usuario[edital_escolhido].get("disciplinas", {})

    if len(disciplinas) == 0:
        st.info("Este edital ainda não tem disciplinas cadastradas.")
    else:
        for nome_disc, topicos in disciplinas.items():
            #calcular progresso
            total = 0
            estudados = 0

            for subtopicos in topicos.values():
                for feito in subtopicos.values():
                    total += 1
                    if feito:
                        estudados += 1
            #calcular porcentagem
            if total > 0:
                percentual = estudados / total
            else:
                percentual = 0
            with st.expander(f"{nome_disc} - {estudados}/{total} concluídos"):
                st.progress(percentual)

                for nome_topico, subtopicos in topicos.items():
                    st.markdown(f"** {nome_topico}**")
                    for nome_sub in subtopicos:
                        estudado = subtopicos[nome_sub]
                        marcado = st.checkbox(
                            label=nome_sub,
                            value=estudado,
                            key=f"{edital_escolhido}_{nome_disc}_{nome_topico}_{nome_sub}"
                        )
                        if marcado != estudado:
                            usuario[edital_escolhido]["disciplinas"][nome_disc][nome_topico][nome_sub] = marcado
                            salvar_editais_usuario(usuario)
                            st.rerun()