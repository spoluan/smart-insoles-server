from flask import Flask
 
@app.route('/')
def index():
    return 'Hello' 

if __name__ == '__main__':
    socketio.run(host='0.0.0.0', debug=True)