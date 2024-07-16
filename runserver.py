import sqlalchemy as sa #type: ignore
import sqlalchemy.orm as so #type: ignore
from app import app, db



@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db}