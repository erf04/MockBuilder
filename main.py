from schema_parser.parser import SchemaParser
from sql_generator.generator import DDLGenerator
import mysql.connector
from mock_builder.builder import MockBuilder
from schema_parser.fields import EmailField
from faker import Faker
from emitter import MySQLEmitter
schema = {
    "tables": {
        "users": {
            "fields": {
                "id": {
                    "type": "integer",
                    "primary_key": True
                },
                "name": {
                    "type": "string"
                },
                "email": {
                    "type": "email"

                },
                "date":{
                    "type":"date"  
                },
                "post_id":{
                    "type":"integer",
                    "refrences":"posts"
                }
            },
            "mock_count":20
        },
        "posts": {
            "fields": {
                "id": {
                    "type": "integer",
                    "primary_key": True
                },
                "title": {
                    "type": "string"
                },
                "content": {
                    "type": "string"
                },
                "user_id": {
                    "type": "integer",
                    "refrences": "users"
                }
            },
            "mock_count":10
        },
        "mmd":{
            "fields":{
                "id":{
                    "type":"integer",
                    "primary_key":True
                },
                "name":{
                    "type":"string",
                },
            },
            "mock_count":0
        }
    }
}


parser = SchemaParser(schema)
parser.register_field("email",EmailField)
parser.parse()
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="test",
    port = 3307
)
# print(connection.__repr__())
# parser.get_table()
# parser.register_field("date",BaseField)
# print(connection.is_connected()
ddl_generator = DDLGenerator(parser=parser)
# print(ddl_generator.gen())
ddl_generator.gen()
emitter = MySQLEmitter(connection=connection)
emitter.emit_all(ddl_generator.gen())
# print(list(tables.keys()))
# ddl_generator.emit()

mock_builder = MockBuilder(parser=parser)
mocks = mock_builder.build_sql_commands_list()
print(mocks)
# emitter.emit_all(mocks)
# mock_builder.register_mock_field(field_class=EmailField,fake_function=Faker().email)
# print(mocks)
# ddl_generator.emit(sql_command="".join(mocks))

# print(SQLConvertor(parser).connection)
# print(tables)