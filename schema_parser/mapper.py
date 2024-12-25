from .fields import *

FIELD_TYPE_MAPPING={
    "string": StringField,
    "str":StringField,
    "int":IntegerField,
    "integer": IntegerField,
    "boolean": BooleanField,
    "bool":BooleanField,
    "datetime": DateTimeField,
    "date": DateField
}