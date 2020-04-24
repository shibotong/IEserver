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
            activity = self.perform_activity(record)
            result.append(activity)
        return result

    def get_activity_with_string(self, search):
        query = 'select * from physical_activity where activity_name like "%' + search + '%"'
        self.cursor.execute(query)
        records = self.cursor.fetchall()
        result = []
        for record in records:
            activity = self.perform_activity(record)
            result.append(activity)
        return result

    def get_recommend_activity(self, userid):
        query = 'select activity_name, sum(review_rating) as ranking from popularity_review p join physical_activity a on p.activity_id = a.activity_id where p.activity_id not in ( select activity_id from popularity_review where user_id = ' + userid + ' and review_rating = -1) group by p.activity_id having ranking > 0 order by ranking desc limit 2;'
        self.cursor.execute(query)
        records = self.cursor.fetchall()
        result = []
        print(records)

        #TODO get activitie based on out put activity name
        
        
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


    def perform_activity(self, record):
        activity = {}
        activity['id'] =  record[0]
        activity['activity_name'] = record[1]
        activity['type'] = record[3]
        activity['duration'] = record[4]
        activity['indoor'] = record[5]
        activity['video_url'] = record[6]
        return activity


    def close(self):
        if(self.connection.is_connected()):
            self.connection.close()
            self.cursor.close()
            print('database disconnected')