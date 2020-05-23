import pandas as pd 
import pyodbc
import numpy as np
import pymysql
from surprise import Dataset
from surprise import Reader


# Connect to the database
connection = pymysql.connect(
    host='db1.crcnvu3pnfow.ap-southeast-2.rds.amazonaws.com',
    port=int(3306),
    user="admin",
    passwd="abcd1234",
    db="b8_db",
    charset='utf8mb4')


# read SQL query into pandas df
# rating data
sql_select_Query = pd.read_sql_query("select * from b8_db.popularity_review",connection)
rating = pd.DataFrame(sql_select_Query, columns=['review_id','user_id','activity_id','review_rating'])
rating = rating[['activity_id','user_id','review_rating']]
rating.columns = ['item','user','rating']
reader = Reader(rating_scale=(-1, 1))
data = Dataset.load_from_df(rating[["user", "item", "rating"]], reader)

# item data
sql_select_Query = pd.read_sql_query("select activity_id, activity_name, activity_type from b8_db.physical_activity",connection)
item_detail = pd.DataFrame(sql_select_Query, columns=['activity_id','activity_name','activity_type'])
item_detail.columns = ['item_id','item_name','item_type']
item_list = item_detail.item_id

if __name__ == "__main__":
    app.run(debug=False)
