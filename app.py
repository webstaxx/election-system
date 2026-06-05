from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# -------------------
# App Initialization
# -------------------

app = Flask(__name__)

# Config (you can move this to config.py later)
app.config["SECRET_KEY"] = "change-this-in-production"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///election.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# -------------------
# Database Init
# -------------------

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# -------------------
# Import Models (IMPORTANT: after db init)
# -------------------

from models.post import Post
from models.candidate import Candidate
from models.vote import Vote
from models.settings import Settings

# -------------------
# Register Routes (Blueprints later)
# -------------------

from routes.api import api_bp
from routes.voting import voting_bp
from routes.admin import admin_bp
from routes.results import results_bp

app.register_blueprint(api_bp, url_prefix="/api")
app.register_blueprint(voting_bp, url_prefix="/vote")
app.register_blueprint(admin_bp, url_prefix="/admin")
app.register_blueprint(results_bp, url_prefix="/results")

# -------------------
# Health Check Route
# -------------------

@app.route("/")
def home():
    return {
        "status": "Election System Online",
        "version": "1.0",
        "message": "Backend is running"
    }

# -------------------
# Run Server
# -------------------

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",   # allows LAN access (VERY important for your 4 machines)
        port=5000,
        debug=True
    )