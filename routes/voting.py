from flask import Blueprint, jsonify, request

from extensions import db
from models import Post, Candidate, Vote, Settings

voting_bp = Blueprint(
    "voting",
    __name__
)


# ==========================================
# STUDENT BALLOT
# ==========================================

@voting_bp.route(
    "/ballot/student/<house>",
    methods=["GET"]
)
def student_ballot(house):

    settings = Settings.query.first()

    if not settings or not settings.election_open:
        return jsonify({
            "success": False,
            "message": "Election is closed"
        }), 403

    posts = Post.query.filter_by(
        active=True
    ).order_by(
        Post.display_order
    ).all()

    ballot_posts = []

    for post in posts:

        include = False

        if post.group_type == "common":
            include = True

        elif (
            post.group_type == "house"
            and post.house.lower() == house.lower()
        ):
            include = True

        if not include:
            continue

        candidates = []

        for candidate in post.candidates:

            if candidate.active:

                candidates.append({
                    "id": candidate.id,
                    "name": candidate.name,
                    "photo": candidate.photo
                })

        ballot_posts.append({
            "id": post.id,
            "title": post.title,
            "group_type": post.group_type,
            "house": post.house,
            "candidates": candidates
        })

    return jsonify({
        "success": True,
        "type": "student",
        "house": house,
        "posts": ballot_posts
    })


# ==========================================
# TEACHER BALLOT
# ==========================================

@voting_bp.route(
    "/ballot/teacher",
    methods=["GET"]
)
def teacher_ballot():

    settings = Settings.query.first()

    if not settings or not settings.election_open:
        return jsonify({
            "success": False,
            "message": "Election is closed"
        }), 403

    posts = Post.query.filter_by(
        active=True
    ).order_by(
        Post.display_order
    ).all()

    ballot_posts = []

    for post in posts:

        candidates = []

        for candidate in post.candidates:

            if candidate.active:

                candidates.append({
                    "id": candidate.id,
                    "name": candidate.name,
                    "photo": candidate.photo
                })

        ballot_posts.append({
            "id": post.id,
            "title": post.title,
            "group_type": post.group_type,
            "house": post.house,
            "candidates": candidates
        })

    return jsonify({
        "success": True,
        "type": "teacher",
        "posts": ballot_posts
    })


# ==========================================
# SUBMIT BALLOT
# ==========================================

@voting_bp.route(
    "/submit",
    methods=["POST"]
)
def submit_ballot():

    settings = Settings.query.first()

    if not settings or not settings.election_open:
        return jsonify({
            "success": False,
            "message": "Election is closed"
        }), 403

    data = request.get_json()

    if not data:
        return jsonify({
            "success": False,
            "message": "No data received"
        }), 400

    votes = data.get("votes", [])
    voter_type = data.get("voter_type")
    machine_id = data.get("machine_id")

    if not votes:
        return jsonify({
            "success": False,
            "message": "No votes submitted"
        }), 400

    try:

        for vote_data in votes:

            post_id = vote_data.get(
                "post_id"
            )

            candidate_id = vote_data.get(
                "candidate_id"
            )

            candidate = Candidate.query.get(
                candidate_id
            )

            if not candidate:
                return jsonify({
                    "success": False,
                    "message": f"Candidate {candidate_id} not found"
                }), 400

            if candidate.post_id != post_id:
                return jsonify({
                    "success": False,
                    "message": f"Candidate {candidate_id} does not belong to Post {post_id}"
                }), 400

            vote = Vote(
                candidate_id=candidate_id,
                voter_type=voter_type,
                machine_id=machine_id
            )

            db.session.add(vote)

        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Ballot submitted successfully"
        })

    except Exception as e:

        db.session.rollback()

        return jsonify({
            "success": False,
            "message": str(e)
        }), 500