from schema_parser.parser import SchemaParser
from sql_generator.generator import DDLGenerator
import mysql.connector
from mock_builder.builder import MockBuilder
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
                    "type": "string"

                }
            },
            "mock_count":10
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
        }
    }
}


parser = SchemaParser(schema).parse()
connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="test",
    port = 3307
)
# print(connection.is_connected())
ddl_generator = DDLGenerator(connection=connection,parser=parser)
# print(list(tables.keys()))
# ddl_generator.emit()
mocks = MockBuilder(parser=parser).build_sql_commands()
print(mocks)
ddl_generator.emit(sql_command="".join(mocks))

# print(SQLConvertor(parser).connection)
# print(tables)