import sqlalchemy as sa #type: ignore
import sqlalchemy.orm as so #type: ignore
from app import db, create_app


app = create_app()

app.run()

@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db}