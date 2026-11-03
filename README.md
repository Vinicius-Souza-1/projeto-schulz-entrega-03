# Projeto Schulz — Entrega 03

MVP acadêmico de medições desenvolvido em Python e SQLite para Projeto Aplicado I — UNI SENAI Florianópolis.

## Funcionalidades

- Cadastro e consulta de técnicos e equipamentos.
- Avaliação de medições como APROVADO ou REPROVADO.
- CRUD completo de medições e relatório com JOIN.
- Validação de dados e tratamento de erros SQL.

## Como executar

Com Python 3 instalado, abra o terminal na pasta do projeto:

```powershell
py 05_main.py
```

Em sistemas com o comando `python3`, use `python3 05_main.py`. Não é necessário instalar bibliotecas externas. Mantenha `03_banco.sql` junto aos arquivos Python.

O programa reutiliza os cadastros existentes, cria exemplos quando não há medições e demonstra o CRUD com uma medição temporária, removida ao final do teste.

## Arquivos

- `03_banco.sql`: estrutura das tabelas.
- `04_classes.py`: classes e acesso ao banco.
- `05_main.py`: demonstração e relatório.
- [Documentação técnica](06_mvp_parte1.md).
- [Relatório da entrega](Relatorio_Entrega_03.pdf).
- `schulz_mvp.db`: banco com dados fictícios.
- `Imagens/`: evidências da execução.

## Integrantes

- Victor Gabriel Jaeger
- Vinicius de Assis Mendes
- Vinícius Itamar de Souza

## Limitações

Protótipo acadêmico com dados fictícios, executado pelo terminal. Não possui interface gráfica, autenticação, importação de planilhas, histórico de alterações ou emissão de certificados.
