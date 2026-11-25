"""Step 0.7: turn phrases into vectors and compare them with cosine similarity.

Run with:  uv run python scripts/hello_embed.py
"""

from chess_coach import config
from chess_coach.models import get_embeddings
from chess_coach.similarity import cosine_similarity

embeddings = get_embeddings()

# Pairs we expect to score high, medium and low.
pairs = [
    ("knight fork", "double attack"),
    ("pin", "skewer"),
    ("knight fork", "castling"),
    ("knight fork", "pasta recipe"),
]

# One vector first, to see what an embedding looks like.
vector = embeddings.embed_query("knight fork")
print(f"Model: {config.EMBEDDING_MODEL}")
print(f"'knight fork' -> {len(vector)} numbers, starting with {[round(x, 3) for x in vector[:5]]}")
print()

for first, second in pairs:
    first_vector, second_vector = embeddings.embed_documents([first, second])
    score = cosine_similarity(first_vector, second_vector)
    print(f"{score:.3f}  {first!r} vs {second!r}")
