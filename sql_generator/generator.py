from schema_parser.fields import IntegerField, StringField, DateField
from schema_parser.table import Table
from .base import SQLGenerator
from mock_builder.builder import MockBuilder

class DDLGenerator(SQLGenerator):


    def gen(self):
        """
        Generate the DDL commands to create all tables and their relations.

        :return: The DDL commands as a string
        """
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
            sql_type = field_obj.get_sql_type()
            sql_pk = "PRIMARY KEY" if field_obj.is_primary_key else ""
            sql_str = f"{sql_type} {sql_pk}" if sql_pk else sql_type

            field_definitions.append(f"{field_name} {sql_str}")

        # Join field definitions and construct the CREATE TABLE SQL
        fields_sql = ", ".join(field_definitions)
        # print(fields_sql)
        return f"CREATE TABLE IF NOT EXISTS {table.name} ({fields_sql});"
    

    def handle_relations(self,table:Table):
        sql_str = ""
        # print(self.table.fields)
        for field_name, field_obj in table.fields.items():
            if field_obj.refrence!=None:
                refrence_table:Table = self.parser.get_table(field_obj.refrence)
                related_field = table.get_primary_key()
                sql_str += f"ALTER TABLE {table.name} ADD FOREIGN KEY ({field_name}) REFERENCES {refrence_table.name}({related_field});"
    
        return sql_str
    




