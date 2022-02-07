#!/bin/sh
export FLASK_APP=app.py
python3 -m venv venv
source ./venv/bin/activate
pip install -r requirements.txt
flask run -h localhost -p 3000
