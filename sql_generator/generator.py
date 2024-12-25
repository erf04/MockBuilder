from schema_parser.fields import IntegerField, StringField, DateField
from schema_parser.table import Table
from .base import SQLGenerator
from mock_builder.builder import MockBuilder

class DDLGenerator(SQLGenerator):

    def __init__(self, connection, parser,*args,**kwargs):
        super().__init__(connection, parser)

    def gen(self):
        sql_str = ""
        for _,table_obj in self.parser.get_tables().items():
            sql_str += self.create_table(table_obj)
        # print(sql_str)
        for _,table_obj in self.parser.get_tables().items():
            sql_str += self.handle_relations(table_obj)
        return sql_str
    

    def create_table(self,table:Table):
        """
        Generate a CREATE TABLE SQL statement for a given Table object.
        """
        field_definitions = []
        for field_name, field_obj in table.fields.items():
            # Map custom fields to SQL types
            # if isinstance(field_obj, IntegerField):
            #     sql_type = "INT"
            #     sql_pk = "PRIMARY KEY" if field_obj.is_primary_key else ""
            #     sql_str = f"{sql_type} {sql_pk}"
            # elif isinstance(field_obj, StringField):
            #     sql_str = "TEXT"
            # elif isinstance(field_obj, DateField):
            #     sql_str = "DATE"
            # sql_type = SQL_FIELD_TYPE_MAPPING[field_obj.__class__]
            sql_type = field_obj.get_sql_type()
            sql_pk = "PRIMARY KEY" if field_obj.is_primary_key else ""
            sql_str = f"{sql_type} {sql_pk}" if sql_pk else sql_type

            field_definitions.append(f"{field_name} {sql_str}")

        # Join field definitions and construct the CREATE TABLE SQL
        fields_sql = ", ".join(field_definitions)
        print(fields_sql)
        return f"CREATE TABLE {table.name} ({fields_sql});"
    

    def handle_relations(self,table:Table):
        sql_str = ""
        # print(self.table.fields)
        for field_name, field_obj in table.fields.items():
            if field_obj.refrence!=None:
                refrence_table:Table = self.parser.get_table(field_obj.refrence)
                related_field = table.get_primary_key()
                sql_str += f"ALTER TABLE {table.name} ADD FOREIGN KEY ({field_name}) REFERENCES {refrence_table.name}({related_field});"
    
        return sql_str
    


class MockInsertGenerator(SQLGenerator):
    def __init__(self, connection , mockBuilder:MockBuilder):
        super.__init__(connection,mockBuilder.parser)
        self.mock_builder = mockBuilder


    def gen(self):
        mocks = self.mock_builder.build()
        sql_str = ""
        for table_name,mock_data in mocks.items():
            for mock in mock_data:
                sql_str += f"INSERT INTO {table_name} VALUES ({','.join(mock)});"
                # self.emit(sql_str)
        return sql_str



