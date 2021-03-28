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

#Main Page
@app.route('/', methods=["GET", "POST"])
def main_page():
    form = ExamForm()
    if request.method == "POST":
        exam_name = request.form.get('name')
        exam_duration = request.form.get('duration')
        exam_info = request.form.get('info')
        show_remaining = request.form.get('show_remaining')
        if not exam_name or not exam_duration: # add checks
            return render_template('index.html',form=form, error = True)
        exam_starttime = datetime.now().strftime("%H:%M")
        exam_endtime = (datetime.now() + timedelta(minutes=int(exam_duration))).strftime("%H:%M")
        key = setData(exam_name, exam_starttime, exam_endtime, exam_info, show_remaining)
        return redirect(url_for("run", key=key))
    else:
        return render_template('index.html',form=form, error = False)

@app.route('/<key>')
def run(key):
    if getData(key) == False:
        return "Sadly the requested Key can't be found on the server..."
    (key, exam_name, exam_starttime, exam_endtime, exam_info, show_remaining) = getData(key)
    return render_template('run.html', exam_name = exam_name, exam_info = exam_info, exam_starttime = exam_starttime, exam_endtime = exam_endtime, show_remaining = show_remaining)

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
                exam_starttime ,
                exam_endtime text,
                exam_info text,
                show_remaining integer
                )""")
    conn.commit()
    conn.close()
    return

def setData(exam_name, exam_starttime, exam_endtime, exam_info, show_remaining):
    conn = sqlite3.connect(database_location)
    c = conn.cursor()
    key = genKey()
    while isKey(key):
        key = genKey()
    c.execute("INSERT INTO main VALUES (?, ?, ?, ?, ?, ?)",(key, exam_name, exam_starttime, exam_endtime, exam_info, show_remaining))
    conn.commit()
    conn.close()
    return key

def getData(key):
    conn = sqlite3.connect(database_location)
    c = conn.cursor()
    c.execute("SELECT * FROM main WHERE key=?", (key, ))
    try:
        (key, exam_name, exam_starttime, exam_endtime, exam_info, show_remaining) = c.fetchone()
    except:
        print("key not found" + key)
        return False
    return (key, exam_name, exam_starttime, exam_endtime, exam_info, show_remaining)

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

if __name__ == '__main__':
    if not checkTable():
        makeTable()
    app.run(host="0.0.0.0", port=int("8000"), debug=False)
    