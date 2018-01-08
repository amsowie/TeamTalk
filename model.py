"""Model for TeamTalk app"""

from flask import Flask
import bcrypt
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

##############################################################################
# Model definitions
# Athletes potentially on teams
class Athlete(db.Model):
    """Table for individual athlete information"""

    __tablename__ = "athletes"

    athlete_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    a_fname = db.Column(db.String(50), nullable=False)
    a_lname = db.Column(db.String(30), nullable=False)
    a_phone = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):  # pragma: no cover
        """Useful printout of person object"""

        return "<Athlete athlete_id={} a_fname={} a_lname={}>".format(self.athlete_id,
                                                                self.a_fname,
                                                                self.a_lname)

# Table to keep track of coach data
class Coach(db.Model):
    """Table for coach information"""

    __tablename__ = "coaches"

    coach_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    coach_fname = db.Column(db.String(30), nullable=False)
    coach_lname = db.Column(db.String(30), nullable=False)
    coach_phone = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):  # pragma: no cover
        """Useful printout of team object"""

        return "<Coach coach_id={} coach_fname={} coach_lname={}>".format(
                                                                self.coach_id,
                                                                self.coach_fname,
                                                                self.coach_lname)

# Add table to show which athletes/coaches are on which team
class Team(db.Model):
    """Association table for connecting athletes/coaches to teams"""

    __tablename__ = "teams"

    team_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    team_name = db.Column(db.String(50), nullable=False)
    coach_id = db.Column(db.Integer, db.ForeignKey('coach.coach_id'), nullable=False)
    athlete_id = db.Column(db.Integer, db.ForeignKey('athletes.athlete_id'), nullable=False)

    def __repr__(self):  # pragma: no cover
        """Useful printout of team object"""

        return "<Team team_id={} team_name={} athlete_id={} coach_id={}>".format(
                                                                self.team_id,
                                                                self.team_name,
                                                                self.athlete_id,
                                                                self.coach_id)

##############################################################################

def connect_to_db(app, db_uri='postgresql:///bundes'):
    """Connect the database to our Flask app."""

    # Configure to use the PostgresSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # app.config['SQLALCHEMY_ECHO'] = True
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app

    connect_to_db(app)  
    print "Connected to DB."
