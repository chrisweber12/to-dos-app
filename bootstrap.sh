#!/bin/sh
export FLASK_APP=app.py
source venv/bin/activate
flask run -h localhost -p 3000
