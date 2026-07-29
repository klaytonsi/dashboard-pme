"""
Modulo de conexao com a planilha Google Sheets.
Funciona localmente (credentials.json) e no Streamlit Community Cloud
(st.secrets), sem nunca expor credenciais no codigo.
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


def _obter_credenciais():
    """Usa st.secrets na nuvem, ou arquivo local em desenvolvimento."""
    try:
        import streamlit as st
        if "gcp_service_account" in st.secrets:
            return Credentials.from_service_account_info(
                dict(st.secrets["gcp_service_account"]), scopes=SCOPES
            )
    except Exception:
        pass

    caminho_credenciais = os.getenv("GOOGLE_SHEETS_CREDENTIALS_PATH", "credentials.json")
    return Credentials.from_service_account_file(caminho_credenciais, scopes=SCOPES)


def carregar_dados_vendas():
    """Conecta na planilha e retorna os dados de vendas como DataFrame."""
    nome_planilha = os.getenv("GOOGLE_SHEET_NAME", "vendas_dashboard")

    creds = _obter_credenciais()
    client = gspread.authorize(creds)

    planilha = client.open(nome_planilha)
    aba = planilha.sheet1

    dados = aba.get_all_records()
    df = pd.DataFrame(dados)
    df.columns = df.columns.str.strip()

    return df
