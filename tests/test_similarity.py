"""Tests for cosine_similarity. Run with:  uv run pytest"""

import pytest
from pytest import approx

from chess_coach.similarity import cosine_similarity


def test_same_vector_is_1():
    assert cosine_similarity([1.0, 2.0, 3.0], [1.0, 2.0, 3.0]) == approx(1.0)


def test_opposite_vectors_are_minus_1():
    assert cosine_similarity([1.0, 2.0], [-1.0, -2.0]) == approx(-1.0)


def test_perpendicular_vectors_are_0():
    assert cosine_similarity([1.0, 0.0], [0.0, 1.0]) == approx(0.0)


def test_length_does_not_matter():
    # Same direction, one vector twice as long: still identical meaning.
    assert cosine_similarity([1.0, 2.0, 3.0], [2.0, 4.0, 6.0]) == approx(1.0)


def test_different_sizes_raise_error():
    # Passes only if the call inside the `with` block raises ValueError.
    with pytest.raises(ValueError):
        cosine_similarity([1.0, 2.0], [1.0, 2.0, 3.0])
