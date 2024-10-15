import hashlib as sh
import json

class EncryptValue:
    def __init__(
        self,
        value
    ):
        hash = sh.sha512()
        hash.update(value.encode('UTF-8'))
        self.value_hashed = hash.hexdigest()

class Types:
    class __Integer:
        @property
        def smallint(self) -> str:
            return 'SMALLINT'.lower()
        
        @property
        def integer(self) -> str:
            return 'INTEGER'.lower()
        
        @property
        def bigint(self) -> str:
            return 'BIGINT'.lower()
        
        @property
        def serial(self) -> str:
            return 'SERIAL'.lower()
        
        @property
        def bigserial(self) -> str:
            return 'BIGSERIAL'.lower()
    
    class Float:
        @property
        def real(self) -> str:
            return 'REAL'.lower()
        
        @property
        def double_precision(self) -> str:
            return 'DOUBLE PRECISION'.lower()
    
    class Decimal:
        def __init__(
            self,
            max_digit: int,
            float_digit: int
        ):
            self.__max_digit = max_digit
            self.__float_digit = float_digit
        
        @property
        def decimal(self) -> str:
            return f'DECIMAL({self.__max_digit}, {self.__float_digit})'.lower()
        
        @property
        def numeric(self) -> str:
            return f'NUMERIC({self.__max_digit}, {self.__float_digit})'.lower()
    
    class Char:
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
    
    class Bit:
        def __init__(
            self,
            length: int
        ):
            self.__length = length
        
        @property
        def bit(self) -> str:
            return f'bit({self.__length})'
        
        @property
        def bit_varying(self) -> str:
            return f'bit varying({self.__length})'
    
    class __DateTime:
        @property
        def date(self) -> str:
            return 'date'
        
        @property
        def time(self) -> str:
            return 'time'
        
        @property
        def timestamp(self) -> str:
            return 'TIMESTAMP'
        
        @property
        def timestamp_with_time_zone(self) -> str:
            return 'timestamp with time zone'
    
    class Geometry:
        @property
        def line(self) -> str:
            return 'line'
        
        @property
        def point(self) -> str:
            return 'point'
        
        @property
        def circle(self) -> str:
            return 'circle'
    
    class Array:
        @property
        def integer(self) -> str:
            return 'integer[]'
        
        @property
        def text(self) -> str:
            return 'text[]'
    
    class Json:
        @property
        def json(self) -> str:
            return 'json'
        
        @property
        def jsonb(self) -> str:
            return 'jsonb'
    
    class Range:
        @property
        def int_range(self) -> str:
            return 'int4range'
        
        @property
        def date_range(self) -> str:
            return 'daterange'
    
    class NetAdress:
        @property
        def ip(self) -> str:
            return 'inet'
        
        @property
        def mac(self) -> str:
            return 'macaddr'
    
    @property
    def uuid(self) -> str:
        return 'uuid'
    
    @property
    def Text(self) -> str:
        return 'TEXT'.lower()
    
    @property
    def Interval(self) -> str:
        return 'interval'
    
    @property
    def Boolean(self) -> str:
        return 'boolean'
    
    @property
    def Money(self) -> str:
        return 'money'
    
    Integer = __Integer()
    DateTime = __DateTime()

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
    ):
        self.name = name
        self.type = column_type
        self.column_parameters = f'{name} {column_type}'

        self.__primary_key: bool = primary_key
        self.__auto_increment: bool = auto_increment
        self.__unique: bool = unique
        self.__not_null: bool = not_null
        self.__default_value = default_value

        
        if primary_key == True:
            self.column_parameters += f' PRIMARY KEY'
        
        if auto_increment == True:
            self.column_parameters += f' SERIAL'
        
        if unique == True:
            self.column_parameters += f' UNIQUE'
        
        if not_null == True:
            self.column_parameters += f' NOT NULL'
        
        if default_value != None:
            self.column_parameters += f' DEFAULT {default_value}'
    
    def __to_dict(self):
        """Converte a coluna para um dicionário."""
        return {
            "name": self.name,
            "type": self.type,
            "primary_key":  self.__primary_key,
            "auto_increment": self.__auto_increment,
            "unique":  self.__unique,
            "not_null":  self.__not_null,
            "default_value": self.__default_value,
        }
    
    def to_json(self):
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
        self.column = column
        self.value = value