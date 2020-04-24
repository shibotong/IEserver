import mysql.connector
from mysql.connector import Error

class DBConnection:

    host = 'db1.crcnvu3pnfow.ap-southeast-2.rds.amazonaws.com'
    database = 'b8_db'
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
        query = 'select * from physical_activity'
        self.cursor.execute(query)
        records = self.cursor.fetchall()
        result = []
        for record in records:
            print(record)
            activity = {}
            activity['id'] = record[0]
            activity['activity_name'] = record[1]
            activity['type'] = record[3]
            activity['duration'] = record[4]
            activity['indoor'] = record[5]
            activity['video_url'] = record[6]
            result.append(activity)
        
        return result

    def get_intensity(self):
        query = 'select * from intensity_level'
        self.cursor.execute(query)
        records = self.cursor.fetchall()
        result = []
        for record in records:
            intensity = {}
            intensity['intensity'] = record[0]
            intensity['duration_aerobic'] = record[1]
            intensity['duration_resistance'] = record[2]
            intensity['description'] = record[3]
            result.append(intensity)
        return result

    def get_activity_with_string(self, search):
        query = 'select * from physical_activity where activity_name like "%' + search + '%"'
        self.cursor.execute(query)
        records = self.cursor.fetchall()
        result = []
        for record in records:
            print(record)
            activity = {}
            activity['activity_name'] = record[0]
            activity['type'] = record[2]
            activity['duration'] = record[3]
            activity['indoor'] = record[4]
            activity['video_url'] = record[5]
            result.append(activity)
        
        return result

    def get_intensity(self):
        query = 'select * from intensity_level'
        self.cursor.execute(query)
        records = self.cursor.fetchall()
        result = []
        for record in records:
            intensity = {}
            intensity['intensity'] = record[0]
            intensity['duration_aerobic'] = record[1]
            intensity['duration_resistance'] = record[2]
            intensity['description'] = record[3]
            result.append(intensity)
        return result

    def get_activity_with_string(self, search):
        query = 'select * from physical_activity where activity_name like "%' + search + '%"'
        print(query)
        self.cursor.execute(query)
        records = self.cursor.fetchall()
        result = []
        for record in records:
            activity = {}
            activity['activity_name'] = record[0]
            activity['type'] = record[2]
            activity['duration'] = record[3]
            activity['indoor'] = record[4]
            activity['video_url'] = record[5]
            result.append(activity)
        
        return result

    def close(self):
        if(self.connection.is_connected()):
            self.connection.close()
            self.cursor.close()
            print('database disconnected')