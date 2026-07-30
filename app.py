"""
Dashboard financeiro para PMEs.
Le dados da planilha de vendas e exibe KPIs e graficos.
"""
import streamlit as st
import plotly.express as px
import pandas as pd

from src.conectar_planilha import carregar_dados_vendas
from src.processar_dados import calcular_kpis

st.set_page_config(page_title="Dashboard Financeiro", page_icon="📊", layout="wide")

st.title("📊 Dashboard Financeiro")
st.caption("Visao geral de vendas, lucro e desempenho de produtos")

with st.spinner("Carregando dados da planilha..."):
    try:
        df = carregar_dados_vendas()
    except Exception as e:
        st.error(f"Erro ao carregar dados: {e}")
        st.stop()

if df.empty:
    st.warning("Nenhum dado encontrado na planilha ainda.")
    st.stop()

df['data'] = pd.to_datetime(df['data'])
kpis = calcular_kpis(df)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Vendas totais", f"R$ {kpis['vendas_totais']:,.2f}")
col2.metric("Lucro total", f"R$ {kpis['lucro_total']:,.2f}")
col3.metric("Ticket medio", f"R$ {kpis['ticket_medio']:,.2f}")
col4.metric("Produto mais vendido", kpis['produto_mais_vendido'])

st.divider()

col_a, col_b = st.columns(2)

with col_a:
    st.subheader("Vendas por dia")
    df['valor_total'] = df['quantidade'] * df['preco_unitario']
    vendas_dia = df.groupby('data')['valor_total'].sum().reset_index()
    fig1 = px.line(vendas_dia, x='data', y='valor_total', markers=True)
    fig1.update_layout(xaxis_title="Data", yaxis_title="Valor (R$)")
    st.plotly_chart(fig1, use_container_width=True)

with col_b:
    st.subheader("Produtos mais vendidos")
    top_produtos = (
        df.groupby('produto')['quantidade'].sum()
        .sort_values(ascending=False).head(5).reset_index()
    )
    fig2 = px.bar(top_produtos, x='produto', y='quantidade')
    fig2.update_layout(xaxis_title="Produto", yaxis_title="Quantidade vendida")
    st.plotly_chart(fig2, use_container_width=True)

st.divider()
st.subheader("Dados detalhados")
st.dataframe(df, use_container_width=True)

st.divider()
from src.gerar_pdf import gerar_relatorio_pdf

if st.button("📄 Gerar Relatorio em PDF"):
    with st.spinner("Gerando PDF..."):
        pdf_bytes = gerar_relatorio_pdf(df, kpis)
    st.download_button(
        label="⬇️ Baixar Relatorio PDF",
        data=pdf_bytes,
        file_name="relatorio_financeiro.pdf",
        mime="application/pdf",
    )
