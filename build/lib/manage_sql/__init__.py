from .SQLITE import SQLITE
from .MYSQL import MYSQL
from .POSTGRESQL import POSTGRESQL

"""
Biblioteca para efectuar conexões com seus bancos de dados relacionais e assim efectuar as conexões e operações de forma eficiente

1. Conectado ao SQLITE
```python
db = SQLITE(
    nomebanco = 'nome_do_banco'
)
```

2. Conectado ao MYSQL
```python
db = MYSQL(
    host='localhost',
    user='root',
    database='nome_do_banco',
    password='Aa12345',
    port=3306
)
```

2. Conectado ao POSTGRESQL
```python
db = POSTGRESQL(
    host='localserver',
    user='postgres',
    database='nome_do_banco',
    password='Aa12345',
    port=5432
)
```

4. Documentação e suporte
Link do github: https://github.com/webtechmoz/manage-sql.git

"""