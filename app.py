from flask import Flask, request, jsonify

standing_right = ''
standing_left = ''

time_right = ''
time_left = ''

standing = []
app = Flask(__name__) 

@app.route('/')
def index():
    return 'Hello' 

@app.route('/req', methods=['POST'])
def prreq():
    global standing_right, standing_left, standing, time_left, time_right
    
    input_json = request.get_json(force=True)   
    
    try:
        standing_left = input_json['left']
        time_left = input_json['time']
    except:
        standing_left = ''
        pass
    
    try:
        standing_right = input_json['right']
        time_right = input_json['right']
    except:
        standing_right = ''
        pass
    
    if standing_right == '' and standing_left != '':
        standing.append([standing_left, time_left])
    
    if standing_left == '' and standing_right != '':
        standing.append([standing_right, time_right])
        
        
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
        
    passing = {'all_joint':standing}
    
    if len(standing) == 2:
        standing = []
    
    return jsonify(passing) 

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)