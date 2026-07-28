# Politica de Seguranca

## Credenciais

Este projeto utiliza a API do Google Sheets atraves de uma conta de servico. O arquivo de credenciais (credentials.json) nunca e versionado neste repositorio, sendo protegido pelo .gitignore.

## Variaveis de ambiente

Configuracoes sensiveis devem ser definidas em um arquivo .env local, nunca commitado. Veja .env.example para o modelo de variaveis necessarias.

## Reportar vulnerabilidades

Caso identifique uma vulnerabilidade neste projeto, abra uma issue no repositorio descrevendo o problema, sem incluir dados sensiveis na descricao.

## Boas praticas seguidas

- Nenhuma credencial, chave ou token e armazenada diretamente no codigo
- .gitignore configurado para bloquear arquivos sensiveis
- Dados de planilhas nao sao versionados neste repositorio
