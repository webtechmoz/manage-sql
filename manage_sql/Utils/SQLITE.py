import sqlite3 as sq
import os
import multiprocessing

try:
    from ..Utils.utils_sqlite import (
        Types,
        Table,
        Column,
        ColumnData,
        Filter,
        EncryptValue
    )

except:
    from .utils_sqlite import (
        Types,
        Table,
        Column,
        ColumnData,
        Filter,
        EncryptValue
    )

class SQLITE:
    """
    A class to manage SQLite database operations such as creating tables, inserting, updating, deleting, and selecting data.
    
    Attributes:
        database (str):
            The name of the SQLite database file.
        path (str, optional):
            The path to the folder where the database will be saved. Defaults to 'database'.
        Column_types (Types):
            Defines column types for the database tables.
        Column (Column):
            A class representing the structure of a column in a table.
        filter_by (Filter):
            Defines filtering rules for queries.
        delete_by (Filter):
            Defines rules for deletion by filtering.
        ColumnData (ColumnData):
            Manages column data, such as values to be inserted or updated.
    """
    def __init__(
        self,
        database: str,
        path: str = 'database'
    ):
        """
        Initializes the SQLITE class with the provided database name and path.

        Args:
            database : str
                Name of the database file.
            path : str, optional
                Directory where the database file will be stored. Defaults to 'database'.
        """

        self.__database = database
        self.__path = path
        self.Column_types = Types
        self.Column = Column
        self.filter_by = Filter
        self.delete_by = Filter
        self.ColumnData = ColumnData
    
    @property
    def __connect(self) -> tuple[sq.Connection, sq.Cursor]:
        """
        Establishes a connection to the SQLite database and returns the connection and cursor.

        Returns:
            tuple[Connection, Cursor]: The SQLite connection and cursor.

        Raises:
            Exception:
                If there is an error connecting to the database or creating the directory.
        """
        def create_connection() -> tuple[sq.Connection, sq.Cursor]:

            if not self.__path.endswith('.db'):
                self.__path = os.path.join(self.__path, f'{self.__database}.db')

            connection = sq.connect(self.__path)
            cursor = connection.cursor()

            return connection, cursor
        
        try:
            os.mkdir(path=self.__path)

            return create_connection()
        
        except Exception as e:
            if 'WinError 183' in str(e):
                return create_connection()
            
            else:
                self.__exception_error(message_error=e)
    
    @property
    def tables(self) -> list[Table]:
        """
        Retrieves a list of all tables in the database.

        Returns:
            list[Table]: A list of Table objects containing table names and their respective columns.
        """

        connection, cursor = self.__connect
            
        tables = cursor.execute(
            'SELECT name FROM sqlite_master WHERE type = "table"'
        ).fetchall()

        db_tables: list[Table] = []

        for table in tables:
            if table[0] != 'sqlite_sequence':
                table_info = Table(name=table[0])
                columns = cursor.execute(
                    f'PRAGMA table_info({table[0]})'
                ).fetchall()

                for column in columns:
                    table_info.columns.append(
                        Column(
                            name=column[1],
                            column_type=self.Column_types(value=column[2])
                        )
                    )
                
                db_tables.append(table_info)
        
        connection.close()

        return db_tables
    
    @property
    def drop_database(self) -> None:
        """
        Drops the SQLite database by removing the database file.
        """

        connection, _ = self.__connect
        connection.close()

        try:
            os.remove(self.__path)
        
        except Exception as e:
            self.__exception_error(message_error=e)
    
    def create_table(self, tablename: str, columns: list[Column]) -> None:
        """
        Creates a table with the specified columns in the database.

        Args:
            tablename (str): Name of the table to be created.
            columns (list[Column]): List of Column objects defining the structure of the table columns.
        """

        def create_table_multi(table_name: str, columns: str):
            connection, cursor = self.__connect
            cursor.execute(
                f'CREATE TABLE IF NOT EXISTS {table_name} ({columns})'
            )

            connection.close()

        try:
            columns_details: list[Column] = [
                Column(
                    name='id',
                    column_type=self.Column_types.integer,
                    primary_key=True,
                    auto_increment=True
                ),
                *columns
            ]

            all_columns = ', '.join(column.column_parameters for column in columns_details)
            multiprocessing.Process(
                target=create_table_multi,
                args=(tablename, all_columns),
                daemon=True
            ).start()

        except Exception as e:
            self.__exception_error(message_error=e)
    
    def insert_data(self, tablename: str, insert_query: list[ColumnData]) -> None:
        """
        Inserts data into the specified table.

        Args:
            tablename: (str): Name of the table where data will be inserted.
            insert_query: (list[ColumnData]): List of ColumnData objects containing the data to be inserted.
        """

        def insert_data_multi(table_name: str, columns: str, key: str, params: list[None]):
            connection, cursor = self.__connect

            cursor.execute(
                f'INSERT INTO {table_name} ({columns}) VALUES ({key})', tuple(params)
            )

            connection.commit()
            connection.close()

        columns: str = ', '.join([f'{edit.column}' for edit in insert_query])
        params: list = [edit.value for edit in insert_query]
        key: str = ', '.join('?' for _ in insert_query)

        try:
            multiprocessing.Process(
                target=insert_data_multi,
                args=(tablename, columns, key, params),
                daemon=True
            ).start()
        
        except Exception as e:
            self.__exception_error(message_error=e)

    def detele_data(self, tablename: str, condition: Filter = None):
        """
        Deletes data from the specified table with an optional condition.

        Args:
            tablename (str): Name of the table where data will be deleted.
            condition (Filter, optional): Filtering condition to specify which records to delete.
        """

        def delete_data_multi(tablename: str, condition: str):
            connection, cursor = self.__connect

            if not condition:
                cursor.execute(f'DELETE FROM {tablename}')
            
            else:
                condition_query = condition._Filter__condition.strip()
                condition_params = condition._Filter__params

                cursor.execute(f'DELETE FROM {tablename} {condition_query}', tuple(condition_params))
            
            connection.commit()
            connection.close()
        
        try:
            multiprocessing.Process(
                target=delete_data_multi,
                args=(tablename, condition),
                daemon=True
            ).start()
        
        except Exception as e:
            self.__exception_error(message_error=e)
    
    def select_data(self, tablename: str, columns: list[str] = ['*'], condition: Filter = None):
        """
        Selects data from the specified table.

        Args:
            tablename (str):
                Name of the table to select data from.
            columns (list[str], optional):
                List of column names to select. Defaults to all columns ('*').
            condition (Filter, optional):
                Condition to filter the data.

        Returns:
            list: List of fetched records from the table.
        """

        connection, cursor = self.__connect

        if not condition:
            cursor.execute(f'SELECT {', '.join(columns)} FROM {tablename}')

        else:
            condition_query: str = condition._Filter__condition.strip()
            condition_params: list = condition._Filter__params

            cursor.execute(f'SELECT {', '.join(columns)} FROM {tablename} {condition_query}', tuple(condition_params))

        dados = cursor.fetchall()

        connection.close()

        return dados
    
    def update_data(self, tablename: str, edit_query: list[ColumnData], condition: Filter = None):
        """
        Updates data in the specified table.

        Args:
            tablename (str):
                Name of the table where data will be updated.
            edit_query (list[ColumnData]):
                List of ColumnData objects containing the new data.
            condition (Filter, optional):
                Condition to specify which records to update.
        """

        def update_data_multi(table_name: str, columns: str, params: list):
            connection, cursor = self.__connect

            if not condition:
                cursor.execute(f"UPDATE {tablename} SET {columns}", tuple(params))
            
            else:
                condition_query: str = condition._Filter__condition.strip()
                params.extend(condition._Filter__params)

                cursor.execute(f"UPDATE {tablename} SET {columns} {condition_query}", tuple(params))
            
            connection.commit()
            connection.close()
        

        columns: str = ', '.join([f'{edit.column} = ?' for edit in edit_query])
        params: list = [edit.value for edit in edit_query]

        try:
            multiprocessing.Process(
                target=update_data_multi,
                args=(tablename, columns, params),
                daemon=True
            ).start()
        
        except Exception as e:
            self.__exception_error(message_error=e)
    
    def add_column(self, tablename: str, column: Column):
        """
        Adds a new column to an existing table.

        Args:
            tablename (str):
                Name of the table where the column will be added.
            column (Column):
                The Column object defining the new column.
        """

        try:
            connection, cursor = self.__connect

            column_details = column.column_parameters
            cursor.execute(f'ALTER TABLE {tablename} ADD COLUMN {column_details}')

            connection.commit()
        
        except:
            pass

        finally:
            connection.close()
    
    def drop_column(self, tablename: str, column_name: str):
        """
        Drops a column from an existing table.

        Args:
            tablename (str):
                Name of the table from which the column will be dropped.
            column_name (str):
                Name of the column to be dropped.
        """

        try:
            connection, cursor = self.__connect
            cursor.execute(f'ALTER TABLE {tablename} DROP COLUMN {column_name}')

            connection.commit()
        
        except:
            pass

        finally:
            connection.close()
    
    def drop_table(self, tablename: str):
        """
        Drops a table from the database.

        Args:
            tablename (str):
                Name of the table to be dropped.
        """

        connection, cursor = self.__connect

        cursor.execute(f'DROP TABLE IF EXISTS {tablename}')

        connection.commit()
        connection.close()
    
    def execute_query(self, query: str):
        """
        Executes a raw SQL query on the SQLite database.

        Args:
            query (str):
                The raw SQL query string to be executed.

        Returns:
            list:
            A list of tuples representing the fetched results from the query.
            If the query does not return any result (e.g., INSERT, UPDATE), it will return an empty list.

        Example:
        ----------
        >>> db.execute_query('SELECT * FROM users WHERE age > 30')
        [(1, 'John', 35), (2, 'Jane', 40)]

        Raises:
            Exception:
                If there is an error in executing the SQL query, the exception is logged or raised.
        """

        def execute_query_multi(query: str):
            try:
                connection, cursor = self.__connect

                cursor.execute(query)

                return cursor.fetchall()
            
            finally:
                connection.close()
        
        multiprocessing.Process(
            target=execute_query_multi,
            args=(query),
            daemon=True
        ).start()
            
    
    def encrypt_value(self, value) -> str:
        """
        Encrypts a given value using a predefined encryption method.

        Args:
            value (str):
                The value to be encrypted (usually a sensitive value like a password).

        Returns:
            str:
                The encrypted (hashed) version of the input value.

        Example:
        ----------
        >>> db.encrypt_value('mypassword')
        '5f4dcc3b5aa765d61d8327deb882cf99'

        Notes:
        ----------
        The encryption algorithm used is defined in the EncryptValue class, which must be
        implemented to handle the encryption logic, such as hashing with salt.

        Raises:
            Exception:
                If there is an error during encryption, the exception is logged or raised.
        """
        return EncryptValue(value).value_hashed

    def __exception_error(self, message_error: str):
        print(f'Error: {message_error}')
        exit()