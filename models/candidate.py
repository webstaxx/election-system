from app import db

class Candidate(db.Model):
    __tablename__ = "candidates"

    id = db.Column(db.Integer, primary_key=True)

    # Candidate name
    name = db.Column(db.String(120), nullable=False)

    # Link to Post (School Captain, Sports Captain, etc.)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), nullable=False)

    # Optional image (for UI later)
    photo = db.Column(db.String(255), nullable=True)

    # Whether candidate is active
    active = db.Column(db.Boolean, default=True)

    # Relationship (lets you do candidate.post.title)
    post = db.relationship("Post", backref="candidates")

    def __repr__(self):
        return f"<Candidate {self.name}>"