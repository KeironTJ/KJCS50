from app import db
from app.game import bp
from app.models import GuessTheNumberSettings, GuessTheNumberHistory
from app.game.forms import UserGuessForm, UserResetForm, UserSettingsForm
from app.game.game_logic import GameService, reset_game_session, start_game_session
from flask import render_template, flash, redirect, url_for, request, session # type: ignore
from flask_login import current_user, login_required #type: ignore
import sqlalchemy as sa # type: ignore
from urllib.parse import urlsplit
from app.game import bp


## Game Routes
@bp.route('/guess_the_number', methods=['GET', 'POST'])
@login_required
def guess_the_number():

    # Check if the user has settings
    game_settings = GuessTheNumberSettings.query.filter_by(user_id=current_user.id).first()
    if game_settings is None:
        new_settings = GuessTheNumberSettings(user_id=current_user.id)
        db.session.add(new_settings)
        db.session.commit()

    # Forms
    guessform = UserGuessForm()
    resetform = UserResetForm()

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

            return redirect(url_for('game.guess_the_number'))
        

    if request.method == 'POST' and resetform.reset.data:
        reset_game_session()
        flash("Game reset.", "info")
        return redirect(url_for('game.guess_the_number'))
    

    return render_template('game/guess_the_number.html', 
                           title='Guess the number',
                           guessform=guessform,
                           game_settings=game_settings,
                           user_guesses=user_guesses)

@bp.route('/guess_the_number_history')
@login_required
def guess_the_number_history():

    # Query the database
    history = db.session.query(GuessTheNumberHistory).filter_by(user_id=current_user.id).all()

    return render_template('game/guess_the_number_history.html', 
                           title='Guess the number history',
                           history=history)


@bp.route('/guess_the_number_settings', methods=['GET', 'POST'])
@login_required
def guess_the_number_settings():

    # Forms
    settingsform = UserSettingsForm()

    # Query the database
    game_settings = GuessTheNumberSettings.query.filter_by(user_id=current_user.id).first()

    # Process the request
    if request.method == 'POST' and settingsform.submit_settings.data:
        
        # Data Validation
        if settingsform.start_range.data is None or settingsform.start_range.data < 0:
            flash("Please enter a start range value greater than 0.", "danger")
            return redirect(url_for('game.guess_the_number_settings'))
        if settingsform.end_range.data is None or settingsform.end_range.data <= settingsform.start_range.data:
            flash("Please enter an end range value greater than the start range.", "danger")
            return redirect(url_for('game.guess_the_number_settings'))
        
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

        return redirect(url_for('game.guess_the_number_settings'))

    return render_template('game/guess_the_number_settings.html', 
                           title='Guess the number settings',
                           settingsform=settingsform,
                           game_settings=game_settings)