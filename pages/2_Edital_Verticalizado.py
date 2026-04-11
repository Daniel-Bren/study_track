import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.data_manager import (
    carregar_editais_plataforma,
    carregar_editais_usuario_db,
    salvar_edital_usuario_db,
)
from utils.navegacao import mostrar_navegacao
from utils.auth import verificar_sessao

st.set_page_config(
    page_title="Edital Verticalizado",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="collapsed"
)

mostrar_navegacao()
verificar_sessao()

# Carrega os dois tipos de edital
plataforma = carregar_editais_plataforma()
usuario    = carregar_editais_usuario_db()

# ---- SEÇÃO 1: Editais da plataforma ----
st.subheader("Editais Prontos")

if len(plataforma) == 0:
    st.info("Nenhum edital disponível na plataforma ainda.")
else:
    edital_selecionado = st.selectbox(
        label="Selecione um edital:",
        options=list(plataforma.keys())
    )

    if st.button("Utilizar este edital"):
        if edital_selecionado in usuario:
            st.warning("Você já adicionou este edital!")
        else:
            disciplinas = plataforma[edital_selecionado].get("disciplinas", {})
            salvar_edital_usuario_db(edital_selecionado, disciplinas, origem="plataforma")
            st.success(f"Edital '{edital_selecionado}' adicionado!")
            st.rerun()

st.markdown("---")

# ---- SEÇÃO 2: Adicionar edital manualmente ----
st.subheader("Criar edital")
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
                salvar_edital_usuario_db(nome_edital, {}, origem="manual")
                st.success(f"Edital '{nome_edital}' adicionado com sucesso!")
                st.rerun()

# ---- SEÇÃO 2.5: Gerenciar disciplinas, tópicos e subtópicos ----
usuario = carregar_editais_usuario_db()

if len(usuario) > 0:
    with st.expander("⚙️ Gerenciar conteúdo do edital"):

        editais_editaveis = [
            nome for nome, dados in usuario.items()
            if dados.get("origem") != "plataforma"
        ]

        if len(editais_editaveis) == 0:
            st.info("Você não possui editais próprios para gerenciar.")
        else:
            edital_gerenciar = st.selectbox(
                label="Selecione o edital para gerenciar:",
                options=editais_editaveis,
                key="selectbox_gerenciar_editavel"
            )

            st.markdown("---")

            # ---- Adicionar disciplina ----
            st.markdown("**📚 Adicionar disciplina**")
            with st.form("form_disciplina"):
                nome_disc_novo = st.text_input("Nome da disciplina (ex: Língua Portuguesa)")
                botao_disc = st.form_submit_button("Adicionar disciplina")

                if botao_disc:
                    if nome_disc_novo == "":
                        st.error("Digite o nome da disciplina!")
                    elif nome_disc_novo in usuario[edital_gerenciar]["disciplinas"]:
                        st.warning("Essa disciplina já existe!")
                    else:
                        usuario[edital_gerenciar]["disciplinas"][nome_disc_novo] = {}
                        salvar_edital_usuario_db(
                            edital_gerenciar,
                            usuario[edital_gerenciar]["disciplinas"]
                        )
                        st.success(f"Disciplina '{nome_disc_novo}' adicionada!")
                        st.rerun()

            st.markdown("---")

            # ---- Adicionar tópico ----
            st.markdown("**📖 Adicionar tópico**")
            disciplinas_existentes = list(usuario[edital_gerenciar]["disciplinas"].keys())

            if len(disciplinas_existentes) == 0:
                st.info("Adicione uma disciplina primeiro!")
            else:
                with st.form("form_topico"):
                    disc_escolhida = st.selectbox(
                        label="Disciplina:",
                        options=disciplinas_existentes
                    )
                    nome_topico_novo = st.text_input("Nome do tópico")
                    botao_topico = st.form_submit_button("Adicionar tópico")

                    if botao_topico:
                        if nome_topico_novo == "":
                            st.error("Digite o nome do tópico!")
                        elif nome_topico_novo in usuario[edital_gerenciar]["disciplinas"][disc_escolhida]:
                            st.warning("Esse tópico já existe!")
                        else:
                            usuario[edital_gerenciar]["disciplinas"][disc_escolhida][nome_topico_novo] = {}
                            salvar_edital_usuario_db(
                                edital_gerenciar,
                                usuario[edital_gerenciar]["disciplinas"]
                            )
                            st.success(f"Tópico '{nome_topico_novo}' adicionado!")
                            st.rerun()

            st.markdown("---")

            # ---- Adicionar subtópico ----
            st.markdown("**📝 Adicionar subtópico**")

            if len(disciplinas_existentes) == 0:
                st.info("Adicione uma disciplina primeiro!")
            else:
                with st.form("form_subtopico"):
                    disc_sub = st.selectbox(
                        label="Disciplina:",
                        options=disciplinas_existentes,
                        key="disc_sub"
                    )
                    topicos_existentes = list(usuario[edital_gerenciar]["disciplinas"][disc_sub].keys())

                    if len(topicos_existentes) == 0:
                        st.warning("Essa disciplina não tem tópicos ainda!")
                        st.form_submit_button("Adicionar subtópico", disabled=True)
                    else:
                        topico_sub = st.selectbox(
                            label="Tópico:",
                            options=topicos_existentes
                        )
                        nome_sub_novo = st.text_input("Nome do subtópico")
                        botao_sub = st.form_submit_button("Adicionar subtópico")

                        if botao_sub:
                            if nome_sub_novo == "":
                                st.error("Digite o nome do subtópico!")
                            elif nome_sub_novo in usuario[edital_gerenciar]["disciplinas"][disc_sub][topico_sub]:
                                st.warning("Esse subtópico já existe!")
                            else:
                                usuario[edital_gerenciar]["disciplinas"][disc_sub][topico_sub][nome_sub_novo] = False
                                salvar_edital_usuario_db(
                                    edital_gerenciar,
                                    usuario[edital_gerenciar]["disciplinas"]
                                )
                                st.success(f"Subtópico '{nome_sub_novo}' adicionado!")
                                st.rerun()

st.markdown("---")

# ---- SEÇÃO 3: Meus editais ----
st.subheader("📚 Meus Editais")
usuario = carregar_editais_usuario_db()

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
            total = 0
            estudados = 0

            for subtopicos in topicos.values():
                for feito in subtopicos.values():
                    total += 1
                    if feito:
                        estudados += 1

            if total > 0:
                percentual = estudados / total
            else:
                percentual = 0

            with st.expander(f"{nome_disc} — {estudados}/{total} concluídos"):
                st.progress(percentual)

                for nome_topico, subtopicos in topicos.items():
                    st.markdown(f"**📖 {nome_topico}**")
                    for nome_sub in subtopicos:
                        estudado = subtopicos[nome_sub]
                        marcado = st.checkbox(
                            label=nome_sub,
                            value=estudado,
                            key=f"{edital_escolhido}_{nome_disc}_{nome_topico}_{nome_sub}"
                        )
                        if marcado != estudado:
                            usuario[edital_escolhido]["disciplinas"][nome_disc][nome_topico][nome_sub] = marcado
                            salvar_edital_usuario_db(
                                edital_escolhido,
                                usuario[edital_escolhido]["disciplinas"]
                            )
                            st.rerun()