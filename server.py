from flask import Flask
from flask import request

app = Flask(__name__) 

@app.route('/')
def index():
    return 'Hello' 

@app.route('/request', methods=['POST'])
def process_request():
	print(request.is_json)
	content = request.get_json()
	print(content)
	print(content['id'])
	print(content['name'])
	return content['name']

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)