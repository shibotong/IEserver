from flask import Flask, request
import json
from connection import DBConnection

db = DBConnection()

app=Flask(__name__)
@app.route("/", methods=["GET"])
def main_page():
    return 'nothing here'

@app.route("/activity",methods=["GET"])
def check():
    # define a return dictionary
    return_dict = {'return_code': '200', 'return_info': 'success', 'result': False}
    if request.args is None:
        return_dict['return_code'] = '5004'
        return_dict['return_info'] = 'empty'
        return json.dumps(return_dict, ensure_ascii=False)

    # get params
    #get_data = request.args.to_dict()
    #name = get_data.get('name')
    #age = get_data.get('age')
    # operate params

    # configure return dict
    return_dict['result'] = get_activity()

    return json.dumps(return_dict, ensure_ascii=False)

def get_activity():
    #get all activity
    return_str = db.get_activity()
    return return_str

if __name__ == "__main__":
    try:
        app.run(debug=True)
    except KeyboardInterrupt:
        db.close()

