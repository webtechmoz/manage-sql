# MANAGE-SQL DOCUMENTATION

A classe **manage-sql** foi feita de modo a facilitar a gestão e interação com bancos de dados sqlite.

## Funcionalidades
- Criação e gestão de bancos de dados sqlite, mysql e postegres.
- Definição de estruturas de tabelas usando tipos de colunas customizadas.
- Maior performance nas operações CRUD.
- Executar operações sql brutas sem depender da classe
- Método próprio para encriptar valores sensíveis como senhas.

## Instalação
Primeiro garanta que tem o python instalando. Caso não tenha o python, [clique aqui](https://www.python.org/downloads/)

Segundo, instale a biblioteca manage-sql usando o comando abaixo na linha de comandos

```bash
pip install manage.sql
```

## Métodos

Para fazer a gestão dos bancos de dados, ao importar pode fazer o *import* dependendo do tipo de banco que pretende gerir.

```python
from manage_sql import SQLITE
from manage_sql import MYSQL
from manage_sql import POSTEGRESQL
```

### Conectando com o banco
#### SQLITE
```python
from manage_sql import SQLITE

db = SQLITE(
    database = 'my_database',
    path = 'path_database'
)
```
**Parametros**
- `database`: *str* (opcional) - nome do banco de dados sqlite
- `path`: *str* (opcional) - local onde pretender colocar o banco de dados. Caso não defina, o caminho padrão será o */database*

***

#### MYSQL
```python
from manage_sql import MYSQL

db = MYSQL(
    host = 'localhost',
    username = 'mysql_user',
    password = 'user_password',
    database = 'database_name',
    port = 3306
)
```

**Parametros**
- `host`: *str* - local onde está a rodar o servidor mysql
- `username`: *str* - usuario do banco de dados
- `password`: *str* - palavra-passe do usuario mysql
- `database`: *str* (opcional) - nome do banco de dados mysql
- `port`: *int* (opcional) - a porta padrão do servidor mysql é o **3306**

***

#### POSTGRESQL
- **Conectar usando o postegres_url (dsn)**
```python
from manage_sql import POSTEGRESQL

db = POSTEGRESQL(
    postegres_url = 'postegres_url',
)
```

- **Conectar usando os parametros normais**
```python
from manage_sql import POSTEGRESQL

db = POSTEGRESQL(
    host = 'localhost',
    username = 'postgres_user',
    password = 'user_password',
    database = 'database_name',
    port = 5432
)
```

**Parametros**
- `portegres_url`: *str* - caminho para o servidor onde está alocado o banco de dados postegres. Mais detalhes consulte [clique aqui](https://www.psycopg.org/docs/connection.html#connection.dsn)
- `host`: *str* - local onde está a rodar o servidor postgres
- `username`: *str* - usuario do banco de dados
- `password`: *str* - palavra-passe do usuario postgres
- `database`: *str* (opcional) - nome do banco de dados postgres
- `port`: *int* (opcional) - a porta padrão do servidor postgres é **5432**

***
*Os métodos abaixo aplicam-se para os três bancos de dados (mysql, sqlite, postegresql). A título de exemplo a documentação tomará como base, o banco de dados **MYSQL***
***

### Criar Tabela
```python
from manage_sql import MYSQL

db = MYSQL(
    host='localhost',
    username='root',
    password='Alex756545!',
    database='usuarios'
)

db.create_table(
    tablename='usuarios',
    columns=[
        db.Column(
            name='nome',
            column_type=db.column_types.Char(60).varchar
        ),
        db.Column(
            name='username',
            column_type=db.column_types.Char(60).varchar
        )
    ]
)
```

**Parametros**
- `tablename`: *str* - nome da tabela que pretende criar no banco de dados especificado na conexão
- `columns`: *list[Column]* - lista de colunas que pretende criar dentro da tabela.

**Nota 1:** A documentação devida do `Column` será feita em breve.
**Nota 2:** Tenha atenção aos tipos do `column_types`, dado que cada tipo de banco de dados possui seus respectivos tipos.

***

### Inserir Dados
```python
from manage_sql import MYSQL

db = MYSQL(
    host='localhost',
    username='root',
    password='Alex756545!',
    database='usuarios'
)

db.insert_data(
    tablename='usuarios',
    insert_query=[
        db.ColumnData(
            column='nome',
            value='Web Tech Moz'
        ),
        db.ColumnData(
            column='nome',
            value='webtechmoz'
        )
    ]
)
```

**Parametros**
- `tablename`: str - nome da tabela que pretende inserir os dados
- `insert_query`: *list[ColumnData]* - lista de ColumnData abaixo descritos
- `ColumnData`: ColumnDate - instância para inserir os dados nas colunas da tabela. Recebe `column` que corresponde ao nome da coluna e `value` correspondente ao valor a inserir

***

### Apagar Dados
```python
from manage_sql import MYSQL

db = MYSQL(
    host='localhost',
    username='root',
    password='Alex756545!',
    database='usuarios'
)

db.detele_data(
    tablename='usuarios',
    condition=db.delete_by(
        column='id'
    ).EQUAL(
        value=1
    )
)
```

**Parametros**
- `tablename`: *str* - nome da tabela que pretende inserir os dados
- `condition`: *Filter* (opcional) - método de filtragem que permite selecionar o(s) dado(s) que pretende apagar.

**Parametros de Filtragem**
O `delete_by` deve receber uma coluna base para fazer a filtragem dos dados. Este método possui várioss metodos de filtragem abaixo indicados:
- `EQUAL`: recebe um valor em que a coluna especificada deverá ser igual `=`
- `GATHER_THAN`: recebe um valor minimo para comparação `>`
- `GATHER_OR_EQUAL`: recebe um valor que deverá ser o mínimo incluido para comparação `>=`
- `LESS_THAN`: recebe um valor máximo para comparação `<`
- `LESS_OR_EQUAL`: recebe um valor máximo incluido `<=`
- `CONTAIN`: recebe uma parte de texto para validação de strings `LIKE`

Pode tambem fazer filtragem em multiplas colunas usando as condicionais abaixo:

- **`OR`** e **`AND`**
```python
from manage_sql import MYSQL

db = MYSQL(
    host='localhost',
    username='root',
    password='Alex756545!',
    database='usuarios'
)

# Filtrando usando o OR
db.detele_data(
    tablename='usuarios',
    condition=db.delete_by(
        column='id'
    ).EQUAL(
        value=1
    ).OR.filterby(
        column='username'
    ).CONTAIN(
        value='moz'
    )
)

# Filtrando usando o AND
db.detele_data(
    tablename='usuarios',
    condition=db.delete_by(
        column='id'
    ).EQUAL(
        value=1
    ).AND.filterby(
        column='username'
    ).CONTAIN(
        value='moz'
    )
)
```
***

### Ver os Dados
```python
from manage_sql import MYSQL

db = MYSQL(
    host='localhost',
    username='root',
    password='Alex756545!',
    database='usuarios'
)

dados = db.select_data(
    tablename='usuarios',
    columns=['id', 'nome', 'username'],
    condition=db.filter_by(
        column='id'
    ).GATHER_OR_EQUAL(
        value=1
    )
)

print(dados)
```

**Parametros**
- `tablename`: *str* - nome da tabela
- `columns`: *list[str]* (opcional) - lista de nome das colunas que pretende retornar. Caso não especifique, irá retornar todas colunas da tabela
- `condition`: *Filter* - Para mais detalhes veja [parametros de filtragem](#Parametros-de-Filtragem)

***

### Actualizar Dados
```python
from manage_sql import MYSQL

db = MYSQL(
    host='localhost',
    username='root',
    password='Alex756545!',
    database='usuarios'
)

db.update_data(
    tablename='usuarios',
    edit_query=db.ColumnData(
        column='nome',
        value='Alex Zunguze'
    ),
    condition=db.filter_by(
        column='id'
    ).EQUAL(
        value=1
    )
)
```

**Parametros**
- `tablename`: str - nome da tabela que pretende inserir os dados
- `edit_query`: *list[ColumnData]* - lista de ColumnData abaixo descritos
- `ColumnData`: ColumnDate - instância para inserir os dados nas colunas da tabela. Recebe `column` que corresponde ao nome da coluna e `value` correspondente ao novo valor a inserir
- `condition`: *Filter* (opcional) - Para mais detalhes veja [parametros de filtragem](#Parametros-de-Filtragem)

***

### Adiconar Coluna
```python
db = MYSQL(
    host='localhost',
    username='root',
    password='Alex756545!',
    database='usuarios'
)

db.add_column(
    tablename='usuarios',
    column=db.Column(
        name='idade',
        column_type=db.column_types.Integer.integer
    )
)
```

**Parametros**
- `tablename`: *str* - nome da tabela
- `column`: *Column* - instância contendo os detalhes na coluna a ser adicionada

Mais Detalhes sobre a `Column` veja a documentação [clicando aqui](#criar-tabela)

***

### Apagar Coluna
```python
from manage_sql import MYSQL

db = MYSQL(
    host='localhost',
    username='root',
    password='Alex756545!',
    database='usuarios'
)

db.drop_column(
    tablename='usuarios',
    column_name='idade'
)
```

**Parametros**
- `tablename`: *str* - nome da tabela
- `column_name`: *str* - nome da coluna que pretende apagar

***

### Apagar Tabela
```python
from manage_sql import MYSQL

db = MYSQL(
    host='localhost',
    username='root',
    password='Alex756545!',
    database='usuarios'
)

db.drop_table(
    tablename='usuarios'
)
```

**Parametros**
- `tablename`: *str* - nome da tabela que pretende apagar

**Atenção**: Tenha em atenção que se executar este comando perderá todos dados dentro da referida tabela.

### Comandos SQL
Caso queira rodar outras queries SQL que o `manage_sql` ainda não possua de forma nativa, pode usar o método `execute_query` conforme vem no exemplo abaixo:

```python
from manage_sql import MYSQL

db = MYSQL(
    host='localhost',
    username='root',
    password='Alex756545!',
    database='usuarios'
)

columns = db.execute_query(
    query='show columns from usuarios'
)

print(columns)
```

### Encriptar Valores
O `manage_sql` possui um metodo proprio para encriptar valores baseado no hash512 que geral 128 caracteres aleatórios. É util para armazenar senhas criptografadas

```python
from manage_sql import MYSQL
db = MYSQL(
    host='localhost',
    username='root',
    password='Alex756545!',
    database='usuarios'
)

hash_value = db.encrypt_value(
    value='Aa12456'
)
```