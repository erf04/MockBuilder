from mocksql.scparse.table import Table
from mocksql.sql_generator.base import SQLGenerator
from mocksql.builder import MockBuilder

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
            sql_args = field_obj.get_sql_args()
            field_definitions.append(f"{field_name} {field_obj.get_sql_type()} {' '.join(sql_args)}")

        # Join field definitions and construct the CREATE TABLE SQL
        fields_sql = ", ".join(field_definitions)
        # print(fields_sql)
        return f"CREATE TABLE IF NOT EXISTS {table.name} ({fields_sql});"
    

    def handle_relations(self,table:Table):
        sql_str = ""
        # print(self.table.fields)
        
        for field_name, field_obj in table.fields.items():
            if field_obj.refrence!=None:
                # print("this line ", field_obj,field_obj.refrence)
                refrence_table:Table = self.parser.get_table(field_obj.refrence)
                related_field = refrence_table.get_primary_key()
                sql_str += f"ALTER TABLE {table.name} ADD FOREIGN KEY ({field_name}) REFERENCES {refrence_table.name}({related_field});"
    
        return sql_str
    




