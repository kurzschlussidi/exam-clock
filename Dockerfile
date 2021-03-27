FROM python:3
ADD static exam-clock/static
ADD templates exam-clock/templates
ADD requirements.txt exam-clock/requirements.txt
ADD app.py exam-clock/app.py
RUN cd exam-clock
RUN pip install -r exam-clock/requirements.txt
RUN mkdir data
EXPOSE 8000
CMD [ "python3", "reminder/app.py" ]