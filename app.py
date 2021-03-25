from flask import Flask, request, redirect, url_for, render_template
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField,SelectField


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
        return redirect('run')
    else:
        return render_template('index.html',form=form)

@app.route('/run')
def run():
    return "run"

class ExamForm(FlaskForm):
    name = StringField('Name der Prüfung: ')
    duration = SelectField('Dauer der Prüfung (in Minuten): ',choices=[60,90,120,150,180])
    info = StringField('Zusätzliche Info (optional): ')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("8000"), debug=True)
    