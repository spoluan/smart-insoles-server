
"""
    # File: serv.py
    # Author: Sevendi Eldrige Rifki Poluan
    # Date modified: March 05, 2022
    # Desc: Heroku server for synchronizing Insoles data
    # Reference:
        [1] Ref: https://www.codementor.io/garethdwyer/building-a-crud-application-with-flask-and-sqlalchemy-dm3wv7yu2
        [2] http://docs.sqlalchemy.org/en/rel_0_9/orm/tutorial.html
"""

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
import os
  
app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']   
db = SQLAlchemy(app)

print('Database url:', os.environ['DATABASE_URL'])

class Database(db.Model): 
    __tablename__ = "tb_heroku_server"
    id = db.Column(db.Integer, primary_key = True) 
    R_HEEL = db.Column(db.Integer)  
    R_THUMB = db.Column(db.Integer)
    R_INNER_BALL = db.Column(db.Integer)
    R_OUTER_BALL = db.Column(db.Integer)
    L_HEEL = db.Column(db.Integer)
    L_THUMB = db.Column(db.Integer)
    L_INNER_BALL = db.Column(db.Integer)
    L_OUTER_BALL = db.Column(db.Integer)
    TIME = db.Column(db.String(20))
    NAME = db.Column(db.String(20))
    
    def __init__(self, R_HEEL, R_THUMB, R_INNER_BALL, R_OUTER_BALL, L_HEEL, L_THUMB, L_INNER_BALL, L_OUTER_BALL, TIME, NAME): 
        self.R_HEEL = R_HEEL
        self.R_THUMB = R_THUMB
        self.R_INNER_BALL = R_INNER_BALL
        self.R_OUTER_BALL = R_OUTER_BALL
        self.L_HEEL = L_HEEL
        self.L_THUMB = L_THUMB
        self.L_INNER_BALL = L_INNER_BALL
        self.L_OUTER_BALL = L_OUTER_BALL
        self.TIME = TIME
        self.NAME = NAME

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
    
    print('Calling method:', method_status)

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
        data_length, id, R_HEEL, R_THUMB, R_INNER_BALL, R_OUTER_BALL, L_HEEL, L_THUMB, L_INNER_BALL, L_OUTER_BALL, TIME, NAME = viewData() 
        if data_length != 0:
            status_ = []
            for i in range(data_length):
                status_.append([
                	{
                		'DATA_INDEX':i, 
                        'ID': id,
                		'R_HEEL' : R_HEEL[i], 
					    'R_THUMB' : R_THUMB[i],
					    'R_INNER_BALL' : R_INNER_BALL[i],
					    'R_OUTER_BALL' : R_OUTER_BALL[i],
					    'L_HEEL' : L_HEEL[i],
					    'L_THUMB' : L_THUMB[i],
					    'L_INNER_BALL' : L_INNER_BALL[i],
					    'L_OUTER_BALL' : L_OUTER_BALL[i],
					    'TIME' : TIME[i],
					    'NAME' : NAME[i]
                	}
                ])
            status_ = {'STATUS': status_}
        else:
            status_ = {'STATUS': 'EMPTY'} 
 
    print('Status:', status_)
        
    return jsonify(status_) 

def createTable():
    try: 
        db.create_all()
        status_ = {'STATUS': 'CREATE_TABLE_OK'}
        return status_
    except Exception as err: 
        status_ = {'STATUS': f'CREATE_TABLE_NO {err}'}
        return status_
    
def insertData(input_json):
    try:  
        db.session.add(
        	Database(
        		input_json['R_HEEL'], 
        		input_json['R_THUMB'], 
        		input_json['R_INNER_BALL'],
        		input_json['R_OUTER_BALL'],
        		input_json['L_HEEL'],
        		input_json['L_THUMB'],
        		input_json['L_INNER_BALL'], 
        		input_json['L_OUTER_BALL'], 
        		input_json['TIME'], 
        		input_json['NAME']  
        	)
        )

        db.session.commit()
        status_ = {'STATUS': 'INSERT_DATA_OK'}
          
        return status_
    except Exception as err:
        status_ = {'STATUS': f'INSERT_DATA_NO {err}'}
        return status_
            
def deleteData():
    try: 
        data = Database.query.all()
        for i in data: 
            data = Database.query.filter_by(id=i.id).first()
            db.session.delete(data) 
        db.session.commit()
        status_ = {'STATUS': 'DELETE_DATA_OK'}
        return status_
    except Exception as err: 
        status_ = {'STATUS': f'DELETE_DATA_NO {err}'}
        return status_ 

def viewData():
    try:  
        data = Database.query.all() 
        id = []
        R_HEEL = []
        R_THUMB = []
        R_INNER_BALL = []
        R_OUTER_BALL = []
        L_HEEL = []
        L_THUMB = []
        L_INNER_BALL = []
        L_OUTER_BALL = []
        TIME = []
        NAME = []
        for i in data: 
            id.append(i.id)
            R_HEEL.append(i.R_HEEL)
            R_THUMB.append(i.R_THUMB)
            R_INNER_BALL.append(i.R_INNER_BALL)
            R_OUTER_BALL.append(i.R_OUTER_BALL)
            L_HEEL.append(i.L_HEEL)
            L_THUMB.append(i.L_THUMB)
            L_INNER_BALL.append(i.L_INNER_BALL)
            L_OUTER_BALL.append(i.L_OUTER_BALL)
            TIME.append(i.TIME)
            NAME.append(i.NAME)

        return len(id), id, R_HEEL, R_THUMB, R_INNER_BALL, R_OUTER_BALL, L_HEEL, L_THUMB, L_INNER_BALL, L_OUTER_BALL, TIME, NAME
        
    except:
        return 'EMPTY' 
 

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)