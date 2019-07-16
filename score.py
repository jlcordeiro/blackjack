import unittest

def score(hand):
    """
    Scores a hand.

    Each hand can have one or two scores:
    (score,)
    (hard_score, soft_score)

    If a hand has an ace and that ace counting as 11
    does not bust the hand, then we score the hand
    once with the ace counting as 1 and again as 11.

    If the returned tuple has only one value, that
    value can be above 21 (busted). However, it is
    guaranteed that in a score with two totals, both
    are valid.
    """
    total_soft = sum(hand)
    if 1 in hand:
        total_hard = total_soft + 10 # adding 10 cause -1 + 11
        if total_hard <= 21:
            return (total_hard, total_soft)

    return (total_soft,)


def is_blackjack(hand):
    """ Check if a hand has a blackjack. """
    return sorted(hand) == [1, 10]


def score_against(hand, dealer):
    """ Score a player's hand against the dealer.
        Returns whatever multiplier should be applied to the bet
        to get the hand winnings.
        0.0 if lost.
        1.0 if tie.
        2.0 on win.
        2.5 on blackjack win.
    """

    (LOST, TIE, WIN, BJWIN) = (0.0, 1.0, 2.0, 2.5)

    player_bj = is_blackjack(hand)
    dealer_bj = is_blackjack(dealer)

    # player blackjack
    if player_bj:
        return TIE if dealer_bj else BJWIN
    # a dealer blackjack wins against everything else
    if dealer_bj:
        return LOST

    # a bust is always a bust
    hand_score = score(hand)[0]
    dealer_score = score(dealer)[0]
    if hand_score > 21:
        return LOST
    if dealer_score > 21:
        return WIN

    if dealer_score > hand_score:
        return LOST
    if dealer_score == hand_score:
        return TIE
    return WIN


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
        self.assertEqual(score((4, 1)), (15, 5))
        self.assertEqual(score((8, 1)), (19, 9))
        self.assertEqual(score((10, 1)), (21, 11))

        # one ace and several other cards
        self.assertEqual(score((4, 1, 3)), (18, 8))
        self.assertEqual(score((8, 2, 1)), (21, 11))
        # blow
        self.assertEqual(score((10, 2, 1)), (13,))

        # multiple aces
        self.assertEqual(score((1, 1)), (12, 2))
        self.assertEqual(score((1, 4, 1)), (16, 6))
        self.assertEqual(score((1, 1, 4, 1)), (17, 7))
        self.assertEqual(score((1, 9, 1)), (21, 11))
        self.assertEqual(score((1, 10, 1)), (12,))
        self.assertEqual(score((1, 9, 1, 1)), (12,))
        self.assertEqual(score((1, 9, 2, 1)), (13,))


class TestIsBJ(unittest.TestCase):
    def test_basic(self):
        self.assertFalse(is_blackjack((4, 0)))
        self.assertFalse(is_blackjack((4, 17)))
        self.assertFalse(is_blackjack((1, 9)))
        self.assertFalse(is_blackjack((1, 1)))
        self.assertTrue(is_blackjack((1, 10)))


class TestScoreAgainst(unittest.TestCase):
    def test_basic(self):
        # define some hands to test all possibilities with
        h_bj = (1, 10)
        h_21 = (1, 10, 10)
        h_bust = (2, 10, 10)
        h_13 = (3, 10)
        h_14 = (3, 1)
        h_17 = (7, 10)

        # user BJ ties against another BJ. wins against all others
        self.assertEqual(1.0, score_against(h_bj, h_bj))
        for h in (h_21, h_bust, h_13, h_17):
            self.assertEqual(2.5, score_against(h_bj, h))

        # user 21 loses against BJ. ties with 21. wins against others.
        self.assertEqual(0.0, score_against(h_21, h_bj))
        self.assertEqual(1.0, score_against(h_21, h_21))
        for h in (h_bust, h_13, h_17):
            self.assertEqual(2.0, score_against(h_21, h), h)


        # if player blows up, he always loses
        for h in (h_bj, h_21, h_bust, h_13, h_17):
            self.assertEqual(0.0, score_against(h_bust, h))


        # any other valid hand wins by rank
        self.assertEqual(1.0, score_against(h_13, h_13))
        for h in (h_bust, (2, 10)):
            self.assertEqual(2.0, score_against(h_13, h), h)
        for h in (h_bj, h_21, h_17, h_14):
            self.assertEqual(0.0, score_against(h_13, h), h)

        self.assertEqual(1.0, score_against(h_17, h_17))
        for h in (h_bust, h_13, h_14, (2, 10)):
            self.assertEqual(2.0, score_against(h_17, h), h)
        for h in (h_bj, h_21):
            self.assertEqual(0.0, score_against(h_17, h), h)


if __name__ == "__main__":
    unittest.main()

