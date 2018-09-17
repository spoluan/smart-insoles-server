from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

time_right = ''
time_left = ''

standing = []

app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Database(db.Model):
    
    __tablename__ = "tb_mms1407blab"
    
    time = db.Column(db.String(10), primary_key=True)
    status = db.Column(db.String(10), unique=False, nullable=False)
    weight = db.Column(db.Integer)
     
    def __init__(self, time, status, weight):
        self.time = time
        self.status = status
        self.weight = weight
    
    def __repr__(self):
        return 'Database %r' % self.time
        

@app.route('/')
def index():
    return 'Hello' 

@app.route('/req', methods=['POST'])
def prreq():
    global standing, time_left, time_right
    
    input_json = request.get_json(force=True)   
        
    if input_json['status'] == 'right':
        standing.append(['right', input_json['weight'], input_json['time']])
        db.session.add(Database(input_json['time'], 'right', input_json['weight']))
        db.session.commit()
        
    if input_json['status'] == 'left':
        standing.append(['left', input_json['weight'], input_json['time']])
        db.session.add(Database(input_json['time'], 'left', input_json['weight']))
        db.session.commit()
      
#    heel = input_json['heel']
#    thumb = input_json['thumb']
#    out_ball = input_json['out_ball']
#    inner_ball = input_json['inner_ball']
#    
#    total = 0
#    for i in range(len(heel)):
#        total = total + int(heel[i]) + int(thumb[i]) + int(out_ball[i]) + int(inner_ball[i])
#     
#    result = {'heel':heel,'thumb':thumb,'out_ball':out_ball,'inner_ball':inner_ball,'hasil':total}
#    
#    standing = '{}' . format(total)
#    if len(standing_posture) < 2:
#        standing_posture.append(int(total))
#    
#    if len(standing_posture) == 2:  
#        # Index 0 left, index 1 right
#        if standing_posture[1] > 700 and standing_posture[0] > 700 or (standing_posture[1] < 100 and standing_posture[0] < 100):
#            standing = 'Normal'
#        elif standing_posture[0] < 600 and standing_posture[1] > 700:
#            standing = 'Right'
#        elif standing_posture[0] > 700 and standing_posture[1] < 600:
#            standing = 'Left'
#        else:
#            standing = 'Normal' 
#            
#        standing_posture = []
#
#    
        
    passing = {'all_joint': '{} . {}' . format(standing, len(standing))}
    
    if len(standing) == 2:
        if standing[0][2] == standing[1][2] and standing[0][0] != standing[1][0]: # check time and check differet foot
            passing = {'all_joint':'Same_{}' . format(standing)}
        else:
            passing = {'all_joint': 'Different_{}' . format(standing)}
        
        for i in range(len(standing)):
            standing.pop(0)
    
    return jsonify(passing) 

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)