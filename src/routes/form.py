from calendar import c
import os
from flask import Blueprint, request
from ..services.db import DBConnect
from ..services.smtp import SmtpGmail

# Instanciate connection with DATABASE
db = DBConnect(
    os.getenv('DB_NAME'),
    os.getenv('DB_USER'),
    os.getenv('DB_PASSWORD'),
    os.getenv('DB_HOST')
)

form = Blueprint('form', __name__)

@form.route('/form/', methods=['POST'])
def _form():
    # Get data of request
    data = request.json
    # Check if exist email
    contact_email = data.get('email')
    if not contact_email:
        return { 'error': 'The email is required.' }
    # Create message to send
    message_to_send = '\nThe Sr/Ms {}, says, {}'.format(data.get('name', 'Anonimus'), data.get('message', 'Message in blanck'))
    # Set receivers emails
    to = os.getenv('OWNER')
    # Instanciate class
    gmail = SmtpGmail(to, message_to_send, 'Oportunity')
    # Send email
    gmail.send()
    # Create response for client
    response_message = 'Sended email to {}.'.format(to)
    # Get connection with db
    conn = db.get_db()
    with conn:
        with conn.cursor() as curs:
            # Check if email exist
            curs.execute('SELECT email FROM contacts WHERE email = %s', (contact_email,))
            if curs.fetchall() == []:
                # If not exist saved in db
                curs.execute("INSERT INTO contacts(email) VALUES(%s)",(contact_email,))
                # Set response for client
                response_message = response_message + ' Saved contact({}) in DB'.format(contact_email)
    return { 'message': response_message }