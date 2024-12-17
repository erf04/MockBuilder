from .base import BaseField
from datetime import datetime
class IntegerField(BaseField):

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f"IntegerField({self.name})"
    
    def validate(self,value):
        if type(value) == int:
            return value
        raise ValueError(f"Invalid value type for {self.name}: {type(value)}. Expected type: int")
    

class StringField(BaseField):

    def __str__(self):
        return self.name
    
    def __repr__(self):
        return f"StringField({self.name})"
    
    def validate(self,value):
        if type(value) == str:
            return value
        raise ValueError(f"Invalid value type for {self.name}: {type(value)}. Expected type: str")


class DateTimeField:

    def __init__(self,name:str,format:str):
        self.name = name.strip()
        self.format = format.strip()
        # self.value = self.validate(value)

    def __str__(self):
        return self.name


    
    def validate(self,value):
        try:
            # Try parsing the date
            parsed_date = datetime.strptime(value, self.format)
            return parsed_date
        except ValueError as e:
            # Raise an error if the date is invalid
            raise ValueError(f"Invalid date: {value}. Expected format: {self.format}")

class BooleanField(BaseField):

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"BooleanField({self.name})"
    

    def validate(self,value):
        if type(value) == bool:
            return value
        raise ValueError(f"Invalid value type for {self.name}: {type(value)}. Expected type: bool")
    


class DateField(DateTimeField):
    pass


    


