import math


def bonus(score, occurrence, tier):
    return score * math.log1p(occurrence) / max(tier, 1)


def test_first_hop_level_is_two_not_one():
    score = 0.7
    wrong = bonus(score, 1, tier=1)
    correct = bonus(score, 1, tier=2)
    assert math.isclose(wrong / correct, 2.0)
