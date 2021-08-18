from flask import Flask, request, redirect, url_for, render_template, send_from_directory
from datetime import datetime, timedelta
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, BooleanField
import sqlite3
import random
import os
import string


dir_path = os.path.dirname(os.path.realpath(__file__))
database_location = dir_path + "/data/database.db"
app = Flask(__name__)
app.config['SECRET_KEY'] = 'blaslasdjasndhjasbfa.bcghvasgdvasjhdbahdbashdasjhdbvz23be2e7wq768asfd867asfvas8f7638vr728'
Bootstrap(app)

@app.before_request
def before_request():
    if not checkTable():
        makeTable()

#Main Page
@app.route('/', methods=["GET", "POST"])
def main_page():
    form = ExamForm()
    if request.method == "POST":
        exam_name = request.form.get('name')
        exam_duration = request.form.get('duration')
        exam_info = request.form.get('info')
        show_remaining = request.form.get('show_remaining')
        show_seconds = request.form.get('show_seconds')
        if not exam_name or not exam_duration: # add checks
            return render_template('index.html',form=form, error = True)
        exam_starttime = 'None'
        key = setData(exam_name, exam_starttime, exam_duration, exam_info, show_remaining, show_seconds)
        return redirect(url_for("run", key=key))
    else:
        return render_template('index.html',form=form, error = False)

@app.route('/<key>', methods=["GET", "POST"])
def run(key):
    if getData(key) == False:
        return "Sadly the requested Key can't be found on the server..."
    (key, exam_name, exam_starttime, exam_duration, exam_info, show_remaining, show_seconds) = getData(key)
    if exam_starttime == 'None':
        if request.method == "POST":
            if request.form.get('submit') == 'Jetzt Beginnen':
                exam_starttime = datetime.now().strftime("%H:%M:%S")
                updateStarttime(key=key, exam_starttime=exam_starttime)
            else:
                try:
                    start_hour = int(request.form.get('start_hour'))
                    start_minute = int(request.form.get('start_minute'))
                except:
                    return render_template('start_view.html',exam_name = exam_name, exam_info = exam_info)
                exam_starttime = datetime.now().replace(hour=start_hour,minute=start_minute,second=0).strftime("%H:%M:%S")
                updateStarttime(key=key, exam_starttime=exam_starttime)
            return redirect(url_for('run', key = key))
        return render_template('start_view.html',exam_name = exam_name, exam_info = exam_info)
    else:
        start_hour, start_minute, start_second = exam_starttime.split(':')
        exam_endtime = (datetime.now().replace(hour=int(start_hour), minute=int(start_minute), second=int(start_second)) + timedelta(minutes=int(exam_duration))).strftime("%H:%M:%S")
        return render_template('run.html', exam_name = exam_name, exam_info = exam_info, exam_starttime = exam_starttime, exam_endtime = exam_endtime, show_remaining = show_remaining, show_seconds = show_seconds)

@app.route('/done')
def exam_over():
   return render_template('exam_over.html')

@app.route('/favicon.ico') 
def favicon(): 
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')

def checkTable():
    conn = sqlite3.connect(database_location)
    c = conn.cursor()
    c.execute(''' SELECT count(name) FROM sqlite_master WHERE type='table' AND name='main' ''')
    if c.fetchone()[0]==1 :
        conn.close()
        return True
    else:
        conn.close()
        return False
    

def makeTable():
    conn = sqlite3.connect(database_location)
    c = conn.cursor()
    c.execute("""CREATE TABLE main (
                key text,
                exam_name text,
                exam_starttime text,
                exam_duration integer,
                exam_info text,
                show_remaining integer,
                show_seconds integer
                )""")
    conn.commit()
    conn.close()
    return

def setData(exam_name, exam_starttime, exam_duration, exam_info, show_remaining, show_seconds):
    conn = sqlite3.connect(database_location)
    c = conn.cursor()
    key = genKey()
    while isKey(key):
        key = genKey()
    c.execute("INSERT INTO main VALUES (?, ?, ?, ?, ?, ?, ?)",(key, exam_name, exam_starttime, exam_duration, exam_info, show_remaining, show_seconds))
    conn.commit()
    conn.close()
    return key

def updateStarttime(key,exam_starttime):
    conn = sqlite3.connect(database_location)
    c = conn.cursor()
    c.execute("UPDATE main SET exam_starttime = ? WHERE key = ?",(exam_starttime,key))
    conn.commit()
    conn.close()


def getData(key):
    conn = sqlite3.connect(database_location)
    c = conn.cursor()
    c.execute("SELECT * FROM main WHERE key=?", (key, ))
    try:
        (key, exam_name, exam_starttime, exam_duration, exam_info, show_remaining, show_seconds) = c.fetchone()
    except:
        print("key not found" + key)
        return False
    return (key, exam_name, exam_starttime, exam_duration, exam_info, show_remaining, show_seconds)

def isKey(key):
    conn = sqlite3.connect(database_location)
    c = conn.cursor()
    c.execute("SELECT * FROM main WHERE key=?", (key, ))
    if c.fetchone() == None:
        conn.close()
        return False
    else:
        conn.close()
        return True
    
def genKey():
    return ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(6))

class ExamForm(FlaskForm):
    name = StringField('Name der Prüfung: ')
    duration = SelectField('Dauer der Prüfung (in Minuten): ',choices=[60,90,120,150,180])
    info = StringField('Zusätzliche Info (optional): ')
    show_remaining = BooleanField('Verbleibende Zeit anzeigen?')
    show_seconds = BooleanField('Sekunden bei der Uhrzeit anzeigen?')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("8000"), debug=False)