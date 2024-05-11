from flask import Blueprint, request, jsonify
from flask import Flask
from flask_mysqldb import MySQL

cowriepage_blueprint = Blueprint('cowriepage', __name__)
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'mypot'
app.config['MYSQL_PASSWORD'] = 'Mypot@123'
app.config['MYSQL_DB'] = 'mypot'
mysql = MySQL(app)


@cowriepage_blueprint.route('/ShowtableCowrie', methods=['POST'])
def ShowtableCowrie():
    selected_option = request.form.get('selection', None)
    if not selected_option:
        return jsonify({"error": "No selection provided"}), 400

    cur = mysql.connection.cursor()

    if selected_option == 'username':
        cur.execute("SELECT username, COUNT(username) FROM auth GROUP BY username ORDER BY COUNT(username) DESC LIMIT 20;")
    elif selected_option == 'password':
        cur.execute("SELECT password, COUNT(password) FROM auth GROUP BY password ORDER BY COUNT(password) DESC LIMIT 20;")
    else:
        return jsonify({"error": "Invalid selection"}), 400

    results = cur.fetchall()
    cur.close()

    result = [{selected_option: row[0], 'count': row[1]} for row in results]
    return jsonify(result)
