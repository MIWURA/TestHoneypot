from flask import Flask, g, redirect, render_template, request, jsonify, make_response, url_for,Response
from flask_socketio import SocketIO, emit
import sqlite3
from urllib.parse import quote, unquote
import secrets
import json
from threading import Thread,Event
import time
from flask_paginate import Pagination
from threading import Lock
from func import *
import matplotlib.pyplot as plt
import io
import numpy as np



app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'mypot'
app.config['MYSQL_PASSWORD'] = 'Mypot@123'
app.config['MYSQL_DB'] = 'cowrie'
app.config['MYSQL_PORT'] = 4040
mysql = MySQL(app)

thread = None
thread_lock = Lock()

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

@app.route('/dionaea')
def dionaea_index():
    return render_template('/dionaea/index.html')

def get_datadionaea():
    conn = sqlite3.connect('/opt/dionaea/var/lib/dionaea/dionaea.db')
    cur = conn.cursor()
    # สมมติว่ามีตาราง 'log' ที่มีคอลัมน์ 'type' และคุณต้องการนับจำนวนแต่ละประเภท
    cur.execute('SELECT protocol, COUNT(protocol) FROM connection GROUP BY protocol ORDER BY COUNT(protocol);')
    data = cur.fetchall()
    cur.close()
    conn.close()
    return data

@app.route('/ShowtableDionaea', methods=['GET', 'POST'])  # ให้สามารถเข้าถึงได้ทั้ง GET และ POST
def show_lollipop_chart():
    data = get_datadionaea()
    labels = [x[0] for x in data]
    sizes = [x[1] for x in data]
    y_pos = np.arange(len(labels))  # ตำแหน่ง y ของแต่ละรายการ

    # สร้าง Lollipop chart
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.hlines(y=y_pos, xmin=0, xmax=sizes, color='skyblue')
    ax.plot(sizes, y_pos, "o")

    ax.set_yticks(y_pos)
    ax.set_yticklabels(labels)
    ax.set_xlabel('Count')
    ax.set_title('Protocol Distribution')

    # บันทึก Lollipop chart เป็น PNG ใน memory
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    plt.close()
    img.seek(0)

    return Response(img.getvalue(), mimetype='image/png')

@app.route('/cowrie')
def cowrie_index():
    return render_template('/cowrie/index.html')

def fetch_cowriedata(selected_option):
    try:
        cur = mysql.connection.cursor()
        query = {
            'username': "SELECT username, COUNT(username) FROM auth GROUP BY username ORDER BY COUNT(username) DESC LIMIT 10;",
            'password': "SELECT password, COUNT(password) FROM auth GROUP BY password ORDER BY COUNT(password) DESC LIMIT 10;"
        }.get(selected_option)

        if query:
            cur.execute(query)
            results = cur.fetchall()
            cur.close()
            return [{"option": selected_option, "value": row[0], 'count': row[1]} for row in results]
        else:
            raise ValueError("Invalid selection provided")
    except Exception as e:
        raise e


@app.route('/ShowtableCowrie', methods=['POST'])
def ShowtableCowrie():
    selected_option = request.form.get('selection', None)
    if not selected_option:
        return jsonify({"error": "No selection provided"}), 400

    try:
        result = fetch_cowriedata(selected_option)
        return jsonify(result)
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

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

    return '', 204  # ส่งกลับสถานะ 204 เพื่อบอกว่าไม่มีเนื้อหาและไม่ต้องรีเฟรชหน้า
    
@app.route('/update_intable_value', methods=['POST'])
def update_intable_value():
    sort_by = request.form['SORTBY']
    
    # Mockup data: replace with your logic to fetch options based on sort_by
    options = []
    if sort_by == 'Type':
        options = [{'value': 'cowrie', 'text': 'Cowrie'}, {'value': 'dionaea', 'text': 'Dionaea'}]
    elif sort_by == 'Alert':
        options = [{'value': 'RED!', 'text': 'Red'}, {'value': 'YELLOW!', 'text': 'Yellow'}, {'value': 'ORANGE!', 'text': 'Orange'}]

    return jsonify(options)

@app.route('/History', methods=['GET', 'POST'])
def History():
    if request.method == 'POST':
        selected_date = request.form.get('selected_date')
        per_page = int(request.form.get('per_page', 10))
    else:
        selected_date = request.args.get('selected_date')
        per_page = int(request.args.get('per_page', 10))
    
    page = request.args.get('page', 1, type=int)
    data = Get_db(selected_date, page, per_page)
    
    pagination = Pagination(page=page, total=data['total'], per_page=per_page, css_framework='bootstrap4')
    
    return render_template('History.html', data=data, pagination=pagination, selected_date=selected_date, per_page=per_page)








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