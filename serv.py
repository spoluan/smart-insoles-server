
# File: serv.py
# Author: Sevendi Eldrige Rifki Poluan
# Date: September 1, 2018
# Desc: Heroku server for synchronizing Insoles data and handing request from MSS1407B's lab app

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy # Ref: https://www.codementor.io/garethdwyer/building-a-crud-application-with-flask-and-sqlalchemy-dm3wv7yu2
import os
  
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
    status_ = {'':''} 
    input_json = request.get_json(force=True)
    method_status = input_json['METHOD']
    
    # Create table
    if method_status == 'CREATE':
        status_ = createTable(input_json)  
    
    # Insert data
    if method_status == 'INSERT':   
        status_ = insertData(input_json)  
    
    # Delete data
    if method_status == 'DELETE':
        status_ = deleteData()
    
    # View data
    if method_status == 'VIEW':
        data_length, id, status, weight, time = viewData(input_json)
        if data_length != 0:
            status_ = []
            for i in range(data_length):
                status_.append({'DATA_INDEX':i, 'STATUS':status[i], 'WEIGHT': weight[i], 'TIME':time[i]})
        else:
            status_ = {'STATUS':'EMPTY'}
    
    # 1407BLAB check standing method
    if method_status == 'CHECK':
        data_length, id, status, weight, time = viewData() 
        status_ = checkStanding(status, time, weight) 
        
    # Delete by time
    if method_status == 'DEL_BY_TIME':
        status_ = deleteByTime(input_json)
        
    return jsonify(status_) 

def createTable(input_json):
    try: 
        db.create_all()
        status_ = {'STATUS':'CREATE_TABLE_OK'}
        return status_
    except: 
        status_ = {'STATUS':'CREATE_TABLE_NO'}
        return status_
    
def insertData(input_json):
    try: 
        db.session.add(Database(input_json['STATUS'], input_json['WEIGHT'], input_json['TIME']))
        db.session.commit()
        status_ = {'STATUS':'INSERT_DATA_OK'}
        return status_
    except:
        status_ = {'STATUS':'INSERT_DATA_NO'}
        return status_
            
def deleteData():
    try: 
        data = Database.query.all()
        for i in data: 
            data = Database.query.filter_by(id=i.id).first()
            db.session.delete(data) 
        db.session.commit()
        status_ = {'STATUS':'DELETE_DATA_OK'}
        return status_
    except: 
        status_ = {'STATUS':'DELETE_DATA_NO'}
        return status_
    
def deleteByTime(input_json):
    try: 
        condition = input_json['TIME']
        data = Database.query.filter_by(time=condition).first()
        db.session.delete(data) 
        db.session.commit()
        status_ = {'STATUS':'DELETE_BY_TIME_OK'}
        return status_
    except: 
        status_ = {'STATUS':'DELETE_BY_TIME_NO'}
        return status_

def viewData(input_json):
    try: 
        condition = input_json['TIME']  
        data = Database.query.all() 
        id = []
        status = []
        weight = []
        time = []
        for i in data:
            if i.time == condition:
                id.append(i.id)
                status.append(i.status)
                weight.append(i.weight)
                time.append(i.time)  
            
        return len(data), id, status, weight, time
    
    except:
        return 'EMPTY'
    
def checkStanding(status, time, weight): 
    try: # Handle array exception   
        if (status[0] == 'RIGHT' and status[1] == 'LEFT') or (status[0] == 'LEFT' and status[1] == 'RIGHT'): 
            if time[0] == time[1]:
                right = 0
                left = 0
                if status[0] == 'RIGHT' and status[1] == 'LEFT':
                    right = int(weight[0])
                    left = int(weight[1]) 
                    if right > 700 and left > 700 or (right < 100 and left < 100):
                        status_ = 'NORMAL' # Normal
                    elif left < 600 and right > 700:
                        status_ = 'RIGHT' # Right
                    elif left > 700 and right < 600:
                        status_ = 'LEFT' # Left
                    else:
                        status_ = 'NORMAL' # Normal 
                        
                if status[0] == 'LEFT' and status[1] == 'RIGHT':
                    left = int(weight[0])
                    right = int(weight[1]) 
                    if right > 700 and left > 700 or (right < 100 and left < 100):
                        status_ = 'NORMAL' # Normal
                    elif left < 600 and right > 700:
                        status_ = 'RIGHT' # Right
                    elif left > 700 and right < 600:
                        status_ = 'LEFT' # Left
                    else:
                        status_ = 'NORMAL' # Normal 
                deleteData()
            else: 
                status_ = 'CHECKING_DEL_TIME'
                deleteData()
        else: 
            status_ = 'CHECKING_DEL_SAME' 
            deleteData()  
            
        return {'STATUS':status_}
    except:
        status_ = {'STATUS':'CHECKING_NO'}
        return status_


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)