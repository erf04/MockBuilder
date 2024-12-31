from mocksql.parser import SchemaParser
from mocksql.generator import DDLGenerator
import mysql.connector
from mocksql.builder import MockBuilder
from mocksql.scparse.fields import EmailField
from faker import Faker
from mocksql.emitter import MySQLEmitter,PostgresEmitter
import psycopg2

parser = SchemaParser.from_json_file("schema.json")
# print(parser)
parser.register_field_type("email",EmailField)
parser.parse()
# connection = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="1234",
#     database="test",
#     port = 3307
# )
connection = psycopg2.connect(
    host = "localhost",
    database = "test",
    user = "postgres",
    password = "koala04"
)
# print(connection.__repr__())
# parser.get_table()
# parser.register_field("date",BaseField)
# print(connection.is_connected()
ddl_generator = DDLGenerator(parser=parser)
# print(ddl_generator.gen())
# print(ddl_generator.gen())
# emitter = MySQLEmitter(connection=connection)
# emitter.emit_all(ddl_generator.gen())
# print(list(tables.keys()))
# ddl_generator.emit()
emitter = PostgresEmitter(connection=connection)
emitter.emit_all(ddl_generator.gen())

mock_builder = MockBuilder(parser=parser)
mocks = mock_builder.build_sql_commands_list()
print(mocks)
# emitter.emit_all(mocks)
# mock_builder.register_mock_field(field_class=EmailField,fake_function=Faker().email)
# print(mocks)
# ddl_generator.emit(sql_command="".join(mocks))

# print(SQLConvertor(parser).connection)
# print(tables)