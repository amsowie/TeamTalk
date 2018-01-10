import sys
import json
import bcrypt
from jinja2 import StrictUndefined
from flask import Flask, render_template, jsonify, request, session, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
import requests
import os


# Imports the Google Cloud client library
from google.cloud import translate

# Instantiates a google client
translate_client = translate.Client()

# Twilio client
from twilio.rest import Client

google_auth = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')

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
                session['name'] = coach.coach_fname
                session['id'] = coach.coach_id
                return render_template('teamboard.html', team="HELLO")

    if member == 'athlete':
        #find athlete in athlete table
        athlete = db.session.query(Athlete).filter(Athlete.a_email == email).first()

        # athlete exists and password correct, redirect to team page with
        if athlete:
            if ((bcrypt.hashpw(password.encode('utf-8'),
            athlete.password.encode('utf-8')) == athlete.password)):

                # add user to session
                session['name'] = athlete.a_fname
                session['id'] = athlete.athlete_id
                print session['name']
                return render_template('teamboard.html', team="HELLO")

    # Redirect to login, incorrect information
    flash("No user exists with that information. Please register or try again.")
    return redirect('/login')  # change to home when you add navbar

@app.route('/register')
def register():
    """Registration page"""


    return render_template('register.html')

@app.route('/register-process', methods=['POST'])
def register_process():
    """Registration processing page"""

    member = request.form.get('member-type')
    fname = request.form.get('firstname')
    lname = request.form.get('lastname')
    phone = request.form.get('phone')
    email = request.form.get('email')
    password = request.form.get('password')
    team = request.form.get('team-name')

    hashed_pass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    if member == 'athlete':
        new_athlete = Athlete(a_fname=fname, a_lname=lname, a_phone=phone,
                              a_email=email, password=hashed_pass)
        db.session.add(new_athlete)
        db.session.commit()

        session['name'] = new_athlete.a_fname
        session['id'] = new_athlete.team_id

    if member == 'coach':
        new_coach = Coach(coach_fname=fname, coach_lname=lname,
                          coach_phone=phone, coach_email=email, password=hashed_pass)
        db.session.add(new_coach)
        db.session.commit()

        session['name'] = new_coach.coach_fname
        session['id'] = new_coach.team_id

    flash('Thank you for registering')

    return render_template('teamboard.html', team=team)

@app.route('/logout')
def logout():
    """Log out and remove session"""

    del session['name']
    del session['id']

    # Delete team session info
    # del session[team_id]
        
    return redirect('/home')

@app.route('/teams')
def teams():
    """Team page"""


    return render_template('teamboard.html')


@app.route('/sms-send', methods=['POST'])
def send_message():

    content = request.form.get('userMessage')


    # The text to translate
    text = content
    # The target language
    target = 'de'

    # Translates some text into Russian
    translation = translate_client.translate(
        text,
        target_language=target)

    print(u'Text: {}'.format(text))
    print(u'Translation: {}'.format(translation['translatedText']))

    translated_text = translation['translatedText']

    content = translated_text

    # phone_numbers = db.session.query(Team.athlete.a_phone).filter(Team.team_id == team_id).all()
    phone_list = [my_phone, '+17196440060']
    #  Cycle through whole team phone list
    for number in phone_list:
        message = client.messages.create(
            to=my_phone,
            from_=twilio_phone,
            body=content)

        print(message.sid)

    confirmation = "Message sent"

    return jsonify(message=confirmation)
##############################################################################
if __name__ == "__main__":  # will connect to db if you run python server.py
    app.debug = True        # won't run in testy.py because it's not server.py
    connect_to_db(app)
    DebugToolbarExtension(app)

    app.run(host="0.0.0.0")