from flask import Flask
from extensions import db

app = Flask(__name__)

app.config["SECRET_KEY"] = "change-this-later"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///election.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

from models import *

@app.route("/")
def home():
    return {
        "status": "Election System Online"
    }

@app.route("/init-db")
def init_db():
    db.create_all()
    return "Database Created"

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )