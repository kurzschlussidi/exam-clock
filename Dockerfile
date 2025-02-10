FROM python:3.12.3
ADD static exam-clock/static
ADD templates exam-clock/templates
ADD requirements.txt exam-clock/requirements.txt
ADD app.py exam-clock/app.py
ADD app.ini exam-clock/app.ini
WORKDIR /exam-clock/
RUN pip install -r requirements.txt
RUN mkdir data
EXPOSE 8000
CMD ["uwsgi", "app.ini"]