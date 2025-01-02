from mocksql.parser import SchemaParser
from mocksql.generator import DDLGenerator
import mysql.connector
from mocksql.builder import MockBuilder
from mocksql.scparse.fields import EmailField
from faker import Faker
import psycopg2
from mocksql.emitter import PostgresEmitter



parser = SchemaParser.from_json_file("schema.json")
parser.register_field_type("email",EmailField)
parser.parse()
connection = psycopg2.connect(
database="test", user="postgres", password="1383Aram", host="localhost", port=5432
)
# print(connection.__repr__())
# parser.get_table()
# parser.register_field("date",BaseField)
# print(connection.is_connected())
# ddl_generator = DDLGenerator(connection=connection,parser=parser)
# print(ddl_generator.gen())
# ddl_generator.emit()
# print(list(tables.keys()))
# ddl_generator.emit()
ddlGenerator = DDLGenerator(parser=parser)
# print(ddlGenerator.gen())
emitter = PostgresEmitter(connection=connection)
emitter.emit_all(ddlGenerator.gen())

mock_builder = MockBuilder(parser=parser)
mocks = mock_builder.build_sql_string()
print("done")
emitter.emit_all(mocks)
# ddl_generator.emit(mocks)
# mock_builder.register_mock_field(field_class=EmailField,fake_function=Faker().email)
# print(mocks)
# ddl_generator.emit(sql_command="".join(mocks))

# print(SQLConvertor(parser).connection)
# print(tables)


