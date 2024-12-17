from schema_parser.parser import SchemaParser
from sql_generator.generator import CreateTableGenerator,RelationGenerator
import mysql.connector
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
            }
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
            }
        }
    }
}


parser = SchemaParser(schema)
tables = parser.parse()
# connection = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="1234",
#     database="test"
# )
for table in tables.values():
    print(CreateTableGenerator(connection=None,parser=parser,table=table).gen())
    print(RelationGenerator(connection=None,parser=parser,table=table).gen())

# print(SQLConvertor(parser).connection)
# print(tables)