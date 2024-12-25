from schema_parser.table import Table
from schema_parser.parser import SchemaParser

class SQLGenerator:
    def __init__(self,parser:SchemaParser):
        # self.table = table
        self.parser = parser






    def gen(self)->str:
        return NotImplementedError("Subclasses must implement this method.")
    

    # def register_field(self,field_name:str,field_class:BaseField) -> None:
    
    

    def __str__(self):
        return self.gen()
    
    def __repr__(self):
        return self.gen()

    
