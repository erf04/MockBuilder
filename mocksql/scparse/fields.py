from .base import BaseField
from datetime import datetime
from faker import Faker
class IntegerField(BaseField):

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f"IntegerField({self.name})"
     

    def get_sql_type(self):
        return "INTEGER"
    
    def fake(self,**kwargs):
        return Faker().random_int(**kwargs)
    

class StringField(BaseField):

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f"StringField({self.name})"
    

    def get_sql_type(self):
        return "VARCHAR(255)"

    def fake(self,**kwargs):
        return Faker().name(**kwargs)

class DateTimeField(BaseField):

    def __str__(self):
        return self.name
    
    def get_sql_type(self):
        return "TIMESTAMP"
    
    def fake(self,**kwargs):
        return Faker().date_time(**kwargs)



        

class BooleanField(BaseField):

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"BooleanField({self.name})"
    
    
    def get_sql_type(self):
        return "BOOLEAN"
    
    def fake(self,**kwargs):
        return Faker().boolean(**kwargs)
    


class DateField(BaseField):
    def get_sql_type(self):
        return "DATE"
    
    def fake(self,**kwargs):
        return Faker().date(**kwargs)
    


class EmailField(StringField):
    
    def get_sql_type(self):
        return "NVARCHAR(255)"
    def fake(self,**kwargs):
        return Faker().email(**kwargs)  


    


