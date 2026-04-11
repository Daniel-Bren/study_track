import streamlit as st
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.data_manager import (
    carregar_editais_usuario,
    carregar_json,
    salvar_json,
    GRADE_FILE
)
from utils.navegacao import mostrar_navegacao

st.set_page_config(
    page_title="Grade de Estudos",
    page_icon="📅",
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

# Configuracao de sessao
if "alterou_grade" not in st.session_state:
    st.session_state["alterou_grade"] = False

if "edital_grade" not in st.session_state:
    st.session_state["edital_grade"] = None

# Carrega dados do usuario
usuario = carregar_editais_usuario()

# Redirecionamento
if len(usuario) == 0:
    st.title("Grade de Estudos")
    st.warning("Você ainda não adicionou nenhum edital!")
    st.page_link("pages/2_Edital_Verticalizado.py", label="Ir para Edital Verticalizado", icon="📋")
    st.stop()

# Cabecalho
st.title("Grade de Estudos")
st.markdown("---")

# Seletor edital
col_edital, col_vazia = st.columns([2, 5])

with col_edital:
    edital_escolhido = st.selectbox(
        label="Edital atual",
        options=list(usuario.keys()),
        index=0,
        key="selectbox_edital_grade"
    )

# Detecta troca de edital
if st.session_state["edital_grade"] != edital_escolhido:
    st.session_state["edital_grade"] = edital_escolhido
    st.session_state["alterou_grade"] = False

st.markdown("---")

# Carrega grades salvas
todas_grades = carregar_json(GRADE_FILE)

# Dias da semana — definido antes de tudo que usa essa variavel
dias = ["Segunda-Feira", "Terça-Feira", "Quarta-Feira", "Quinta-Feira", "Sexta-Feira", "Sábado", "Domingo"]

# Se nao existir grade pra esse edital, cria uma vazia
if edital_escolhido not in todas_grades:
    todas_grades[edital_escolhido] = {
        dia: ["-", "-", "-", "-", "-", "-"]
        for dia in dias
    }

grade_atual = todas_grades[edital_escolhido]

# Disciplinas disponiveis
disciplinas = list(usuario[edital_escolhido].get("disciplinas", {}).keys())
opcoes = ["-"] + disciplinas

# Pre-popula session_state com valores salvos no JSON
for dia in dias:
    for bloco in range(6):
        chave = f"grade_{edital_escolhido}_{dia}_{bloco}"
        if chave not in st.session_state:
            valor = grade_atual[dia][bloco]
            st.session_state[chave] = valor if valor in opcoes else "-"

# Grade visual
colunas = st.columns(7)
nova_grade = {}

for i, dia in enumerate(dias):
    with colunas[i]:
        st.markdown(f"**{dia}**")
        blocos_dia = []

        for bloco in range(6):
            valor_atual = grade_atual[dia][bloco]

            escolha = st.selectbox(
                label=f"Bloco {bloco + 1}",
                options=opcoes,
                key=f"grade_{edital_escolhido}_{dia}_{bloco}",
                label_visibility="collapsed"
            )

            # Detecta alteracao
            if escolha != valor_atual:
                st.session_state["alterou_grade"] = True

            blocos_dia.append(escolha)

        nova_grade[dia] = blocos_dia

# Botao salvar
st.markdown("---")

if st.session_state["alterou_grade"]:
    if st.button("Salvar"):
        todas_grades[edital_escolhido] = nova_grade
        salvar_json(GRADE_FILE, todas_grades)
        st.session_state["alterou_grade"] = False
        st.success("Grade salva com sucesso!")
        st.rerun()