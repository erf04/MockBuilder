from schema_parser.table import Table
from schema_parser.mapper import FIELD_TYPE_MAPPING
from schema_parser.base import BaseField
from typing import Dict
class SchemaParser:
    def __init__(self, schema:dict):
        """
        .. highlight:: python
        Initialize a SchemaParser with a given schema.

        .. code-block:: python

        Parameters:
            schema (dict): A dictionary defining the structure of the database schema,
                    including tables and their fields. 
        >>> parser = SchemaParser(schema)
        >>> parser.parse()



        """

        self.schema:Dict[str,Dict[str]] = schema
        self._tables:Dict[str,Table] = {}


    def parse(self):
        """
        Parse the schema and instantiate Table objects.
        """
        for table_name, table_data in self.schema.get("tables", {}).items():
            fields = {}
            for field_name, field_data in table_data.get("fields", {}).items():
                field_type = field_data.get("type")
                if not field_type:
                    raise ValueError(f"Field '{field_name}' in table '{table_name}' is missing a type.")

                field_class = FIELD_TYPE_MAPPING.get(field_type)
                if not field_class:
                    raise ValueError(f"Unknown field type '{field_type}' in table '{table_name}'.Have you registered the field {field_type}?")

                # Instantiate the field class
                field_args = {k: v for k, v in field_data.items() if k != "type"}
                # print(field_args)
                field_object:BaseField = field_class(field_name,**field_args)

                fields[field_name] = field_object
            kwargs = {k: v for k, v in table_data.items() if k != "fields"}
            # Instantiate the table
            self._tables[table_name] = Table(name=table_name, fields=fields,parser=self,**kwargs)
            

        return self
    

    def get_tables(self) -> dict:
        """
        Return a dictionary of all parsed tables, keyed by table name.

        :return: A dictionary of Table objects, keyed by table name
        """
        return self._tables
    
    def get_table(self, table_name:str) -> Table:
        """
        Retrieve a Table object by its name.

        :param table_name: The name of the table to retrieve.
        :return: The Table object if found, otherwise None.
        """

        return self._tables.get(table_name) if self._tables!={} else None
    

    def register_field(self,field_name:str,field_class:BaseField) -> None:

        """
        Register a custom field class with the parser.

        :param field_name: The name to associate with the custom field class.
        :param field_class: The custom field class to register.
        :type field_class : BaseField
        :return: None
        """
        FIELD_TYPE_MAPPING[field_name] = field_class
    