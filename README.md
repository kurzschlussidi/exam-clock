# exam-clock
A crude Website spinning up an Exam-Clock

Please don't assume that this software is safe to use :)

This a a small python script spinning up an Website on port 8000, which displays the exam-name, as well as the start/end-time of the exam and the current time in 24h format.

## Installation:

### Manual (not recommended):

    git clone https://github.com/kurzschlussidi/exam-clock.git
    cd exam-clock
    mkdir data
    pip install -r requirements.txt
    python app.py

Use as is, or point your reverse proxy towards the ip:port of this instance.

### Docker (recommended):

    docker run -d -p 80:8000 -v '/mnt/user/appdata/exam-clock':'/exam-clock/data':'rw' kurzschlussidi/exam-clock

Use as is, or point your reverse proxy towards the ip:port of this instance.

## Usage:

Open the Website and create the exam by entering the reqired information. By pressing start "Jetzt Beginnen" you can start the Exam.