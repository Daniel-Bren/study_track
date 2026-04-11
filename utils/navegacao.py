import streamlit as st

def mostrar_navegacao():

    st.markdown("""
        <style>
            [data-testid="stSidebarNav"] {display: none;}
            .block-container {padding-top: 3.5rem !important;}
            hr {margin-top: 0.3rem !important; margin-bottom: 0.3rem !important;}
        </style>
    """, unsafe_allow_html=True)

    st.components.v1.html("""
    <div style="display:flex; flex-direction:row; gap:8px; 
                flex-wrap:nowrap; overflow-x:auto;
                padding: 4px 0px 8px 0px;">
        <a href="/" target="_self" style="text-decoration:none;">
            <div style="padding:8px 16px; border-radius:8px; 
                        background:#f0f2f6; color:#333;
                        font-size:14px; white-space:nowrap;
                        border:1px solid #ddd; cursor:pointer;">
                 Home
            </div>
        </a>
        <a href="/1_Grade_de_Estudos" target="_self" style="text-decoration:none;">
            <div style="padding:8px 16px; border-radius:8px;
                        background:#f0f2f6; color:#333;
                        font-size:14px; white-space:nowrap;
                        border:1px solid #ddd; cursor:pointer;">
                 Grade
            </div>
        </a>
        <a href="/2_Edital_Verticalizado" target="_self" style="text-decoration:none;">
            <div style="padding:8px 16px; border-radius:8px;
                        background:#f0f2f6; color:#333;
                        font-size:14px; white-space:nowrap;
                        border:1px solid #ddd; cursor:pointer;">
                 Edital
            </div>
        </a>
        <a href="/3_Sessao_de_Estudo" target="_self" style="text-decoration:none;">
            <div style="padding:8px 16px; border-radius:8px;
                        background:#f0f2f6; color:#333;
                        font-size:14px; white-space:nowrap;
                        border:1px solid #ddd; cursor:pointer;">
                ️ Sessão
            </div>
        </a>
    </div>
    <hr style="margin: 4px 0 8px 0; border:none; border-top:1px solid #ddd;">
    """, height=60)