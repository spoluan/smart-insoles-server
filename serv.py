# 

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy # Ref: https://www.codementor.io/garethdwyer/building-a-crud-application-with-flask-and-sqlalchemy-dm3wv7yu2
import os

time_right = ''
time_left = ''

standing = []

# postgresql-rugged-65055

app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']  
    
db = SQLAlchemy(app)

class Database(db.Model): 
    __tablename__ = "tb_mss1407blab"
    id = db.Column(db.Integer, primary_key = True)
    status = db.Column(db.String(20)) # right | left
    weight = db.Column(db.Integer)
    time = db.Column(db.String(20))
    
    def __init__(self, status, weight, time):
        self.status = status
        self.weight = weight
        self.time = time
        
    def __repr__(self):
        return '<id %r>' % self.id
            

@app.route('/')
def index():
    return 'Hello'  

@app.route('/req', methods=['POST'])
def prreq():
    global standing, time_left, time_right
      
    status_ = {'':''}
    
    input_json = request.get_json(force=True)
    
    # Create table
    try:  
        if input_json['create'] == 'yes':
            db.create_all()
            status_ = input_json
    except: 
        try:
            db.session.add(Database(input_json['status'], input_json['weight'], input_json['time']))
            db.session.commit()
            status_ = input_json
        except:     
            status_ = 'skiped_create'
            pass
        
    # View table
    try:
        if input_json['view'] == 'yes':
            data = Database.query.all()
            status = []
            weight = []
            time = []
            for i in data:
                status.append(i.status)
                weight.append(i.weight)
                time.append(i.time)
            status_ = '{}, {}, {}' . format(status, weight, time)
            
#            if status[0] != status[1] and time[0] == time[1]:
#                right = 0
#                left = 0
#                if status[0] == 'right':
#                    right = int(weight[0])
#                    left = int(weight[1])
#                    
#                if status[0] == 'left':
#                    left = int(weight[0])
#                    right = int(weight[1])
#                     
#                if right > 700 and left > 700 or (right < 100 and left < 100):
#                    status_ = 'Normal' # Normal
#                elif left < 600 and right > 700:
#                    status_ = 'Right' # Right
#                elif left > 700 and right < 600:
#                    status_ = 'Left' # Left
#                else:
#                    status_ = 'Normal' # Normal 
    except: 
        status_ = 'skipped_view'
        pass 
    
#    # Delete table
#    try:
#        if input_json['delete'] == 'yes':
#            data = Database.query.filter_by(time='1:3:32').first()
#            db.session.delete(data)
#            db.session.commit()
#            status_ = input_json
#    except:
#        status_ = 'skipped_delete'
#        pass
      
    passing = {'all_joint': '{}' . format(status_)}
 
    return jsonify(passing) 

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)