import os
import csv
import sqlite3
from datetime import datetime
from time import time
from flask import Flask, g, render_template, request, flash, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from data import *
import json
# pseudo-user for testing
users = {'FootHow': {'password': '0000'}}

app = Flask(__name__)
app.secret_key = os.urandom(16).hex()

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "strong"
login_manager.login_view = 'login'
login_manager.login_message = 'Please Login'

SQLITE_DB_PATH = 'backend/foothow.db'
SQLITE_DB_SCHEMA = 'backend/create_db.sql'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(SQLITE_DB_PATH)
        # Enable foreign key check
        db.execute("PRAGMA foreign_keys = ON")
    return db


def reset_db():
    with open(SQLITE_DB_SCHEMA, 'r') as f:
        create_db_sql = f.read()
    db = get_db()
    # Reset database
    # Note that CREATE/DROP table are *immediately* committed
    # even inside a transaction
    with db:
        db.execute("PRAGMA foreign_keys = OFF")
        db.execute("DROP TABLE IF EXISTS members")
        db.execute("DROP TABLE IF EXISTS histories")
        db.execute("DROP TABLE IF EXISTS test")
        db.execute("DROP TABLE IF EXISTS temp")
        db.execute("PRAGMA foreign_keys = ON")
        db.executescript(create_db_sql)
        db.execute (
            'INSERT INTO members (account, password) VALUES ("FootHow", "0000")'
        )


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


class User(UserMixin):
    pass

@login_manager.user_loader
def user_loader(user_id):

    db = get_db()
    password = db.execute(
        'SELECT password FROM members WHERE account = ?', (user_id, )
    ).fetchall()

    if not password:
        return

    user = User()
    user.id = user_id
    return user

@login_manager.request_loader
def request_loader(request):

    user_id = request.form.get('ID')

    db = get_db()
    password = db.execute(
        'SELECT password FROM members WHERE account = ?', (user_id, )
    ).fetchall()

    if not password:
        return

    user = User()
    user.id = user_id
    
    # DO NOT ever store passwords in plaintext and always compare password
    # hashes using constant-time comparison!

    return user if (request.form['password'] == password[0][0]) else None


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'GET':
        return render_template('register.html')

    user_id = request.form['ID']
    user_password = request.form['password']
    check_passowrd= request.form.get('checkpassword')

    if(user_password != check_passowrd):
        errorMsg='<span style="color:#35858B">__</span><i class="fa fa-exclamation-triangle" aria-hidden="true"></i>您輸入的密碼有誤'
        return render_template('register.html', errorMsg = errorMsg)

    db = get_db()

    try:
        with db:
            db.execute (
                'INSERT INTO members (account, password) VALUES (?, ?)',
                (user_id, user_password)
            )
    except sqlite3.IntegrityError:
        errorMsg='<span style="color:#35858B">__</span><i class="fa fa-exclamation-triangle" aria-hidden="true"></i>該帳號已有人使用'
        return render_template('register.html', errorMsg = errorMsg)

    return redirect( url_for('index') )

@app.route('/login', methods=['GET', 'POST'])
def login():

    remember = True if request.form.get('remember') else False
    next = request.args.get('next', None)
    
    if request.method == 'GET':
        return render_template("login.html", next = next)

    user_id = request.form['ID']
    user_password = request.form['password']

    db = get_db()
    password = db.execute(
        'SELECT password FROM members WHERE account = ?', (user_id, )
    ).fetchall()

    if not password:
        errorMsg='<span style="color:#35858B">__</span><i class="fa fa-exclamation-triangle" aria-hidden="true"></i>您輸入的帳號不存在'
        return render_template('login.html', errorMsg = errorMsg)
    
    password = password[0][0]
    
    if user_password != password:
        errorMsg='<span style="color:#35858B">__</span><i class="fa fa-exclamation-triangle" aria-hidden="true"></i>您輸入的帳號或密碼有誤'
        return render_template('login.html', errorMsg = errorMsg)
    
    user = User()
    user.id = user_id
    login_user(user, remember = remember)
    return redirect(next or url_for('index'))

@app.route('/logout')
def logout():
    user_id = current_user.get_id()
    logout_user()
    return redirect( url_for('index') )

@app.route('/video')
def video():
    return render_template('video.html')

'''
@app.route('/showdata')
@login_required
def showdata():
    username = current_user.get_id()
    return render_template('showdata.html', username = username)
'''
@app.route('/showdata', methods=['GET', 'POST'])
# @app.route('/showdata')
@login_required
def showdata():
    db = get_db()
    username = current_user.get_id()
    selTime=request.form.get('time')
    histories = get_histories_by_account(username, db = db)
    # temps = [get_temp_record_by_id(history[0], db = db) for history in histories]
    tests = [get_test_record_by_id(history[0], db = db) for history in histories]

    print(histories, tests, username, sep = '\n')
    return render_template('showdata.html', username = username,data=tests,time=histories,selTime=selTime)

@app.errorhandler(404)
def not_found(e):
    return render_template('error.html', error = 'Not Found'), 404

@app.errorhandler(500)
def not_found(e):
    return render_template('error.html', error = 'Internal Server Error'), 500

@app.route('/new_index')
def test():
    title=['FootHouse','FootHow','FootWow']
    content=['新世代智慧醫療居家糖尿病足檢測儀器','新世代智慧醫療醫院端糖尿病足檢測儀器','新世代智慧醫療護理糖尿病足襪']
    return render_template('new_index.html',title=title,content=content)

@app.route('/temperature')
@login_required
def show_temperature():
    db = get_db()
    username = current_user.get_id()
    histories = get_histories_by_account(username, db = db)
    temps = [get_temp_record_by_id(history[0], db = db) for history in histories]
    print(histories, temps, username, sep = '\n')
    return render_template('showtemperature.html', username = username,time=histories,temp=temps)

@app.route('/_data', methods=['POST'])
def data():
    memberid = request.form.get('memberid')
    test = [int(n) for n in request.form.get('test').split(', ')]
    temp = [float(n) for n in request.form.get('temp').split(', ')]

    db = get_db()

    id = db.execute('SELECT COUNT(*) from histories').fetchone()[0] + 1
    test = [id] + test
    temp = [id] + temp

    test_cols = '(id, actual_1, actual_2, actual_3, actual_4, actual_5, guess_1, guess_2, guess_3, guess_4, guess_5)'
    temp_cols = '(id, temp_0, temp_1, temp_2, temp_3, temp_4, temp_5, temp_6, temp_7, temp_8, temp_9)'
    question_mark = '(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'

    with db:
        db.execute (
            'INSERT INTO histories (memberid) VALUES (?)',
            (int(memberid), )
        )
        db.execute (
            f'INSERT INTO test {test_cols} VALUES {question_mark}',
            tuple(test)
        )
        db.execute (
            f'INSERT INTO temp {temp_cols} VALUES {question_mark}',
            tuple(temp)
        )
    return '<h1>insert successfully</h1>'

if __name__ == '__main__':
    
    #with app.app_context():
    #    reset_db()

    app.run(debug = True)
