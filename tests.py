from app import app, db
from app.models import GuessTheNumberSettings, User, GuessTheNumberHistory, UserRoles, Role
from app.game_logic import GameService, reset_game_session, start_game_session
import sqlalchemy as sa
import random
from flask import session, flash, request, redirect, url_for, render_template
from flask_login import current_user, login_user, logout_user, login_required
from app.forms import LoginForm, RegistrationForm, UserGuessForm, UserSettingsForm, UserResetForm
from urllib.parse import urlsplit


app_context = app.app_context()
app_context.push()

# Test to create roles
def create_role(name):
    role = Role(name=name)
    db.session.add(role)
    return role

def create_user(username, email, password): 
    user = User(username=username, email=email)
    user.set_password(password)
    db.session.add(user)
    return user

def add_game_settings(user_id, start_range, end_range):
    settings = GuessTheNumberSettings(user_id=user_id, start_range=start_range, end_range=end_range)
    db.session.add(settings)
    return settings


def delete_existing_data():
    db.session.query(GuessTheNumberSettings).delete()
    db.session.query(GuessTheNumberHistory).delete()
    db.session.query(User).delete()
    db.session.query(Role).delete()
    db.session.query(UserRoles).delete
    db.session.commit()
    print("Data Deleted")
    

delete_existing_data()


# Create admin and user roles
admin_role = create_role('admin')
user_role = create_role('user')

# Create admin user
admin_user = create_user('KeironTJ', 'test1@test.com', 'abc123')
test_user = create_user('test', 'test2@test.com', 'abc123')
db.session.commit()

# Assign role to admin 
admin_user_role = UserRoles(user_id=admin_user.id, role_id=admin_role.id)
test_user_role = UserRoles(user_id=test_user.id, role_id=user_role.id)
db.session.add(admin_user_role)
db.session.add(test_user_role)

# Create Guess the number settings
add_game_settings(admin_user.id, 1, 100)
add_game_settings(test_user.id, 1, 100)

# Commit all changes 
db.session.commit()


             




db.session.commit()
