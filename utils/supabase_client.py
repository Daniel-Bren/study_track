# utils/supabase_client.py

import os
from supabase import create_client
from dotenv import load_dotenv

# Carrega as variáveis do arquivo .env
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


def get_supabase():
    """
    Cria e retorna o cliente do Supabase.

    Entrada: nenhuma
    Saída: cliente conectado ao banco de dados
    """
    return create_client(SUPABASE_URL, SUPABASE_KEY)