# MVP — Parte 1: Sistema de Medições Schulz

## 1. Objetivo

Desenvolver um protótipo em Python para cadastrar técnicos e
equipamentos, registrar medições e consultar seus resultados.

O sistema compara o valor obtido com o intervalo permitido e
classifica a medição como APROVADO ou REPROVADO. Os registros
são armazenados em um banco SQLite.

Os dados utilizados na demonstração são fictícios.

## 2. Organização dos arquivos

| Arquivo | Finalidade |
|---|---|
| 03_banco.sql | Define as tabelas e os relacionamentos do banco. |
| 04_classes.py | Contém as classes do sistema e as operações no banco. |
| 05_main.py | Executa os exemplos, demonstra o CRUD e apresenta o relatório. |
| 06_mvp_parte1.md | Documenta a implementação e sua validação. |
| schulz_mvp.db | Armazena os dados cadastrados. |

## 3. Organização das classes

### Tecnico

Representa o profissional responsável pelas medições.

- Atributos: matrícula, nome, e-mail e setor.
- Validação: os campos devem conter textos preenchidos.
- Método apresentar(): retorna o nome e a matrícula.

### Equipamento

Representa o equipamento associado às medições.

- Atributos: código, descrição, fabricante e modelo.
- Validação: os campos devem conter textos preenchidos.
- Método apresentar(): retorna a descrição e o código.

A descrição do objeto é gravada na coluna nome_equipamento
do banco.

### Medicao

Representa os valores usados na avaliação de uma medição.

- Atributos: parâmetro medido, valor nominal, tolerância
  inferior, tolerância superior e valor obtido.
- Validações: parâmetro preenchido e números finitos.
- As tolerâncias são tratadas como magnitudes positivas.
- Método avaliar(): calcula APROVADO ou REPROVADO.
- Método apresentar(): apresenta os valores e o resultado.

### BancoDados

Centraliza o acesso ao SQLite.

Responsabilidades:

- Abrir e fechar conexões.
- Ativar a verificação das chaves estrangeiras.
- Executar o arquivo SQL de criação das tabelas.
- Cadastrar e consultar técnicos e equipamentos.
- Cadastrar, consultar, atualizar e excluir medições.
- Consultar medições com os dados do técnico e do equipamento.

Os identificadores são gerados pelo banco. O programa utiliza
esses IDs para vincular cada medição ao técnico e ao equipamento.

## 4. Aplicação da orientação a objetos

O sistema separa as responsabilidades entre as classes.

Tecnico e Equipamento representam os cadastros. Medicao concentra
a regra de avaliação. BancoDados executa as operações SQL.
O arquivo 05_main.py organiza a demonstração e a apresentação
dos resultados.

Os atributos iniciados com sublinhado são considerados internos
por convenção do Python. As propriedades com @property permitem
a leitura dos valores sem fornecer um setter público.

As validações são realizadas na criação dos objetos, antes
do envio dos dados ao banco.

## 5. Regra de avaliação

O intervalo permitido é calculado da seguinte forma:

- Limite mínimo = valor nominal − tolerância inferior.
- Limite máximo = valor nominal + tolerância superior.

A medição é APROVADA quando o valor obtido está dentro desse
intervalo, incluindo os limites. Fora dele, é REPROVADA.

Exemplo:

| Valor nominal | Tolerâncias | Valor obtido | Resultado |
|---|---|---|---|
| 10,00 | 0,10 para cada lado | 10,05 | APROVADO |
| 10,00 | 0,10 para cada lado | 10,20 | REPROVADO |

Nos dois casos, o intervalo permitido vai de 9,90 até 10,10.

A classe Medicao utiliza Decimal nos cálculos. No SQLite,
as colunas numéricas são do tipo REAL, que possui precisão
aproximada.

## 6. Persistência e relacionamentos

O banco possui três tabelas:

- tecnico;
- equipamento;
- medicao.

Cada medição está associada a um técnico e a um equipamento
por meio de chaves estrangeiras.

