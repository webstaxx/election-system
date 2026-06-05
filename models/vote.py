from app import db
from datetime import datetime

class Vote(db.Model):
    __tablename__ = "votes"

    id = db.Column(db.Integer, primary_key=True)

    # Who got the vote
    candidate_id = db.Column(db.Integer, db.ForeignKey("candidates.id"), nullable=False)

    # When it happened
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    # Which machine (useful for debugging)
    machine_id = db.Column(db.Integer, nullable=True)

    # student / teacher / admin (important for your system rules)
    voter_type = db.Column(db.String(20), nullable=False)

    # relationship
    candidate = db.relationship("Candidate")