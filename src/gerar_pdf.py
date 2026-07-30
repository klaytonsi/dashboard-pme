"""
Modulo de geracao de relatorio em PDF.
Recebe o DataFrame de vendas e os KPIs calculados, gera um PDF em memoria.
"""
import io
import plotly.express as px
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors


def gerar_relatorio_pdf(df, kpis) -> bytes:
    """Gera o relatorio em PDF e retorna os bytes prontos para download."""
    styles = getSampleStyleSheet()
    elementos = []

    elementos.append(Paragraph("Relatorio Financeiro", styles['Title']))
    elementos.append(Spacer(1, 12))

    dados_kpi = [
        ["Vendas totais", f"R$ {kpis['vendas_totais']:.2f}"],
        ["Lucro total", f"R$ {kpis['lucro_total']:.2f}"],
        ["Ticket medio", f"R$ {kpis['ticket_medio']:.2f}"],
        ["Produto mais vendido", kpis['produto_mais_vendido']],
    ]
    tabela_kpi = Table(dados_kpi, colWidths=[8 * cm, 6 * cm])
    tabela_kpi.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor("#f0f2f6")),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('FONTSIZE', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
    ]))
    elementos.append(tabela_kpi)
    elementos.append(Spacer(1, 20))

    df = df.copy()
    df['valor_total'] = df['quantidade'] * df['preco_unitario']
    vendas_dia = df.groupby('data')['valor_total'].sum().reset_index()
    fig1 = px.line(vendas_dia, x='data', y='valor_total', title="Vendas por dia")
    img1_bytes = fig1.to_image(format="png", width=700, height=350)
    elementos.append(Image(io.BytesIO(img1_bytes), width=16 * cm, height=8 * cm))
    elementos.append(Spacer(1, 12))

    elementos.append(Paragraph("Dados detalhados", styles['Heading2']))
    cabecalho = list(df.columns)
    linhas = df.astype(str).values.tolist()
    tabela_dados = Table([cabecalho] + linhas)
    tabela_dados.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#4a4a4a")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.3, colors.grey),
        ('FONTSIZE', (0, 0), (-1, -1), 6),
    ]))
    elementos.append(tabela_dados)

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    doc.build(elementos)
    buffer.seek(0)
    return buffer.getvalue()
