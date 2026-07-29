"""
Modulo de conexao com a planilha Google Sheets.
Le as credenciais a partir de variavel de ambiente, nunca hardcoded.
"""
import os
import gspread
from google.oauth2.service_account import Credentials
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.readonly"
]


def carregar_dados_vendas():
    """Conecta na planilha e retorna os dados de vendas como DataFrame."""
    caminho_credenciais = os.getenv("GOOGLE_SHEETS_CREDENTIALS_PATH", "credentials.json")
    nome_planilha = os.getenv("GOOGLE_SHEET_NAME", "vendas_dashboard")

    creds = Credentials.from_service_account_file(caminho_credenciais, scopes=SCOPES)
    client = gspread.authorize(creds)

    planilha = client.open(nome_planilha)
    aba = planilha.sheet1

    dados = aba.get_all_records()
    df = pd.DataFrame(dados)
    df.columns = df.columns.str.strip()

    return df
