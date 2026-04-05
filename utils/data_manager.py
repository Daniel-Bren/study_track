import json #ler e escrever json
import os   #trabalhar com pastas e arquivos

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

EDITAIS_FILE = os.path.join(DATA_DIR, "editais.json")
GRADE_FILE = os.path.join(DATA_DIR, "grade.json")

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
