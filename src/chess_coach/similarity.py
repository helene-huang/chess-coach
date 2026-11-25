"""Compare embedding vectors."""

import math


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """Return the cosine of the angle between vectors a and b.

    1.0 means same direction (same meaning), 0.0 unrelated, -1.0 opposite.
    Formula: (a · b) / (|a| * |b|)
    - a · b (dot product): multiply the numbers pair by pair, then add them up.
    - |a| (length): square root of the sum of each number squared.
    """
    # Vectors from two different embedding models have different sizes and
    # cannot be compared, so stop with a clear message instead.
    if len(a) != len(b):
        raise ValueError(
            f"Vectors have different sizes ({len(a)} and {len(b)}). "
            "Were they made by different embedding models?"
        )

    dot = sum(x * y for x, y in zip(a, b))
    length_a = math.sqrt(sum(x * x for x in a))
    length_b = math.sqrt(sum(y * y for y in b))
    return dot / (length_a * length_b)
