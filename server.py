from flask import Flask
from flask import request, Response

app = Flask(__name__) 

@app.route('/')
def index():
    return 'Hello' 

@app.route('/requesting', methods=['POST'])
def process_request():
	print('Recieved from client: {}'.format(request.data))
	return Response('We received something')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)