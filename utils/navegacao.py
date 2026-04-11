import streamlit as st


def mostrar_navegacao():
    st.markdown("""
        <style>
            [data-testid="stSidebarNav"] {display: none;}
            .block-container {padding-top: 3.5rem !important;}
            hr {margin-top: 0.3rem !important; margin-bottom: 0.3rem !important;}

            /* Força colunas em linha horizontal sempre */
            div[class*="stColumns"] {
                display: flex !important;
                flex-direction: row !important;
                flex-wrap: nowrap !important;
                overflow-x: auto !important;
            }
            div[class*="stColumns"] > div[class*="stColumn"] {
                min-width: fit-content !important;
                flex: none !important;
                width: auto !important;
            }
            [data-testid="stPageLink"] p {
                font-size: 13px !important;
                white-space: nowrap !important;
            }
        </style>
    """, unsafe_allow_html=True)

    paginas = {
        "Home": "Home.py",
        "Grade": "pages/1_Grade_de_Estudos.py",
        "Edital": "pages/2_Edital_Verticalizado.py",
        "Sessão": "pages/3_Sessao_de_Estudo.py"
    }

    cols = st.columns(len(paginas))
    for i, (nome, caminho) in enumerate(paginas.items()):
        with cols[i]:
            st.page_link(caminho, label=nome)

    st.markdown("---")