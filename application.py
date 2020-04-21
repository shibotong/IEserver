from flask import Flask, request
import json
from connection import DBConnection

db = DBConnection()

app=Flask(__name__)

return_default = {'return_code': '200', 'return_info': 'success', 'result': False}
@app.route("/", methods=["GET"])
def main_page():
    return_str = """
    This is the server of ActiDiabet App. This server only provide APIs for ActiDiabet Application. \n
    '/Intensity': get all intensity levels\n
    """

    return return_str

#@app.route("/activity",methods=["GET"])
#def check():
    # define a return dictionary
#    return_dict = return_default.copy()

#    if request.args is None:
#        return_dict['return_code'] = '5004'
#        return_dict['return_info'] = 'empty'
 #       return json.dumps(return_dict, ensure_ascii=False)
#    return_str = db.get_activity()
 #   return_dict['result'] = return_str

#    return json.dumps(return_dict, ensure_ascii=False)

@app.route("/intensity", methods=["GET"])
def get_intensity():
    return_dict = return_default.copy()
    return_str = db.get_intensity()
    return_dict['result'] = return_str
    return json.dumps(return_dict, ensure_ascii=False)


if __name__ == "__main__":
    try:
        app.run(debug=True)
    except KeyboardInterrupt:
        db.close()

