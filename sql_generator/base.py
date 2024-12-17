from schema_parser.table import Table
from schema_parser.parser import SchemaParser


class SQLGenerator:
    def __init__(self,connection,parser:SchemaParser, table:Table):
        self.table = table
        self.parser = parser
        self.connection = connection
        # self.curser = connection.cursor()


    def emit(self):
        self.cursor.execute(self.gen())
        self.connection.commit()


    def gen(self):
        return NotImplementedError("Subclasses must implement this method.")
    
    

    def __str__(self):
        return self.gen()
    
    def __repr__(self):
        return self.gen()
    
