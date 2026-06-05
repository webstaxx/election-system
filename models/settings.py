from app import db

class Settings(db.Model):
    __tablename__ = "settings"

    id = db.Column(db.Integer, primary_key=True)

    # election state
    election_open = db.Column(db.Boolean, default=False)

    # results visibility
    results_visible = db.Column(db.Boolean, default=False)

    # current year/session
    election_year = db.Column(db.String(10), default="2026")

    # safety lock (prevents accidental resets)
    locked = db.Column(db.Boolean, default=False)