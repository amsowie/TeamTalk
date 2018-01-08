import sys
import json
import bcrypt
from jinja2 import StrictUndefined
from flask import Flask, render_template, jsonify, request, session, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
import requests
import os

from twilio.rest import Client
auth_token = os.environ.get('TWILIO_AUTH')
account_sid = os.environ.get('TWILIO_SID')
twilio_phone = os.environ.get('TWILIO_PHONE')
my_phone = os.environ.get('AMY_PHONE')

from model import connect_to_db, db, Team, Athlete, Coach
app = Flask(__name__)
app.secret_key = "Thanksforallthefish"

##############################################################################

# Homepage
@app.route('/sms')
def index():
    """Welcome to bundesliga project page"""

    # client = Client(account_sid, auth_token)

    # message = client.messages.create(
    #     to=my_phone,
    #     from_=twilio_phone,
    #     body="Hello from Python!")

    # print(message.sid)

    return render_template('home.html')

@app.route('/login')
def login():
    """Log in"""

   
    return render_template('login.html')

@app.route('/login-process', methods=['POST'])
def login_process():
    """Process login page"""

    #pull email and password and coach or athlete from form
    email = request.form.get('email')
    password = request.form.get('password')
    member = request.form.get('member-type')

    # check the coach email and password against database/hashed password of
    # coach only table
    if member == 'coach':
        #find coach in coach table
        coach = db.session.query(Coach).filter(Coach.email == email).first()

        # coach exists and password correct, redirect to team page with
        if coach:
            if ((bcrypt.hashpw(password.encode('utf-8'),
            coach.password.encode('utf-8')) == coach.password)):

                # add user to session
                session['coach_name'] = coach.coach_fname
                session['coach_id'] = coach.coach_id
            return render_template('/teams')

    if member == 'athlete':
        #find athlete in athlete table
        athlete = db.session.query(Athlete).filter(Athlete.email == email).first()

        # athlete exists and password correct, redirect to team page with
        if athlete:
            if ((bcrypt.hashpw(password.encode('utf-8'),
            athlete.password.encode('utf-8')) == athlete.password)):

                # add user to session
                session['athlete_name'] = athlete.a_fname
                session['athlete_id'] = athlete.athlete_id
            return render_template('/teams')

        # Redirect to login, incorrect information
    flash("No user exists with that information. Please register or try again.")
    return redirect('/login')

@app.route('/register')
def register():
    """Registration page"""


    return render_template('register.html')
##############################################################################
if __name__ == "__main__":  # will connect to db if you run python server.py
    app.debug = True        # won't run in testy.py because it's not server.py
    connect_to_db(app)
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")