
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
    time = db.Column(db.String(20))
    name = db.Column(db.String(20))
    
    def __init__(self, status, time, name): 
        self.status = status 
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
        data_length, id, status, time, name = viewData() 
        if data_length != 0:
            status_ = []
            for i in range(data_length):
                status_.append([{'DATA_INDEX':i, 'STATUS':status[i], 'TIME':time[i], 'NAME':name[i]}])
            status_ = {'STATUS':status_}
        else:
            status_ = {'STATUS':'EMPTY'} 
            
    # Get tag list
    if method_status == 'TAG_LIST':
        status_ = tagNameList() 
        
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
            db.session.add(Database(input_json['STATUS'], input_json['TIME'], input_json['NAME']))
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
        time = []
        name = []
        for i in data: 
            id.append(i.id)
            status.append(i.status) 
            time.append(i.time)  
            name.append(i.name)
        
        return len(id), id, status, time, name
    
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
            return {'STATUS':list(set(name))} # Applied distinction
        else:
            return {'STATUS':'EMPTY'}
    except:
        return {'STATUS':'EMPTY'} 

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)