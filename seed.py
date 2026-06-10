from app import app
from extensions import db
from models import Post


POSTS = [

    # Common Posts
    ("School Captain", "common", None),
    ("School Vice Captain", "common", None),

    ("Junior Captain", "common", None),
    ("Junior Vice Captain", "common", None),

    ("Co-Curricular Captain", "common", None),
    ("Co-Curricular Vice Captain", "common", None),

    ("Discipline Captain", "common", None),
    ("Discipline Vice Captain", "common", None),

    ("Sports Captain", "common", None),
    ("Sports Vice Captain", "common", None),

    # Agni
    ("Agni House Captain", "house", "agni"),
    ("Agni House Vice Captain", "house", "agni"),

    # Jalam
    ("Jalam House Captain", "house", "jalam"),
    ("Jalam House Vice Captain", "house", "jalam"),

    # Vayu
    ("Vayu House Captain", "house", "vayu"),
    ("Vayu House Vice Captain", "house", "vayu"),

    # Prithvi
    ("Prithvi House Captain", "house", "prithvi"),
    ("Prithvi House Vice Captain", "house", "prithvi")
]


with app.app_context():

    existing = Post.query.count()

    if existing > 0:
        print("Posts already exist.")
        exit()

    for order, (title, group_type, house) in enumerate(
        POSTS,
        start=1
    ):

        post = Post(
            title=title,
            group_type=group_type,
            house=house,
            display_order=order
        )

        db.session.add(post)

    db.session.commit()

    print(
        f"Inserted {len(POSTS)} posts successfully."
    )