from flask import Flask

app = Flask(__name__) 

@app.route('/')
def index():
    return 'Hello' 

@app.route('/request', methods=['GET', 'POST'])
def process_request():
	if request.methods == 'GET':
		return 'GET'
	else:
		return 'POST: key = %s, val = %s' % (request.args.get('key'), request.args.get('val'))
    return 'Hello'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)