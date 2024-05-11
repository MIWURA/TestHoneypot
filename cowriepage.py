from flask import Blueprint, request, jsonify, current_app
from sqlalchemy import func

cowriepage_blueprint = Blueprint('cowriepage', __name__)

class AuthLog(current_app.db.Model):
    __tablename__ = 'auth'
    id = current_app.db.Column(current_app.db.Integer, primary_key=True)
    username = current_app.db.Column(current_app.db.String(100), nullable=False)
    password = current_app.db.Column(current_app.db.String(100), nullable=False)

@cowriepage_blueprint.route('/ShowtableCowrie', methods=['POST'])
def ShowtableCowrie():
    selected_option = request.form['selection']
    if selected_option == 'username':
        with current_app.app_context():
            username_count = AuthLog.query.with_entities(AuthLog.username, func.count(AuthLog.username)).group_by(AuthLog.username).order_by(func.count(AuthLog.username).desc()).limit(20).all()
        result = [{'username': row[0], 'count': row[1]} for row in username_count]
        return jsonify(result)
    elif selected_option == 'password':
        with current_app.app_context():
            password_count = AuthLog.query.with_entities(AuthLog.password, func.count(AuthLog.password)).group_by(AuthLog.password).order_by(func.count(AuthLog.password).desc()).limit(20).all()
        result = [{'password': row[0], 'count': row[1]} for row in password_count]
        return jsonify(result)
    else:
        return "No data available for the selected option."
