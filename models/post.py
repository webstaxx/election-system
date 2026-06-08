from extensions import db


class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)

    title = db.Column(
        db.String(120),
        nullable=False
    )

    group_type = db.Column(
        db.String(20),
        nullable=False
    )

    house = db.Column(
        db.String(20),
        nullable=True
    )

    display_order = db.Column(
        db.Integer,
        default=0
    )

    active = db.Column(
        db.Boolean,
        default=True
    )

    candidates = db.relationship(
        "Candidate",
        back_populates="post",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Post {self.title}>"