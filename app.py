from flask import Flask, request

app = Flask(__name__) 

@app.route('/')
def index():
    return 'Hello' 

@app.route('/req', methods=['POST'])
def prreq():
    return "key %s, val %s" % (request.json['key'], request.json['val'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)