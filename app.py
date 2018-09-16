from flask import Flask, request, jsonify

app = Flask(__name__) 

@app.route('/')
def index():
    return 'Hello' 

@app.route('/req', methods=['POST'])
def prreq():
    input_json = request.get_json(force=True) 
#    print 'data from client:', input_json
    dictToReturn = {'answer': 42}
    return jsonify(dictToReturn)
#    return "key %s, val %s" % (request.form['key'], request.form['val'])

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)