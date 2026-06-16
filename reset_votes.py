from app import app
from extensions import db
from models import Vote

confirm = input(
    "DELETE ALL VOTES? (yes/no): "
)

if confirm.lower() != "yes":
    print("Cancelled.")
    exit()

with app.app_context():

    deleted = Vote.query.delete()

    db.session.commit()

    print(
        f"Deleted {deleted} votes."
    )