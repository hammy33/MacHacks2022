import os
from pydoc import Doc
from wsgiref.util import request_uri
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify, redirect, url_for, render_template, session, flash
from werkzeug.utils import secure_filename
import upload

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'

app.secret_key = "BOOBY TRAP"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
#app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set('png')

db = SQLAlchemy(app)


def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

class Doctor(db.Model):
        userid = db.Column(db.String(20), unique=True,  primary_key=True, nullable=False) 
        password = db.Column(db.String(20))
        name = db.Column(db.String(80), nullable=False)
        picture = db.Column(db.String(10))
        bio = db.Column(db.String(120))
        def __repr__(self):
                return f"{self.userid} - {self.name}"

@app.route("/")
def Homepage():
    return render_template('Index.html')

@app.route('/sign_up', methods=["POST", "GET"])
def sign_up():
    if request.method =="POST":
        # session.permanent = True
        password = request.form["password"]
        name = request.form["name"]
        # email = request.form["email"]

        Doc = Doctor(password=password, name=name, userid=len(Doctor.query.all()))
        db.session.add(Doc)
        db.session.commit()

        flash("Signed up successfully!")
        return redirect(url_for("Home"))
    else:
        if "name" in session:
            flash("Already logged in!")
            return redirect(url_for("name"))
        return render_template("SignUp.html")

@app.route('/login', methods=["POST", "GET"])
def login():
    if request.method == "POST":
        session.permanent = True
        seller = request.form["nm"]
        session["nm"] = seller
        password = request.form["password"]
        session["password"] = password

        found_user = Doctor.query.filter_by(name=seller).first()
        if found_user:
            if found_user.password == password:
                session["userid"] = found_user.userid
                session["bio"] = found_user.bio
            else:
                flash("Name or password is incorrect.")
                return redirect(url_for("login"))
        else:
            flash("User not found.")
            return redirect(url_for("login"))

        db.flash("Logged in successfully!")
        return redirect(url_for("Home"))
    else:
        if "user" in session:
            flash("Already logged in!")
            return redirect(url_for("user"))
        return render_template("Login.html")

@app.route('/Home', methods=["GET","POST"])
def Home():
    if(): #Picks enter new
        return redirect(url_for("load"))

    else: #Lookatold
        return

@app.route("/new-scan")
def load():
    return render_template("Upload.html")

@app.route("/new-scan", methods=["POST", "GET"])
def upload():
    if ('files[]' not in request.files):
        flash('No file part')
        return redirect(request.url)
    
    files = request.files.getlist('files[]')
    file_names = []
    for file in files:
        filename = secure_filename(file.filename)
        file_names.append(filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    return render_template('upload.html', filenames=file_names)

@app.route('/display/<filename>')
def display_image(filename):
	print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

@app.route('/doctors')
def get_doctors():
    sellers = Doctor.query.all()
    output = []
    for seller in sellers:
        seller_data = {'User ID': Doctor.userid, 'Name': Doctor.name}
        output.append(seller_data)
    return{"sellers": output}

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)