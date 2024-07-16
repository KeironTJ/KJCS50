from app import app, db
from app.models import GuessTheNumberSettings, User, GuessTheNumberHistory
from app.game_logic import GameService, reset_game_session, start_game_session
import sqlalchemy as sa
import random
from flask import session, flash, request, redirect, url_for, render_template
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import LoginForm, RegistrationForm, UserGuessForm, UserSettingsForm, UserResetForm
from urllib.parse import urlsplit


app_context = app.app_context()
app_context.push()


# existing data
db.session.query(GuessTheNumberSettings).delete()
db.session.query(GuessTheNumberHistory).delete()
db.session.query(User).delete()


db.session.commit()
