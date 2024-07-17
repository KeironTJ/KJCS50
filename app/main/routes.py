from app.main import bp
from flask import render_template
from flask_login import login_required #type: ignore




### The index view function
@bp.route('/')
@bp.route('/index')
@login_required
def index():


    return render_template("main/index.html", title="Home")