import typing
from main.card import lamaCard

class Hand:
    def __init__(self, cards: list[lamaCard] = None):
        if cards is None:
            cards = []
        self.cards: list[lamaCard] = cards

    def __repr__(self):
        return self.save()

    def save(self) -> str:
        """Convert hand to string in '3 1 6' format."""
        scards = [c.save() for c in self.cards]  # ['3', '1', '6']
        return ' '.join(scards)

    def __eq__(self, other):
        if isinstance(other, Hand):
            return self.cards == other.cards
        elif isinstance(other, str):
            other_hand = Hand.load(other)
            return self.cards == other_hand.cards
        return False

    def add_card(self, card: lamaCard):
        self.cards.append(card)

    @classmethod
    def load(cls, text: str) -> typing.Self:
        """Convert string in '3 1 6' format to Hand. Return hand."""
        cards = [lamaCard.load(s) for s in text.split()]
        return cls(cards=cards)

    def remove_card(self, card: lamaCard):
        self.cards.remove(card)

    def score(self) -> int:
        """Возвращает сумму очков карт в руке."""
        return sum(c.score() for c in self.cards)  # Убедитесь, что score() в lamaCard не требует аргументов

    def playable_cards(self, top_card):
        return [card for card in self.cards if card.can_play_on(top_card)]
