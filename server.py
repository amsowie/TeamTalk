import sys
import json
import bcrypt
from jinja2 import StrictUndefined
from flask import Flask, render_template, jsonify, request, session, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
import requests
import os

from twilio.rest import Client

# Secrets and create client for Twilio
auth_token = os.environ.get('TWILIO_AUTH')
account_sid = os.environ.get('TWILIO_SID')
twilio_phone = os.environ.get('TWILIO_PHONE')
my_phone = os.environ.get('AMY_PHONE')
client = Client(account_sid, auth_token)

from model import connect_to_db, db, Team, Athlete, Coach
app = Flask(__name__)
app.secret_key = "Thanksforallthefish"

##############################################################################

# Homepage
@app.route('/home')
def index():
    """Welcome to bundesliga project page"""

    

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
        coach = db.session.query(Coach).filter(Coach.coach_email == email).first()

        # coach exists and password correct, redirect to team page with
        if coach:
            if ((bcrypt.hashpw(password.encode('utf-8'),
            coach.password.encode('utf-8')) == coach.password)):

                # add user to session
                session['coach_name'] = coach.coach_fname
                session['coach_id'] = coach.coach_id
                return render_template('teamboard.html', name=coach.coach_fname)

    if member == 'athlete':
        #find athlete in athlete table
        athlete = db.session.query(Athlete).filter(Athlete.a_email == email).first()

        # athlete exists and password correct, redirect to team page with
        if athlete:
            if ((bcrypt.hashpw(password.encode('utf-8'),
            athlete.password.encode('utf-8')) == athlete.password)):

                # add user to session
                session['athlete_name'] = athlete.a_fname
                session['athlete_id'] = athlete.athlete_id
                return render_template('teamboard.html', name=athlete.a_fname)

    # Redirect to login, incorrect information
    flash("No user exists with that information. Please register or try again.")
    return redirect('/login')  # change to home when you add navbar

@app.route('/register')
def register():
    """Registration page"""


    return render_template('register.html')

@app.route('/register-process')
def register_process():
    """Registration processing page"""


    return render_template('register.html')

@app.route('/logout')
def logout():
    """Log out and remove session"""

    # Delete athlete session info
    if member == 'athlete':
        del session['athlete_name']
        del session['athlete_id']
    # Delete coach session info
    else:
        del session['coach_name']
        del session['coach_id']

    # Delete team session info
    # del session[team_id]
        
    return redirect('/home')

@app.route('/sms')
def send_message():


    message = client.messages.create(
        to=my_phone,
        from_=twilio_phone,
        body="Hello from Python!")

    print(message.sid)
    return redirect('/sms')
##############################################################################
if __name__ == "__main__":  # will connect to db if you run python server.py
    app.debug = True        # won't run in testy.py because it's not server.py
    connect_to_db(app)
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")