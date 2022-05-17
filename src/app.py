import os

from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__, template_folder='../templates')
app.config['SECRET_KEY'] = os.urandom(32)
# app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://127.0.0.1:5432/user_finder"
# db = SQLAlchemy(app)


@app.route('/add/user', methods=['POST'])
def addUser():
    print([request.files.getlist('image')])
    print(request.form.get('user'))
    return redirect(url_for('root'))


@app.route('/add/video', methods=['POST'])
def addVideo():
    file = request.files.get('video')
    print(file)
    return redirect(url_for('root'))


@app.route('/', methods=['GET', 'POST'])
def root():
    context = {'url': url_for('addVideo'),
               'url_user': url_for('addUser'),
               'users': [('1', 'volzock'), ('2', 'kst_obd')]}

    return render_template('root.html', context=context)
