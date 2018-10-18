
# File: serv.py
# Author: Sevendi Eldrige Rifki Poluan
# Date: October 18, 2018
# Desc: Heroku server for synchronizing Insoles data

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy # Ref: https://www.codementor.io/garethdwyer/building-a-crud-application-with-flask-and-sqlalchemy-dm3wv7yu2
# http://docs.sqlalchemy.org/en/rel_0_9/orm/tutorial.html
import os
  
app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']   
db = SQLAlchemy(app)

class Database(db.Model): 
    __tablename__ = "tb_heroku"
    id = db.Column(db.Integer, primary_key = True) 
    thumb = db.Column(db.String(20))  
    outer_ball = db.Column(db.String(20))
    inner_ball = db.Column(db.String(20))
    heel = db.Column(db.String(20))
    time = db.Column(db.String(20))
    name = db.Column(db.String(20))
    
    def __init__(self, thumb, outer_ball, inner_ball, heel, time, name): 
        self.thumb = thumb 
        self.outer_ball = outer_ball
        self.inner_ball = inner_ball
        self.heel = heel
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
  
    # View data
    if method_status == 'VIEW':
        data_length, id, thumb, outer_ball, ineer_ball, heel, time, name = viewData() 
        if data_length != 0:
            status_ = []
            for i in range(data_length):
                status_.append([{'DATA_INDEX':i, 'THUMB':thumb[i], 'OUTER_BALL':outer_ball[i], 'INNER_BALL':ineer_ball[i], 'HEEL':heel[i], 'TIME':time[i], 'NAME':name[i]}])
            status_ = {'STATUS':status_}
        else:
            status_ = {'STATUS':'EMPTY'} 
 
        
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
            db.session.add(
            	Database(
            		input_json['THUMB'], 
            		input_json['OUTER_BALL'], 
            		input_json['INNER_BALL'],
            		input_json['HEEL'],
            		input_json['TIME'],
            		input_json['NAME'] 
            	)
            )

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

def viewData():
    try:  
        data = Database.query.all() 
        id = []
        thumb = [] 
        outer_ball = []
        inner_ball = []
        heel = []
        time = []
        name = []
        for i in data: 
            id.append(i.id)
	        thumb.append(i.thumb)
	        outer_ball.append(i.outer_ball)
	        inner_ball.append(i.inner_ball)
	        heel.append(i.heel)
	        time.append(i.time)
	        name.append(i.name)
        
        return len(id), id, thumb, outer_ball, inner_ball, heel, time, name
    
    except:
        return 'EMPTY'

def checkInsert(input_json):
    try:  
 
		time = input_json['TIME'] 
		name = input_json['NAME'] 

        data = Database.query.all() 
        id = [] 
        for i in data:
            if i.time == time and i.name == name:
                id.append(i.id) 
         
        if len(id) != 0:
            return False
        else:
            return True 
    except:
        return False
 

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)