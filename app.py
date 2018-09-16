from flask import Flask, request, jsonify

app = Flask(__name__) 

@app.route('/')
def index():
    return 'Hello' 

@app.route('/req', methods=['POST'])
def prreq():
    input_json = request.get_json(force=True)  
    result = {input_json['key']:input_json['val']}
    return jsonify(result) 

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)