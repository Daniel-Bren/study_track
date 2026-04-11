import streamlit as st
import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from utils.data_manager import carregar_editais_usuario, carregar_json, GRADE_FILE
from utils.navegacao import mostrar_navegacao

st.set_page_config(
    page_title="Sessão de Estudo",
    page_icon="⏱️",
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

st.title("Sessão de Estudo")
st.markdown("---")

# ---- DISCIPLINAS DE HOJE ----
usuario = carregar_editais_usuario()
todas_grades = carregar_json(GRADE_FILE)

dia_semana = datetime.now().strftime("%A")
traducao = {
    "Monday": "Segunda-Feira",
    "Tuesday": "Terça-Feira",
    "Wednesday": "Quarta-Feira",
    "Thursday": "Quinta-Feira",
    "Friday": "Sexta-Feira",
    "Saturday": "Sábado",
    "Sunday": "Domingo"
}
hoje = traducao[dia_semana]

col_esq, col_dir = st.columns([1, 2])

with col_esq:
    st.subheader(f"Hoje — {hoje}")

    if len(usuario) == 0:
        st.info("Nenhum edital adicionado ainda.")
    else:
        edital_sessao = st.selectbox(
            label="Edital:",
            options=list(usuario.keys()),
            key="selectbox_sessao"
        )

        if edital_sessao in todas_grades:
            blocos_hoje = todas_grades[edital_sessao][hoje]
            disciplinas_hoje = [b for b in blocos_hoje if b != "-"]

            if len(disciplinas_hoje) == 0:
                st.info("Nenhuma disciplina na grade de hoje.")
            else:
                st.markdown("**Disciplinas de hoje:**")
                for disc in disciplinas_hoje:
                    st.markdown(f"{disc}")
        else:
            st.info("Nenhuma grade montada para este edital.")

with col_dir:
    st.markdown("<h2 style='text-align:center'>Relógio de Estudo</h2>", unsafe_allow_html=True)

    minutos = 25

    st.components.v1.html(f"""
    <div style="text-align:center; padding: 20px;">

        <div style="display:flex; justify-content:center; gap:24px; margin-bottom:20px;">
            <label style="color:var(--text-color,#333); font-size:16px; 
              cursor:pointer; display:flex; align-items:center; gap:6px;">
    <input type="radio" name="modo" value="Cronometro" checked
           onchange="trocarModo(this.value)"
           style="width:18px; height:18px; cursor:pointer;">
    <span>⏱ Cronômetro</span>
            </label>
            <label style="color:var(--text-color,#333); font-size:16px; 
                          cursor:pointer; display:flex; align-items:center; gap:6px;">
                <input type="radio" name="modo" value="Temporizador"
                       onchange="trocarModo(this.value)"
                       style="width:18px; height:18px; cursor:pointer;">
                <span>⏳ Temporizador</span>
            </label>
        </div>

        <div id="input-minutos" style="display:none; margin-bottom:16px;">
            <input type="number" id="minutos-input" value="25"
                   min="1" max="120"
                   style="padding:8px; font-size:16px; border-radius:8px;
                          border:none; width:80px; text-align:center;">
            <span style="color:white; font-size:16px;"> minutos</span>
        </div>

        <div id="display" style="font-size:80px; font-weight:bold;
             font-family:monospace; color:#ffffff; margin-bottom:20px;">
            00:00
        </div>

        <div style="display:flex; gap:12px; justify-content:center;">
            <button onclick="iniciar()" style="padding:12px 28px; font-size:16px;
                background:#1f77b4; color:white; border:none;
                border-radius:8px; cursor:pointer;">
                ▶ 
            </button>
            <button onclick="pausar()" style="padding:12px 28px; font-size:16px;
                background:#ff7f0e; color:white; border:none;
                border-radius:8px; cursor:pointer;">
                ⏸ 
            </button>
            <button onclick="resetar()" style="padding:12px 28px; font-size:16px;
                background:#d62728; color:white; border:none;
                border-radius:8px; cursor:pointer;">
    <script>
        var modoAtual = "Cronometro";
        var totalSegundos = 0;
        var rodando = false;
        var intervalo = null;

        function trocarModo(novoModo) {{
            modoAtual = novoModo;
            var inputDiv = document.getElementById("input-minutos");
            inputDiv.style.display = novoModo === "Temporizador" ? "block" : "none";
            resetar();
        }}

        function atualizar() {{
            var min = Math.floor(totalSegundos / 60);
            var seg = totalSegundos % 60;
            document.getElementById("display").innerText =
                String(min).padStart(2, "0") + ":" + String(seg).padStart(2, "0");
        }}

        function iniciar() {{
            if (rodando) return;
            rodando = true;
            intervalo = setInterval(function() {{
                if (modoAtual === "Cronometro") {{
                    totalSegundos++;
                }} else {{
                    if (totalSegundos <= 0) {{
                        clearInterval(intervalo);
                        rodando = false;
                        document.getElementById("display").innerText = "Fim!";
                        return;
                    }}
                    totalSegundos--;
                }}
                atualizar();
            }}, 1000);
        }}

        function pausar() {{
            clearInterval(intervalo);
            rodando = false;
        }}

        function resetar() {{
            clearInterval(intervalo);
            rodando = false;
            var min = parseInt(document.getElementById("minutos-input").value || 25);
            totalSegundos = modoAtual === "Temporizador" ? min * 60 : 0;
            atualizar();
        }}

        atualizar();
    </script>
    """, height=320)