

from app import db
from app.models import User, GuessTheNumberHistory, GuessTheNumberSettings
import sqlalchemy as sa # type: ignore
import random
from flask import session, flash # type: ignore
from flask_login import current_user # type: ignore




# class to service the guess the number
class GameService():
    def __init__(self, user_guess):
        self.user_guess = user_guess
        self.ainumber = session['ainumber']
        self.user_guesses = session['user_guesses']
        self.user_id = current_user.id
        self.start_range = db.session.query(GuessTheNumberSettings).filter_by(user_id=self.user_id).first().start_range
        self.end_range = db.session.query(GuessTheNumberSettings).filter_by(user_id=self.user_id).first().end_range

    def check_guess(self):
        if self.user_guess == self.ainumber:
            return flash("Congratulations! You guessed the number!", 'success')
        elif self.user_guess < self.ainumber:
            return flash("Your guess is too low!", 'danger')
        else:
            return flash("Your guess is too high!", 'danger')

    def save_guess(self):
        user_guess = GuessTheNumberHistory(user_id=self.user_id, 
                                           start_range=self.start_range, 
                                           end_range=self.end_range, 
                                           correct_number=self.ainumber, 
                                           number_of_guesses=len(self.user_guesses))
        db.session.add(user_guess)
        db.session.commit()

    def add_guess(self):
        self.user_guesses.append(self.user_guess)
        session['user_guesses'] = self.user_guesses

    def get_guesses(self):
        return self.user_guesses

    def get_ainumber(self):
        return self.ainumber


## Helper functions for the game logic
def reset_game_session():
    session['ainumber'] = 0
    session['user_guesses'] = []

def start_game_session(user_id):
    settings = db.session.query(GuessTheNumberSettings).filter_by(user_id=user_id).first()
    if settings is None:
        settings = GuessTheNumberSettings(user_id=user_id, start_range=1, end_range=100)
        db.session.add(settings)
        db.session.commit()
    
    if 'ainumber' not in session or session['ainumber'] == 0:
        session['ainumber'] = random.randint(settings.start_range, settings.end_range)
    if 'user_guesses' not in session:
        session['user_guesses'] = []