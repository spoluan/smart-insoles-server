from flask import Flask
from flask import request, Response

app = Flask(__name__) 

@app.route('/')
def index():
    return 'Hello' 

@app.route('/requesting', methods=['POST', 'GET', 'PUT'])
def process_request():
	if request.method == 'GET':
		return "Get key: %s, val: %s" % (request.args.get('key'), request.args.get('value'))
	elif request.method == 'POST':
		return "Post key: %s, val: %s" % (request.form['key'], request.form['val'])
	else:
		return "Put method"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)