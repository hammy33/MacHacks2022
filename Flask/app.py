import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify, redirect, url_for, render_template, session, flash
from werkzeug.utils import secure_filename


app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'

app.secret_key = "FDM_fcg3_2021"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


@app.route("/")
def index():
    return render_template('Index.html')