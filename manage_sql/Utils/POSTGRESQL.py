import psycopg2 as postgresql

try:
    from ..Utils.utils_postgres import (
        Types,
        Table,
        Column,
        ColumnData,
        Filter,
        EncryptValue
    )

except:
    from .utils_postgres import (
        Types,
        Table,
        Column,
        ColumnData,
        Filter,
        EncryptValue
    )

class POSTGRESQL:
    """
    A class to manage PostgreSQL database connections and operations.

    Attributes:
        postgre_url (str): The connection URL for the PostgreSQL database.
        host (str): The host address for the PostgreSQL server.
        username (str): The username for the PostgreSQL connection.
        database (str): The name of the database to connect to.
        password (str): The password for the PostgreSQL connection.
        port (int): The port for the PostgreSQL server. Default is 5432.
        column_types (Types): A reference to column types.
        Column (Column): A reference to the `Column` object.
        filter_by (Filter): A reference to the `Filter` object for filtering.
        delete_by (Filter): A reference to the `Filter` object for deleting.
        ColumnData (ColumnData): A reference to column data.
        CURRENT_TIMESTAMP (str): String constant for the PostgreSQL current timestamp.
    """

    def __init__(
        self,
        postgre_url: str = None,
        host: str = None,
        username: str = None,
        database: str = None,
        password: str = None,
        port: int = 5432
    ):
        """
        Initializes the POSTGRESQL class with optional connection details.

        Args:
            postgre_url (str): The connection URL for PostgreSQL.
            host (str): The host address of the PostgreSQL server.
            username (str): The username for connecting to the database.
            database (str): The name of the database to connect to.
            password (str): The password for connecting to the database.
            port (int): The port number for PostgreSQL, default is 5432.
        """

        self.__postgres_url = postgre_url
        self.__host = host
        self.__username = username
        self.__password = password
        self.__database = database
        self.__port = port
        self.column_types = Types()
        self.Column = Column
        self.filter_by = Filter
        self.delete_by = Filter
        self.ColumnData = ColumnData
        self.CURRENT_TIMESTAMP = 'CURRENT_TIMESTAMP'
    
    @property
    def __connect(self):
        """
        Private property that establishes a connection to the PostgreSQL database.

        Returns:
            tuple: A connection object and a cursor object.
        """

        def connect_with_url():
            connection = postgresql.connect(
                dsn=self.__postgres_url
            )

            connection.autocommit = True

            return connection

        def connect_without_database():
            connection = postgresql.connect(
                host = self.__host,
                port = self.__port,
                user = self.__username,
                password = self.__password
            )
            
            connection.autocommit = True
            return connection
        
        def connect_with_database():
            connection = postgresql.connect(
                host = self.__host,
                port = self.__port,
                database = self.__database,
                user = self.__username,
                password = self.__password
            )

            connection.autocommit = True
            return connection
        
        if self.__postgres_url != None:
            connection = connect_with_url()

            cursor = connection.cursor()
            return connection, cursor
        
        else:
            if not self.__database:
                connection = connect_without_database()

                cursor = connection.cursor()
                return connection, cursor
            
            else:
                try:
                    connection = connect_with_database()

                    cursor = connection.cursor()
                    return connection, cursor
                
                except:
                    try:
                        connection = connect_without_database()
                        connection.cursor().execute(f'CREATE DATABASE IF NOT EXISTS {self.__database}')

                        connection = connect_with_database()
                        cursor = connection.cursor()
                        return connection, cursor
                    
                    except Exception as e:
                        self.__exception_error(message_error=e)
                    
                    finally:
                        connection.close()
    
    @property
    def tables(self) -> list[Table]:
        """
        Property to retrieve a list of all tables in the public schema of the database.

        Returns:
            list[Table]: A list of Table objects representing the database tables.
        """
        
        connection, cursor = self.__connect
            
        cursor.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema='public'"
        )

        tables = cursor.fetchall()

        db_tables: list[Table] = []

        for table in tables:
            if table[0] != 'sqlite_sequence':
                table_info = Table(name=table[0])
                cursor.execute(
                    f"""
                    SELECT 
                        c.column_name, 
                        c.data_type,
                        CASE WHEN tc.constraint_type = 'PRIMARY KEY' THEN 'YES' ELSE 'NO' END AS is_primary_key,
                        CASE WHEN c.column_default LIKE 'nextval%' THEN 'YES' ELSE 'NO' END AS is_identity,
                        CASE WHEN c.is_nullable = 'NO' THEN 'NO' ELSE 'YES' END AS is_nullable,
                        c.column_default
                    FROM information_schema.columns AS c
                    LEFT JOIN information_schema.table_constraints AS tc 
                        ON c.table_name = tc.table_name 
                        AND c.table_schema = tc.table_schema
                    LEFT JOIN information_schema.key_column_usage AS kcu 
                        ON kcu.table_name = c.table_name AND kcu.column_name = c.column_name 
                        AND kcu.table_schema = c.table_schema
                    WHERE c.table_name = '{table[0]}';
                    """
                )

                columns = cursor.fetchall()

                for column in columns:
                    table_info.columns.append(
                        Column(
                            name = column[0],
                            column_type = column[1],
                            primary_key = column[2],
                            auto_increment = column[3],
                            not_null = column[4],
                            default_value = column[5] if column[5] else None
                        )
                    )
                
                db_tables.append(table_info)
        
        connection.close()

        return db_tables
    
    @property
    def drop_database(self) -> None:
        """
        Drops the connected database.

        Raises:
            Exception: If there's an error in dropping the database.
        """

        try:
            connection, cursor = self.__connect

            if self.__database != None:
                cursor.execute(f'DROP DATABASE {self.__database}')
            
            else:
                cursor.execute(f'DROP DATABASE {self.__postgres_url}')
        
        except Exception as e:
            self.__exception_error(message_error=e)
        
        finally:
            connection.close()
    
    def create_table(self, tablename: str, columns: list[Column]) -> None:
        """
        Creates a new table in the database with the specified columns.

        Args:
            tablename (str): The name of the table to be created.
            columns (list[Column]): A list of Column objects representing the table schema.

        Raises:
            Exception: If there's an error in creating the table.
        """

        try:
            columns_details: list[Column] = [
                Column(
                    name='id',
                    column_type=self.column_types.Integer.serial,
                    primary_key=True
                ),
                *columns
            ]

            all_columns = ', '.join(column.column_parameters for column in columns_details)
            
            connection, cursor = self.__connect
            cursor.execute(
                f'CREATE TABLE IF NOT EXISTS {tablename} ({all_columns})'
            )

            connection.close()
        
        except Exception as e:
            self.__exception_error(message_error=e)
    
    def insert_data(self, tablename: str, insert_query: list[ColumnData]) -> None:
        """
        Inserts data into a specified table.

        Args:
            tablename (str): The name of the table where data will be inserted.
            insert_query (list[ColumnData]): A list of ColumnData objects representing the data to be inserted.

        Raises:
            Exception: If there's an error in inserting the data.
        """

        columns: str = ', '.join([f'{edit.column}' for edit in insert_query])
        params: list = [edit.value for edit in insert_query]
        key: str = ', '.join('%s' for _ in insert_query)

        try:
            connection, cursor = self.__connect

            cursor.execute(
                f'INSERT INTO {tablename} ({columns}) VALUES ({key})', tuple(params)
            )

            connection.commit()
            connection.close()
        
        except Exception as e:
            self.__exception_error(message_error=e)
    
    def detele_data(self, tablename: str, condition: Filter = None):
        """
        Deletes data from a specified table, optionally filtered by a condition.

        Args:
            tablename (str): The name of the table where data will be deleted.
            condition (Filter, optional): A Filter object representing the condition for deletion.

        Raises:
            Exception: If there's an error in deleting the data.
        """

        connection, cursor = self.__connect

        if not condition:
            cursor.execute(f'DELETE FROM {tablename}')
        
        else:
            condition_query = condition._Filter__condition.strip()
            condition_params = condition._Filter__params

            cursor.execute(f'DELETE FROM {tablename} {condition_query}', tuple(condition_params))
        
        connection.commit()
        connection.close()
    
    def select_data(self, tablename: str, columns: list[str] = ['*'], condition: Filter = None):
        """
        Selects data from a specified table.

        Args:
            tablename (str): The name of the table to select data from.
            columns (list[str], optional): A list of columns to retrieve. Defaults to all columns.
            condition (Filter, optional): A Filter object for query conditions.

        Returns:
            list: A list of tuples containing the fetched rows.
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
        Updates data in a specified table.

        Args:
            tablename (str): The name of the table to update.
            edit_query (list[ColumnData]): A list of ColumnData objects representing the columns and their new values.
            condition (Filter, optional): A Filter object to specify which rows to update.

        Raises:
            Exception: If there's an error in updating the data.
        """
        
        connection, cursor = self.__connect
        columns: str = ', '.join([f'{edit.column} = %s' for edit in edit_query])
        params: list = [edit.value for edit in edit_query]

        if not condition:
            cursor.execute(f"UPDATE {tablename} SET {columns}", tuple(params))
        
        else:
            condition_query: str = condition._Filter__condition.strip()
            params.extend(condition._Filter__params)

            cursor.execute(f"UPDATE {tablename} SET {columns} {condition_query}", tuple(params))
        
        connection.commit()
        connection.close()
    
    def add_column(self, tablename: str, column: Column):
        """
        Adds a new column to an existing table.

        Args:
            tablename (str): The name of the table to modify.
            column (Column): The column to add to the table.

        Raises:
            Exception: If there's an error adding the column.
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
            tablename (str): The name of the table to modify.
            column_name (str): The name of the column to drop.

        Raises:
            Exception: If there's an error dropping the column.
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
        Drops a specified table from the database.

        Args:
            tablename (str): The name of the table to drop.

        Raises:
            Exception: If there's an error dropping the table.
        """

        connection, cursor = self.__connect

        cursor.execute(f'DROP TABLE IF EXISTS {tablename}')

        connection.commit()
        connection.close()
    
    def encrypt_value(self, value) -> str:
        """
        Encrypts a given value.

        Args:
            value: The value to encrypt.

        Returns:
            str: The encrypted value.
        """

        return EncryptValue(value).value_hashed

    def execute_query(self, query: str):
        """
        Executes a raw SQL query.

        Args:
            query (str): The raw SQL query to execute.

        Returns:
            list: A list of tuples representing the result of the query.
        """

        try:
            connection, cursor = self.__connect

            cursor.execute(query)

            return cursor.fetchall()
        
        finally:
            connection.close()
    
    def __exception_error(self, message_error: str):
        """
        Handles exceptions and prints the error message.

        Args:
            message_error (str): The error message to be printed.
        """
        
        print(f'Error: {message_error}')
        exit()