A matrícula do técnico e o código do equipamento são únicos.
O resultado da medição aceita somente APROVADO ou REPROVADO.

O relatório utiliza JOIN para reunir as informações das três
tabelas. A data é preenchida pelo banco com CURRENT_TIMESTAMP
e apresentada como UTC.

## 7. Operações implementadas

| Entidade | Operações |
|---|---|
| Técnico | Cadastro e consulta por matrícula. |
| Equipamento | Cadastro e consulta por código. |
| Medição | Cadastro, consulta, atualização e exclusão. |

O CRUD completo foi implementado para as medições:

- CREATE: cadastra uma medição.
- READ: consulta uma medição ou lista o relatório.
- UPDATE: altera os valores e recalcula o resultado.
- DELETE: exclui a medição pelo ID.

Os comandos utilizam parâmetros com ?, evitando a montagem
do SQL pela concatenação dos valores.

## 8. Tratamento de erros

O programa trata os seguintes problemas:

- ValueError: dados inválidos na criação dos objetos.
- sqlite3.IntegrityError: violação das regras do banco.
- sqlite3.Error: outras falhas nas operações SQL.
- OSError: problemas de acesso aos arquivos.
- RuntimeError: falhas identificadas na demonstração do CRUD.

Nas operações de gravação, commit confirma as alterações.
Em caso de erro SQL, rollback desfaz alterações ainda não
confirmadas na conexão.

As conexões são fechadas no bloco finally, inclusive quando
ocorre um erro.

## 9. Fluxo de execução

1. O programa prepara o banco e suas tabelas.
2. Cria os objetos de técnico e equipamento de exemplo.
3. Consulta os cadastros e insere somente os que não existem.
4. Se não houver medições, cadastra dois exemplos iniciais.
5. Cria uma medição temporária para demonstrar o CRUD.
6. Consulta essa medição, atualiza seus valores e a exclui.
7. Consulta as medições restantes com JOIN.
8. Exibe o relatório e a quantidade de resultados de cada tipo.

## 10. Validação realizada

A execução no terminal apresentou os seguintes resultados:

| Verificação | Resultado observado |
|---|---|
| Cadastro e consulta do técnico | Ana Souza, matrícula TEC001. |
| Cadastro e consulta do equipamento | Paquímetro digital, código EQ001. |
| Medição dentro do intervalo | APROVADO para 10,05. |
| Medição fora do intervalo | REPROVADO para 10,20. |
| Criação da medição temporária | Registro criado com ID 3 nessa execução. |
| Consulta da medição temporária | Resultado inicial APROVADO. |
| Atualização da medição temporária | Um registro alterado para REPROVADO. |
| Exclusão da medição temporária | Um registro excluído. |
| Consulta após a exclusão | Registro não encontrado: False. |
| Relatório final | Duas medições: uma aprovada e uma reprovada. |

O ID da medição temporária pode variar entre execuções.

As capturas do terminal registram a demonstração do CRUD
e o relatório final.

Os tratamentos de erro estão implementados, mas esta
demonstração não comprova todos os cenários de falha.

## 11. Como executar

Requisitos:

- Python 3.
- Permissão de leitura e gravação na pasta do projeto.
- Arquivo 03_banco.sql na mesma pasta dos arquivos Python.

O programa utiliza apenas bibliotecas padrão do Python.

Abra um terminal na pasta Entrega_03_Schulz e execute:

    py 05_main.py

O banco schulz_mvp.db será criado caso não exista.
Em novas execuções, os cadastros de exemplo existentes são
reutilizados. A medição temporária do CRUD é criada e excluída
durante a demonstração.

## 12. Limitações desta versão

O protótipo funciona pelo terminal e utiliza dados fictícios
definidos no código.

Ainda não possui interface gráfica, importação de planilhas,
autenticação, histórico de alterações ou emissão de certificados.

A atualização e a exclusão demonstradas são operações do
protótipo acadêmico. O sistema ainda não oferece rastreabilidade
completa para utilização em uma operação real.