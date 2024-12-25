class BaseField:
    def __init__(self, name:str,primary_key:bool=False,refrences:str=None,**kwargs):
        """
        Constructor shared by all fields.
        :param value: The value to be validated.
        :param kwargs: Additional arguments for specific fields.
        """
        self.name = name.strip()
        # self.value = self.validate(value)
        self.extra_args = kwargs
        self.is_primary_key = primary_key
        self.refrence = refrences

    def validate(self,value) -> bool:
        """Validation method to be overridden by child classes."""
        raise NotImplementedError("Each field type must implement its own validate method.")
    

    def get_sql_type(self) -> str:
        """Returns the SQL type of the field."""
        raise NotImplementedError("Each field type must implement its own get_sql_type method.")
    

    def fake(self,**kwargs):
        """Returns a fake value for the field."""
        raise NotImplementedError("Each field type must implement its own fake method.")
    

    def get_sql_args(self) -> list[str]:
        """Returns the SQL arguments for the field."""
        return ""

    

    def set_primary_key(self):
        self.is_primary_key = True


    def __str__(self):
        return f"{self.__class__.__name__}({self.name})"



    