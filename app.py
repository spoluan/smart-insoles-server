from flask import Flask, request

app = Flask(__name__) 

@app.route('/')
def index():
    return 'Hello' 

@app.route('/request', methods=['POST'])
def processrequest():
    return "key %s, val %s" % (request.form['key'], request.form['val'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)