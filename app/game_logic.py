

from app import db
from app.models import User, GuessTheNumberHistory, GuessTheNumberSettings
import sqlalchemy as sa
import random
from flask import session
from flask_login import current_user



# class to service the guess the number
class GameService():
    pass

## Helper functions for the game logic
def reset_game_session():
    session['ainumber'] = 0
    session['user_guesses'] = []

def start_game_session():
    settings = db.session.query(GuessTheNumberSettings).filter_by(user_id=current_user.id).first()
    if settings is None:
        settings = GuessTheNumberSettings(user_id=current_user.id, start_range=1, end_range=100)
        db.session.add(settings)
        db.session.commit()
    
    if 'ainumber' not in session or session['ainumber'] == 0:
        session['ainumber'] = random.randint(settings.start_range, settings.end_range)
    if 'user_guesses' not in session:
        session['user_guesses'] = []