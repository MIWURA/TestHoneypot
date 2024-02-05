# app.py

from flask import Flask, g, render_template, request, jsonify, make_response
from flask_socketio import SocketIO, emit
import sqlite3
from urllib.parse import quote, unquote
from flask_mysqldb import MySQL
import secrets
import json
from threading import Thread
import time
from flask_sqlalchemy import SQLAlchemy
from flask_paginate import Pagination
from models import db,Mypot
from threading import Lock

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(16)
#DATABASE = '../Database_test/dionaea.sqlite'

thread = None
thread_lock = Lock()

password_encoded = quote("Mypot@123")
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://mypot@localhost/mypot?password={password_encoded}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'mypot'
app.config['MYSQL_PASSWORD'] = 'Mypot@123'
app.config['MYSQL_DB'] = 'mypot'

mysql = MySQL(app)
db.init_app(app)
socketio = SocketIO(app)

def Get_db():
   with app.app_context():
        with mysql.connection.cursor() as cur:
            cur.execute("SELECT * FROM honeypot ORDER BY id DESC")
            data = cur.fetchall()

        response_data = {
            'data': [{
                'type': item[1],  
                'alert': item[2],  
                'date': str(item[3]),
                'time': str(item[4]), 
                'ip_attacker': item[5],
                'ip_server': item[6],
                'protocol': item[7],
                'comment': item[8],
            } for item in data]
        }

        return response_data

def Get_20db():
    with app.app_context():
        with mysql.connection.cursor() as cur:
            cur.execute("SELECT * FROM honeypot ORDER BY id DESC LIMIT 20")
            data = cur.fetchall()

        response_data = {
            'data': [{
                'type': item[1],  
                'alert': item[2],  
                'date': str(item[3]),
                'time': str(item[4]), 
                'ip_attacker': item[5],
                'ip_server': item[6],
                'protocol': item[7],
                'comment': item[8],
            } for item in data]
        }

        return response_data
    
@socketio.on('connect')
def connect():
    global thread
    print('Client connected')

    global thread
    with thread_lock:
        print("Current thread:", thread)
        thread = socketio.start_background_task(background_thread)

def background_thread():
    print("Query Database Limit 20")
    with app.app_context():
        while True:
            response_data = Get_20db()
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

@app.route('/Monitor')
def Monitor():
    return render_template('Monitor.html') 

@app.route('/History')
def History():
    data = Get_db()
    return render_template('History.html',data=data) 



if __name__ == '__main__':
    socketio.run(app,debug=True)