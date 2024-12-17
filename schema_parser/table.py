from schema_parser.base import BaseField
from typing import Dict
class Table:
    def __init__(self, name:str, fields:dict[str,BaseField],mock=True):
        self.name = name
        self.fields = fields
        self.build_mock = mock


    def __str__(self):
        return f"table {self.name}"
    

    def __repr__(self):
        return f"Table('{self.name}', {self.fields})"
    

    def get_primary_key(self):
        for field_name, field_obj in self.fields.items():
            if field_obj.is_primary_key:
                return field_name