from mocksql.scparse.table import Table
from mocksql.scparse.fields import *
from mocksql.scparse.base import BaseField
from typing import Dict
import yaml
import xml.etree.ElementTree as ET
import json

class SchemaParser:


    __FIELD_TYPE_MAPPING={
        "string": StringField,
        "str":StringField,
        "int":IntegerField,
        "integer": IntegerField,
        "boolean": BooleanField,
        "bool":BooleanField,
        "datetime": DateTimeField,
        "date": DateField
    }


    def __init__(self, schema):
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


    @classmethod
    def from_dict(cls, schema_dict):
        """Alternative constructor for creating an instance from a dictionary."""
        return cls(schema_dict)

    @classmethod
    def from_yaml(cls, yaml_string):
        """Alternative constructor for creating an instance from a YAML string."""
        schema_dict = yaml.safe_load(yaml_string)
        return cls(schema_dict)

    @classmethod
    def from_xml(cls, xml_string):
        """Alternative constructor for creating an instance from an XML string."""
        tree = ET.ElementTree(ET.fromstring(xml_string))
        schema_dict = {elem.tag: elem.text for elem in tree.iter()}
        return cls(schema_dict)

    @classmethod
    def from_json(cls, json_string):
        """Alternative constructor for creating an instance from a JSON string."""
        schema_dict = json.loads(json_string)
        return cls(schema_dict)
    

    @classmethod
    def from_json_file(cls, file_path):
        """Alternative constructor for creating an instance from a JSON file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            schema_dict = json.load(f)
        return cls(schema_dict)

    @classmethod
    def from_yaml_file(cls, file_path):
        """Alternative constructor for creating an instance from a YAML file."""
        with open(file_path, 'r', encoding='utf-8') as f:
            schema_dict = yaml.safe_load(f)
        return cls(schema_dict)

    @classmethod
    def from_xml_file(cls, file_path):
        """Alternative constructor for creating an instance from an XML file."""
        tree = ET.parse(file_path)
        schema_dict = {elem.tag: elem.text for elem in tree.iter()}
        return cls(schema_dict)


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

                field_class = self.__FIELD_TYPE_MAPPING.get(field_type)
                if not field_class:
                    raise ValueError(f"Unknown field type '{field_type}' in table '{table_name}'.Have you registered the field {field_type}?")

                # Instantiate the field class
                field_args = {k: v for k, v in field_data.items() if k != "type"}
                # print(field_args)
                field_object:BaseField = field_class(field_name,**field_args)

                fields[field_name] = field_object
            kwargs = {k: v for k, v in table_data.items() if k != "fields"}
            # Instantiate the table
            # print(kwargs)
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
    

    def register_field_type(self,field_name:str,field_class:BaseField) -> None:

        """
        Register a custom field class with the parser.

        :param field_name: The name to associate with the custom field class.
        :param field_class: The custom field class to register.
        :type field_class : BaseField
        :return: None
        """
        self.__FIELD_TYPE_MAPPING[field_name] = field_class
    