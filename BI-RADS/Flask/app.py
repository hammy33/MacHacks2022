import os
from pydoc import Doc
from wsgiref.util import request_uri
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, jsonify, redirect, url_for, render_template, session, flash
from werkzeug.utils import secure_filename
import birads_prediction_torch as prediction
import argparse
import utils
import models_torch as models

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads/'

app.secret_key = "BOOBYTRAP"
list = [0.264, 0.299, 0.437]
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
    return render_template('HomePage.html')


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
	return redirect(url_for('static', filename='uploads/' + filename), code=301)


@app.route('/doctors')
def get_doctors():
    doctors = Doctor.query.all()
    output = []
    for doc in doctors:
        doc_data = {'User ID': doc.userid, 'Name': doc.name}
        output.append(doc_data)
    return{"Doctors": output}

@app.route('/doctors/<id>', methods=['DELETE'])
def delete_doctor(id):
    doc  = Doctor.query.get(id)
    if doc is None:
        return {"Error":"404"}
    db.session.delete(doc)
    db.session.commit()
    return ("Doctor ID Number " + id + " has been deleted.")

@app.route('/next', methods=['GET'])
def nextSteps():

    if (max(list) == list[0]):
        return render_template("BI_RADS0.html")

    elif (max(list) == list[1]):
        return render_template("BI_RADS1.html")

    else:
        return render_template("BI_RADS2.html")

def Predictions():
    parser = argparse.ArgumentParser(description='Run Inference')
    parser.add_argument('--model-path', default='model.p')
    parser.add_argument('--device-type', default="cpu")
    parser.add_argument('--gpu-number', default=0, type=int)
    parser.add_argument('--image-path', default="static/uploads/")
    args = parser.parse_args()

    parameters_ = {
        "model_path": args.model_path,
        "device_type": args.device_type,
        "gpu_number": args.gpu_number,
        "image_path": args.image_path,
        "input_size": (2600, 2000),
    }

    x, y, z = prediction.inference(parameters_) 
    print(x,y,z)
    return x,y,z

if __name__ == "__main__":
    db.create_all()

