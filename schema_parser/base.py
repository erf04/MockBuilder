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

    def validate(self,value):
        """Validation method to be overridden by child classes."""
        raise NotImplementedError("Each field type must implement its own validate method.")
    

    def set_primary_key(self):
        self.is_primary_key = True


    def __str__(self):
        return f"{self.__class__.__name__}({self.name})"



    