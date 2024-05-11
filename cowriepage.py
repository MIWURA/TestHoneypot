from flask import Blueprint, request, jsonify
from sqlalchemy import func
from app import db  # นำเข้า SQLAlchemy instance จากไฟล์ app.py

cowriepage_blueprint = Blueprint('cowriepage', __name__)

class AuthLog(db.Model):
    __tablename__ = 'auth'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

@cowriepage_blueprint.route('/ShowtableCowrie', methods=['POST'])
def ShowtableCowrie():
    selected_option = request.form['selection']
    if selected_option == 'username':
        username_count = AuthLog.query.with_entities(AuthLog.username, func.count(AuthLog.username)).group_by(AuthLog.username).order_by(func.count(AuthLog.username).desc()).limit(20).all()
        result = [{'username': row[0], 'count': row[1]} for row in username_count]
        return jsonify(result)
    elif selected_option == 'password':
        password_count = AuthLog.query.with_entities(AuthLog.password, func.count(AuthLog.password)).group_by(AuthLog.password).order_by(func.count(AuthLog.password).desc()).limit(20).all()
        result = [{'password': row[0], 'count': row[1]} for row in password_count]
        return jsonify(result)
    else:
        return "No data available for the selected option."
