from flask import Blueprint, request, jsonify
from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'mypot'
app.config['MYSQL_PASSWORD'] = 'Mypot@123'
app.config['MYSQL_DB'] = 'cowrie'
app.config['MYSQL_PORT'] = 4040
mysql = MySQL(app)

def fetch_cowriedata(selected_option):
    try:
        cur = mysql.connection.cursor()
        query = {
            'username': "SELECT username, COUNT(username) FROM auth GROUP BY username ORDER BY COUNT(username) DESC LIMIT 20;",
            'password': "SELECT password, COUNT(password) FROM auth GROUP BY password ORDER BY COUNT(password) DESC LIMIT 20;"
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
