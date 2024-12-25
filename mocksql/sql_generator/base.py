from mocksql.parser import SchemaParser

class SQLGenerator:
    def __init__(self,parser:SchemaParser):
        # self.table = table
        self.parser = parser
    def gen(self)->str:
        return NotImplementedError("Subclasses must implement this method.")

    def __str__(self):
        return self.gen()
    
    def __repr__(self):
        return self.gen()

    
