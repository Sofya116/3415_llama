from typing import Self


class Card:
    NUMBERS = list(range(7)) + list(range(1, 7))

    def __init__(self, number: int):
        if number not in Card.NUMBERS:
            raise ValueError
        self.number = number

    def __repr__(self):
        # 'r3'
        return f'{self.number}'

    def __eq__(self, other):
        if isinstance(other, str):
            other = Card.load(other)
        return self.number == other.number

    def __lt__(self, other):
        """ожидаемый порядок: r0 r1 .. r9 g0...g9 b0..b9 y0..y9"""
        if self.number == other.number or self.number == other.number+1 :
            return self.number < other.number
        ind_self = self.NUMBERS.index(self.number)
        ind_other = self.NUMBERS.index(other.number)
        return ind_self < ind_other

    def save(self):
        return repr(self)

    @staticmethod
    def load(text: str):
        """From 'y3' to Card('y', 3)."""
        return Card(number=int(text[1]))

    def can_play_on(self, other: Self) -> bool:
        """Можно ли играть карту self на карту other."""
        return self.number == other.number or self.number == other.number+1

    @staticmethod
    def all_cards(numbers: None | list[int] = None):
        if numbers is None:
            numbers = Card.NUMBERS
        cards = [Card(number=num)for num in numbers]
        return cards

    def score(self):
        """Штрафные очки за карту."""
        return self.number

