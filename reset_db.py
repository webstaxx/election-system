from app import app
from extensions import db
from models import Post, Candidate, Vote, Settings

with app.app_context():

    Vote.query.delete()
    Candidate.query.delete()
    Post.query.delete()

    db.session.commit()

    print("Database cleared.")