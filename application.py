from flask import Flask, request, send_file
import json
from pathlib import Path
from connection import DBConnection

db = DBConnection()

app=Flask(__name__)

return_default = {'return_code': '200', 'return_info': 'success', 'result': False}
@app.route("/", methods=["GET"])
def main_page():
    return_str = """
    <p>This is the server of ActiDiabet App. This server only provide APIs for ActiDiabet Application. </p>
    <p>'/adduser/zipcode_intensity': create a new  user and return userid, </p>
    <p>'/Intensity': get all intensity levels</p>
    <p>'/addreview/userid_activityid_rating': post the rating of user</p>
    <p>'/activity': return all activities</p>
    <p>'/activity/search/byID/<activityID>': return a specific activity with id </p>
    <p>'/activity/recommendation/<userid>' : get recommendation with specific user id (return 2 activities)</p>
    <p>'/activity/search/byString/<search>': search activities</p>
    <p>'/activity/place/<postcode>': get all open spaces for specific postcode</p>
    <p>'/activity/pool/<postcode>': get all pools for specific postcode</p>

    """
    return return_str

# performs an SQL query to insert a new user into the db
# when a web browser requests the below URL 
@app.route("/adduser/<string:insert>")
def new_user(insert):
    return_dict = return_default.copy()
    result = db.add_user(insert) # returns the newly registered user ID
    return_dict['result'] = result
    return json.dumps(return_dict)

# performs an SQL query to insert a new user review into the db
# when a web browser requests the below URL 
@app.route("/addreview/<string:insert>")
def new_review(insert):
    result = db.add_review(insert)
    return result

# returns a json object of the intensity data
# when a web browser requests the below URL 
@app.route("/intensity", methods=["GET"])
def get_intensity():
    return_dict = return_default.copy()
    return_str = db.get_intensity()
    return_dict['result'] = return_str
    return json.dumps(return_dict, ensure_ascii=False)

# returns a json object of the activity data
# when a web browser requests the below URL 
@app.route("/activity", methods=["GET"])
def get_activity():
    return_dict = return_default.copy()
    return_str = db.get_activity()
    return_dict['result'] = return_str
    return json.dumps(return_dict, ensure_ascii=False),200,{'contentType': 'application/json'}

# returns a json object of the matched activity data based on the input activity_id
# when a web browser requests the below URL 
@app.route("/activity/search/byID/<activityId>")
def search_activity_byID(activityId):
    return_dict = return_default.copy()
    return_str = db.match_acticityName_by_id(activityId)
    return_dict['result'] = return_str
    return json.dumps(return_dict, ensure_ascii=False)

# returns a json object of the matched activity data based on the input activity_name
# when a web browser requests the below URL 
@app.route("/activity/search/byName/<activityName>")
def search_activityID_byName(activityName):
    return_dict = return_default.copy()
    return_str = db.match_acticityId_by_name(activityName)
    return_dict['result'] = return_str
    return json.dumps(return_dict, ensure_ascii=False)


# returns a json object of the matched activity data based on the input keyword
# when a web browser requests the below URL 
@app.route("/activity/search/byString/<search>")
def search_activity(search):
    return_dict = return_default.copy()
    return_str = db.get_activity_with_string(search)
    return_dict['result'] = return_str
    return json.dumps(return_dict, ensure_ascii=False)

# returns a json object for the recommeded activities
# when a web browser requests the below URL 
@app.route("/activity/recommendation/<userid>")
def get_recommend(userid):
    return_dict = return_default.copy()
    return_str = db.get_recommend_activity(userid) 
    return_dict['result'] = return_str
    return json.dumps(return_dict, ensure_ascii=False)

# returns a json object of the place data 
# (including open spaces and pools that belong to the input postcode)
# when a web browser requests the below URL 
@app.route("/activity/place/<postcode>")
def get_place(postcode):
    return_dict = return_default.copy()
    return_str = db.query_place(postcode) 
    return_dict['result'] = return_str
    return json.dumps(return_dict, ensure_ascii=False)

# to be commented out (no longer in use)
@app.route("/activity/pool/<postcode>")
def get_pool(postcode):
    return_dict = return_default.copy()
    return_str = db.get_pool(postcode) 
    return_dict['result'] = return_str
    return json.dumps(return_dict, ensure_ascii=False)

# returns imnage based on the imgID
# when a web browser requests the below URL
@app.route("/activity/img/<imgID>")
def get_img(imgID):
    filename = Path('./img/' + imgID + '.png')
    if not filename.exists():
        print('file not exist')
        filename = Path('./img/1.png')
    
    return send_file(filename, mimetype='image/png')

if __name__ == "__main__":
    app.run(debug=False)

