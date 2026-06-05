from app import db

class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)

    # Name of the post (e.g., School Captain, Sports Captain)
    title = db.Column(db.String(120), nullable=False)

    # common / house
    group_type = db.Column(db.String(20), nullable=False)

    # Agni / Jalam / Vayu / Prithvi / NULL for common posts
    house = db.Column(db.String(20), nullable=True)

    # ordering in UI flow
    display_order = db.Column(db.Integer, default=0)

    # enable/disable without deleting
    active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"<Post {self.title}>"