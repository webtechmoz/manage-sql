import hashlib as sh
import json

class EncryptValue:
    """
    Encrypts a given value using SHA-512 hashing.

    Attributes:
    ----------
    value_hashed : str
        The SHA-512 hashed value of the input.

    Methods:
    ----------
    __init__(value: str)
        Initializes the class with the value to be hashed, and hashes it using SHA-512.
    """
    def __init__(
        self,
        value
    ):
        """
        Initializes the encryption by hashing the input value.

        Parameters:
        ----------
        value : str
            The string value to be hashed.
        
        Example:
        ----------
        >>> EncryptValue("my_password").value_hashed
        'c9b3e32f...'
        """

        hash = sh.sha512()
        hash.update(value.encode('UTF-8'))
        self.value_hashed = hash.hexdigest()

class Types:
    """
    A collection of various SQL data types grouped by category.

    Nested Classes:
    ----------
    __Integer : Provides SQL integer types like TINYINT, SMALLINT, etc.
    Decimal : Allows the definition of decimal types with custom precision.
    __Text : Provides SQL text types like TINYTEXT, TEXT, etc.
    Char : Allows the definition of CHAR and VARCHAR types with custom length.
    Binary : Allows the definition of BINARY and VARBINARY types with custom length.
    __Blob : Provides SQL blob types like TINYBLOB, BLOB, etc.
    __DateTime : Provides SQL date/time types like DATETIME, TIMESTAMP, etc.

    Methods:
    ----------
    Enum(values: tuple[str]) -> str
        Defines an SQL ENUM type with the provided values.
    
    Set(values: tuple[str]) -> str
        Defines an SQL SET type with the provided values.
    """
    class __Integer:
        """Provides SQL integer data types."""
        @property
        def tinyint(self) -> str:
            return 'TINYINT'
        
        @property
        def smallint(self) -> str:
            return 'SMALLINT'
        
        @property
        def mediumint(self) -> str:
            return 'MEDIUMINT'
        
        @property
        def integer(self) -> str:
            return 'INTEGER'
        
        @property
        def bigint(self) -> str:
            return 'BIGINT'
    
    class Decimal:
        """
        Defines SQL decimal types with precision and scale.

        Parameters:
        ----------
        max_digit : int
            Maximum number of digits for the decimal.
        
        float_digit : int
            Number of digits after the decimal point.
        """

        def __init__(
            self,
            max_digit: int,
            float_digit: int
        ):
            self.__max_digit = max_digit
            self.__float_digit = float_digit
        
        @property
        def decimal(self) -> str:
            return f'DECIMAL({self.__max_digit}, {self.__float_digit})'
        
        @property
        def float(self) -> str:
            return f'DECIMAL({self.__max_digit}, {self.__float_digit})'
        
        @property
        def double(self) -> str:
            return f'DECIMAL({self.__max_digit}, {self.__float_digit})'
    
    class __Text:
        """Provides SQL text data types."""

        @property
        def tinytext(self) -> str:
            return 'TINYTEXT'
        
        @property
        def text(self) -> str:
            return 'TEXT'
        
        @property
        def mediumtext(self) -> str:
            return 'MEDIUMTEXT'
        
        @property
        def longtext(self) -> str:
            return 'LONGTEXT'
    
    class Char:
        """
        Defines SQL character types (CHAR, VARCHAR).

        Parameters:
        ----------
        length : int
            The length of the character type.
        """

        def __init__(
            self,
            length: int
        ):
            self.__length = length
        
        @property
        def char(self) -> str:
            return f'CHAR({self.__length})'
        
        @property
        def varchar(self) -> str:
            return f'VARCHAR({self.__length})'
    
    class Binary:
        """
        Defines SQL binary types (BINARY, VARBINARY).

        Parameters:
        ----------
        length : int
            The length of the binary type.
        """

        def __init__(
            self,
            length: int
        ):
            self.__length = length
        
        @property
        def binary(self) -> str:
            return f'BINARY({self.__length})'
        
        @property
        def varbinary(self) -> str:
            return f'VARBINARY({self.__length})'
    
    class __Blob:
        """Provides SQL blob data types."""

        @property
        def tinyblob(self) -> str:
            return 'TINYBLOB'
        
        @property
        def blob(self) -> str:
            return 'BLOB'
        
        @property
        def mediumblob(self) -> str:
            return 'MEDIUMBLOB'
        
        @property
        def longblob(self) -> str:
            return 'LONGBLOB'
    
    class __DateTime:
        """Provides SQL date and time data types."""

        @property
        def datetime(self) -> str:
            return 'DATETIME'
        
        @property
        def date(self) -> str:
            return 'DATE'
        
        @property
        def hour(self) -> str:
            return 'HOUR'
        
        @property
        def timestamp(self) -> str:
            return 'TIMESTAMP'
        
        @property
        def year(self) -> str:
            return 'YEAR'
    
    def Enum(self, values: tuple[str]) -> str:
        """Defines an SQL ENUM type with the provided values."""

        return f'ENUM({', '.join(values)})'
    
    def Set(self, values: tuple[str]) -> str:
        """Defines an SQL SET type with the provided values."""

        return f'SET({', '.join(values)})'
    
    Integer = __Integer()
    Text = __Text()
    DateTime = __DateTime()
    Blob = __Blob()

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
        default_value (Any):
            The default value for the column.
        unsigned (bool):
            Whether the column is unsigned.
        on_update (str):
            The action to take on update (e.g., `CURRENT_TIMESTAMP`).
    """

    def __init__(
        self,
        name: str,
        column_type: Types,
        primary_key: bool = False,
        auto_increment: bool = False,
        unique: bool = False,
        not_null: bool = False,
        default_value = None,
        unsigned: bool = False,
        on_update: str = None
    ):
        """
        Initializes a Column object with the provided attributes.

        Example:
        ----------
        >>> Column('id', Types.Integer.tinyint, primary_key=True, auto_increment=True)
        """

        self.name = name
        self.type = column_type
        self.column_parameters = f'{name} {column_type}'

        self.__primary_key: bool = primary_key
        self.__auto_increment: bool = auto_increment
        self.__unique: bool = unique
        self.__not_null: bool = not_null
        self.__default_value = default_value
        self.__unsigned: bool = unsigned
        self.__on_update: str = on_update

        
        if primary_key == True:
            self.column_parameters += f' PRIMARY KEY'
        
        if auto_increment == True:
            self.column_parameters += f' AUTO_INCREMENT'
        
        if unique == True:
            self.column_parameters += f' UNIQUE'
        
        if not_null == True:
            self.column_parameters += f' NOT NULL'
        
        if unsigned == True:
            self.column_parameters += f' UNSIGNED'
        
        if default_value != None:
            self.column_parameters += f' DEFAULT {default_value}'
        
        if on_update != None:
            self.column_parameters += f' ON UPDATE {on_update}'
    
    def __to_dict(self):
        """Converts the column attributes to a dictionary."""

        return {
            "name": self.name,
            "type": self.type,
            "primary_key":  self.__primary_key,
            "auto_increment": self.__auto_increment,
            "unique":  self.__unique,
            "not_null":  self.__not_null,
            "default_value": self.__default_value,
            "unsigned":  self.__unsigned,
            "on_update": self.__on_update
        }
    
    def to_json(self):
        """Converts the column to JSON format."""

        return json.dumps(self.__to_dict(), indent=4)

class Table:
    def __init__(
        self,
        name: str
    ):
        self.columns: list[Column] = []
        self.name = name
    
    def __to_dict(self):
        """Converte a tabela e suas colunas para um dicionário."""
        return {
            'table_name': self.name,
            'columns': [column._Column__to_dict() for column in self.columns]
        }

    def to_json(self):
        return json.dumps(self.__to_dict(), indent=4)

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
    
    def NOT_EQUAL(self, value):
        """Adds a not equality filter."""

        self.__add_filter(condition='!=', value=value)
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
    
    def NOT_CONTAIN(self, value):
        """Adds a 'NOT LIKE' filter for partial matches."""

        self.__add_filter(condition='NOT LIKE', value=f'%{value}%')
        return self
    
    def __add_filter(self, condition: str, value):
        """Helper method to add a filter with a specific condition and value."""

        self.__params.append(value)
        self.__condition += f'{condition} %s '

class ColumnData:
    def __init__(
        self,
        column: str,
        value: str | int | float | bool | None
    ):
        """
        Initialize a ColumnData instance.

        :param column: The name of the column.
        :param value: The value associated with the column.
        """
        self.column = column
        self.value = value