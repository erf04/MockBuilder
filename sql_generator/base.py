from schema_parser.table import Table
from schema_parser.parser import SchemaParser

class SQLGenerator:
    def __init__(self,connection, parser:SchemaParser):
        # self.table = table
        self.parser = parser
        self.connection = connection
        self.cursor = connection.cursor()


    def emit(self,sql_command:str=None):
        sql_str = self.gen() if not sql_command else sql_command 
        commands = sql_str.split(";")
        for command in commands:
            self.cursor.execute(command)
            self.connection.commit()


    def gen(self)->str:
        return NotImplementedError("Subclasses must implement this method.")
    
    

    def __str__(self):
        return self.gen()
    
    def __repr__(self):
        return self.gen()

    
