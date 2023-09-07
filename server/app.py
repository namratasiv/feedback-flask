from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3
from sqlite3 import Error
from flask_socketio import SocketIO
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins='https://a3281e8a.vue-feedback-display.pages.dev', logger=True, engineio_logger=True)
api_v2_cors_config = {
  "origins": ["*"],
  "methods": ["OPTIONS", "GET", "POST"],
  "allow_headers": ["Authorization", "Content-Type"]
}
CORS(app, resources={"/*": api_v2_cors_config})


@socketio.on('insert')
def handle_socket(data):
    print("inside sockey!")
    print(data)
    socketio.emit('insert',{'message':'New data inserted'}, callback=messageReceived)
    response = jsonify({"MESSAGE": "Event Triggered!!"})
    response.headers['Access-Control-Allow-Methods']='*'
    response.headers['Access-Control-Allow-Origin']='*'
    response.headers['Vary']='Origin'
    return response 

@app.route('/', methods=['OPTIONS'])
def pong():
    
    response = jsonify({
        'status': "SUCCESS!!! options",
    })
    response.headers['Access-Control-Allow-Methods']='*'
    response.headers['Access-Control-Allow-Origin']='*'
    response.headers['Vary']='Origin'
    return response

@app.route('/', methods=['GET'])
def pinggggg():
    handle_socket('test')
    response = jsonify({
        'status': "SUCCESS!!!",
    })
    response.headers['Access-Control-Allow-Methods']='*'
    response.headers['Access-Control-Allow-Origin']='*'
    response.headers['Vary']='Origin'
    return response

@app.route('/poll/', methods=['GET'])
def getData():
    seeResponse()
    return jsonify({
        'status': seeResponse(),
    })

@app.route('/1/', methods=['POST'])
def response1():
    print("entered 1")
    insertResponse("1")
    #seeResponse()
    socketio.emit('insert',{'message':'1'})
    response = jsonify({
        'status': "Received POST 1!",
    })
    response.headers['Access-Control-Allow-Methods']='*'
    response.headers['Access-Control-Allow-Origin']='*'
    response.headers['Vary']='Origin'
    return response
@app.route('/2/', methods=['POST'])
def response2():
    insertResponse("2")
    #seeResponse()
    socketio.emit('insert',{'message':'2'})
    response = jsonify({
        'status': "Received POST 2!",
    })
    response.headers['Access-Control-Allow-Methods']='*'
    response.headers['Access-Control-Allow-Origin']='*'
    response.headers['Vary']='Origin'
    return response
@app.route('/3/', methods=['POST'])
def response3():
    insertResponse("3")
    #seeResponse()
    socketio.emit('insert',{'message':'3'})
    response = jsonify({
        'status': "Received POST 3!",
    })
    response.headers['Access-Control-Allow-Methods']='*'
    response.headers['Access-Control-Allow-Origin']='*'
    response.headers['Vary']='Origin'
    return response

def insertResponse(x):
    """ create a database connection to a database that resides
        in the memory
    """
    connection_obj = sqlite3.connect('feedback.db')
 
    # cursor object
    cursor_obj = connection_obj.cursor()
 

    table = """INSERT INTO FEEDBACK(RESPONSE) VALUES(""" + x +  """)"""
    
    cursor_obj.execute(table)
    print("done inserting")
    connection_obj.commit()
    
    # Close the connection
    connection_obj.close()
     
def seeResponse():
    
    connection_obj = sqlite3.connect('livefeedback.db')
 
    # cursor object
    cursor_obj = connection_obj.cursor()
    select = "SELECT RESPONSE FROM LIVEFEEDBACK"
    l = []
    for raw in cursor_obj.execute(select):
        print(raw)
        l.append(raw)
    print("------>", cursor_obj.execute(select))
    print("done")
    connection_obj.close()
    return l

def messageReceived(methods=['GET', 'POST']):
    print('message was received!!!')

@app.route('/live1/', methods=['POST'])
def liveresponse1():
    print("entered 1")
    insertLiveResponse("1")
    seeResponse()
    #seeResponse()
    socketio.emit('insert',{'message':'1'})
    response = jsonify({
        'status': "Received LIVEPOST 1!",
    })
    response.headers['Access-Control-Allow-Methods']='*'
    response.headers['Access-Control-Allow-Origin']='*'
    response.headers['Vary']='Origin'
    return response
@app.route('/live2/', methods=['POST'])
def liveresponse2():
    insertLiveResponse("2")
    #seeResponse()
    socketio.emit('insert',{'message':'2'})
    response = jsonify({
        'status': "Received LIVEPOST 1!",
    })
    response.headers['Access-Control-Allow-Methods']='*'
    response.headers['Access-Control-Allow-Origin']='*'
    response.headers['Vary']='Origin'
    return response
@app.route('/live3/', methods=['POST'])
def liveresponse3():
    insertLiveResponse("3")
    #seeResponse()
    socketio.emit('insert',{'message':'3'})
    response = jsonify({
        'status': "Received LIVEPOST 3!",
    })
    response.headers['Access-Control-Allow-Methods']='*'
    response.headers['Access-Control-Allow-Origin']='*'
    response.headers['Vary']='Origin'
    return response

def insertLiveResponse(x):
    """ create a database connection to a database that resides
        in the memory
    """
    connection_obj = sqlite3.connect('livefeedback.db')
    #print(x)
    # cursor object
    cursor_obj = connection_obj.cursor()
 
    # table = """ CREATE TABLE LIVEFEEDBACK(RESPONSE_ID INTEGER PRIMARY KEY AUTOINCREMENT,
    # RESPONSE TEXT);"""
    table = """INSERT INTO LIVEFEEDBACK(RESPONSE) VALUES(""" + x +  """)"""
    
    cursor_obj.execute(table)
    # print("done inserting")
    connection_obj.commit()
    
    # Close the connection
    connection_obj.close()
if __name__ == '__main__':
    
    socketio.run(app, debug=True, host='0.0.0.0', port=8080)


