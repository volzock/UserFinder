# It's really bad code, I'm so sorry about it, but it works (/*W*)/
import os

from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import subprocess


app = Flask(__name__, template_folder='../templates', static_folder='../templates/static')
app.config['SECRET_KEY'] = os.urandom(32)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:1234@127.0.0.1:5432/user_finder"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), unique=True)

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"User_{self.id} - {self.name}"


class PhotoUserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username_id = db.Column(db.Integer, db.ForeignKey('user_model.id'), nullable=False)
    photo = db.Column(db.LargeBinary, nullable=False)

    def __init__(self, username_id, photo):
        self.username_id = username_id
        self.photo = photo

    def __repr__(self):
        return f"User({self.username_id}) - {self.name}"


class DetectUserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username_id = db.Column(db.Integer, db.ForeignKey('user_model.id'), nullable=False)
    time = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, username_id):
        self.username_id = username_id


@app.before_first_request
def create_tables():
    db.create_all()


@app.route('/add/user', methods=['POST'])
def addUser():
    username = request.form.get('user')
    if username:
        if not db.session.query(UserModel).filter(UserModel.name == username).first():
            user = UserModel(username)
            db.session.add(user)
            db.session.commit()

        if request.files.getlist('image')[0].filename:
            for file in request.files.getlist('image'):
                user = db.session.query(UserModel).filter(UserModel.name == username).first()
                user_id = user.id

                photo = PhotoUserModel(user_id, file.read())
                db.session.add(photo)
                db.session.commit()

    return redirect(url_for('root'))


@app.route('/users')
def users():
    context = {
        'users': db.session.query(UserModel),
        'root_url': url_for('root')
    }
    return render_template('users.html', context=context)


@app.route('/statistics')
def statistics():
    context = {
        'statistics': db.session.query(DetectUserModel),
        'root_url': url_for('root')
    }
    return render_template('statistics.html', context=context)


@app.route('/start', methods=['POST'])
def startProcessing():
    camera_ip = request.form.get('camera_ip')
    subprocess.Popen(["python", "stream.py", "--device_id", camera_ip, "--fps", "30", "--image_width", "640", "--image_height", "480"])

    # start in this point
    # https://www.the-analytics.club/python-shell-commands#:~:text=If%20you%20need%20to%20execute,arguments%20or%20producing%20text%20output.
    return redirect(url_for('root'))


@app.route('/main', methods=['GET', 'POST'])
def root():
    context = {'url_user': url_for('addUser'),
               'users_url': url_for('users'),
               'statistics_url': url_for('statistics'),
               'processing_url': url_for('startProcessing'),
               }
    return render_template('main.html', context=context)


@app.route('/')
def hello_page():
    context = {
    }
    return render_template('hello.html', context=context)


