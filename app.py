"""Dashboard de demonstracao: dados ficticios, sem APIs ou credenciais.

Arquivo autocontido para facilitar a publicacao no Streamlit Community Cloud.
Nao representa a planilha original excluida nem resultados de uma empresa real.
"""
from io import BytesIO

import streamlit as st
import plotly.express as px
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak,
)
from reportlab.graphics.shapes import Drawing, String
from reportlab.graphics.charts.lineplots import LinePlot


AVISO_DEMO = "Demonstração - dados fictícios. Não representam uma empresa real."


def carregar_dados_demo():
    """Gera sempre as mesmas 60 vendas ficticias de agosto de 2026."""
    produtos = [
        ("Caderno", "Papelaria", 25.0, 12.0),
        ("Caneta", "Papelaria", 6.0, 2.0),
        ("Mochila", "Acessórios", 120.0, 70.0),
        ("Garrafa", "Acessórios", 45.0, 22.0),
        ("Agenda", "Papelaria", 38.0, 18.0),
    ]
    linhas = []
    for dia, data in enumerate(pd.date_range("2026-08-01", periods=30)):
        for venda in range(2):
            produto, categoria, preco, custo = produtos[(dia + venda * 2) % len(produtos)]
            linhas.append({
                "data": data, "produto": produto, "categoria": categoria,
                "quantidade": 1 + (dia * 3 + venda) % 5,
                "preco_unitario": preco, "custo_unitario": custo,
            })
    df = pd.DataFrame(linhas)
    df["valor_total"] = df["quantidade"] * df["preco_unitario"]
    df["lucro"] = df["quantidade"] * (df["preco_unitario"] - df["custo_unitario"])
    return df


def moeda(valor):
    return "R$ " + f"{valor:,.2f}".replace(",", "_").replace(".", ",").replace("_", ".")


def calcular_kpis(df):
    if df.empty:
        return {"vendas_totais": 0.0, "lucro_total": 0.0,
                "ticket_medio": 0.0, "produto_mais_vendido": "-"}
    return {
        "vendas_totais": float(df["valor_total"].sum()),
        "lucro_total": float(df["lucro"].sum()),
        "ticket_medio": float(df["valor_total"].mean()),
        "produto_mais_vendido": df.groupby("produto")["quantidade"].sum().idxmax(),
    }


def gerar_relatorio_demo(df):
    """PDF em memoria, sem navegador, Kaleido, rede ou arquivos temporarios."""
    if df.empty:
        raise ValueError("Selecione pelo menos uma venda para gerar o relatório.")
    buffer = BytesIO()
    styles = getSampleStyleSheet()
    kpis = calcular_kpis(df)
    elementos = [
        Paragraph("Dashboard Financeiro para PMEs", styles["Title"]),
        Paragraph(AVISO_DEMO, styles["Normal"]),
        Spacer(1, 12),
        Paragraph(
            f"Período: {df['data'].min():%d/%m/%Y} a {df['data'].max():%d/%m/%Y}"
            f" | {len(df)} vendas fictícias selecionadas", styles["Normal"]),
        Spacer(1, 14),
    ]
    tabela = Table([
        ["Indicador", "Resultado demonstrativo"],
        ["Vendas totais", moeda(kpis["vendas_totais"])],
        ["Lucro bruto", moeda(kpis["lucro_total"])],
        ["Ticket médio", moeda(kpis["ticket_medio"])],
        ["Produto mais vendido", kpis["produto_mais_vendido"]],
    ], colWidths=[8 * cm, 9 * cm])
    estilo = TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#16324f")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.whitesmoke, colors.white]),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("TOPPADDING", (0, 0), (-1, -1), 7),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ])
    tabela.setStyle(estilo)
    elementos.extend([tabela, Spacer(1, 12), Paragraph(
        "Lucro bruto = vendas menos custo dos produtos; não inclui despesas ou impostos. "
        "Nesta base, cada linha representa uma venda de um único produto.", styles["Normal"]),
        Spacer(1, 20), Paragraph("Vendas por dia (R$)", styles["Heading2"])])
    vendas = df.groupby("data")["valor_total"].sum()
    desenho = Drawing(17 * cm, 6.5 * cm)
    grafico = LinePlot()
    grafico.x, grafico.y = 45, 35
    grafico.width, grafico.height = 14.5 * cm, 4.5 * cm
    grafico.data = [[(int(data.day), float(valor)) for data, valor in vendas.items()]]
    grafico.xValueAxis.valueMin = max(0, int(vendas.index.min().day) - 1)
    grafico.xValueAxis.valueMax = int(vendas.index.max().day) + 1
    grafico.yValueAxis.valueMin = 0
    grafico.lines[0].strokeColor = colors.HexColor("#167dbe")
    grafico.lines[0].strokeWidth = 2
    desenho.add(grafico)
    desenho.add(String(220, 5, "Dia de agosto de 2026", fontSize=9, textAnchor="middle"))
    elementos.extend([desenho, PageBreak(), Paragraph("Vendas fictícias detalhadas", styles["Heading2"])])
    linhas = [["Data", "Produto", "Qtd.", "Preço un.", "Custo un.", "Total", "Lucro bruto"]]
    for row in df.itertuples(index=False):
        linhas.append([row.data.strftime("%d/%m/%Y"), row.produto, str(row.quantidade),
                       moeda(row.preco_unitario), moeda(row.custo_unitario),
                       moeda(row.valor_total), moeda(row.lucro)])
    detalhes = Table(linhas, repeatRows=1, colWidths=[2.4*cm, 2.6*cm, 1*cm, 2.5*cm, 2.5*cm, 2.8*cm, 3.2*cm])
    detalhes.setStyle(estilo)
    detalhes.setStyle(TableStyle([("FONTSIZE", (0, 0), (-1, -1), 8)]))
    elementos.append(detalhes)

    def rodape(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 8)
        canvas.setFillColor(colors.grey)
        canvas.drawString(2*cm, 1*cm, "DEMONSTRAÇÃO - DADOS FICTÍCIOS")
        canvas.drawRightString(A4[0]-2*cm, 1*cm, f"Página {doc.page}")
        canvas.restoreState()

    doc = SimpleDocTemplate(buffer, pagesize=A4, leftMargin=2*cm, rightMargin=2*cm,
                            topMargin=1.6*cm, bottomMargin=1.8*cm)
    doc.build(elementos, onFirstPage=rodape, onLaterPages=rodape)
    return buffer.getvalue()


