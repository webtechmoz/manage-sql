import mysql.connector as mysql
import hashlib as sh

class MYSQL:
    '''
    Faça a gestão dos seus bancos de dados com esta classe.
    
    Importe a classe e use um dos métodos abaixo:
    ```python
    # Importando a classe
    from manage-sql import MYSQL
    
    # Instaciando a classe
    db = MYSQL(
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

    def __init__(self, host: str, user: str, database: str, password: str = '', port: int = 3306):
        """
        Inicializa a classe com o nome do banco de dados.
        
        :param host: Endereço de onde o banco de dados está alocado.
        :param user: Nome do usuário de autenticação da base de dados.
        :param database: Nome do banco de dados a ser utilizado.
        :param password: Palavra-passe de autenticação na base de dados.
        :param port: Porta na qual o banco de dados está a executar.
        
        Exemplo de uso:
        ```python
        db = MYSQL(
            host='localhost',
            user='root',
            database='usuarios',
            password='admin',
            port=3306
        )
        ```
        """
        
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port

    @property
    def numeroTabelas(self) -> int:
        """
        Retorna o número de tabelas no banco de dados conectado.
        
        Returns:
            _int_: número de tabelas constantes no banco de dados
        
        Exemplo de uso:
        ```python
        db = MYSQL(
            host='localhost',
            user='root',
            database='usuarios',
            password='admin',
            port=3306
        )
        db.numeroTabelas
        ```
        """
        
        return self._numeroTabelas
    
    @property
    def nomeTabelas(self) -> list:
        """
        Retorna o nome de tabelas no banco de dados conectado.
        
        Returns:
            _list_: nome de tabelas constantes no banco de dados
        
        Exemplo de uso:
        ```python
        db = MYSQL(
            host='localhost',
            user='root',
            database='usuarios',
            password='admin',
            port=3306
        )
        db.nomeTabelas
        ```
        """
        
        return self._nomeTabelas
    
    def conectarBanco(self):
        """
        Conecta ao banco de dados e cria a pasta 'database' se não existir.

        Returns:
            _tuple_: Um objeto de conexão e cursor do banco de dados.
        
        Exemplo de uso:
        ```python
        db = MYSQL(
            host='localhost',
            user='root',
            database='usuarios',
            password='admin',
            port=3306
        )
        database, cursor = db.conectarBanco()
        ```
        """
        
        try:
            database = mysql.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
                port=self.port
            )
            
            if database.is_connected() == True:
                cursor = database.cursor()
                
                return database, cursor
        
        except:
            try:
                database = mysql.connect(
                    host=self.host,
                    user=self.user,
                    password=self.password,
                    port=self.port
                )
                
                database.cursor().execute(f'CREATE DATABASE IF NOT EXISTS {self.database}')
                database.cursor().execute(f'USE {self.database}')
                
                cursor = database.cursor()
                
                return database, cursor
            
            except Exception as e:
                print(f'Erro: {e}')
                

    def criarTabela(self, nomeTabela: str, Colunas: list, ColunasTipo: list):
        """
        Cria uma tabela no banco de dados.

        :param nomeTabela: Nome da tabela a ser criada.
        :param Colunas: Lista com os nomes das colunas.
        :param ColunasTipo: Lista com os tipos das colunas.

        Exemplo de uso:
        ```python
        db = MYSQL(
            host='localhost',
            user='root',
            database='usuarios',
            password='admin',
            port=3306
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

                cursor.execute(f'CREATE TABLE IF NOT EXISTS {nomeTabela} (id INTEGER PRIMARY KEY AUTO_INCREMENT,{ColunaSQL})')

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
        db = MYSQL(
            host='localhost',
            user='root',
            database='usuarios',
            password='admin',
            port=3306
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
        Apaga registros de uma tabela no banco de dados MYSQL.

        :param nomeTabela: Nome da tabela da qual os dados serão apagados.
        :param conditions: Condição SQL para selecionar os registros a serem apagados. Se vazio, todos os registros serão apagados.
        
        Exemplo de uso:
        
        ```python
        db = MYSQL(
            host='localhost',
            user='root',
            database='usuarios',
            password='admin',
            port=3306
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

    def editarDados(self, nomeTabela: str, Coluna: str, Valor: str, conditions: str = ''):
        """
        Edita registros em uma tabela no banco de dados MYSQL.

        :param nomeTabela: Nome da tabela a ser editada.
        :param Coluna: Nome da coluna a ser editada.
        :param Valor: Novo valor a ser atribuído à coluna.
        :param conditions: Condição SQL para selecionar os registros a serem editados. Se vazio, todos os registros serão atualizados.
        
        Exemplo de uso:
        ```python
        db = MYSQL(
            host='localhost',
            user='root',
            database='usuarios',
            password='admin',
            port=3306
        )
        
        # Edita registros com id = 1
        db.editarDados("minha_tabela", "nome_coluna", "novo_valor", "id = 1")
        
        # Edita todos os registros da tabela
        db.editarDados("minha_tabela", "nome_coluna", "novo_valor")
        ```
        """
        database, cursor = self.conectarBanco()

        if conditions == '':
            cursor.execute(f"UPDATE {nomeTabela} SET {Coluna} = %s", (Valor,))
        
        else:
            cursor.execute(f"UPDATE {nomeTabela} SET {Coluna} = %s WHERE {conditions}", (Valor,))
        
        database.commit()
        database.close()

    def adicionarColuna(self, nomeTabela: str, Coluna: str, ColunaTipo: str):
        """
        Adiciona uma nova coluna a uma tabela no banco de dados MYSQL.

        :param nomeTabela: Nome da tabela na qual a coluna será adicionada.
        :param Coluna: Nome da nova coluna.
        :param ColunaTipo: Tipo de dados da nova coluna (por exemplo, INTEGER, VARCHAR(256)).
        
        Exemplo de uso:
        ```python
        db = MYSQL(
            host='localhost',
            user='root',
            database='usuarios',
            password='admin',
            port=3306
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
        db = MYSQL(
            host='localhost',
            user='root',
            database='usuarios',
            password='admin',
            port=3306
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
        db = MYSQL(
            host='localhost',
            user='root',
            database='usuarios',
            password='admin',
            port=3306
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
        Apaga um banco de dados MYSQL.

        :param nomeBanco: Nome do banco de dados a ser apagada.
        
        Exemplo de uso:
        ```python
        db = MYSQL(
            host='localhost',
            user='root',
            database='usuarios',
            password='admin',
            port=3306
        )
        db.apagarBanco('usuarios')
        ```
        """
        database, cursor = self.conectarBanco()

        cursor.execute(f'DROP DATABASE IF EXISTS {nomeBanco}')

        database.commit()
        database.close()

    def verDados(self, nomeTabela: str, conditions: str = '', colunas: str = '*'):
        """
        Consulta dados de uma tabela do banco de dados.

        :param nomeTabela: Nome da tabela a ser consultada.
        :param conditions: Condições para a consulta (opcional).
        :param colunas: Colunas a serem selecionadas (opcional).
        :return: Dados consultados.
        
        Exemplo de uso:
        ```python
        db = MYSQL(
            host='localhost',
            user='root',
            database='usuarios',
            password='admin',
            port=3306
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
        db = MYSQL(
            host='localhost',
            user='root',
            database='usuarios',
            password='admin',
            port=3306
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
    def _nomeTabelas(self):
        """
        Retorna o nome de tabelas no banco de dados conectado.
        
        Returns:
            _list_: nome de tabelas constantes no banco de dados
        
        Exemplo de uso:
        ```python
        db = MYSQL(
            host='localhost',
            user='root',
            database='usuarios',
            password='admin',
            port=3306
        )
        db.nomeTabelas()
        ```
        """
        
        database, cursor = self.conectarBanco()
        rows = []
        
        cursor.execute('SHOW TABLES')
        tables = cursor.fetchall()
        
        database.close()
        
        for table in tables:
            rows.append(table[0])
        
        return rows
    
    @property
    def _numeroTabelas(self):
        """
        Retorna o número de tabelas no banco de dados conectado.
        
        Returns:
            _int_: número de tabelas constantes no banco de dados
        
        Exemplo de uso:
        ```python
        db = MYSQL(
            host='localhost',
            user='root',
            database='usuarios',
            password='admin',
            port=3306
        )
        db.numeroTabelas()
        ```
        """
        
        database, cursor = self.conectarBanco()
        
        cursor.execute('SHOW TABLES')
        number = len(cursor.fetchall())
        
        database.close()
        
        return number
    
    def totalLinhas(self, nomeTabela: str):
        """
        Retona o número total de registos de uma tabela no banco de dados.
        
        Parameters:
            _nomeTabela_: Nome da Tabela que pretende saber o número de registos
        
        Returns:
            _int_: Número total de linhas constantes na tabela
        
        Exemplo de uso:
        ```python
        db = MYSQL(
            host='localhost',
            user='root',
            database='usuarios',
            password='admin',
            port=3306
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
    
    def ultimaLinha(self, nomeTabela: str):
        """
        Retorna os dados do último registo na tabela do banco de dados.
        
        Parameters:
            _nomeTabela_: Nome da Tabela que pretende saber o número de registos
        
        Returns:
            _list_: Dados do último registona tabela do banco de dados
        
        Exemplo de uso:
        ```python
        db = MYSQL(
            host='localhost',
            user='root',
            database='usuarios',
            password='admin',
            port=3306
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
    
    def numeroColunas(self, nomeTabela: str):
        """
        Retorna o número total de colunas na tabela do banco de dados.
        
        Parameters:
            _nomeTabela_: Nome da Tabela que pretende saber o número de registos
        
        Returns:
            _int_: Número total de colunas na tabela de dados
        
        Exemplo de uso:
        ```python
        db = MYSQL(
            host='localhost',
            user='root',
            database='usuarios',
            password='admin',
            port=3306
        )
        db.numeroColunas(
            nomeTabela = 'nome_da_tabela'
        )
        ```
        """
        
        database, cursor = self.conectarBanco()
        
        cursor.execute(f'SHOW COLUMNS FROM {nomeTabela}')
        columns = cursor.fetchall()
        
        database.close()
        
        return len(columns)
    
    def nomeColunas(self, nomeTabela: str):
        """
        Retorna o número total de colunas na tabela do banco de dados.
        
        Parameters:
            _nomeTabela_: Nome da Tabela que pretende saber o número de registos
        
        Returns:
            _int_: Número total de colunas na tabela de dados
        
        Exemplo de uso:
        ```python
        db = MYSQL(
            host='localhost',
            user='root',
            database='usuarios',
            password='admin',
            port=3306
        )
        db.numeroColunas(
            nomeTabela = 'nome_da_tabela'
        )
        ```
        """
        
        database, cursor = self.conectarBanco()
        
        cursor.execute(f'SHOW COLUMNS FROM {nomeTabela}')
        columns = cursor.fetchall()
        
        database.close()
        
        return [column[0] for column in columns]


if __name__ == '__main__':

    """
    Nesta secção vamos ver exemplo de como implementar cada função desta biblioteca
    """
    
    # Criando a conexão com o banco de dados
    db = MYSQL(
        host='localhost',
        user='root',
        database='users',
        password='Alex756545!',
        port=3307
    )
    
    # Criando as variáveis necessárias
    nomebela = 'usuarios'
    colunas = {
        'nome': 'VARCHAR(256)',
        'usuario': 'VARCHAR(256)',
        'senha': 'VARCHAR(256)',
    }
    
    dados = {
        'nome': 'Alexandre Zunguze',
        'usuario': 'azunguze',
        'senha': 'Aa123'
    }
    
    # db.criarTabela()
    db.criarTabela(
        nomeTabela=nomebela,
        Colunas=[col for col in colunas],
        ColunasTipo=[col for col in colunas.values()]
    )
    
    # db.inserirDados()
    for _ in range(3):
        db.inserirDados(
            nomeTabela=nomebela,
            Colunas=[col for col in dados],
            dados=[dado for dado in dados.values()]
        )
    
    # db.apagarDados()
    db.apagarDados(
        nomeTabela=nomebela,
        conditions='id = 3'
    )
    
    # db.editarDados()
    db.editarDados(
        nomeTabela=nomebela,
        Coluna=list(colunas.keys())[2],
        Valor=db.encriptarValor('Aa123')
    )
    
    db.editarDados(
        nomeTabela=nomebela,
        Coluna=list(colunas.keys())[2],
        Valor=db.encriptarValor('Aa123'),
        conditions='id = 2'
    )
    
    # db.adicionarColuna()
    db.adicionarColuna(
        nomeTabela=nomebela,
        Coluna='email',
        ColunaTipo='VARCHAR(256)'
    )
    
    # db.apagarColuna()
    db.apagarColuna(
        nomeTabela=nomebela,
        Coluna='email'
    )
    
    # db.verDados()
    dados_1 = db.verDados(
        nomeTabela=nomebela
    )
    
    dados_2 = db.verDados(
        nomeTabela=nomebela,
        conditions='id = 1'
    )
    
    # db.numeroTabelas
    print(f'numero de tabelas: {db.numeroTabelas}')
    
    # db.nomeTabelas
    print(f'nome tabelas: {db.nomeTabelas}')
    
    # db.numeroLinhas()
    print(
        f'numero linhas: {db.totalLinhas(nomeTabela=nomebela)}'
    )
    
    # db.ultimaLinha()
    print(
        f'ultima linha: {db.ultimaLinha(nomeTabela=nomebela)}'
    )
    
    # db.numeroColunas()
    print(f'numero de colunas: {db.numeroColunas(nomeTabela=nomebela)}')
    
    # db.nomeColunas()
    print(f'nome de colunas: {db.nomeColunas(nomeTabela=nomebela)}')
    
    # Apagador todos dados
    db.apagarDados(
        nomeTabela=nomebela
    )
    
    # db.apagarTabela()
    db.apagarTabela(
        nomeTabela=nomebela
    )
    
    # db.apagarBanco()
    db.apagarBanco(
        nomeBanco=db.database
    )