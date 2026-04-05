import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.data_manager import carregar_editais, salvar_editais

st.set_page_config(page_title="Edital Verticalizado", page_icon="📋", layout="wide")

st.title("Edital Verticalizado")
st.markdown("---")

editais = carregar_editais()

st.subheader("Criar novo edital")

with st.form("formm_edital"):
    nome_edital = st.text_input("Nome do edital (ex:PRF 2024)")
    botao = st.form_submit_button("Criar edital")

    if botao:
        if nome_edital == "":
            st.error("Digite um nome para o edital")
        elif nome_edital in editais:
            st.warning("Já existe um edital com esse nome!")
        else:
            editais[nome_edital] = {"disciplinas": {}}
            salvar_editais(editais)
            st.success(f"Edital '{nome_edital}' criado com sucesso!")
st.markdown("---")

st.subheader("Editais cadastrados")

if len(editais) == 0:
    st.info("Nenhum edital cadstrado ainda. Crie um acima!")
else:
    for nome, dados in editais.items():
        st.markdown(f"### {nome}")

st.markdown("---")

# Visualizar editial verticalizado
st.subheader("Visualizar Edital")

if len(editais) == 0:
    st.info("Nenhum edital disponível ainda.")
else:
    edital_escolhido = st.selectbox(
        label="Selecione um edital para estudar:",
        options=list(editais.keys())
    )

    disciplinas = editais[edital_escolhido].get("disciplinas", {})

    if len(disciplinas) == 0:
        st.info("Este edital ainda não tem disciplinas cadastradas.")
    else:
        for nome_disc, topicos in disciplinas.items():
            with st.expander(f"{nome_disc}"):
                for nome_topico, subtopicos in topicos.items():
                    st.markdown(f"***{nome_topico}***")
                    for nome_sub in subtopicos:
                        estudado = subtopicos[nome_sub]
                        marcado = st.checkbox(
                            label=nome_sub,
                            value=estudado,
                            key=f"{edital_escolhido}_{nome_disc}_{nome_topico}_{nome_sub}"
                        )
                        if marcado != estudado:
                            editais[edital_escolhido]["disciplinas"][nome_disc][nome_topico][nome_sub] = marcado
                            salvar_editais(editais)
                            st.rerun()
