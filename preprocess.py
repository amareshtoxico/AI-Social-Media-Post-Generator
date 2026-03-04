import json

def preprocess_posts(input_file, output_file):

    with open(input_file, encoding="utf-8") as f:
        posts = json.load(f)

    processed_posts = []

    for post in posts:

        text = post["text"]

        processed_post = {
            "text": text,
            "likes": post.get("likes", 0),
            "comments": post.get("comments", 0),
            "shares": post.get("shares", 0),
            "engagement": post.get("engagement", 0),
            "category": post.get("category", "General"),
            "line_count": len(text.split("\n")),
            "language": "English",
            "tags": [post.get("category", "General")]
        }

        processed_posts.append(processed_post)

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(processed_posts, f, indent=4)


if __name__ == "__main__":
    preprocess_posts(
        "data/social_media_posts.json",
        "data/processed_posts.json"
    )