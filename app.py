# app.py

from flask import Flask, g, redirect, render_template, request, jsonify, make_response, url_for,Response
from flask_socketio import SocketIO, emit
import sqlite3
from urllib.parse import quote, unquote
from flask_mysqldb import MySQL
import secrets
import json
from threading import Thread,Event
import time
from flask_sqlalchemy import SQLAlchemy
from flask_paginate import Pagination
from models import db,Mypot
from threading import Lock
from func import *
from cowriepage import cowriepage

app = Flask(__name__)
app.register_blueprint(cowriepage)
# app.config['SECRET_KEY'] = secrets.token_hex(16)
#DATABASE = '../Database_test/dionaea.sqlite'

thread = None
thread_lock = Lock()

# password_encoded = quote("Mypot@123")
# app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://mypot@localhost/mypot?password={password_encoded}'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'mypot'
# app.config['MYSQL_PASSWORD'] = 'Mypot@123'
# app.config['MYSQL_DB'] = 'mypot'

app.config['MYSQL_URI_MYPOT'] = 'mysql://mypot:Mypot%40123@localhost/mypot'

mysql = MySQL(app)
db.init_app(app)
socketio = SocketIO(app)  
stop_event = Event()

@socketio.on('connect')
def connect():
    global thread
    print('Client connected')

    global thread
    with thread_lock:
        if thread is None:
            print("Current thread Start:", thread)
            thread = socketio.start_background_task(background_thread)


@socketio.on('disconnect')
def disconnect():
    print('Client disconnected',  request.sid)

def background_thread(sort_by=None, intable_value=None):
    print("Query Database Limit 20")
    with app.app_context():
        while not stop_event.is_set():
            response_data = Get_SortDB(sort_by=sort_by,intable_value=intable_value)
            #print('----------------------------------Emit data-------------------------------------')
            socketio.emit('updateResponse_data', response_data, namespace='')
            socketio.sleep(1)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/dionaea/chart')
def dionaea_chart():
    return render_template('/dionaea/Chart_1.html')

@app.route('/dionaea/table')
def dionaea_table():
    return render_template('/dionaea/table_1.html')

@app.route('/dionaea')
def dionaea_index():
    return render_template('/dionaea/index.html')

@app.route('/cowrie')
def cowrie_index():
    return render_template('/cowrie/index.html')

@app.route('/ShowtableCowrie', methods=['POST'])
def ShowtableCowrie():
    selected_option = request.form['selection']
    process_data(selected_option)
    # ทำอะไรก็ตามที่ต้องการเมื่อได้ข้อมูลแล้ว เช่น บันทึกข้อมูลลงในฐานข้อมูล
    return "Data processed successfully!"

@app.route('/Monitor')
def Monitor():
    return render_template('Monitor.html') 

@app.route('/Monitor', methods=['POST'])
def submit_filter():
    sort_by = request.form['SORTBY']
    intable_value = request.form['intable_value']
    print("Sort by:", sort_by)
    print("Intable value:", intable_value)
    
    global thread
    with thread_lock:
        if thread:  # ตรวจสอบว่าเธรดเก่ายังมีอยู่หรือไม่
            stop_event.set()  # เซ็ต stop_event เป็น True เพื่อให้เธรดเก่าหยุดทำงาน
            thread.join()  # รอให้เธรดเก่าจบการทำงานก่อน
            thread = None  # ลบเธรดเก่าทิ้ง
        stop_event.clear()  # เซ็ต stop_event เป็น False เพื่อเตรียมสำหรับเธรดใหม่
        
        
        thread = socketio.start_background_task(lambda: background_thread(sort_by, intable_value))
        print("Current thread Switch:", thread)

    return redirect(url_for('Monitor'))
    

@app.route('/History')
def History():
    data = Get_db()
    return render_template('History.html',data=data) 


def respond_to_client():
    while True:
        global counter
        with open("DBcowrie.txt", "r+") as f:
            lines = f.readlines()
            if not lines or (len(lines) == 1 and lines[0].strip() == ''):
                time.sleep(0.5)
                continue
            
            for line in lines:
                getDB(line)
                print(line)
                print("******************")
                print(counter)
                counter += 1
                _data = json.dumps({"line": line, "counter": counter})
                yield f"id: 1\ndata: {_data}\nevent: online\n\n"
                
            f.truncate(0) 

if __name__ == '__main__':
    respond_to_client()
    socketio.run(app,debug=True,host='0.0.0.0', port=5000)