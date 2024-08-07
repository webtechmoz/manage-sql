# GESTÃO DE BANCOS DE DADOS (MYSQL & SQLITE)

## Índice da Biblioteca
1. [SQLITE](#sqlitepy)
2. [MYSQL](#mysqlpy)
3. [POSTGRESQL](#postgresqlpy)
4. [CONTRIBUIÇÃO](#contribuição)
5. [LICENÇA](#licença)


# SQLITE.py

`SQLITE.py` é uma classe Python para interagir com bancos de dados SQLite de forma simplificada. Esta classe fornece métodos para conectar a um banco de dados, criar tabelas, inserir dados e outras operações básicas.

## Índice SQLITE
1. [Instalação](#instalação)
2. [Uso da Classe SQLITE](#uso)
    1. [Métodos Disponíveis](#Métodos)
        - [conectarBanco](#Conectar-Banco)
        - [criarTabela](#Criar-Tabela)
        - [inserirDados](#Inserir-Dados)
        - [apagarDados](#Apagar-Dados)
        - [editarDados](#Editar-Dados)
        - [adicionarColuna](#Adicionar-Coluna)
        - [apagarColuna](#Apagar-Coluna)
        - [apagarTabela](#Apagar-Tabela)
        - [verDados](#Ver-Dados)
        - [encriptarValor](#Encriptar-valor)
        - [numeroTabelas](#número-de-tabelas)
        - [nomeTabelas](#nome-de-tabelas)
        - [totalLinhas](#total-linhas)
        - [ultimaLinha](#última-linha)
        - [numeroColunas](#número-de-colunas)
        - [nomeColunas](#nome-de-colunas)

## Instalação

Não há requisitos especiais de instalação além do Python 3.6+.

## Uso

Primeiro, importe a classe `SQLITE` e crie uma instância fornecendo o nome do banco de dados:

```python
# Importando a biblioteca
from manage_sql import SQLITE

# Instanciando a classe SQLITE
db = SQLITE('meu_banco')
```

## Métodos

### __init__
Inicializa a classe com o nome do banco de dados.

#### Parâmetros:
nomeBanco (str): Nome do banco de dados a ser utilizado.

#### Exemplo de uso:
```python
db = SQLITE('meu_banco')
```

### Conectar Banco
Conecta ao banco de dados e cria a pasta database se não existir.

#### Retorno:
Um objeto de conexão e cursor do banco de dados.

#### Exemplo de uso:
```python
database, cursor = db.conectarBanco()
```

### Criar Tabela
Cria uma tabela no banco de dados.

#### Parâmetros:
nomeTabela (str): Nome da tabela a ser criada.
Colunas (list): Lista com os nomes das colunas.
ColunasTipo (list): Lista com os tipos das colunas.

#### Exemplo de uso:
```python
db.criarTabela(
    nomeTabela='minha_tabela',
    Colunas=['coluna1', 'coluna2'],
    ColunasTipo=['TEXT', 'INTEGER']
)
```

### Inserir Dados
Insere dados na tabela especificada.

#### Parâmetros:
nomeTabela (str): Nome da tabela onde os dados serão inseridos.
Colunas (list): Lista com os nomes das colunas onde os dados serão inseridos.
Valores (list): Lista com os valores a serem inseridos.

#### Exemplo de uso:
```python
db.inserirDados(
    nomeTabela='minha_tabela',
    Colunas=['coluna1', 'coluna2'],
    Valores=['valor1', 123]
)
```

### Ver Dados
Consulta dados da tabela especificada.

#### Parâmetros:
nomeTabela (str): Nome da tabela de onde os dados serão consultados.
Colunas (list): Lista com os nomes das colunas a serem consultadas.

#### Exemplo de uso:
```python
resultados = db.consultarDados(
    nomeTabela='minha_tabela',
    Colunas=['coluna1', 'coluna2']
)
```

### Apagar Dados
Deleta dados da tabela especificada com base em uma condição.

#### Parâmetros:
nomeTabela (str): Nome da tabela de onde os dados serão deletados.
Condicao (str): Condição para deletar os dados.

#### Exemplo de uso:
```python
db.deletarDados(
    nomeTabela='minha_tabela',
    Condicao='coluna1 = "valor1"'
)
```

### Número de Tabelas
Retorna o número de tabelas constantes na base de dados.

#### Exemplo de uso:
```python
db.numeroTabelas
```

### Nome de Tabelas
Retorna o nome de todas tabelas constantes na base de dados.

#### Exemplo de uso:
```python
db.nomeTabelas
```

### Total Linhas
Retorna o numero total de registos dentro de uma tabela.

#### Parâmetros:
nomeTabela (str): Nome da tabela de onde os dados serão contados.
return (int): total de registos dentro do banco de dados

#### Exemplo de uso:
```python
db.totalLinhas(
    nomeTabela='minha_tabela',
)
```

### Última Linha
Retorna todos os dados do último registo dentro de uma tabela.

#### Parâmetros:
nomeTabela (str): Nome da tabela de onde os dados serão verificados.
return (list): dados do ultimo registo da tabela

#### Exemplo de uso:
```python
db.ultimaLinhas(
    nomeTabela='minha_tabela',
)
```

### Número de Colunas
Retorna o número total de colunas dentro de uma tabela.

#### Parâmetros:
nomeTabela (str): Nome da tabela de onde as colunas serão verificadas.
return (int): número de colunas dentro da tabela

#### Exemplo de uso:
```python
db.numeroColunas(
    nomeTabela='minha_tabela',
)
```

### Nome de Colunas
Retorna o nome de todas as colunas dentro de uma tabela.

#### Parâmetros:
nomeTabela (str): Nome da tabela de onde as colunas serão verificadas.
return (list): nome de colunas dentro da tabela

#### Exemplo de uso:
```python
db.nomeColunas(
    nomeTabela='minha_tabela',
)
```


# MYSQL.py

`MYSQL.py` é uma classe Python para interagir com bancos de dados MYSQL de forma simplificada. Esta classe fornece métodos para conectar a um banco de dados, criar tabelas, inserir dados e outras operações básicas.

## Índice MYSQL
1. [Instalação](#instalação)
2. [Uso da Classe MYSQL](#uso)
    1. [Métodos Disponíveis](#Métodos)
        - [conectarBanco](#Conectar-Banco)
        - [criarTabela](#Criar-Tabela)
        - [inserirDados](#Inserir-Dados)
        - [apagarDados](#Apagar-Dados)
        - [editarDados](#Editar-Dados)
        - [adicionarColuna](#Adicionar-Coluna)
        - [apagarColuna](#Apagar-Coluna)
        - [apagarTabela](#Apagar-Tabela)
        - [verDados](#Ver-Dados)
        - [encriptarValor](#Encriptar-valor)
        - [numeroTabelas](#número-de-tabelas)
        - [nomeTabelas](#nome-de-tabelas)
        - [totalLinhas](#total-linhas)
        - [ultimaLinha](#última-linha)
        - [numeroColunas](#número-de-colunas)
        - [nomeColunas](#nome-de-colunas)

## Instalação

Não há requisitos especiais de instalação além do Python 3.10+.

## Uso

Primeiro, importe a classe `MYSQL` e crie uma instância fornecendo o nome do banco de dados:

```python
# Importando a biblioteca
from manage_sql import MYSQL

# Instanciando a classe MYSQL
db = MYSQL(
    host='host',
    user='user',
    database='database',
    password='password',
    port='port'
)
```

## Métodos

### __init__
Inicializa a classe com o nome do banco de dados.

#### Parâmetros:
nomeBanco (str): Nome do banco de dados a ser utilizado.

#### Exemplo de uso:
```python
db = MYSQL(
    host='host',
    user='user',
    database='database',
    password='password',
    port='port'
)
```

### Conectar Banco
Conecta ao banco de dados e cria a pasta database se não existir.

#### Retorno:
Um objeto de conexão e cursor do banco de dados.

#### Exemplo de uso:
```python
database, cursor = db.conectarBanco()
```

### Criar Tabela
Cria uma tabela no banco de dados.

#### Parâmetros:
nomeTabela (str): Nome da tabela a ser criada.
Colunas (list): Lista com os nomes das colunas.
ColunasTipo (list): Lista com os tipos das colunas.

#### Exemplo de uso:
```python
db.criarTabela(
    nomeTabela='minha_tabela',
    Colunas=['coluna1', 'coluna2'],
    ColunasTipo=['TEXT', 'INTEGER']
)
```

### Inserir Dados
Insere dados na tabela especificada.

#### Parâmetros:
nomeTabela (str): Nome da tabela onde os dados serão inseridos.
Colunas (list): Lista com os nomes das colunas onde os dados serão inseridos.
Valores (list): Lista com os valores a serem inseridos.

#### Exemplo de uso:
```python
db.inserirDados(
    nomeTabela='minha_tabela',
    Colunas=['coluna1', 'coluna2'],
    Valores=['valor1', 123]
)
```

### Ver Dados
Consulta dados da tabela especificada.

#### Parâmetros:
nomeTabela (str): Nome da tabela de onde os dados serão consultados.
Colunas (list): Lista com os nomes das colunas a serem consultadas.

#### Exemplo de uso:
```python
resultados = db.consultarDados(
    nomeTabela='minha_tabela',
    Colunas=['coluna1', 'coluna2']
)
```

### Apagar Dados
Deleta dados da tabela especificada com base em uma condição.

#### Parâmetros:
nomeTabela (str): Nome da tabela de onde os dados serão deletados.
Condicao (str): Condição para deletar os dados.

#### Exemplo de uso:
```python
db.deletarDados(
    nomeTabela='minha_tabela',
    Condicao='coluna1 = "valor1"'
)
```

### Número de Tabelas
Retorna o número de tabelas constantes na base de dados.

#### Exemplo de uso:
```python
db.numeroTabelas
```

### Nome de Tabelas
Retorna o nome de todas tabelas constantes na base de dados.

#### Exemplo de uso:
```python
db.nomeTabelas
```

### Total Linhas
Retorna o numero total de registos dentro de uma tabela.

#### Parâmetros:
nomeTabela (str): Nome da tabela de onde os dados serão contados.
return (int): total de registos dentro do banco de dados

#### Exemplo de uso:
```python
db.totalLinhas(
    nomeTabela='minha_tabela',
)
```

### Última Linha
Retorna todos os dados do último registo dentro de uma tabela.

#### Parâmetros:
nomeTabela (str): Nome da tabela de onde os dados serão verificados.
return (list): dados do ultimo registo da tabela

#### Exemplo de uso:
```python
db.ultimaLinhas(
    nomeTabela='minha_tabela',
)
```

### Número de Colunas
Retorna o número total de colunas dentro de uma tabela.

#### Parâmetros:
nomeTabela (str): Nome da tabela de onde as colunas serão verificadas.
return (int): número de colunas dentro da tabela

#### Exemplo de uso:
```python
db.numeroColunas(
    nomeTabela='minha_tabela',
)
```

### Nome de Colunas
Retorna o nome de todas as colunas dentro de uma tabela.

#### Parâmetros:
nomeTabela (str): Nome da tabela de onde as colunas serão verificadas.
return (list): nome de colunas dentro da tabela

#### Exemplo de uso:
```python
db.nomeColunas(
    nomeTabela='minha_tabela',
)
```

# POSTGRESQL.py

`POSTGRESQL.py` é uma classe Python para interagir com bancos de dados POSTGRESQL de forma simplificada. Esta classe fornece métodos para conectar a um banco de dados, criar tabelas, inserir dados e outras operações básicas.

## Índice POSTGRESQL
1. [Instalação](#instalação)
2. [Uso da Classe POSTGRESQL](#uso)
    1. [Métodos Disponíveis](#Métodos)
        - [conectarBanco](#Conectar-Banco)
        - [criarTabela](#Criar-Tabela)
        - [inserirDados](#Inserir-Dados)
        - [apagarDados](#Apagar-Dados)
        - [editarDados](#Editar-Dados)
        - [adicionarColuna](#Adicionar-Coluna)
        - [apagarColuna](#Apagar-Coluna)
        - [apagarTabela](#Apagar-Tabela)
        - [verDados](#Ver-Dados)
        - [encriptarValor](#Encriptar-valor)
        - [numeroTabelas](#número-de-tabelas)
        - [nomeTabelas](#nome-de-tabelas)
        - [totalLinhas](#total-linhas)
        - [ultimaLinha](#última-linha)
        - [numeroColunas](#número-de-colunas)
        - [nomeColunas](#nome-de-colunas)

## Instalação

Não há requisitos especiais de instalação além do Python 3.10+.

## Uso

Primeiro, importe a classe `POSTGRESQL` e crie uma instância fornecendo o nome do banco de dados:

```python
# Importando a biblioteca
from manage_sql import POSTGRESQL

# Instanciando a classe POSTGRESQL
db = POSTGRESQL(
    host='host',
    user='user',
    database='database',
    password='password',
    port='port'
)
```

## Métodos

### __init__
Inicializa a classe com o nome do banco de dados.

#### Parâmetros:
nomeBanco (str): Nome do banco de dados a ser utilizado.

#### Exemplo de uso:
```python
db = POSTGRESQL(
    host='host',
    user='user',
    database='database',
    password='password',
    port='port'
)
```

### Conectar Banco
Conecta ao banco de dados e cria a pasta database se não existir.

#### Retorno:
Um objeto de conexão e cursor do banco de dados.

#### Exemplo de uso:
```python
database, cursor = db.conectarBanco()
```

### Criar Tabela
Cria uma tabela no banco de dados.

#### Parâmetros:
nomeTabela (str): Nome da tabela a ser criada.
Colunas (list): Lista com os nomes das colunas.
ColunasTipo (list): Lista com os tipos das colunas.

#### Exemplo de uso:
```python
db.criarTabela(
    nomeTabela='minha_tabela',
    Colunas=['coluna1', 'coluna2'],
    ColunasTipo=['TEXT', 'INTEGER']
)
```

### Inserir Dados
Insere dados na tabela especificada.

#### Parâmetros:
nomeTabela (str): Nome da tabela onde os dados serão inseridos.
Colunas (list): Lista com os nomes das colunas onde os dados serão inseridos.
Valores (list): Lista com os valores a serem inseridos.

#### Exemplo de uso:
```python
db.inserirDados(
    nomeTabela='minha_tabela',
    Colunas=['coluna1', 'coluna2'],
    Valores=['valor1', 123]
)
```

### Ver Dados
Consulta dados da tabela especificada.

#### Parâmetros:
nomeTabela (str): Nome da tabela de onde os dados serão consultados.
Colunas (list): Lista com os nomes das colunas a serem consultadas.

#### Exemplo de uso:
```python
resultados = db.consultarDados(
    nomeTabela='minha_tabela',
    Colunas=['coluna1', 'coluna2']
)
```

### Apagar Dados
Deleta dados da tabela especificada com base em uma condição.

#### Parâmetros:
nomeTabela (str): Nome da tabela de onde os dados serão deletados.
Condicao (str): Condição para deletar os dados.

#### Exemplo de uso:
```python
db.deletarDados(
    nomeTabela='minha_tabela',
    Condicao='coluna1 = "valor1"'
)
```

### Número de Tabelas
Retorna o número de tabelas constantes na base de dados.

#### Exemplo de uso:
```python
db.numeroTabelas
```

### Nome de Tabelas
Retorna o nome de todas tabelas constantes na base de dados.

#### Exemplo de uso:
```python
db.nomeTabelas
```

### Total Linhas
Retorna o numero total de registos dentro de uma tabela.

#### Parâmetros:
nomeTabela (str): Nome da tabela de onde os dados serão contados.
return (int): total de registos dentro do banco de dados

#### Exemplo de uso:
```python
db.totalLinhas(
    nomeTabela='minha_tabela',
)
```

### Última Linha
Retorna todos os dados do último registo dentro de uma tabela.

#### Parâmetros:
nomeTabela (str): Nome da tabela de onde os dados serão verificados.
return (list): dados do ultimo registo da tabela

#### Exemplo de uso:
```python
db.ultimaLinhas(
    nomeTabela='minha_tabela',
)
```

### Número de Colunas
Retorna o número total de colunas dentro de uma tabela.

#### Parâmetros:
nomeTabela (str): Nome da tabela de onde as colunas serão verificadas.
return (int): número de colunas dentro da tabela

#### Exemplo de uso:
```python
db.numeroColunas(
    nomeTabela='minha_tabela',
)
```

### Nome de Colunas
Retorna o nome de todas as colunas dentro de uma tabela.

#### Parâmetros:
nomeTabela (str): Nome da tabela de onde as colunas serão verificadas.
return (list): nome de colunas dentro da tabela

#### Exemplo de uso:
```python
db.nomeColunas(
    nomeTabela='minha_tabela',
)
```

# Contribuição
Sinta-se à vontade para contribuir com melhorias e novas funcionalidades.

# Licença
Este projeto está licenciado sob a licença MIT.