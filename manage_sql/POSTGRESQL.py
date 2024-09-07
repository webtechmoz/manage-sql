import psycopg2 as postgresql
import hashlib as sh

class POSTGRESQL:
    '''
    Faça a gestão dos seus bancos de dados com esta classe.
    
    Importe a classe e use um dos métodos abaixo:
    ```python
    # Importando a classe
    from manage_sql import POSTGRESQL
    
    # Instaciando a classe
    db = POSTGRESQL(
        host='host',
        user='user',
        database='database',
        password='password',
        port='port'
    )
    
    # Propriedades da classe
    db.numeroTabelas
    db.nomeTabelas
    
    # Métodos da Classe:
    db.criarTabela()
    db.inserirDados()
    db.apagarDados()
    db.editarDados()
    db.adicionarColuna()
    db.apagarColuna()
    db.apagarTabela()
    db.apagarBanco()
    db.verDados()
    db.encriptarValor()
    db.totalLinhas()
    db.ultimaLinha()
    db.numeroColunas()
    db.nomeColunas()
    ```
    '''

    def __init__(self, postgre_url: str = None, host: str = None, user: str = None, database: str = None, password: str = '', port: int = 5432):
        """
        Inicializa a classe com o nome do banco de dados.
        
        :param host: Endereço de onde o banco de dados está alocado.
        :param user: Nome do usuário de autenticação da base de dados.
        :param database: Nome do banco de dados a ser utilizado.
        :param password: Palavra-passe de autenticação na base de dados.
        :param port: Porta na qual o banco de dados está a executar.
        
        Exemplo de uso:
        ```python
        db = POSTGRESQL(
            host='serverhost',
            user='root',
            database='dbname',
            password='admin',
            port=5432
        )
        ```
        """
        
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port
        self.postgre_url = postgre_url
    
    def conectarBanco(self):
        """
        Conecta ao banco de dados e cria a pasta 'database' se não existir.

        Returns:
            _tuple_: Um objeto de conexão e cursor do banco de dados.
        
        Exemplo de uso:
        ```python
        db = POSTGRESQL(
            host='serverhost',
            user='root',
            database='usuarios',
            password='admin',
            port=5432
        )
        database, cursor = db.conectarBanco()
        ```
        """
        

        try:
            if self.postgre_url != None:
                database = postgresql.connect(
                    dsn=self.postgre_url
                )

                database.autocommit = True
                cursor = database.cursor()

                return database, cursor
            
            else:
                database = postgresql.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    port=self.port
                )
                
                database.autocommit = True
                database.cursor().execute(f'CREATE DATABASE {self.database}')

                database = postgresql.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    database=self.database,
                    port=self.port
                )

                cursor = database.cursor()
                
                return database, cursor
        
        except Exception as e:
            if self.postgre_url == None:
                if 'already exists' in str(e):
                    database = postgresql.connect(
                        host=self.host,
                        user=self.user,
                        password=self.password,
                        database=self.database,
                        port=self.port
                    )

                    database.autocommit = True
                    cursor = database.cursor()

                    return database, cursor
            
            print(f'Erro: {e}')
            exit()
                

    def criarTabela(self, nomeTabela: str, Colunas: list, ColunasTipo: list):
        """
        Cria uma tabela no banco de dados.

        :param nomeTabela: Nome da tabela a ser criada.
        :param Colunas: Lista com os nomes das colunas.
        :param ColunasTipo: Lista com os tipos das colunas.

        Exemplo de uso:
        ```python
        db = POSTGRESQL(
            host='serverhost',
            user='root',
            database='usuarios',
            password='admin',
            port=5432
        )
        db.criarTabela(
            nomeTabela='minha_tabela',
            Colunas=['coluna1', 'coluna2'],
            ColunasTipo=['VARCHAR(256)', 'INTEGER']
        )
        ```
        """
        if type(Colunas) == list and type(ColunasTipo) == list:
            if len(Colunas) == len(ColunasTipo):
                database, cursor = self.conectarBanco()
                ListaColunas = []

                for i in range(len(Colunas)):
                    ListaColunas.append(f'{Colunas[i]} {ColunasTipo[i]}')

                ColunaSQL = ','.join(ListaColunas)

                cursor.execute(f'CREATE TABLE IF NOT EXISTS {nomeTabela} (id SERIAL PRIMARY KEY,{ColunaSQL})')

                database.commit()
                database.close()
            else:
                print('Impossível criar tabelas: quantidade de colunas e tipos não coincide.')
        else:
            print('Impossível criar tabelas: parâmetros devem ser listas.')

    def inserirDados(self, nomeTabela: str, Colunas: list, dados: list):
        """
        Insere dados em uma tabela do banco de dados.

        :param nomeTabela: Nome da tabela onde os dados serão inseridos.
        :param Colunas: Lista com os nomes das colunas.
        :param dados: Lista com os valores a serem inseridos.
        
        Exemplo de uso:
        ```python
        db = POSTGRESQL(
            host='serverhost',
            user='root',
            database='usuarios',
            password='admin',
            port=5432
        )
        db.inserirDados(
            nomeTabela='minha_tabela',
            Colunas=['coluna1', 'coluna2'],
            dados=['valor1', 123]
        )
        ```
        """
        if type(Colunas) == list and type(dados) == list:
            if len(Colunas) == len(dados):
                database, cursor = self.conectarBanco()

                ColunaSQL = ','.join(Colunas)

                params = ', '.join(['%s'] * len(dados))

                cursor.execute(f'INSERT INTO {nomeTabela} ({ColunaSQL}) VALUES ({params})', tuple(dados))

                database.commit()
                database.close()
            else:
                print('Impossível inserir dados: quantidade de colunas e valores não coincide.')
        else:
            print('Impossível inserir dados: parâmetros devem ser listas.')

    def apagarDados(self, nomeTabela: str, conditions: str = ''):
        """
        Apaga registros de uma tabela no banco de dados POSTGRESQL.

        :param nomeTabela: Nome da tabela da qual os dados serão apagados.
        :param conditions: Condição SQL para selecionar os registros a serem apagados. Se vazio, todos os registros serão apagados.
        
        Exemplo de uso:
        
        ```python
        db = POSTGRESQL(
            host='serverhost',
            user='root',
            database='usuarios',
            password='admin',
            port=5432
        )
        
        # Apaga registros com id = 1
        db.apagarDados("minha_tabela", "id = 1")
        
        # Apaga todos os registros da tabela
        db.apagarDados("minha_tabela")
        ```
        """
        database, cursor = self.conectarBanco()

        if conditions == '':
            cursor.execute(f'DELETE FROM {nomeTabela}')
        
        else:
            cursor.execute(f'DELETE FROM {nomeTabela} WHERE {conditions}')
        
        database.commit()
        database.close()

    def editarDados(self, nomeTabela: str, colunas_valores: dict, conditions: str = ''):
        """
        Edita registos em uma tabela no banco de dados POSTGRESQL.

        :param nomeTabela: Nome da tabela a ser editada.
        :param colunas_valores: Dicionário contendo as colunas e os valores a editar.
        :param conditions: Condição SQL para selecionar os registos a serem editados. Se vazio, todos os registos serão atualizados.
        
        Exemplo de uso:
        ```python
        db = POSTGRESQL(
            host='serverhost',
            user='root',
            database='usuarios',
            password='admin',
            port=5432
        )
        
        # Edita registros com id = 1
        db.editarDados(
            nomeTabela="minha_tabela",
            colunas_valores = {"coluna_1": "novo_valor", "coluna_2": "novo_valor"}
            conditions="id = 1"
        )
        
        # Edita todos os registos da tabela
        db.editarDados(
            nomeTabela="minha_tabela",
            colunas_valores = {"coluna_1": "novo_valor", "coluna_2": "novo_valor"}
            Valor="novo_valor"
        )
        ```
        """
        database, cursor = self.conectarBanco()

        colunas = ", ".join([f"{col} = %s" for col in colunas_valores.keys()])
        valores = list(colunas_valores.values())

        if conditions == '':
            cursor.execute(f"UPDATE {nomeTabela} SET {colunas}", valores)
        
        else:
            cursor.execute(f"UPDATE {nomeTabela} SET {colunas} WHERE {conditions}", valores)
        
        database.commit()
        database.close()

    def adicionarColuna(self, nomeTabela: str, Coluna: str, ColunaTipo: str):
        """
        Adiciona uma nova coluna a uma tabela no banco de dados POSTGRESQL.

        :param nomeTabela: Nome da tabela na qual a coluna será adicionada.
        :param Coluna: Nome da nova coluna.
        :param ColunaTipo: Tipo de dados da nova coluna (por exemplo, INTEGER, VARCHAR(256)).
        
        Exemplo de uso:
        ```python
        db = POSTGRESQL(
            host='serverhost',
            user='root',
            database='usuarios',
            password='admin',
            port=5432
        )
        
        # Adiciona uma coluna do tipo VARCHAR(256)
        db.adicionarColuna("minha_tabela", "nova_coluna", "VARCHAR(256)")```
        """
        database, cursor = self.conectarBanco()

        cursor.execute(f'ALTER TABLE {nomeTabela} ADD COLUMN {Coluna} {ColunaTipo}')

        database.commit()
        database.close()
    
    def apagarColuna(self, nomeTabela: str, Coluna: str):
        """
        Apaga uma coluna de uma tabela do banco de dados.

        :param nomeTabela: Nome da tabela onde a coluna será apagada.
        :param Coluna: Nome da coluna a ser apagada.
        
        Exemplo de uso:
        ```python
        db = POSTGRESQL(
            host='serverhost',
            user='root',
            database='usuarios',
            password='admin',
            port=5432
        )
        db.apagarColuna('minha_tabela', 'coluna2')
        ```
        """
        database, cursor = self.conectarBanco()

        cursor.execute(f'ALTER TABLE {nomeTabela} DROP COLUMN {Coluna}')

        database.commit()
        database.close()

    def apagarTabela(self, nomeTabela: str):
        """
        Apaga uma tabela do banco de dados.

        :param nomeTabela: Nome da tabela a ser apagada.
        
        Exemplo de uso:
        ```python
        db = POSTGRESQL(
            host='serverhost',
            user='root',
            database='usuarios',
            password='admin',
            port=5432
        )
        db.apagarTabela('minha_tabela')
        ```
        """
        database, cursor = self.conectarBanco()

        cursor.execute(f'DROP TABLE IF EXISTS {nomeTabela}')

        database.commit()
        database.close()
    
    def apagarBanco(self, nomeBanco: str):
        """
        Apaga um banco de dados POSTGRESQL.

        :param nomeBanco: Nome do banco de dados a ser apagada.
        
        Exemplo de uso:
        ```python
        db = POSTGRESQL(
            host='serverhost',
            user='root',
            database='usuarios',
            password='admin',
            port=5432
        )
        db.apagarBanco('usuarios')
        ```
        """

        database = postgresql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            port=self.port
        )

        try:
            database.autocommit = True
            cursor = database.cursor()
            cursor.execute(f'DROP DATABASE IF EXISTS {nomeBanco}')

            cursor.close()
            database.close()
        
        except Exception as e:
            print(f'Erro: {e}')
            exit()
        

    def verDados(self, nomeTabela: str, conditions: str = '', colunas: str = '*'):
        """
        Consulta dados de uma tabela do banco de dados.

        :param nomeTabela: Nome da tabela a ser consultada.
        :param conditions: Condições para a consulta (opcional).
        :param colunas: Colunas a serem selecionadas (opcional).
        :return: Dados consultados.
        
        Exemplo de uso:
        ```python
        db = POSTGRESQL(
            host='serverhost',
            user='root',
            database='usuarios',
            password='admin',
            port=5432
        )
        dados = db.verDados('minha_tabela')
        print(dados)
        ```
        """
        database, cursor = self.conectarBanco()

        if conditions == '':
            cursor.execute(f'SELECT {colunas} FROM {nomeTabela}')
        else:
            cursor.execute(f'SELECT {colunas} FROM {nomeTabela} WHERE {conditions}')

        dados = cursor.fetchall()

        database.commit()
        database.close()

        return dados
    
    def encriptarValor(self, value: str):
        """
        Gera um hash SHA-512 de um valor fornecido.

        :param value: Valor a ser criptografada.
        :return: Valor criptografado em SHA-512.
        
        Exemplo de uso:
        ```python
        db = POSTGRESQL(
            host='serverhost',
            user='root',
            database='usuarios',
            password='admin',
            port=5432
        )
        value_hashed = db.encryptValor('valor')
        print(value_hashed)
        ```
        """
        hash = sh.sha512()
        hash.update(value.encode('UTF-8'))
        value_hashed = hash.hexdigest()

        return value_hashed
    
    @property
    def is_connected(self) -> bool:

        """Teste se o banco de dados está conectado com o servidor ou não

        Returns:
            _bool_: Retorna True caso esteja conectado ou falso caso contrario
        """

        database = postgresql.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port
        )
        rows = []
        database.cursor().execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
        tables = database.cursor().fetchall()
        database.close()

        for i, table in enumerate(tables):
            if i > 1:
                rows.append(table[0])

        if self.database in rows:
            return True

        else:
            return False
    
    @property
    def nomeTabelas(self) -> list[str]:
        """
        Retorna o nome de tabelas no banco de dados conectado.
        
        Returns:
            _list_: nome de tabelas constantes no banco de dados
        
        Exemplo de uso:
        ```python
        db = POSTGRESQL(
            host='serverhost',
            user='root',
            database='usuarios',
            password='admin',
            port=5432
        )
        db.nomeTabelas()
        ```
        """
        
        database, cursor = self.conectarBanco()
        rows = []
        
        cursor.execute("SELECT table_name FROM information_schema.tables WHERE table_schema='public'")
        tables = cursor.fetchall()
        
        database.close()
        
        for i, table in enumerate(tables):
            if i > 1:
                rows.append(table[0])
        
        return rows
    
    @property
    def numeroTabelas(self) -> int:
        """
        Retorna o número de tabelas no banco de dados conectado.
        
        Returns:
            _int_: número de tabelas constantes no banco de dados
        
        Exemplo de uso:
        ```python
        db = POSTGRESQL(
            host='serverhost',
            user='root',
            database='usuarios',
            password='admin',
            port=5432
        )
        db.numeroTabelas()
        ```
        """
        
        number = len(self._nomeTabelas)
        
        return number
    
    def totalLinhas(self, nomeTabela: str) -> int:
        """
        Retona o número total de registos de uma tabela no banco de dados.
        
        Parameters:
            _nomeTabela_: Nome da Tabela que pretende saber o número de registos
        
        Returns:
            _int_: Número total de linhas constantes na tabela
        
        Exemplo de uso:
        ```python
        db = POSTGRESQL(
            host='serverhost',
            user='root',
            database='usuarios',
            password='admin',
            port=5432
        )
        db.totalLinhas(
            nomeTabela = 'nome_da_tabela'
        )
        ```
        """
        
        database, cursor = self.conectarBanco()
        
        cursor.execute(f'SELECT COUNT(*) FROM {nomeTabela}')
        number = cursor.fetchone()[0]
        
        database.close()
        
        return number
    
    def ultimaLinha(self, nomeTabela: str) -> list:
        """
        Retorna os dados do último registo na tabela do banco de dados.
        
        Parameters:
            _nomeTabela_: Nome da Tabela que pretende saber o número de registos
        
        Returns:
            _list_: Dados do último registona tabela do banco de dados
        
        Exemplo de uso:
        ```python
        db = POSTGRESQL(
            host='serverhost',
            user='root',
            database='usuarios',
            password='admin',
            port=5432
        )
        db.ultimaLinha(
            nomeTabela = 'nome_da_tabela'
        )
        ```
        """
        id = self.totalLinhas(nomeTabela)
        database, cursor = self.conectarBanco()
        
        if id != 0:
            cursor.execute(f'SELECT * FROM {nomeTabela} ORDER BY id DESC LIMIT 1')
            lastrow = cursor.fetchone()
            
            database.close()
            
            return lastrow
        
        else:
            database.close()
            
            return id
    
    def numeroColunas(self, nomeTabela: str) -> int:
        """
        Retorna o número total de colunas na tabela do banco de dados.
        
        Parameters:
            _nomeTabela_: Nome da Tabela que pretende saber o número de registos
        
        Returns:
            _int_: Número total de colunas na tabela de dados
        
        Exemplo de uso:
        ```python
        db = POSTGRESQL(
            host='serverhost',
            user='root',
            database='usuarios',
            password='admin',
            port=5432
        )
        db.numeroColunas(
            nomeTabela = 'nome_da_tabela'
        )
        ```
        """
        
        database, cursor = self.conectarBanco()
        
        cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name='{nomeTabela}'")
        columns = cursor.fetchall()
        
        database.close()
        
        return len(columns)
    
    def nomeColunas(self, nomeTabela: str) -> list[str]:
        """
        Retorna o número total de colunas na tabela do banco de dados.
        
        Parameters:
            _nomeTabela_: Nome da Tabela que pretende saber o número de registos
        
        Returns:
            _int_: Número total de colunas na tabela de dados
        
        Exemplo de uso:
        ```python
        db = POSTGRESQL(
            host='serverhost',
            user='root',
            database='usuarios',
            password='admin',
            port=5432
        )
        db.numeroColunas(
            nomeTabela = 'nome_da_tabela'
        )
        ```
        """
        
        database, cursor = self.conectarBanco()
        
        cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name='{nomeTabela}'")
        columns = cursor.fetchall()
        
        database.close()
        
        return [column[0] for column in columns]