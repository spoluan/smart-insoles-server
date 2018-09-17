from flask import Flask, request, jsonify

standing_posture = []
standing = ''
app = Flask(__name__) 

@app.route('/')
def index():
    return 'Hello' 

@app.route('/req', methods=['POST'])
def prreq():
    global standing_posture, standing
    
    input_json = request.get_json(force=True)   
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
    passing = {'left':input_json}
    
    return jsonify(passing) 

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)