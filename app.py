from flask import Flask
from flask import request
from flask_json import FlaskJSON, JsonError, json_response, as_json

app = Flask(__name__) 

@app.route('/')
def index():
    return 'Hello' 

@app.route('/requesting', methods=['POST', 'GET', 'PUT'])
def process_request():
    if request.method == 'GET':
        return "Get key: %s, val: %s" % (request.args.get('key'), request.args.get('value'))
    elif request.method == 'POST':
        # Ref: https://scotch.io/bar-talk/processing-incoming-request-data-in-flask
#        req_data = request.get_json()   
#        heel = req_data['heel']
#        thumb = req_data['thumb']
#        outball = req_data['outball']
#        innerball = req_data['innerball']
        
        data = request.get_json(force=True)
        try:
            value = data['heel']
        except (KeyError, TypeError, ValueError):
            raise JsonError(description='Invalid value.')
        
        return json_response(value)
        
        #return '''heel = {}, thumb = {}, outball = {}, innerball = {}''' . format(heel, thumb, outball, innerball)
        
        #data = request.form
        #return "Post => heel : %s, thumb: %s, out_ball: %s, inner_ball %s" % (data.get('heel'), data.get('thumb'), data.get('outball'), data.get('innerball'))
    else:
        return "Put method"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)