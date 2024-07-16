
from flask import render_template, flash, redirect, url_for, request # type: ignore
from app import app, db
from app.forms import LoginForm, RegistrationForm, UserGuessForm, UserSettingsForm
from flask_login import current_user, login_user, logout_user, login_required #type: ignore
import sqlalchemy as sa # type: ignore
from app.models import User, GuessTheNumberSettings, GuessTheNumberHistory
from urllib.parse import urlsplit
from app.game_logic import GameService, reset_game_session, start_game_session


### The index view function
@app.route('/')
@app.route('/index')
@login_required
def index():


    return render_template("index.html", title="Home")


### The login view function
@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()

    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')

        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():

    logout_user()

    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')

        #obtain user id
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        login_user(user)

        # Set game settings
        start_game_session()

        return redirect(url_for('index'))
    
    return render_template('register.html', title='Register', form=form)



@app.route('/guess_the_number', methods=['GET', 'POST'])
@login_required
def guess_the_number():

    guessform = UserGuessForm()

    if request.method == 'POST' and guessform.submit_guess.data:
        pass

    return render_template('guess_the_number.html', 
                           title='Guess the number',
                           guessform=guessform)

@app.route('/guess_the_number_history')
@login_required
def guess_the_number_history():

    # Query the database
    history = db.session.query(GuessTheNumberHistory).filter_by(user_id=current_user.id).all()


    return render_template('guess_the_number_history.html', 
                           title='Guess the number history',
                           history=history)


@app.route('/guess_the_number_settings', methods=['GET', 'POST'])
@login_required
def guess_the_number_settings():

    # Forms
    settingsform = UserSettingsForm()

    if request.method == 'POST' and settingsform.submit_settings.data:
        game_settings = GuessTheNumberSettings.query.filter_by(user_id=current_user.id).first()
        if game_settings is None:
            game_settings = GuessTheNumberSettings(user_id=current_user.id, start_range=settingsform.start_range.data, end_range=settingsform.end_range.data)
            db.session.add(game_settings)
        else:
            game_settings.start_range = settingsform.start_range.data
            game_settings.end_range = settingsform.end_range.data
        db.session.commit()
        flash('Settings updated!')


    return render_template('guess_the_number_settings.html', 
                           title='Guess the number settings',
                           settingsform=settingsform)