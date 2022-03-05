# -*- coding: utf-8 -*-
"""
Created on Thu Oct 18 23:39:09 2018

@author: Sevendi Eldrige Rifki Poluan
""" 

# File: tester_client.py
# Author: Sevendi Eldrige Rifki Poluan
# Date: September 1, 2018
# Desc: Client of connecting to Heroku server

import requests, json  

class Client(object):
    
    def __init__(self):
        print('## Start . . .')
        
    def createTable(self):
        url = 'https://insoles.herokuapp.com/req'  
        
        # Create table
        data = {} 
        data['METHOD'] = 'CREATE' 
        json_data = json.dumps(data) 
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, json=json.loads(json_data), headers=headers) # Refs: http://docs.python-requests.org/en/v0.10.7/user/quickstart/#make-a-get-request
        r.json() 
        
    def insertData(self):
        url = 'https://insoles.herokuapp.com/req'  
        # Insert data
        data = {} 
        data['METHOD'] = 'INSERT' 
        data['R_HEEL'] = '45'
        data['R_THUMB'] = '23' 
        data['R_INNER_BALL'] = '56'
        data['R_OUTER_BALL'] = '67'
        data['L_HEEL'] = '34'
        data['L_THUMB'] = '12' 
        data['L_INNER_BALL'] = '34' 
        data['L_OUTER_BALL'] = '12'
        data['TIME'] = '01:08:38' 
        data['NAME'] = 'SEVENDI' 
        
        json_data = json.dumps(data) 
        r = requests.post(url, json=json.loads(json_data))
        r.json() 
        
    # Delete data
    def deleteInsoles(self):
        url = 'https://insoles.herokuapp.com/req'  
        data = {}
        data['METHOD'] = 'DELETE'
        json_data = json.dumps(data)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, json=json.loads(json_data), headers=headers)
        r.json()
    
    def extractInsoles(self):    
        url = 'https://insoles.herokuapp.com/req'  
          
        ## Get data from heroku
        data = {} 
        data['METHOD'] = 'VIEW'  
        json_data = json.dumps(data)
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        r = requests.post(url, json=json.loads(json_data), headers=headers)
        r = r.json()['STATUS'] 
         
        ## Read all detected users
        get_user = []
        for i in r:
            data = i[0] # [{}]
            try:
                if data['NAME'] not in get_user:
                    get_user.append(data['NAME'])
            except:
                pass          
    
        ## Distinguish all user with its data
        separate = [] 
        for x in get_user:
            temp = []
            
            for i in r:
                data = i[0] # [{}]
                if data['NAME'] == x:
                    temp.append([data['R_HEEL'], data['R_THUMB'], data['R_INNER_BALL'], data['R_OUTER_BALL'], data['L_HEEL'], data['L_THUMB'], data['L_INNER_BALL'], data['L_OUTER_BALL'], data['TIME'], data['NAME']])
                        
            if len(temp) > 0:
                separate.append(temp)
        
        self.deleteInsoles()
        print(separate)
        
if __name__ == '__main__':        
    app = Client()
    while True:
        app.extractInsoles()