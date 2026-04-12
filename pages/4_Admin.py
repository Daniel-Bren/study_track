# pages/4_Admin.py

import streamlit as st
import sys
import os
import json

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.navegacao import mostrar_navegacao
from utils.auth import verificar_sessao, is_admin
from utils.data_manager import (
    carregar_editais_plataforma_db,
    salvar_edital_plataforma_db,
    deletar_edital_plataforma_db
)

st.set_page_config(
    page_title="Admin — StudyTrack",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

mostrar_navegacao()
verificar_sessao()

if not is_admin():
    st.error("Acesso negado!")
    st.stop()

st.title("⚙️ Painel de Administração")
st.markdown("---")

editais_plataforma = carregar_editais_plataforma_db()

st.subheader("📤 Importar Edital via JSON")

st.markdown("""
O arquivo JSON deve seguir este formato:
```json
{
    "Nome do Edital": {
        "disciplinas": {
            "Nome da Disciplina": {
                "Nome do Tópico": {
                    "Nome do Subtópico": false
                }
            }
        }
    }
}
```
""")

arquivo = st.file_uploader("Selecione o arquivo JSON", type="json")

if arquivo is not None:
    try:
        conteudo = json.load(arquivo)
        st.success("Arquivo lido com sucesso!")
        st.text(str(list(conteudo.keys())))

        if st.button("✅ Confirmar importação"):
            for nome, dados in conteudo.items():
                disciplinas = dados.get("disciplinas", {})
                salvar_edital_plataforma_db(nome, disciplinas)
            st.success("Editais importados com sucesso!")
            st.rerun()

    except Exception as e:
        st.error(f"Erro ao ler o arquivo: {e}")

st.markdown("---")

st.subheader("📋 Gerenciar Editais da Plataforma")

editais_plataforma = carregar_editais_plataforma_db()

if len(editais_plataforma) == 0:
    st.info("Nenhum edital cadastrado ainda.")
else:
    edital_remover = st.selectbox(
        label="Selecione o edital para remover:",
        options=list(editais_plataforma.keys())
    )
    if st.button("🗑️ Remover edital selecionado"):
        deletar_edital_plataforma_db(edital_remover)
        st.success(f"Edital '{edital_remover}' removido!")
        st.rerun()