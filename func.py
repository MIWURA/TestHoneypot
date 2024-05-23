from flask_mysqldb import MySQL
from flask import Flask
import time
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'mypot'
app.config['MYSQL_PASSWORD'] = 'Mypot@123'
app.config['MYSQL_DB'] = 'mypot'
app.config['MYSQL_PORT'] = 4040
mysql = MySQL(app)



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
    
def Get_SortDB(sort_by=None, intable_value=None):
    with app.app_context():
        with mysql.connection.cursor() as cur:
            if sort_by and intable_value:
                try:
                    cur.execute("SELECT * FROM honeypot WHERE {} = '{}' ORDER BY id DESC LIMIT 20".format(sort_by,intable_value))
                    data = cur.fetchall()
                except Exception as e:
                    print("Error executing SQL query:", e)
                    cur.execute("SELECT * FROM honeypot ORDER BY id DESC LIMIT 20")
                    data = cur.fetchall()
            else:
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


def Get_db(selected_date=None, page=1, per_page=10):
    offset = (page - 1) * per_page
    with app.app_context():
        with mysql.connection.cursor() as cur:
            if selected_date:
                cur.execute("SELECT COUNT(*) FROM honeypot WHERE date=%s", (selected_date,))
                total = cur.fetchone()[0]
                cur.execute("SELECT * FROM honeypot WHERE date=%s ORDER BY id DESC LIMIT %s OFFSET %s", (selected_date, per_page, offset))
            else:
                cur.execute("SELECT COUNT(*) FROM honeypot")
                total = cur.fetchone()[0]
                cur.execute("SELECT * FROM honeypot ORDER BY id DESC LIMIT %s OFFSET %s", (per_page, offset))
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
            } for item in data],
            'total': total
        }

        return response_data



   
def Get_ForDw(sort_by):
   with app.app_context():
        with mysql.connection.cursor() as cur:
            cur.execute("SELECT DISTINCT {} FROM honeypot ORDER BY id DESC".format(sort_by))
            data = cur.fetchall()
        
        return data
   
def getDB(data):
    try:
        with app.app_context():
            with mysql.connection.cursor() as cur:
                data_list = data.split(", ")
                print(data_list)
                cur.execute("INSERT INTO honeypot (type, alert, date, time, ip_attacker, ip_server, protocol, comment) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (data_list[0], data_list[1], data_list[2], data_list[3], data_list[4], "-", data_list[5], data_list[6]))
                print("commit")
                mysql.connection.commit()
    except Exception as e:
        print("emty")
    #db.close()
