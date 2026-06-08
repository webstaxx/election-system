from flask import Blueprint, jsonify
from models import Post

api_bp = Blueprint(
    "api",
    __name__
)

@api_bp.route("/posts")
def get_posts():

    posts = Post.query.order_by(
        Post.display_order
    ).all()

    return jsonify([
        {
            "id": post.id,
            "title": post.title,
            "group_type": post.group_type,
            "house": post.house
        }
        for post in posts
    ])