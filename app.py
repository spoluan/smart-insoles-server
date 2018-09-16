from flask import Flask
from flask import request

app = Flask(__name__) 

@app.route('/')
def index():
    return 'Hello' 

@app.route('/requesting', methods=['POST', 'GET', 'PUT'])
def process_request():
    if request.method == 'GET':
        return "Get key: %s, val: %s" % (request.args.get('key'), request.args.get('value'))
    elif request.method == 'POST':
        data = request.form.get('data')
        return "Post => heel : %s, thumb: %s, out_ball: %s, inner_ball %s" % (data['heel'], data['thumb'], data['out_ball'], data['inner_ball'])
    else:
        return "Put method"

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)