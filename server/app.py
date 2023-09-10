from flask import Flask, jsonify
from flask_cors import CORS
from pysondb import db
from flask_socketio import SocketIO
#import datetime
from datetime import datetime
import time
import pendulum

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='*', logger=True, engineio_logger=True)
api_v2_cors_config = {
  "origins": ["*"],
  "methods": ["OPTIONS", "GET", "POST"],
  "allow_headers": ["Authorization", "Content-Type"]
}
CORS(app, resources={"/*": api_v2_cors_config})

ist = pendulum.timezone('Asia/Calcutta')


@socketio.on('insert')
def handle_socket(data):
    print("inside sockey!")
    print(data)
    socketio.emit('insert',{'message':'New data inserted'}, callback=messageReceived)
    return jsonify({"MESSAGE": "Event Triggered!!"})

@app.route('/', methods=['OPTIONS'])
def pong():
    
    response = jsonify({
        'status': "Options Successful!",
    })
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
@app.route('/', methods=['GET'])
def pinggggg():
    handle_socket('test')
    response = jsonify({
        'status': "SUCCESS!!!",
    })
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response
@app.route('/poll/', methods=['GET'])
def getData():
    
    return jsonify({
        'status': "poll",
    })

@app.route('/1/', methods=['POST'])
def response1():
    print("entered 1")
    insertResponse("1")
    #seeResponse()
    socketio.emit('insert',{'message':'1'})
    getResponse("1")
    return jsonify({
        'status': "Received POST 1!",
    })
@app.route('/2/', methods=['POST'])
def response2():
    insertResponse("2")
    #seeResponse()
    getResponse("2")
    socketio.emit('insert',{'message':'2'})
    return jsonify({
        'status': "Received POST 2!",
    })
@app.route('/3/', methods=['POST'])
def response3():
    insertResponse("3")
    #seeResponse()
    getResponse("3")
    socketio.emit('insert',{'message':'3'})
    return jsonify({
        'status': "Received POST 3!",
    })

def insertResponse(x):
    a=db.getDb("feedback.json")
    
    res = {"response": x, "timestamp": str(datetime.now(ist))}
    a.add(res)
    print(a.getAll())
     

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@app.route('/live1/', methods=['POST'])
def liveresponse1():
    print("entered 1")
    insertLiveResponse("1")
    seeResponse()
    #seeResponse()
    socketio.emit('insert',{'message':'1'})
    return jsonify({
        'status': "Received POST 1!",
    })
@app.route('/live2/', methods=['POST'])
def liveresponse2():
    insertLiveResponse("2")
    #seeResponse()
    socketio.emit('insert',{'message':'2'})
    return jsonify({
        'status': "Received POST 2!",
    })
@app.route('/live3/', methods=['POST'])
def liveresponse3():
    insertLiveResponse("3")
    #seeResponse()
    socketio.emit('insert',{'message':'3'})
    return jsonify({
        'status': "Received POST 3!",
    })

def insertLiveResponse(x):
    a=db.getDb("livefeedback.json")
    ist = pendulum.timezone('Asia/Calcutta')
    res = {"response": x, "timestamp": str(datetime.now(ist))}
    a.add(res)
    print(a.getAll())
    
def getResponse(x):
    a=db.getDb("feedback.json")
    data = a.getByQuery(query={"response": x})
    print(len(data))
    socketio.emit('update',{'response' + x :len(data)})

if __name__ == '__main__':
    
    socketio.run(app, debug=True, host='0.0.0.0', port=8080)


