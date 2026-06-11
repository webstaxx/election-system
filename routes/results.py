from flask import Blueprint, jsonify

from models import (
    Post,
    Candidate,
    Vote,
    Settings
)

results_bp = Blueprint(
    "results",
    __name__
)


@results_bp.route(
    "/",
    methods=["GET"]
)
def get_results():

    settings = Settings.query.first()

    if not settings:
        return jsonify({
            "success": False,
            "message": "Settings not found"
        }), 404

    results = []

    posts = Post.query.order_by(
        Post.display_order
    ).all()

    for post in posts:

        candidates_data = []

        for candidate in post.candidates:

            vote_count = Vote.query.filter_by(
                candidate_id=candidate.id
            ).count()

            candidates_data.append({
                "id": candidate.id,
                "name": candidate.name,
                "votes": vote_count
            })

        candidates_data.sort(
            key=lambda x: x["votes"],
            reverse=True
        )

        results.append({
            "post_id": post.id,
            "post_title": post.title,
            "candidates": candidates_data
        })

    return jsonify({
        "success": True,
        "election_open": settings.election_open,
        "results": results
    })