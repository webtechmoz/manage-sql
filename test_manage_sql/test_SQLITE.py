import unittest
import os
from dataclasses import is_dataclass
import sys

sys.path.append('manage_sql')
from manage_sql import SQLITE

class TestSQLITE(unittest.TestCase):
    
    @classmethod
    def setUp(self):
        self.db_name: str = 'db_test'
        self.table_name = 'tabela_test'
        self.columns = ['Col_1', 'Col_2', 'Col_3']
        self.columns_type = ['TEXT', 'TEXT', 'INTEGER']
        self.path: str = rf"{os.getcwd()}\database\{self.db_name}.db"
        self.database: SQLITE = SQLITE(self.db_name)
        self.database.criarTabela(
            nomeTabela=self.table_name,
            Colunas=self.columns,
            ColunasTipo=self.columns_type
        )
    
    def tearDown(self) -> None:
        os.remove(self.path)
    
    # Testando a classe importada
    def test_e_classe(self):
        self.assertFalse(is_dataclass(SQLITE))
    
    # Testando a conexão
    def test_conectarBanco(self):
        database = SQLITE(self.db_name).conectarBanco()
        database[0].close()
        self.assertEqual(type(database), tuple)
    
    def test_inserirDados(self):
        self.database.inserirDados(
            nomeTabela=self.table_name,
            Colunas=self.columns,
            dados=['A1','A2', 123]
        )
        data = self.database.verDados(
            nomeTabela=self.table_name,
            conditions='id = 1'
        )
        self.assertEqual(len(data), 1)
    
    def test_adicionarColuna(self):
        self.database.adicionarColuna(
            nomeTabela=self.table_name,
            Coluna='Col_4',
            ColunaTipo='TEXT'
        )
    
    def test_editarDados(self):
        self.database.inserirDados(
            nomeTabela=self.table_name,
            Colunas=self.columns,
            dados=['A1','A2', 123]
        )
        
        self.database.editarDados(
            nomeTabela=self.table_name,
            Coluna=self.columns[2],
            Valor='125'
        )
        
        data = self.database.verDados(
            nomeTabela=self.table_name
        )
        
        self.assertEqual(data[0][3], 125)
    
    def test_apagarDados(self):
        self.database.inserirDados(
            nomeTabela=self.table_name,
            Colunas=self.columns,
            dados=['A1','A2', 123]
        )
        self.database.apagarDados(
            nomeTabela=self.table_name
        )
        data = self.database.verDados(
            nomeTabela=self.table_name
        )
        self.assertEqual(len(data), 0)
    
    def test_numeroTabelas(self):
        data = self.database.numeroTabelas
        self.assertEqual(data, 1)
    
    def test_nomeTabelas(self):
        data = self.database.nomeTabelas
        self.assertEqual(data, [self.table_name])
    
    def test_totalColunas(self):
        data = self.database.numeroColunas(self.table_name)
        self.assertEqual(data, 3)
    
    def test_totalColunas(self):
        data = self.database.nomeColunas(self.table_name)[1:]
        self.assertEqual(data, self.columns)
    
    def test_totalLinhas(self):
        [self.database.inserirDados(
            nomeTabela=self.table_name,
            Colunas=self.columns,
            dados=['Web', 'Tech', value]
        ) for value in range(10)]
        data = self.database.totalLinhas(self.table_name)
        self.assertEqual(data, 10)
    
    def test_totalLinhas(self):
        [self.database.inserirDados(
            nomeTabela=self.table_name,
            Colunas=self.columns,
            dados=['Web', 'Tech', value]
        ) for value in range(10)]
        data = self.database.ultimaLinha(self.table_name)
        self.assertEqual(list(data), [10, 'Web', 'Tech', 9])

if __name__ == '__main__':
    unittest.main()