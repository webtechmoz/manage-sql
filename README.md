# SQLITE.py

`SQLITE.py` é uma classe Python para interagir com bancos de dados SQLite de forma simplificada. Esta classe fornece métodos para conectar a um banco de dados, criar tabelas, inserir dados e outras operações básicas.

## Índice
1. [Introdução](#introdução)
2. [Instalação](#instalação)
3. [Uso da Classe SQLITE](#uso-da-classe-sqlite)
    1. [Instanciando a Classe](#instanciando-a-classe)
    2. [Métodos Disponíveis](#métodos-disponíveis)
        - [conectarBanco](#conectarbanco)
        - [criarTabela](#criartabela)
        - [inserirDados](#inserirdados)
        - [apagarDados](#apagardados)
        - [editarDados](#editardados)
        - [adicionarColuna](#adicionarcoluna)
        - [apagarColuna](#apagarcoluna)
        - [apagarTabela](#apagartabela)
        - [verDados](#verdados)
        - [encryptPass (descontinuado)](#encryptpass-descontinuado)
        - [encriptarValor](#encriptarvalor)
        - [verDadosPlus (descontinuado)](#verdadosplus-descontinuado)

4. [Contibuição](#contribuição)
5. [Licença](#licença)

## Instalação

Não há requisitos especiais de instalação além do Python 3.6+.

## Uso

Primeiro, importe a classe `SQLITE` e crie uma instância fornecendo o nome do banco de dados:

```python
# Importando a biblioteca
from manage-sql import SQLITE

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

### Consultar Dados
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

## Contribuição
Sinta-se à vontade para contribuir com melhorias e novas funcionalidades.

## Licença
Este projeto está licenciado sob a licença MIT.
