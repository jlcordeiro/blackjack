import mock
import itertools
import unittest
import random
from score import *

def play_dealer(card, card_generator):
    """
    Gets the first dealer card and a geneerator,
    and returns the final dealer hand.
    """

    hand = [card,]
    while score(hand)[0] < 17: 
        hand.append(next(card_generator))
    return tuple(hand)


def random_card_generator():
    while True:
        yield random.choice([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10])


class TestPlayDealer(unittest.TestCase):
    def test_basic(self):
        gen = mock.Mock()
        gen.return_value = itertools.cycle([2, 3])
        self.assertEquals(play_dealer(5, gen()), (5, 2, 3, 2, 3, 2))
        self.assertEquals(play_dealer(10, gen()), (10, 3, 2, 3))

        gen.return_value = itertools.cycle([6, 5, 3])
        self.assertEquals(play_dealer(10, gen()), (10, 6, 5))

    def test_bust(self):
        gen = mock.Mock()
        gen.return_value = itertools.cycle([2, 10, 4])
        self.assertEquals(play_dealer(3, gen()), (3, 2, 10, 4))
        self.assertEquals(play_dealer(10, gen()), (10, 2, 10))

    def test_bj(self):
        gen = mock.Mock()
        gen.return_value = itertools.cycle([10, 4])
        self.assertEquals(play_dealer(1, gen()), (1, 10))

    def test_soft(self):
        gen = mock.Mock()
        gen.return_value = itertools.cycle([1, 10, 4])
        self.assertEquals(play_dealer(6, gen()), (6, 1))

        gen.return_value = itertools.cycle([1, 10, 4])
        self.assertEquals(play_dealer(5, gen()), (5, 1, 10, 4))

    def test_random(self):
        """ Just to check that method works with a random generator. """
        hand = play_dealer(4, random_card_generator())
        self.assertTrue(len(hand) > 2)
        self.assertTrue(score(hand) >= 17)

if __name__ == "__main__":
    unittest.main()
