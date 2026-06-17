from app import app
from extensions import db
from models import Vote

BALLOT_ID = "6332958a-91dd-4b9a-96a5-59e4c5bda1a6"

with app.app_context():

    votes = Vote.query.filter_by(
        ballot_id=BALLOT_ID
    ).all()

    print(
        f"Found {len(votes)} vote(s)"
    )

    if not votes:
        print("No votes found.")
        exit()

    for vote in votes:

        print(
            f"Deleting Vote ID {vote.id}"
        )

        db.session.delete(vote)

    db.session.commit()

    print(
        f"Removed {len(votes)} vote(s)"
    )