from extensions import db
from datetime import datetime


class Vote(db.Model):
    __tablename__ = "votes"

    id = db.Column(db.Integer, primary_key=True)

    candidate_id = db.Column(
        db.Integer,
        db.ForeignKey("candidates.id"),
        nullable=False
    )

    timestamp = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    machine_id = db.Column(
        db.Integer,
        nullable=True
    )

    voter_type = db.Column(
        db.String(20),
        nullable=False
    )

    candidate = db.relationship(
        "Candidate",
        back_populates="votes"
    )

    def __repr__(self):
        return f"<Vote {self.id}>"