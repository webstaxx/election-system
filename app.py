from flask import Flask, render_template
from waitress import serve

from extensions import db

app = Flask(__name__)

app.config["SECRET_KEY"] = "change-this-later"

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:///election.db"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Helps prevent SQLite lock issues
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
    "connect_args": {
        "timeout": 30
    }
}

db.init_app(app)

from models import *

from routes.api import api_bp
from routes.admin import admin_bp
from routes.voting import voting_bp
from routes.results import results_bp

app.register_blueprint(
    api_bp,
    url_prefix="/api"
)

app.register_blueprint(
    admin_bp,
    url_prefix="/admin"
)

app.register_blueprint(
    voting_bp,
    url_prefix="/vote"
)

app.register_blueprint(
    results_bp,
    url_prefix="/results"
)

@app.route("/")
def home():
    return render_template(
        "index.html"
    )

@app.route("/init-db")
def init_db():

    db.create_all()

    return "Database Created"

@app.route("/admin")
def admin_panel():

    return render_template(
        "admin.html"
    )

@app.route("/results-page")
def results_page():

    return render_template(
        "results.html"
    )

@app.route("/student")
def student():

    return render_template(
        "student_vote.html"
    )

@app.route("/teacher")
def teacher():

    return render_template(
        "teacher_vote.html"
    )

if __name__ == "__main__":

    print(
        "\nElection System Running"
        "\nServer: Waitress"
        "\nPort: 5000\n"
    )

    serve(
        app,
        host="0.0.0.0",
        port=5000,
        threads=8
    )