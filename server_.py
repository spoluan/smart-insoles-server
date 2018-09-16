from flask import Flask
 
@app.route('/')
def index():
    return 'Hello' 

if __name__ == '__main__':
    socketio.run(app)