"""Utility file to seed bundes database"""

from model import Team, Athlete, connect_to_db, db
from server import app
import bcrypt
import requests
import json
import os
from datetime import datetime as dt

##############################################################################

def write_data():
    """Write trial user data"""

    athlete1 = Athlete(a_fname="Brian", a_lname="Bestie", a_phone="+17196440060",
                       a_email="bb@bb.com", team_id=1, language="de")
    team1 = Team(team_name="Affy", coach_fname="Kari",
                  coach_lname="Bestova", coach_phone="+18595823016",
                  coach_email="kb@bb.com", password=bcrypt.hashpw('sugar', bcrypt.gensalt()))


    # db.session.add_all([coach1])
    # db.session.commit()
    db.session.add_all([team1])
    db.session.commit()
    db.session.add_all([athlete1])
    db.session.commit()
##############################################################################

if __name__ == '__main__':
    connect_to_db(app)
    db.create_all()

write_data()
