import streamlit as st
import sys
import os
#Encontrar a pasta utils
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.data_manager import carregar_editais, salvar_editais

#Titulo
st.title("Grade de Estudos")
st.markdown("""---""")

#Carrega Editais Salvos
editais = carregar_editais()

st.subheader("Selecione seu edital:")

if len(editais) == 0:
    st.warning("Nenhum edital cadastrado ainda.")
else:
    edital_escolhido = st.selectbox(
        label="Qual edital você está estudando?",
        options=list(editais.keys())
    )

