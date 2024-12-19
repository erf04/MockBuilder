from schema_parser.base import BaseField
from typing import Dict

class Table:
    def __init__(self, name:str, fields:dict[str,BaseField],parser,mock_count=0):
        self.name = name
        self.fields = fields
        self.parser = parser
        self.mock_count = mock_count


    def __str__(self):
        return f"table {self.name}"
    

    def __repr__(self):
        return f"Table('{self.name}', {self.fields})"
    

    def get_primary_key(self):
        for field_name, field_obj in self.fields.items():
            if field_obj.is_primary_key:
                return field_name
            

    def has_foreign_key(self):
        for field_name, field_obj in self.fields.items():
            if field_obj.refrence:
                return True
            
        return False