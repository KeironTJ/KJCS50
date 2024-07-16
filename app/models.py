from typing import Optional
from sqlalchemy import Column, Integer, String, DateTime # type: ignore
import sqlalchemy.orm as so # type: ignore
from flask_login import UserMixin # type: ignore
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash # type: ignore

# 
@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

# Model for the User table
class User(UserMixin, db.Model):
    id = db.Column(Integer, primary_key=True)
    username = db.Column(String(64), index=True, unique=True)
    email = db.Column(String(120), index=True, unique=True)
    password_hash = db.Column(String(256))

    #Relationships
    guesses = so.relationship('GuessTheNumberHistory', back_populates='user')
    guess_settings = so.relationship('GuessTheNumberSettings', back_populates='user')


    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Model for the Guess the number game table
class GuessTheNumberSettings(db.Model):
    id = db.Column(Integer, primary_key=True)
    user_id = db.Column(Integer, db.ForeignKey('user.id'))
    start_range = db.Column(Integer, default=1)
    end_range = db.Column(Integer, default=100)

    # Relationships
    user = so.relationship('User', back_populates='guess_settings')




# Model for the Guess the number game history table
class GuessTheNumberHistory(db.Model):
    id = db.Column(Integer, primary_key=True)
    user_id = db.Column(Integer, db.ForeignKey('user.id'))
    start_range = db.Column(Integer)
    end_range = db.Column(Integer)
    correct_number = db.Column(Integer)
    number_of_guesses = db.Column(Integer)

    # Relationships
    user = so.relationship('User', back_populates='guesses')
    