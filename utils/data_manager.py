import json
import os
from utils.supabase_client import get_supabase
import streamlit as st

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

EDITAIS_FILE            = os.path.join(DATA_DIR, "editais.json")
GRADE_FILE              = os.path.join(DATA_DIR, "grade.json")
EDITAIS_PLATAFORMA_FILE = os.path.join(DATA_DIR, "editais_plataforma.json")
EDITAIS_USUARIO_FILE    = os.path.join(DATA_DIR, "editais_usuario.json")


def garantir_pasta_data():
    """Cria a pasta /data se ela ainda nao existir"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)


def carregar_json(caminho):
    """Le um arquivo JSON e retorna os dados"""
    if not os.path.exists(caminho):
        return {}
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)


def salvar_json(caminho, dados):
    """Salva dados em um arquivo JSON"""
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)


def carregar_editais():
    """Retorna todos os editais salvos"""
    return carregar_json(EDITAIS_FILE)


def salvar_editais(editais):
    """Salva todos os editais"""
    salvar_json(EDITAIS_FILE, editais)


def carregar_editais_plataforma():
    """Retorna os editais disponiveis no arquivo local"""
    return carregar_json(EDITAIS_PLATAFORMA_FILE)


def carregar_editais_usuario():
    """Retorna os editais cadastrados pelo usuario no arquivo local"""
    return carregar_json(EDITAIS_USUARIO_FILE)


def salvar_editais_usuario(editais):
    """Salva os editais do usuario no arquivo local"""
    salvar_json(EDITAIS_USUARIO_FILE, editais)


def get_usuario_id():
    """
    Retorna o ID do usuario logado.
    Entrada: nenhuma
    Saida: string com o UUID do usuario ou None
    """
    if "usuario" in st.session_state and st.session_state["usuario"]:
        return st.session_state["usuario"].id
    return None


def carregar_editais_usuario_db():
    """
    Carrega os editais do usuario logado direto do Supabase.
    Entrada: nenhuma
    Saida: dicionario com os editais do usuario
    """
    usuario_id = get_usuario_id()
    if not usuario_id:
        return {}

    try:
        supabase = get_supabase()
        resposta = supabase.table("editais_usuario") \
            .select("*") \
            .eq("usuario_id", usuario_id) \
            .execute()

        editais = {}
        for item in resposta.data:
            editais[item["nome"]] = {
                "disciplinas": item["disciplinas"],
                "origem": item["origem"]
            }
        return editais
    except Exception as e:
        st.error(f"Erro ao carregar editais: {e}")
        return {}


def salvar_edital_usuario_db(nome, disciplinas, origem="manual"):
    """
    Salva ou atualiza um edital do usuario no Supabase.
    Entrada: nome, disciplinas, origem
    Saida: True se salvou, False se deu erro
    """
    usuario_id = get_usuario_id()
    if not usuario_id:
        return False

    try:
        supabase = get_supabase()
        resposta = supabase.table("editais_usuario") \
            .select("id") \
            .eq("usuario_id", usuario_id) \
            .eq("nome", nome) \
            .execute()

        if resposta.data:
            supabase.table("editais_usuario") \
                .update({"disciplinas": disciplinas}) \
                .eq("usuario_id", usuario_id) \
                .eq("nome", nome) \
                .execute()
        else:
            supabase.table("editais_usuario") \
                .insert({
                    "usuario_id": usuario_id,
                    "nome": nome,
                    "disciplinas": disciplinas,
                    "origem": origem
                }) \
                .execute()
        return True
    except Exception as e:
        st.error(f"Erro ao salvar edital: {e}")
        return False


def carregar_grade_db(edital_nome):
    """
    Carrega a grade de um edital do Supabase.
    Entrada: edital_nome
    Saida: dicionario com a grade ou vazio
    """
    usuario_id = get_usuario_id()
    if not usuario_id:
        return {}

    try:
        supabase = get_supabase()
        resposta = supabase.table("grades") \
            .select("dados") \
            .eq("usuario_id", usuario_id) \
            .eq("edital_nome", edital_nome) \
            .execute()

        if resposta.data:
            return resposta.data[0]["dados"]
        return {}
    except Exception as e:
        st.error(f"Erro ao carregar grade: {e}")
        return {}


def salvar_grade_db(edital_nome, dados):
    """
    Salva ou atualiza a grade de um edital no Supabase.
    Entrada: edital_nome, dados
    Saida: True se salvou, False se deu erro
    """
    usuario_id = get_usuario_id()
    if not usuario_id:
        return False

    try:
        supabase = get_supabase()
        resposta = supabase.table("grades") \
            .select("id") \
            .eq("usuario_id", usuario_id) \
            .eq("edital_nome", edital_nome) \
            .execute()

        if resposta.data:
            supabase.table("grades") \
                .update({"dados": dados}) \
                .eq("usuario_id", usuario_id) \
                .eq("edital_nome", edital_nome) \
                .execute()
        else:
            supabase.table("grades") \
                .insert({
                    "usuario_id": usuario_id,
                    "edital_nome": edital_nome,
                    "dados": dados
                }) \
                .execute()
        return True
    except Exception as e:
        st.error(f"Erro ao salvar grade: {e}")
        return False


def carregar_editais_plataforma_db():
    """
    Carrega os editais da plataforma direto do Supabase.
    Entrada: nenhuma
    Saida: dicionario com os editais da plataforma
    """
    try:
        supabase = get_supabase()
        resposta = supabase.table("editais_plataforma") \
            .select("*") \
            .execute()

        editais = {}
        for item in resposta.data:
            editais[item["nome"]] = {
                "disciplinas": item["disciplinas"]
            }
        return editais
    except Exception as e:
        st.error(f"Erro ao carregar editais da plataforma: {e}")
        return {}


def salvar_edital_plataforma_db(nome, disciplinas):
    """
    Salva ou atualiza um edital da plataforma no Supabase.
    Entrada: nome, disciplinas
    Saida: True se salvou, False se deu erro
    """
    try:
        supabase = get_supabase()
        resposta = supabase.table("editais_plataforma") \
            .select("id") \
            .eq("nome", nome) \
            .execute()

        if resposta.data:
            supabase.table("editais_plataforma") \
                .update({"disciplinas": disciplinas}) \
                .eq("nome", nome) \
                .execute()
        else:
            supabase.table("editais_plataforma") \
                .insert({
                    "nome": nome,
                    "disciplinas": disciplinas
                }) \
                .execute()
        return True
    except Exception as e:
        st.error(f"Erro ao salvar edital da plataforma: {e}")
        return False


def deletar_edital_plataforma_db(nome):
    """
    Remove um edital da plataforma do Supabase.
    Entrada: nome
    Saida: True se deletou, False se deu erro
    """
    try:
        supabase = get_supabase()
        supabase.table("editais_plataforma") \
            .delete() \
            .eq("nome", nome) \
            .execute()
        return True
    except Exception as e:
        st.error(f"Erro ao deletar edital: {e}")
        return False