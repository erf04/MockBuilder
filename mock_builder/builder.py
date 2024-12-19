from schema_parser.table import Table
from faker import Faker
from schema_parser import fields
from schema_parser.base import BaseField
from schema_parser.parser import SchemaParser
from typing import Dict,List
class MockBuilder:

    def __init__(self,parser:SchemaParser):
        self.mocks = []
        self.parser:SchemaParser = parser
        # self.table = table
        self.faker = Faker()



    def get_base_insert_sql(self,table:Table):
        base_str = ""
        fields = ",".join(list(table.fields.keys()))
        base_str = f"INSERT INTO {table.name} ({fields}) VALUES "
        return base_str
    

    def set_non_fk_values(self,table:Table,last_pk):
        values = []
        
        for field_name,field_obj in table.fields.items():
            if not field_obj.refrence:
                if field_obj.is_primary_key:
                    values.append(str(last_pk))
                    last_pk += 1
                elif isinstance(field_obj,fields.IntegerField):
                    values.append(str(self.faker.random_int()))
                elif isinstance(field_obj,fields.StringField):
                    values.append(f"{self.faker.word()}")
            else:
                values.append(f"__")
        return values,last_pk
    

    def set_fk_values(self,table:Table,values):
        fields_list = list(table.fields.values())
        for i in range(len(values)):
            if values[i] == "__":
                refrence_table_name = fields_list[i].refrence
                refrence_table = self.parser.get_table(refrence_table_name)
                if refrence_table.mock_count <= 0:
                    raise ValueError(f"Table {refrence_table_name} has no mock count value.")
                values[i] = str(self.faker.random_int(min=1,max=refrence_table.mock_count))

        return values



    def build(self) -> Dict[str,list[list[str]]]:
        final_data = {}
        for _,table_obj in self.parser.tables.items():
            if table_obj.mock_count > 0:
                helper =[]
                base_str = self.get_base_insert_sql(table_obj)
                last_pk=1
                for x in range(table_obj.mock_count):
                    values,last_pk = self.set_non_fk_values(table=table_obj,last_pk=last_pk)
                    final_values = self.set_fk_values(table=table_obj,values=values)
                    helper.append(final_values)
                    # print(final_values)
                final_data[table_obj.name] = helper

        return final_data
    