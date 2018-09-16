from flask import Flask
from flask import request

app = Flask(__name__) 

@app.route('/')
def index():
    return 'Hello' 

@app.route('/request', methods=['PUT'])
def process_request():
	 
	return {'status': 'success', 'message': 'updated'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)