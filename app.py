from flask import Flask, request, jsonify, json

app = Flask(__name__) 

@app.route('/')
def index():
    return 'Hello' 

@app.route('/req', methods=['POST'])
def prreq():
    input_json = request.get_json(force=True)  
#    heel = input_json['heel']
#    thumb = input_json['thumb']
#    out_ball = input_json['out_ball']
#    inner_ball = input_json['inner_ball']
    return jsonify(input_json) 

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)