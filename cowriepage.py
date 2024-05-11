from flask_mysqldb import MySQL
from flask import Blueprint, request, jsonify, Flask
from sqlalchemy import func
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
cowriepage = Blueprint('cowriepage', __name__)

# กำหนดการเชื่อมต่อ MySQL โดยตรงในอ็อบเจ็กต์ MySQL
cowrie_mysql = MySQL()

cowrie_mysql.host = 'localhost'
cowrie_mysql.user = 'mypot'
cowrie_mysql.password = 'Mypot@123'
cowrie_mysql.db = 'cowrie'

cowrie_mysql.init_app(app)

# สร้างอ็อบเจ็กต์ SQLAlchemy
db = SQLAlchemy(app)

class AuthLog(db.Model):
    __tablename__ = 'auth'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

@cowriepage.route('/ShowtableCowrie', methods=['POST'])
def ShowtableCowrie():
    selected_option = request.form['selection']
    if selected_option == 'username':
        username_count = db.session.query(AuthLog.username, func.count(AuthLog.username)).group_by(AuthLog.username).order_by(func.count(AuthLog.username).desc()).limit(20).all()
        result = [{'username': row[0], 'count': row[1]} for row in username_count]
        return jsonify(result)
    elif selected_option == 'password':
        password_count = db.session.query(AuthLog.password, func.count(AuthLog.password)).group_by(AuthLog.password).order_by(func.count(AuthLog.password).desc()).limit(20).all()
        result = [{'password': row[0], 'count': row[1]} for row in password_count]
        return jsonify(result)
    else:
        return "No data available for the selected option."

# ที่นี่เราต้องเรียกใช้ Blueprint ของ cowriepage ในแอพพลิเคชั่น Flask ของเรา
app.register_blueprint(cowriepage)

if __name__ == "__main__":
    app.run(debug=True)
