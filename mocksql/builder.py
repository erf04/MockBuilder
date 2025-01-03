from mocksql.scparse.table import Table
from mocksql.scparse.base import BaseField
from mocksql.parser import SchemaParser
from typing import Dict,List
import csv
import os

class MockBuilder:

    def __init__(self,parser:SchemaParser):
        self.mocks = []
        self.parser:SchemaParser = parser
        # self.table = table
        self.final_str = ""
        self._fk_dict:Dict[str,List[str]] = {}
        self._non_fk_dict : Dict[str,List[str]] = {}
        self._tables_dict : Dict[str,List[str]] = {}
        self._pk_dict : Dict[str,int] = {}
        



    def get_base_insert_sql(self,table:Table):
        base_str = ""
        base_str = f"INSERT INTO {table.name}"
        return base_str
    

    def get_last_pk(self,table:Table):
        last_pk = self._pk_dict.get(table.name)
        if not last_pk:
            last_pk =0 
        self._pk_dict[table.name] = last_pk+1

        return last_pk+1

    def __get_non_fk_values(self,table:Table):
        values = []
        
        for field_name,field_obj in table.fields.items():
            if not field_obj.refrence:
                if field_obj.is_primary_key:
                    pk=self.get_last_pk(table=table)
                    values.append(str(pk))
                else:
                    values.append(f"'{field_obj.fake()}'")
        return values
    

    def __get_fk_values(self,table:Table):
        values = []
        for field_name,field_obj in table.fields.items():
            if field_obj.refrence:
                refrence_table = self.parser.get_table(field_obj.refrence)
                values.append(str(field_obj.fake(min=1,max=refrence_table.mock_count)))
        return values
    
    def generate_random_value(self,field_obj:BaseField,**kwargs):
        return field_obj.fake(**kwargs)
    
        

    def get_base_update_sql(self,table:Table):
        base_str = ""
        base_str = f"UPDATE {table.name}"
        return base_str
    

    def get_full_values(self,table:Table):
        values = []
        for field_name,field_obj in table.fields.items():
            if field_obj.is_primary_key:
                last_pk = self._pk_dict.get(table.name)
                if last_pk:
                    values.append(last_pk+1)
                else:
                    values.append(1)
                    last_pk=0
                self._pk_dict[table.name] = last_pk+1
            elif field_obj.refrence:
                refrence_table = self.parser.get_table(field_obj.refrence)
                values.append(field_obj.fake(min=1,max=refrence_table.mock_count))
            else:
                values.append(field_obj.fake())
        return values
    
    def __build_fk_fields(self,table:Table,pk:int):
        fk_fields = table.get_fk_fields()
        if len(fk_fields) == 0:
            return ""
        fk_values = self.__get_fk_values(table=table)
        fk_zip = zip(fk_fields,fk_values)
        fk_list = [f"{field} = {value}" for field,value in fk_zip]
        return f"{self.get_base_update_sql(table=table)} SET {','.join(fk_list)} WHERE {table.get_primary_key()} = {pk};"
        # return values

    def __build_non_fk_fields(self,table:Table):
        fk_fields = table.get_non_fk_fields()
        if len(fk_fields) ==0:
            return ""
        fk_values = self.__get_non_fk_values(table=table)
        return f"{self.get_base_insert_sql(table=table)} ({','.join(fk_fields)}) VALUES ({','.join(fk_values)});"
        # return values

    def build_non_fk_mock(self):
        final_data:Dict[str,List[str]] = {}
        for _,table_obj in self.parser._tables.items():
            if table_obj.mock_count > 0:
                for _ in range(table_obj.mock_count):
                    value = final_data.get(table_obj.name)
                    if value:
                        value.append(self.__build_non_fk_fields(table_obj))
                    else:
                        final_data[table_obj.name] = [self.__build_non_fk_fields(table_obj)]
        self._non_fk_dict = final_data
        return self
    

    def __update_for_fk_mock(self) -> Dict[str,list[list[str]]]:
        final_data:Dict[str,List[str]] = {}
        for _,table_obj in self.parser._tables.items():
            if table_obj.has_foreign_key():
                if table_obj.mock_count > 0:
                    for pk in range(1,table_obj.mock_count+1):
                        value = final_data.get(table_obj.name)
                        fk_build = self.__build_fk_fields(table_obj,pk)

                        if value:
                            value.append(fk_build)
                        else:
                            final_data[table_obj.name] = [fk_build]
        self._fk_dict = final_data
        return final_data
    

    def build_sql_string(self):
        self.build_non_fk_mock()
        self.__update_for_fk_mock()
        final =""
        for key,value in self._non_fk_dict.items():
            for sql_str in value:
                final+=sql_str
        for key,value in self._fk_dict.items():
            for sql_str in value:
                final+=sql_str
        return final
    

    def build_sql_file(self,folder_path:str=".") -> None:
        sql_str = self.build_sql_string()
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        with open(f"{folder_path}/mock.sql", "w") as f:
            f.write(sql_str)


    def build_sql_commands_list(self) -> list[str]:
        return self.build_sql_string().split(";")
    

    def build_csv(self,folder_path:str=".") -> None:
        data:Dict[Table,List[str]] = {}
        for table_name,table_obj in self.parser.get_tables().items():
            data[table_obj]=[]
            if table_obj.mock_count > 0:
                for pk in range(1,table_obj.mock_count+1):
                    data[table_obj].append(self.get_full_values(table_obj))

        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        ## Generate CSV            
        for table, rows in data.items():
            with open(f"{folder_path}/{table}.csv", "w", newline="") as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(table.fields)  # Header
                writer.writerows(rows)# Rows

    


        

        
    