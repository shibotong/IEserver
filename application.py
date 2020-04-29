from flask import Flask, request, send_file
import json
from connection import DBConnection
from flask_mysqldb import MySQL
import Config



app=Flask(__name__)
app.config['MYSQL_HOST'] = Config.host
app.config['MYSQL_USER'] = Config.user
app.config['MYSQL_PASSWORD'] = Config.password
app.config['MYSQL_DB'] = Config.database
db = DBConnection(app)

return_default = {'return_code': '200', 'return_info': 'success', 'result': False}

@app.route('/test', methods=["GET"])
def testing():
    query = 'select * from physical_activity'
    result = []
    rv = db.get_activity()
    print(rv)
    return str(rv)

@app.route("/", methods=["GET"])
def main_page():
    return_str = """
    <p>This is the server of ActiDiabet App. This server only provide APIs for ActiDiabet Application. </p>
    <p>'/activity': return all activities</p>
    
    <p>'/adduser/zipcode_intensity': create a new user and return userid, </p>
    <p>'/Intensity': get all intensity levels</p>
    <p>'/addreview/userid_activityid_rating': post the rating of user</p>
    <p>'/activity/search/byID/<activityID>': return a specific activity with id </p>
    <p>'/activity/recommendation/<userid>' : get recommendation with specific user id (return 2 activities)</p>
    <p>'/activity/search/byString/<search>': search activities</p>
    <p>'/activity/place/<postcode>': get all open spaces for specific postcode</p>
    <p>'/activity/pool/<postcode>': get all pools for specific postcode</p>

    """
    return return_str

@app.route("/adduser")
def new_user(insert):
    return_dict = return_default.copy()
    result = db.add_user(insert) # returns the newly registered user ID
    return_dict['result'] = result
    return json.dumps(return_dict)


## WIP
@app.route("/addreview/<string:insert>")
def new_review(insert):
    result = db.add_review(insert)
    return result


@app.route("/intensity", methods=["GET"])
def get_intensity():
    return_dict = return_default.copy()
    return_str = db.get_intensity()
    return_dict['result'] = return_str
    return json.dumps(return_dict, ensure_ascii=False)

@app.route("/activity", methods=["GET"])
def get_activity():
    return_dict = return_default.copy()
    return_str = db.get_activity()
    return_dict['result'] = return_str
    return json.dumps(return_dict, ensure_ascii=False),200,{'contentType': 'application/json'}


@app.route("/activity/search/byID/<activityId>")
def search_activity_byID(activityId):
    return_dict = return_default.copy()
    return_str = db.match_acticityName_by_id(activityId)
    return_dict['result'] = return_str
    return json.dumps(return_dict, ensure_ascii=False)


@app.route("/activity/search/byName/<activityName>")
def search_activityID_byName(activityName):
    return_dict = return_default.copy()
    return_str = db.match_acticityId_by_name(activityName)
    return_dict['result'] = return_str
    return json.dumps(return_dict, ensure_ascii=False)


@app.route("/activity/search/byString/<search>")
def search_activity(search):
    return_dict = return_default.copy()
    return_str = db.get_activity_with_string(search)
    return_dict['result'] = return_str
    return json.dumps(return_dict, ensure_ascii=False)


@app.route("/activity/recommendation/<userid>")
def get_recommend(userid):
    return_dict = return_default.copy()
    return_str = db.get_recommend_activity(userid) 
    return_dict['result'] = return_str
    return json.dumps(return_dict, ensure_ascii=False)

@app.route("/activity/place/<postcode>")
def get_place(postcode):
    return_dict = return_default.copy()
    return_str = db.get_openSpace(postcode) 
    return_dict['result'] = return_str
    return json.dumps(return_dict, ensure_ascii=False)

@app.route("/activity/pool/<postcode>")
def get_pool(postcode):
    return_dict = return_default.copy()
    return_str = db.get_pool(postcode) 
    return_dict['result'] = return_str
    return json.dumps(return_dict, ensure_ascii=False)

@app.route("/activity/img/<imgID>")
def get_img(imgID):
    filename = './img/exercise_' + imgID + '.png'
    return send_file(filename, mimetype='image/png')

if __name__ == "__main__":
    app.run(debug=True)

