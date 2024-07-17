# create imports
from app import db
from app.models import User, Role, UserRoles, GuessTheNumberSettings, GuessTheNumberHistory
from flask import render_template, flash, redirect, url_for, request, session # type: ignore
from flask_login import login_required, current_user #type: ignore
from app.admin.decorators import admin_required
from app.admin import bp



## Admimn Routes
@bp.route('/admin_home', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_home():

    users = db.session.query(User).all()
    roles = db.session.query(Role).all()
    user_roles = db.session.query(UserRoles).all()
    gamesettings = db.session.query(GuessTheNumberSettings).all()
    gamehistory = db.session.query(GuessTheNumberHistory).all()

    return render_template('admin/admin_home.html',
                           title='Admin Home',
                           users=users,
                           roles=roles,
                           user_roles=user_roles,
                           gamesettings=gamesettings,
                           gamehistory=gamehistory)

@bp.route('/not_admin')
def not_admin():
    return render_template('admin/not_admin.html', title='Not Admin')