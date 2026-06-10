from flask import Flask
from extensions import db

app = Flask(__name__)

app.config["SECRET_KEY"] = "change-this-later"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///election.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

from models import *
from routes.api import api_bp
from routes.admin import admin_bp
from routes.voting import voting_bp

from flask import Flask, render_template

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

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/init-db")
def init_db():
    db.create_all()
    return "Database Created"

@app.route("/admin-panel")
def admin_panel():
    return render_template("admin.html")

@app.route("/results")
def results_page():
    return "<h1>Results Coming Soon</h1>"


@app.route("/student")
def student():
    return render_template("student_vote.html")

@app.route("/teacher")
def teacher():
    return render_template("teacher_vote.html")

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )