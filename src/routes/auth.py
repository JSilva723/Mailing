import os
from flask import Blueprint, request, render_template, redirect, session, url_for
from ..services.db import DBConnect
from werkzeug.security import generate_password_hash, check_password_hash

# Instanciate connection with DATABASE
db = DBConnect(
    os.getenv('DB_NAME'),
    os.getenv('DB_USER'),
    os.getenv('DB_PASSWORD'),
    os.getenv('DB_HOST')
)

admin = Blueprint('admin', __name__)

@admin.route('/admin/', methods=['POST', 'GET'])
def _admin():
    error = None
    if request.method == 'POST':
        if not request.form['username'] or not request.form['password']:
            error = 'Username and Password are required.'
        # Get connection with db
        conn = db.get_db()
        with conn:
            with conn.cursor() as curs:
                # Check if user exist
                curs.execute('SELECT * FROM users')
                user = curs.fetchone()
                if not user:
                    # If not exist saved in db
                    curs.execute("INSERT INTO users(username, password) VALUES(%s, %s)",
                            (request.form['username'], 
                            generate_password_hash(request.form['password'])))
                    session['username'] = request.form['username']
                    return redirect('/newsletters')
                else:
                    # Check password and user
                    if user[0] == request.form['username'] and check_password_hash(user[1], request.form['password']):
                        session['username'] = request.form['username']
                        return redirect('/newsletters')
                    error = 'Invalid credentials'
    return render_template('admin.html', error=error)

@admin.route('/logout/')
def logout():    
    session.pop('username', None)
    return redirect('/admin')