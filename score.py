import unittest

"""
Scores a hand.

Each hand can have one or two scores.

If a hand has an ace and that ace counting as 11
does not bust the hand, then we score the hand
once with the ace counting as 1 and again as 11.

If the returned tuple has only one value, that
value can be above 21 (busted). However, it is
guaranteed that in a score with two totals, both
are valid.
"""
def score(hand):
    total_soft = sum(hand)
    if 1 in hand:
        total_hard = total_soft + 10 # adding 10 cause -1 + 11
        if total_hard <= 21:
            return (total_soft, total_hard)

    return (total_soft,)



class TestScore(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(score((4, 0)), (4,))
        self.assertEqual(score((2, 0)), (2,))
        self.assertEqual(score((10, 0)), (10,))
        self.assertEqual(score((10, 4)), (14,))
        self.assertEqual(score((10, 4, 7)), (21,))
        self.assertEqual(score((10, 4, 8)), (22,))

    def test_ace_soft(self):
        # one ace and another card
        self.assertEqual(score((4, 1)), (5, 15))
        self.assertEqual(score((8, 1)), (9, 19))
        self.assertEqual(score((10, 1)), (11, 21))

        # one ace and several other cards
        self.assertEqual(score((4, 1, 3)), (8, 18))
        self.assertEqual(score((8, 2, 1)), (11, 21))
        # blow
        self.assertEqual(score((10, 2, 1)), (13,))

        # multiple aces
        self.assertEqual(score((1, 1)), (2, 12))
        self.assertEqual(score((1, 4, 1)), (6, 16))
        self.assertEqual(score((1, 1, 4, 1)), (7, 17))
        self.assertEqual(score((1, 9, 1)), (11, 21))
        self.assertEqual(score((1, 10, 1)), (12,))
        self.assertEqual(score((1, 9, 1, 1)), (12,))
        self.assertEqual(score((1, 9, 2, 1)), (13,))

if __name__ == "__main__":
    unittest.main()

