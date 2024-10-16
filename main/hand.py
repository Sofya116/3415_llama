import typing

from src.card import lamaCard


class Hand:
    def __init__(self, cards:  list[lamaCard] = []):
        if cards is None:
            cards = []
        self.cards: list[lamaCard] = cards

    def __repr__(self):
        return self.save()

    def save(self) -> str:
        """Convert deck to string in '3 1 6' format."""
        scards = [c.save() for c in self.cards]         # ['3', '1', '6']
        s = ' '.join(scards)
        return s

    def __eq__(self, other):
        if isinstance(other, str):
            other = Hand.load(other)
        return self.cards == other.cards


    def add_card(self, card: lamaCard):
        self.cards.append(card)

    @classmethod
    def load(cls, text: str) -> typing.Self:
        """Convert string in '3 1 6' format to Deck. Return deck."""
        cards = [lamaCard.load(s) for s in text.split()]
        return cls(cards=cards)

    def remove_card(self, card: lamaCard):
        self.cards.remove(card)

    def score(self):
        """Штрафные очки"""
        res = 0
        for c in self.cards:
            res += c.score()
        return res

