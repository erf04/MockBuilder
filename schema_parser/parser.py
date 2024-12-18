from schema_parser.table import Table
from schema_parser.mapper import FIELD_TYPE_MAPPING
from schema_parser.base import BaseField
class SchemaParser:
    def __init__(self, schema:dict):
        self.schema = schema
        self.tables = {}


    def parse(self) ->dict:
        """
        Parse the schema and instantiate Table objects.
        """
        for table_name, table_data in self.schema.get("tables", {}).items():
            fields = {}
            for field_name, field_data in table_data.get("fields", {}).items():
                field_type = field_data.get("type")
                if not field_type:
                    raise ValueError(f"Field '{field_name}' in table '{table_name}' is missing a type.")

                field_class = FIELD_TYPE_MAPPING.get(field_type)
                if not field_class:
                    raise ValueError(f"Unknown field type '{field_type}' in table '{table_name}'.")

                # Instantiate the field class
                field_args = {k: v for k, v in field_data.items() if k != "type"}
                print(field_args)
                fields[field_name] = field_class(field_name,**field_args)

            # Instantiate the table
            self.tables[table_name] = Table(name=table_name, fields=fields,parser=self)
            

        return self.tables
    

    def get_tables(self) -> dict:
        return self.tables
    
    def get_table(self, table_name) -> Table:
        return self.tables.get(table_name) if self.tables!={} else None
    

    def register_field(self,field_name,field_class:BaseField) -> None:
        FIELD_TYPE_MAPPING[field_name] = field_class
    