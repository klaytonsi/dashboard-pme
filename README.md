# Dashboard Financeiro para PMEs

Dashboard financeiro automatizado que transforma planilhas de vendas em relatorios profissionais em PDF, feito para pequenas e medias empresas que ainda controlam tudo manualmente.

## Sobre o projeto

Muitas pequenas e medias empresas ainda registram vendas em planilhas soltas e perdem horas todo mes montando relatorios manuais para o contador, socios ou reunioes de resultado. Este projeto resolve esse problema com uma solucao simples e de custo zero para operar.

O sistema se conecta a uma planilha de vendas (Google Sheets) ja usada pela empresa, processa os dados automaticamente e entrega:

- Dashboard interativo com vendas, lucro, ticket medio, produto mais vendido e tendencias, atualizado em tempo real
- Relatorio em PDF gerado automaticamente, pronto para enviar ao contador, socios ou investidores, com um clique

## Demonstracao

Dashboard ao vivo: https://dashboard-pme-yejyp3hjqrtsyfm3n6eixn.streamlit.app/
Notebook no Kaggle: https://www.kaggle.com/code/klaytonvieira/dashboard-financeiro-para-pmes-analis

## Tecnologias utilizadas

- Python
- Streamlit
- pandas
- gspread e Google Sheets API
- Plotly
- ReportLab e Kaleido
- Streamlit Community Cloud

## Estrutura do projeto

- app.py: aplicacao principal do dashboard
- requirements.txt: dependencias do projeto
- .env.example: modelo de variaveis de ambiente
- SECURITY.md: politica de seguranca
- src/conectar_planilha.py: conexao segura com Google Sheets
- src/processar_dados.py: calculo de KPIs
- src/gerar_pdf.py: geracao do relatorio em PDF
- data/, reports/, images/, docs/, tests/: pastas de apoio

## Como funciona

1. O usuario mantem sua planilha de vendas no Google Sheets, com colunas de data, produto, categoria, quantidade, preco e custo
2. O dashboard le esses dados automaticamente via Google Sheets API
3. Os KPIs (vendas totais, lucro, ticket medio, produto mais vendido) sao calculados em tempo real
4. O usuario pode gerar e baixar um relatorio em PDF com um clique, sem qualquer conhecimento tecnico

## Rodando localmente

Este projeto foi desenvolvido inteiramente pelo celular (Android, via Termux), sem depender de computador.

Clone o repositorio e instale as dependencias:

pip install -r requirements.txt

Configure suas credenciais copiando .env.example para .env e preenchendo com seus dados. Veja SECURITY.md para detalhes sobre como obter a credencial do Google Sheets API.

Rode o dashboard com: streamlit run app.py

## Seguranca

Este projeto segue praticas de seguranca desde o design:

- Nenhuma credencial e versionada no repositorio (protegido por .gitignore)
- Credenciais gerenciadas via variaveis de ambiente localmente e via Secrets no Streamlit Community Cloud
- Rotacao periodica de chaves de API
- Veja SECURITY.md para a politica completa

## Status

MVP funcional. Dashboard e geracao de PDF implementados e testados com dados reais.

## Melhorias futuras

- Filtros por periodo e categoria no dashboard
- Suporte a multiplas planilhas e clientes
- Envio automatico do PDF por e-mail
- Autenticacao de usuarios para uso multi-cliente

## Autor

Klayton. Projeto desenvolvido como peca de portfolio e produto para pequenas e medias empresas.
