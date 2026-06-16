from waitress import serve

from flask import (
    Flask,
    render_template,
    request,
    session,
    redirect,
    url_for
)

from datetime import timedelta

from extensions import db

app = Flask(__name__)

app.config["SECRET_KEY"] = "change-this-later"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(
    minutes=5
)

ADMIN_PASSWORD = "Election2026!"

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

# ================
# Password Protected Admin routes
# =================

@app.route(
    "/admin-login",
    methods=["GET", "POST"]
)
def admin_login():

    if request.method == "POST":

        password = request.form.get(
            "password"
        )

        if password == ADMIN_PASSWORD:

            session.permanent = True
            session["admin"] = True

            return redirect(
                "/admin"
            )

        return render_template(
            "admin_login.html",
            error="Invalid Password"
        )

    return render_template(
        "admin_login.html"
    )

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")

@app.route("/admin")
def admin_panel():

    if not session.get("admin"):
        return redirect(
            "/admin-login"
        )

    return render_template(
        "admin.html"
    )

@app.route("/results-page")
def results_page():

    if not session.get("admin"):
        return redirect(
            "/admin-login"
        )

    return render_template(
        "results.html"
    )

# =========================

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