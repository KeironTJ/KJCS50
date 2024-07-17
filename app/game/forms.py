from flask_wtf import FlaskForm # type: ignore
from wtforms import IntegerField, SubmitField # type: ignore
from wtforms.validators import DataRequired # type: ignore



class UserGuessForm(FlaskForm):
    user_guess = IntegerField('Guess', validators=[DataRequired()])
    submit_guess = SubmitField('Submit')

class UserSettingsForm(FlaskForm):
    start_range = IntegerField('Start Range', validators=[DataRequired()])
    end_range = IntegerField('End Range', validators=[DataRequired()])
    submit_settings = SubmitField('Submit')

class UserResetForm(FlaskForm):
    reset = SubmitField('Reset Game')