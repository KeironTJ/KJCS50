# create imports
from app import db
from app.auth.forms import LoginForm, RegistrationForm
from app.models import User, GuessTheNumberSettings
from flask import render_template, redirect, url_for, flash, request # type: ignore
from flask_login import current_user, login_user, logout_user #type: ignore
import sqlalchemy as sa # type: ignore
from urllib.parse import urlsplit
from app.auth import bp

## Authentication Routes
### The login view function
@bp.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    form = LoginForm()

    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.username == form.username.data))
        
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('auth.login'))
        
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')

        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('main.index')
        return redirect(next_page)
    
    return render_template('auth/login.html', title='Sign In', form=form)


@bp.route('/logout')
def logout():

    logout_user()

    return redirect(url_for('main.index'))


@bp.route('/register', methods=['GET', 'POST'])
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



        return redirect(url_for('main.index'))
    
    return render_template('auth/register.html', title='Register', form=form)