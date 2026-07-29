"""
Modulo de processamento dos dados de vendas.
Calcula os KPIs principais do dashboard.
"""
import pandas as pd


def calcular_kpis(df: pd.DataFrame) -> dict:
    """Calcula vendas totais, lucro, ticket medio e produto mais vendido."""
    df = df.copy()
    df['valor_total'] = df['quantidade'] * df['preco_unitario']
    df['lucro'] = (df['preco_unitario'] - df['custo_unitario']) * df['quantidade']

    return {
        "vendas_totais": df['valor_total'].sum(),
        "lucro_total": df['lucro'].sum(),
        "ticket_medio": df['valor_total'].sum() / len(df),
        "produto_mais_vendido": df.groupby('produto')['quantidade'].sum().idxmax(),
    }
