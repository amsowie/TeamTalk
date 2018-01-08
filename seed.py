"""Utility file to seed bundes database"""

from model import Coach, Team, Athlete, connect_to_db, db
from server import app
import requests
import json
import os
from datetime import datetime as dt

##############################################################################



##############################################################################

if __name__ == '__main__':
    connect_to_db(app)
    db.create_all()