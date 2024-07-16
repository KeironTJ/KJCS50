
from flask import render_template, flash, redirect, url_for, request, session # type: ignore
from app import app, db
from app.forms import LoginForm, RegistrationForm, UserGuessForm, UserSettingsForm, UserResetForm
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
        user = db.session.query(User).filter_by(username=form.username.data).first()

        # Set game settings
                
        game_settings = GuessTheNumberSettings(user_id=user.id)
        db.session.add(game_settings)
        db.session.commit()



        return redirect(url_for('index'))
    
    return render_template('register.html', title='Register', form=form)



@app.route('/guess_the_number', methods=['GET', 'POST'])
@login_required
def guess_the_number():

    # Check if the user has settings
    if GuessTheNumberSettings.query.filter_by(user_id=current_user.id).first() is None:
        GuessTheNumberSettings(user_id=current_user.id)
        db.session.commit()

    # Forms
    guessform = UserGuessForm()
    resetform = UserResetForm()

    # Queries
    game_settings = GuessTheNumberSettings.query.filter_by(user_id=current_user.id).first()
    start_range = game_settings.start_range
    end_range = game_settings.end_range

    # Start the game session
    start_game_session(user_id=current_user.id)

    # Session variables
    ai_number = session['ainumber']
    user_guesses = session['user_guesses']

    # Process the request using GameService
    if request.method == 'POST' and guessform.submit_guess.data:

        game_service = GameService(guessform.user_guess.data)
        game_service.add_guess()
        game_service.check_guess()

        if guessform.user_guess.data == ai_number:
            game_service.save_guess()
            reset_game_session()

            return redirect(url_for('guess_the_number'))
        

    if request.method == 'POST' and resetform.reset.data:
        reset_game_session()
        flash("Game reset.")
        return redirect(url_for('guess_the_number'))
    

    return render_template('guess_the_number.html', 
                           title='Guess the number',
                           guessform=guessform,
                           game_settings=game_settings,
                           user_guesses=user_guesses)

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

    # Query the database
    game_settings = GuessTheNumberSettings.query.filter_by(user_id=current_user.id).first()

    # Process the request
    if request.method == 'POST' and settingsform.submit_settings.data:
        
        # Data Validation
        if settingsform.start_range.data == None or settingsform.start_range.data < 0:
            flash("Please enter a start range value greater than 0.", "danger")
            return redirect(url_for('guess_the_number_settings'))
        if settingsform.end_range.data == None or settingsform.end_range.data <= settingsform.start_range.data:
            flash("Please enter an end range value greater than the start range.", "danger")
            return redirect(url_for('guess_the_number_settings'))
        
        if game_settings is None:
            game_settings = GuessTheNumberSettings(user_id=current_user.id, start_range=settingsform.start_range.data, end_range=settingsform.end_range.data)
            db.session.add(game_settings)
        else:
            game_settings.start_range = settingsform.start_range.data
            game_settings.end_range = settingsform.end_range.data
        db.session.commit()
        flash('Settings updated!')

        # Update Session
        reset_game_session()

        return redirect(url_for('guess_the_number_settings'))

    return render_template('guess_the_number_settings.html', 
                           title='Guess the number settings',
                           settingsform=settingsform,
                           game_settings=game_settings)