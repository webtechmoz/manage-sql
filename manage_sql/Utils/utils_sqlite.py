from enum import Enum
import hashlib as sh

class EncryptValue:
    """
    Encrypts a given value using SHA-512 hashing.

    Attributes:
        value_hashed (str):
            The SHA-512 hashed value of the input.
    """

    def __init__(
        self,
        value
    ):
        """
        Initializes the encryption by hashing the input value.

        Parameters:
            value (str):
                The string value to be hashed.
        
        Example:
        ----------
        >>> EncryptValue("my_password").value_hashed
        'c9b3e32f...'
        """

        hash = sh.sha512()
        hash.update(value.encode('UTF-8'))
        self.value_hashed = hash.hexdigest()


class Types(Enum):
    """
    A collection of various SQL data types.
    """

    integer = 'INTEGER'
    text = 'TEXT'
    real = 'REAL'
    null = 'NULL'
    blob = 'BLOB'

class Column:
    """
    Represents a SQL table column with various parameters.

    Attributes:
        name (str):
            The name of the column.
        column_type (Types):
            The SQL data type for the column.
        column_parameters (str):
            The compiled column parameters string.
        primary_key (bool):
            Whether the column is a primary key.
        auto_increment (bool):
            Whether the column has auto-increment enabled.
        unique (bool):
            Whether the column has a unique constraint.
        not_null (bool):
            Whether the column has a NOT NULL constraint.
    """
    def __init__(
        self,
        name: str,
        column_type: Types,
        primary_key: bool = False,
        auto_increment: bool = False,
        unique: bool = False,
        not_null: bool = False
    ):
        """
        Initializes a Column object with the provided attributes.

        Example:
        ----------
        >>> Column('id', Types.integer, primary_key=True, auto_increment=True)
        """
        self.name = name
        self.type = column_type

        if not isinstance(column_type, Types):
            raise ValueError(f'O tipo da coluna deve ser um valor de `column_types`, e não {type(column_type)}.')
        
        self.column_parameters = f'{name} {column_type.value}'
        
        if primary_key == True:
            self.column_parameters += f' PRIMARY KEY'
        
        if auto_increment == True:
            self.column_parameters += f' AUTOINCREMENT'
        
        if unique == True:
            self.column_parameters += f' UNIQUE'
        
        if not_null == True:
            self.column_parameters += f' NOT NULL'
    
    def to_dict(self):
        """Converts the column attributes to a dictionary."""
        return {
            'name': self.name,
            'type': self.type.value,
            'parameters': self.column_parameters
        }

class Table:
    def __init__(
        self,
        name: str
    ):
        self.columns: list[Column] = []
        self.name = name
    
    def to_dict(self):
        """Converte a tabela e suas colunas para um dicionário."""
        return {
            'table_name': self.name,
            'columns': [column.to_dict() for column in self.columns]
        }

class Filter:
    def __init__(
        self,
        column: str
    ):
        self.column_name = column
        self.__condition: str = f"WHERE {column} "
        self.__params: list = []
    
    def filterby(self, column):
        """Adds a filter condition."""

        self.__condition += f'{column} '
        return self

    @property
    def OR(self):
        """Adds an OR clause."""

        self.__condition += "OR "
        return self
    
    @property
    def AND(self):
        """Adds an AND clause."""

        self.__condition += "AND "
        return self
    
    def EQUAL(self, value):
        """Adds an equality filter."""

        self.__add_filter(condition='=', value=value)
        return self
    
    def GATHER_THAN(self, value):
        """Adds a greater-than filter."""

        self.__add_filter(condition='>', value=value)
        return self
    
    def GATHER_OR_EQUAL(self, value):
        """Adds a greater-than-or-equal-to filter."""

        self.__add_filter(condition='>=', value=value)
        return self
    
    def LESS_THAN(self, value):
        """Adds a less-than filter."""

        self.__add_filter(condition='<', value=value)
        return self
    
    def LESS_OR_EQUAL(self, value):
        """Adds a less-than-or-equal-to filter."""

        self.__add_filter(condition='<=', value=value)
        return self
    
    def CONTAIN(self, value):
        """Adds a 'LIKE' filter for partial matches."""

        self.__add_filter(condition='LIKE', value=f'%{value}%')
        return self
    
    def __add_filter(self, condition: str, value):
        """Helper method to add a filter with a specific condition and value."""

        self.__params.append(value)
        self.__condition += f'{condition} ? '

class ColumnData:
    """
    Initialize a ColumnData instance.

    :param column: The name of the column.
    :param value: The value associated with the column.
    """
    def __init__(
        self,
        column: str,
        value: str | int | float | bool | None
    ):
        self.column = column
        self.value = value