import mysql.connector
from mysql.connector import Error

class DBConnection:

    host = 'db1.crcnvu3pnfow.ap-southeast-2.rds.amazonaws.com'
    database = 'b8_db'
    user = 'admin'
    password = 'abcd1234'
    
    def add_user(self,insert):
        connection = mysql.connector.connect(user=self.user, database=self.database, host=self.host, password=self.password)
        input = insert.split("_")
        input1 = input[1]
        input2 = input[0]
        query = "insert into app_user (user_id, intensity, postcode) values (null,'" + input1 + "'," + input2 + ")"
        cursor = connection.cursor()

        cursor.execute(query)
        connection.commit()
        
        # get id
        cursor.execute('''select max(user_id) from b8_db.app_user''')
        maxid = cursor.fetchone()[0]
        connection.close()
        return str(maxid)


    def match_acticityName_by_id(self,activity_id):
        connection = mysql.connector.connect(user=self.user, database=self.database, host=self.host, password=self.password)
        query = 'select * from physical_activity where activity_id =' + activity_id
        cursor = connection.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        result = []
        for record in records:
            activity = self.perform_activity(record)
            result.append(activity)
        connection.close()
        return result


    def match_acticityId_by_name(self,activity_name):
        connection = mysql.connector.connect(user=self.user, database=self.database, host=self.host, password=self.password)
        query = 'select * from physical_activity where activity_name  like "%' + activity_name + '%"'
        cursor = connection.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        connection.close()
        result = []
        for record in records:
            activity = self.perform_activity(record)
            result.append(activity)
        return result

    
    def add_review(self,insert): 
        connection = mysql.connector.connect(user=self.user, database=self.database, host=self.host, password=self.password)
        input = insert.split("_")
        userId = input[0]
        activityId = input[1]
        reviewRating = input[2]
        query = "insert into popularity_review (review_id, user_id, activity_id, review_rating)\
            values (null," + userId + "," + activityId + "," + reviewRating +")"
        cursor = connection.cursor()

        cursor.execute(query)
        connection.commit()
        connection.close()
        return "Successfully added a review"

    
    def get_activity(self):
        connection = mysql.connector.connect(user=self.user, database=self.database, host=self.host, password=self.password)
        query = 'select * from physical_activity'
        cursor = connection.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        connection.close()
        result = []
        for record in records:
            activity = self.perform_activity(record)
            result.append(activity)
        return result

    def get_activity_with_string(self, search):
        connection = mysql.connector.connect(user=self.user, database=self.database, host=self.host, password=self.password)
        query = 'select * from physical_activity where activity_name like "%' + search + '%"'
        cursor = connection.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        connection.close()
        result = []
        for record in records:
            activity = self.perform_activity(record)
            result.append(activity)
        return result


    def find_place(self, record):
        place = {}
        place['place_name'] = record[0]
        place['long'] = record[1]
        place['lat'] = record[2]
        return place

    def get_openSpace(self, postcode):
        connection = mysql.connector.connect(user=self.user, database=self.database, host=self.host, password=self.password)
        query = 'SELECT space_name, space_long, space_lat FROM b8_db.public_open_space where postcode = ' + postcode
        cursor = connection.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        connection.close()
        result = []
        for record in records:
            place = self.find_place(record)
            result.append(place)
        return result

    def get_pool(self, postcode):
        connection = mysql.connector.connect(user=self.user, database=self.database, host=self.host, password=self.password)
        query = 'SELECT pool_name, pool_long, pool_lat FROM b8_db.swimming_pool where postcode = ' + postcode
        cursor = connection.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        connection.close()
        result = []
        for record in records:
            place = self.find_place(record)
            result.append(place)
        return result


    #TODO indoor query and outdoor query

    def get_recommend_activity(self, userid):
        connection = mysql.connector.connect(user=self.user, database=self.database, host=self.host, password=self.password)
        query = 'select p.activity_id, activity_name, a.video_url, a.activity_type, a.duration_min, a.indoor_only, a.video_url_short,sum(review_rating) as ranking \
            from popularity_review p join physical_activity a on p.activity_id = a.activity_id\
                 where p.activity_id not in (\
                    select activity_id from popularity_review where user_id = ' + userid + ' and review_rating = -1)\
                        group by p.activity_id having ranking > 0\
                            order by ranking desc;'
                                
        cursor = connection.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        connection.close()
        result = []
        for record in records:
            activity = self.perform_activity(record)
            result.append(activity)
        return result


    def get_intensity(self):
        connection = mysql.connector.connect(user=self.user, database=self.database, host=self.host, password=self.password)
        query = 'select * from intensity_level'
        cursor = connection.cursor()
        cursor.execute(query)
        records = cursor.fetchall()
        connection.close()
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
        activity['id'] = record[0]
        activity['activity_name'] = record[1]
        activity['type'] = record[3]
        activity['duration'] = record[4]
        activity['indoor'] = record[5]
        activity['video_url'] = record[6]
        return activity
