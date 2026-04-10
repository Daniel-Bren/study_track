import streamlit as st

def mostrar_navegacao():
    st.markdown("""
        <style>
            [data-testid="stSidebarNav"] {display: none;}
            .block-container {padding-top: 3.5rem !important;}
            [data-testid="stPageLink"] {padding: 0px !important;}
            hr {margin-top: 0.3rem !important; margin-bottom: 0.3rem !important;}
            div[data-testid="stRadio"] {
                display: flex;
                justify-content: center;
            }
        </style>
    """, unsafe_allow_html=True)

    paginas = {
        "Home": "Home.py",
        "Grade": "pages/1_Grade_de_Estudos.py",
        "Edital": "pages/2_Edital_Verticalizado.py",
        "Sessão": "pages/3_Sessao_de_Estudo.py"
    }

    cols = st.columns([1, 1, 1, 1, 6])
    for i, (nome, caminho) in enumerate(paginas.items()):
        with cols[i]:
            st.page_link(caminho, label=nome)

    st.markdown("---")