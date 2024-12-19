from schema_parser.fields import *
from faker import Faker
MOCK_TYPE_MAPPING ={
    IntegerField : Faker().random_int,
    StringField : Faker().word,
    DateField : Faker().date,
    DateTimeField : Faker().date
}