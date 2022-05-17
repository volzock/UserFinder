# It's really bad code, I'm so sorry about it, but it works (/*W*)/
import os

from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, template_folder='../templates')
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


class VideoModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    video_name = db.Column(db.String())

    def __init__(self, name):
        self.video_name = name

    def __repr__(self):
        return f"Video_{self.id} - {self.video_name}"


# Add to these model the ouput data (mayby frame(where user had detected), position of user, idk :) )
class ProcessingDatarModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    video_id = db.Column(db.Integer, db.ForeignKey('video_model.id'), nullable=False)


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


@app.route('/add/video', methods=['POST'])
def addVideo():
    # these function upload video
    # process video here
    # create output function
    file = request.files.get('video')
    print(file)
    return redirect(url_for('root'))


@app.route('/', methods=['GET', 'POST'])
def root():
    context = {'url': url_for('addVideo'),
               'url_user': url_for('addUser'),
               'users': [('1', 'volzock'), ('2', 'kst_obd')]}

    return render_template('root.html', context=context)
