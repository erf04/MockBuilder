from schema_parser.parser import SchemaParser
from sql_generator.generator import DDLGenerator
import mysql.connector
from mock_builder.builder import MockBuilder
from schema_parser.fields import EmailField
from faker import Faker



parser = SchemaParser.fr
parser.register_field("email",EmailField)
parser.parse()
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1383Aram",
    database="library",
    port = 3306
)
# print(connection.__repr__())
# parser.get_table()
# parser.register_field("date",BaseField)
# print(connection.is_connected())
ddl_generator = DDLGenerator(connection=connection,parser=parser)
# print(ddl_generator.gen())
ddl_generator.emit()
# print(list(tables.keys()))
# ddl_generator.emit()
mock_builder = MockBuilder(parser=parser)
mocks = mock_builder.build_sql_commands()
print(mocks)
ddl_generator.emit(mocks)
# mock_builder.register_mock_field(field_class=EmailField,fake_function=Faker().email)
# print(mocks)
# ddl_generator.emit(sql_command="".join(mocks))

# print(SQLConvertor(parser).connection)
# print(tables)