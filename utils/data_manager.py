import json #ler e escrever json
import os   #trabalhar com pastas e arquivos

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

EDITAIS_FILE = os.path.join(DATA_DIR, "editais.json")
GRADE_FILE = os.path.join(DATA_DIR, "grade.json")

EDITAIS_PLATAFORMA_FILE = os.path.join(DATA_DIR, "editais_plataforma.json")
EDITAIS_USUARIO_FILE = os.path.join(DATA_DIR, "editais_usuario.json")

def garantir_pasta_data():
    """cria a pasta /data se ela ainda nao existir"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def carregar_json(caminho):
    """Lê um arquivo JSON e retorna os dados"""
    if not os.path.exists(caminho):
        return{}
    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_json(caminho, dados):
    """Salva dados em um arquivo JSON"""
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=4)

def carregar_editais():
    """retorna todos os editais salvos"""
    return carregar_json(EDITAIS_FILE)

def salvar_editais(editais):
    """salva todos os editais"""
    salvar_json(EDITAIS_FILE, editais)

def carregar_editais_plataforma():
    """ Retorna os editais disponiveis"""
    return carregar_json(EDITAIS_PLATAFORMA_FILE)

def carregar_editais_usuario():
    """Retorna os editais cadastrados pelo usuario"""
    return carregar_json(EDITAIS_USUARIO_FILE)

def salvar_editais_usuario(editais):
    """Salvar os editais do usuario"""
    salvar_json(EDITAIS_USUARIO_FILE, editais)

def adicionar_edital_plataforma(nome_edital):
    """
    Copia um edital da plataforma para a lista do usuario.
    Marca a origem como 'plataforma' para bloquear edicao.
    Retorna True se adicionou, False se ja existia.
    """
    plataforma = carregar_editais_plataforma()
    usuario    = carregar_editais_usuario()

    if nome_edital in usuario:
        return False

    usuario[nome_edital] = plataforma[nome_edital]
    usuario[nome_edital]["origem"] = "plataforma"
    salvar_editais_usuario(usuario)
    return True