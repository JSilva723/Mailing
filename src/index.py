import os
from flask import Flask
from flask_cors import CORS
from .services.db import DBConnect
from .routes.auth import admin
from .routes.newsletters import newsletters
from .routes.form import form

# Instanciate connection with DATABASE
db = DBConnect(
    os.getenv('DB_NAME'),
    os.getenv('DB_USER'),
    os.getenv('DB_PASSWORD'),
    os.getenv('DB_HOST')
)

# Create tables
db.create_tables()

# Instanciate flask
app = Flask(__name__)
app.secret_key = 'any random string'

# Add Routes
app.register_blueprint(admin)
app.register_blueprint(newsletters)
app.register_blueprint(form)

# Add CORS
cors = CORS(app)