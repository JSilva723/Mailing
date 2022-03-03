import os
from flask import Blueprint, request, render_template, session, redirect
from ..services.smtp import SmtpGmail
from ..services.db import DBConnect

# Instanciate connection with DATABASE
db = DBConnect(
    os.getenv('DB_NAME'),
    os.getenv('DB_USER'),
    os.getenv('DB_PASSWORD'),
    os.getenv('DB_HOST')
)

newsletters = Blueprint('newsletters', __name__)

@newsletters.route('/newsletters/', methods=['GET', 'POST'])
def _newsletters():
    if 'username' in session:
        conn = db.get_db()
        with conn:
            with conn.cursor() as curs:
                curs.execute('SELECT email FROM contacts ORDER BY email ASC')
                to = [x[0] for x in curs.fetchall()]
        if request.method == 'POST':
            message = request.form.get('message')
            gmail = SmtpGmail(to, message, 'Newsletter')
            gmail.send()
            
        return render_template('newsletters.html', num_contacts=len(to), contacts=to)
    return redirect('/admin')
