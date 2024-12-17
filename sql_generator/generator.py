from schema_parser.fields import IntegerField, StringField, DateField
from schema_parser.table import Table
from .base import SQLGenerator
from schema_parser.base import BaseField

class CreateTableGenerator(SQLGenerator):

    def gen(self):
        """
        Generate a CREATE TABLE SQL statement for a given Table object.
        """
        field_definitions = []
        for field_name, field_obj in self.table.fields.items():
            # Map custom fields to SQL types
            sql_str = None
            if isinstance(field_obj, IntegerField):
                sql_type = "INTEGER"
                sql_pk = "PRIMARY KEY" if field_obj.is_primary_key else ""
                sql_str = f"{sql_type} {sql_pk}"
            elif isinstance(field_obj, StringField):
                sql_str = "TEXT"
            elif isinstance(field_obj, DateField):
                sql_str = "DATE"
            else:
                raise ValueError(f"Unsupported field type for {field_name}")

            field_definitions.append(f"{field_name} {sql_str}")

        # Join field definitions and construct the CREATE TABLE SQL
        fields_sql = ", ".join(field_definitions)
        return f"CREATE TABLE {self.table.name} ({fields_sql});"
    

class RelationGenerator(SQLGenerator):

    def gen(self):
        sql_str = ""
        # print(self.table.fields)
        for field_name, field_obj in self.table.fields.items():
            if field_obj.refrence!=None:
                table:Table = self.parser.get_table(field_obj.refrence)
                related_field = table.get_primary_key()
                sql_str += f"ALTER TABLE {self.table.name} ADD FOREIGN KEY ({field_name}) REFERENCES {table.name}({related_field});"

        return sql_str

