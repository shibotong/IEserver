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
    <p>This is the server of Active Boomers the App. This server provide APIs for this particular app only. </p>
    <p>'/adduser/zipcode_intensity': creates a new  user and returns userid, </p>
    <p>'/Intensity': gets all intensity levels in db</p>
    <p>'/addreview/userid_activityid_rating': posts the rating from user</p>
    <p>'/activity': return all activities</p>
    <p>'/activity/search/byID/<activityID>': returns a specific activity associated with the input id </p>
    <p>'/activity/recommendation/<userid>' : gets recommendation for specific user id (return 2 activities)</p>
    <p>'/activity/search/byString/<search>': searches activities by keywords</p>
    <p>'/activity/place/<postcode>': returns all place data associated with the input postcode</p>
    <p>'/activity/recommender/aerobic/<userid>': gets a recommended aerobic activity given input useid</p>
    <p>'/activity/recommender/resistance/<userid>': gets a recommended resistance activity given input useid</p>

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


# returns a aerobic activity based on input userid
@app.route("/activity/recommender/aerobic/<user_id>")
def get_aerobic_recommender(user_id):
    from recommender import algo
    from load_data import data,item_detail,item_list
    import random
    # building model on training data
    trainingSet = data.build_full_trainset()
    algo.fit(trainingSet)

    # generates predictions using trained model
    def rating_pred(user_id,item_list,algo):
        pred = {}
        for i in item_list:
            prediction = algo.predict(user_id, i)
            pred[i] = prediction.est
        return pred

    def generate_weights(user_id,item_list,algo):
        """generates a list of items based on their weights"""   
        weighted_list = []
        pred = rating_pred(user_id,item_list,algo)
    
        for i in pred.keys():
            if pred[i] <0: # if the predicted rating is negative
                weighted_list += [i]
            elif pred[i] <0.9: # if the predicted rating < 0.9
                weighted_list += 2 * [i]
            else: # if pred == 1
                weighted_list += 3 * [i]
        return weighted_list

    def generate_recommendation(user_id,item_list,algo):
        weighted_l = generate_weights(user_id,item_list,algo)
        return random.choice(weighted_l)

    # make sure activity type returned correctly
    found = False
    while not found:
        activityId = str(generate_recommendation(user_id,item_list,algo))
        if db.match_actvityType_by_id(activityId) =='Aerobic exercise':
            found = True
            
    # formatting output data
    return_str = db.match_acticityName_by_id(activityId)
    return_dict = return_default.copy()
    return_dict['result'] = return_str
    return json.dumps(return_dict, ensure_ascii=False)


# returns a resistance activity based on input userid
@app.route("/activity/recommender/resistance/<user_id>")
def get_resistance_recommender(user_id):
    from recommender import algo
    from load_data import data,item_detail,item_list
    import random
    # building model on training data
    trainingSet = data.build_full_trainset()
    algo.fit(trainingSet)

    # generates predictions using trained model
    def rating_pred(user_id,item_list,algo):
        pred = {}
        for i in item_list:
            prediction = algo.predict(user_id, i)
            pred[i] = prediction.est
        return pred

    def generate_weights(user_id,item_list,algo):
        """generates a list of items based on their weights"""   
        weighted_list = []
        pred = rating_pred(user_id,item_list,algo)
    
        for i in pred.keys():
            if pred[i] <0: # if the predicted rating is negative
                weighted_list += [i]
            elif pred[i] <0.9: # if the predicted rating < 0.9
                weighted_list += 2 * [i]
            else: # if pred == 1
                weighted_list += 3 * [i]
        return weighted_list

    def generate_recommendation(user_id,item_list,algo):
        weighted_l = generate_weights(user_id,item_list,algo)
        return random.choice(weighted_l)

    # make sure activity type returned correctly
    found = False
    while not found:
        activityId = str(generate_recommendation(user_id,item_list,algo))
        if db.match_actvityType_by_id(activityId) =='Resistance exercise':
            found = True

    # formatting output data
    return_str = db.match_acticityName_by_id(activityId)
    return_dict = return_default.copy()
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


@app.route("/ratings", methods=["GET"])
def search_ratings():
    return_dict = return_default.copy()
    return_str = db.get_ratings()
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

