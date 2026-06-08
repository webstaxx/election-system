from extensions import db


class Settings(db.Model):
    __tablename__ = "settings"

    id = db.Column(db.Integer, primary_key=True)

    election_open = db.Column(
        db.Boolean,
        default=False
    )

    results_visible = db.Column(
        db.Boolean,
        default=False
    )

    election_year = db.Column(
        db.String(10),
        default="2026"
    )

    locked = db.Column(
        db.Boolean,
        default=False
    )

    def __repr__(self):
        return f"<Settings {self.election_year}>"