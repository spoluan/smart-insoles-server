
# File: serv.py
# Author: Sevendi Eldrige Rifki Poluan
# Date: September 1, 2018
# Desc: Heroku server for synchronizing Insoles data and handing request from MSS1407B's lab app

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy # Ref: https://www.codementor.io/garethdwyer/building-a-crud-application-with-flask-and-sqlalchemy-dm3wv7yu2
# http://docs.sqlalchemy.org/en/rel_0_9/orm/tutorial.html
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
    name = db.Column(db.String(20))
    
    def __init__(self, status, weight, time, name): 
        self.status = status
        self.weight = weight
        self.time = time
        self.name = name
        
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
        status_ = createTable()  
    
    # Insert data
    if method_status == 'INSERT':     
        status_ = insertData(input_json)   
    
    # Delete data
    if method_status == 'DELETE':
        status_ = deleteData()
        
    # Delete by time
    if method_status == 'DEL_BY_TIME':
        status_ = deleteByTime(input_json)
        
    # View data
    if method_status == 'VIEW':
        data_length, id, status, weight, time, name = viewData() 
        if data_length != 0:
            status_ = []
            for i in range(data_length):
                status_.append({'DATA_INDEX':i, 'STATUS':status[i], 'WEIGHT': weight[i], 'TIME':time[i], 'NAME':name[i]})
            status_ = {'STATUS':status_}
        else:
            status_ = {'STATUS':'EMPTY'} 
            
    # Get tag list
    if method_status == 'TAG_LIST':
        status_ = tagNameList()
    
    # 1407BLAB check standing method
    if method_status == 'CHECK': 
        status_ = checkStanding(input_json)
        
    return jsonify(status_) 

def createTable():
    try: 
        db.create_all()
        status_ = {'STATUS':'CREATE_TABLE_OK'}
        return status_
    except: 
        status_ = {'STATUS':'CREATE_TABLE_NO'}
        return status_
    
def insertData(input_json):
    try: 
        if checkInsert(input_json) == True:
            db.session.add(Database(input_json['STATUS'], input_json['WEIGHT'], input_json['TIME'], input_json['NAME']))
            db.session.commit()
            status_ = {'STATUS':'INSERT_DATA_OK'}
        else:
            status_ = {'STATUS':'INSERT_DATA_NO'}
            
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
        n = input_json['NAME']
        data = Database.query.all()
        for i in data:  
            if i.time == condition and i.name == n:
                data = Database.query.filter_by(id=i.id).first() 
                db.session.delete(data) 
        db.session.commit()
        status_ = {'STATUS':'DELETE_BY_TIME_YES'}
        return status_
    except Exception as e: 
        status_ = {'STATUS':'DELETE_BY_TIME_NO'}
        return status_

def viewData():
    try:  
        data = Database.query.all() 
        id = []
        status = []
        weight = []
        time = []
        name = []
        for i in data: 
            id.append(i.id)
            status.append(i.status)
            weight.append(i.weight)
            time.append(i.time)  
            name.append(i.name)
        
        return len(id), id, status, weight, time, name
    
    except:
        return 'EMPTY'

def checkInsert(input_json):
    try: 
        t = input_json['TIME']  
        s = input_json['STATUS']
        n = input_json['NAME']
        data = Database.query.all() 
        id = [] 
        for i in data:
            if i.time == t and i.status == s and i.name == n:
                id.append(i.id) 
         
        if len(id) != 0:
            return False
        else:
            return True 
    except:
        return False

def tagNameList():
    try:  
        data = Database.query.all()  
        name = []
        for i in data:  
            name.append(i.name)
        
        if len(name) > 0:
            return {'STATUS':name} 
        else:
            return {'STATUS':'EMPTY'}
    except:
        return {'STATUS':'EMPTY'}
    
def checkStanding(input_json): 
    try: # Handle array exception  
        t = input_json['TIME']
        n = input_json['NAME']
        data = Database.query.all()
        status = []  
        weight = []
        for i in data: 
            if t == i.time and i.name == n:
                status.append(i.status)
                weight.append(i.weight)
                
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
        
        deleteByTime(input_json)   
            
        return {'STATUS':status_, 'NAME':''}
    except Exception as a:
        status_ = {'STATUS':'CHECKING_NO'}
        return status_


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)