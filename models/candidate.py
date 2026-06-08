from extensions import db


class Candidate(db.Model):
    __tablename__ = "candidates"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(
        db.String(120),
        nullable=False
    )

    post_id = db.Column(
        db.Integer,
        db.ForeignKey("posts.id"),
        nullable=False
    )

    photo = db.Column(
        db.String(255),
        nullable=True
    )

    active = db.Column(
        db.Boolean,
        default=True
    )

    post = db.relationship(
        "Post",
        back_populates="candidates"
    )

    votes = db.relationship(
        "Vote",
        back_populates="candidate",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Candidate {self.name}>"