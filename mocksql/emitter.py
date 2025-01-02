
class Emitter:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

        

    
    def emit_one(self, sql_command:str):
        self.cursor.execute(sql_command)
        self.connection.commit()


    def emit_all(self, sql_commands:str):
        commands = sql_commands.split(";")
        for command in commands:
            print("skfns")
            self.cursor.execute(command)
            self.connection.commit()


    def emit_array_of_commands(self,sql_commands:list):
        for command in sql_commands:
            self.cursor.execute(command)
            self.connection.commit()



class MySQLEmitter(Emitter):
    def __init__(self, connection):
        super().__init__(connection)# Call the constructor of the parent class


class PostgresEmitter(Emitter):
    def __init__(self, connection):
        super().__init__(connection)# Call the constructor of the parent class

    def emit_all(self, sql_commands):
        sql_list = [cmd.strip() for cmd in sql_commands.split(";") if cmd.strip()]
        for sql_command in sql_list:
                self.cursor.execute(sql_command)
        self.connection.commit()
                # print("error",sql_command)


    def emit_one(self, sql_command):
        return self.cursor.execute(sql_command)
    

    def emit_array_of_commands(self, sql_commands):
        for sql_command in sql_commands:
            if sql_command!="":
                self.cursor.execute(sql_command)

