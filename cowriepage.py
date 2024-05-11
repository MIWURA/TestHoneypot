from flask_mysqldb import MySQL
from flask import Blueprint, request, jsonify
from sqlalchemy import func
from app import db, app

cowriepage = Blueprint('cowriepage', __name__)

cowrie_mysql = MySQL()

cowrie_mysql.config['MYSQL_HOST'] = 'localhost'
cowrie_mysql.config['MYSQL_USER'] = 'mypot'
cowrie_mysql.config['MYSQL_PASSWORD'] = 'Mypot@123'
cowrie_mysql.config['MYSQL_DB'] = 'cowrie'

cowrie_mysql.init_app(cowriepage)

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