def main():
    st.set_page_config(page_title="Dashboard Financeiro para PMEs", page_icon="📊", layout="wide")
    st.title("📊 Dashboard Financeiro para PMEs")
    st.info(AVISO_DEMO)
    st.caption("Base demonstrativa incluída no projeto. Funciona sem Google Sheets, login ou credenciais.")
    base = carregar_dados_demo()
    with st.sidebar:
        st.header("Filtros")
        categorias = st.multiselect("Categorias", sorted(base["categoria"].unique()),
                                    default=sorted(base["categoria"].unique()))
        periodo = st.date_input("Período", value=(base["data"].min().date(), base["data"].max().date()),
                               min_value=base["data"].min().date(), max_value=base["data"].max().date())
    if len(periodo) != 2:
        st.warning("Selecione a data inicial e a data final.")
        return
    df = base[base["categoria"].isin(categorias) & base["data"].between(
        pd.Timestamp(periodo[0]), pd.Timestamp(periodo[1]))].copy()
    if df.empty:
        st.warning("Nenhuma venda para os filtros selecionados. Selecione uma categoria e um período.")
        return
    kpis = calcular_kpis(df)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Vendas totais", moeda(kpis["vendas_totais"]))
    col2.metric("Lucro bruto", moeda(kpis["lucro_total"]))
    col3.metric("Ticket médio", moeda(kpis["ticket_medio"]))
    col4.metric("Produto mais vendido", kpis["produto_mais_vendido"])
    st.caption("Cada linha representa uma venda de um único produto. Lucro bruto não inclui despesas ou impostos.")
    st.divider()
    col_a, col_b = st.columns(2)
    with col_a:
        st.subheader("Vendas por dia")
        vendas = df.groupby("data", as_index=False)["valor_total"].sum()
        st.plotly_chart(px.line(vendas, x="data", y="valor_total", markers=True,
                               labels={"data": "Data", "valor_total": "Vendas (R$)"}), width="stretch")
    with col_b:
        st.subheader("Produtos mais vendidos")
        produtos = df.groupby("produto", as_index=False)["quantidade"].sum().sort_values("quantidade", ascending=False)
        st.plotly_chart(px.bar(produtos, x="produto", y="quantidade",
                              labels={"produto": "Produto", "quantidade": "Unidades"}), width="stretch")
    st.subheader("Dados detalhados - fictícios")
    st.dataframe(df, width="stretch", hide_index=True)
    st.download_button(
        label="⬇️ Baixar relatório PDF demonstrativo",
        data=gerar_relatorio_demo(df),
        file_name="relatorio_financeiro_demonstrativo.pdf",
        mime="application/pdf",
    )


if __name__ == "__main__":
    main()
