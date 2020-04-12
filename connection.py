import mysql.connector
from mysql.connector import Error

class DBConnection:

    host = 'db1.crcnvu3pnfow.ap-southeast-2.rds.amazonaws.com'
    database = 'activity'
    user = 'admin'
    password = 'abcd1234'
    cursor = None
    connection = None

    def __init__(self):
        try:
            # connection to database
            self.connection = mysql.connector.connect(user=self.user, database=self.database, host=self.host, password=self.password)

            if self.connection.is_connected():
                db_info = self.connection.get_server_info()
                print('db_info', db_info)
                self.cursor = self.connection.cursor()
                print('connect to database success')

        except Error as e:
            print(e)

    def get_activity(self):
        query = 'select * from activity'
        self.cursor.execute(query)
        record = self.cursor.fetchall()
        print(record[0])
        return record[0]

    def close(self):
        if(self.connection.is_connected()):
            self.connection.close()
            self.cursor.close()
            print('database disconnected')