from flask import Blueprint, jsonify, request

from extensions import db
from models import Post, Candidate, Settings

admin_bp = Blueprint(
    "admin",
    __name__
)


# ==========================================
# POSTS
# ==========================================

# ==========================================
# GET POSTS
# ==========================================

@admin_bp.route("/posts", methods=["GET"])
def get_posts():

    posts = Post.query.order_by(
        Post.display_order
    ).all()

    return jsonify([
        {
            "id": post.id,
            "title": post.title,
            "group_type": post.group_type,
            "house": post.house,
            "active": post.active
        }
        for post in posts
    ])

@admin_bp.route("/post/<int:post_id>", methods=["PUT"])
def update_post(post_id):

    post = Post.query.get(post_id)

    if not post:
        return {
            "success": False,
            "message": "Post not found"
        }, 404

    data = request.get_json()

    if "title" in data:
        post.title = data["title"]

    db.session.commit()

    return {
        "success": True
    }

@admin_bp.route(
    "/post/<int:post_id>/toggle",
    methods=["PUT"]
)
def toggle_post(post_id):

    post = Post.query.get(post_id)

    if not post:
        return {
            "success": False,
            "message": "Post not found"
        }, 404

    post.active = not post.active

    db.session.commit()

    return {
        "success": True,
        "active": post.active
    }


# ==========================================
# CANDIDATES
# ==========================================

@admin_bp.route("/candidates/<int:post_id>", methods=["GET"])
def get_candidates(post_id):

    candidates = Candidate.query.filter_by(
        post_id=post_id
    ).all()

    return jsonify([
        {
            "id": candidate.id,
            "name": candidate.name,
            "active": candidate.active
        }
        for candidate in candidates
    ])


# ==========================================
# ADD CANDIDATE
# ==========================================

@admin_bp.route("/candidate", methods=["POST"])
def add_candidate():

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "No data provided"
        }), 400

    name = data.get("name")
    post_id = data.get("post_id")

    if not name or not post_id:
        return jsonify({
            "success": False,
            "message": "name and post_id required"
        }), 400

    post = Post.query.get(post_id)

    if not post:
        return jsonify({
            "success": False,
            "message": "Post not found"
        }), 404

    candidate = Candidate(
        name=name,
        post_id=post_id
    )

    db.session.add(candidate)
    db.session.commit()

    return jsonify({
        "success": True,
        "candidate_id": candidate.id
    })
    

# ==========================================
# UPDATE CANDIDATE
# ==========================================

@admin_bp.route("/candidate/<int:candidate_id>", methods=["PUT"])
def update_candidate(candidate_id):

    candidate = Candidate.query.get(candidate_id)

    if not candidate:
        return jsonify({
            "success": False,
            "message": "Candidate not found"
        }), 404

    data = request.get_json()

    if "name" in data:
        candidate.name = data["name"]

    if "active" in data:
        candidate.active = data["active"]

    db.session.commit()

    return jsonify({
        "success": True
    })


# ==========================================
# DELETE CANDIDATE
# ==========================================

@admin_bp.route("/candidate/<int:candidate_id>", methods=["DELETE"])
def delete_candidate(candidate_id):

    candidate = Candidate.query.get(candidate_id)

    if not candidate:
        return jsonify({
            "success": False,
            "message": "Candidate not found"
        }), 404

    db.session.delete(candidate)
    db.session.commit()

    return jsonify({
        "success": True
    })

#=========================================
# SETTINGS
#=========================================

@admin_bp.route("/status", methods=["GET"])
def get_status():

    settings = Settings.query.first()

    if not settings:

        settings = Settings()

        db.session.add(settings)
        db.session.commit()

    return jsonify({
        "election_open": settings.election_open,
        "results_visible": settings.results_visible,
        "locked": settings.locked,
        "year": settings.election_year
    })

@admin_bp.route("/open-election", methods=["PUT"])
def open_election():

    settings = Settings.query.first()

    if not settings:

        settings = Settings()

        db.session.add(settings)

    settings.election_open = True

    db.session.commit()

    return jsonify({
        "success": True,
        "election_open": True
    })

@admin_bp.route("/close-election", methods=["PUT"])
def close_election():

    settings = Settings.query.first()

    if not settings:

        settings = Settings()

        db.session.add(settings)

    settings.election_open = False

    db.session.commit()

    return jsonify({
        "success": True,
        "election_open": False
    })