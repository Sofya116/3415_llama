from abc import ABC, abstractmethod

from card import lamaCard
from hand import Hand
from player import Player


class PlayerInteraction(ABC):
    @classmethod
    @abstractmethod
    def choose_card(
            cls, hand: Hand, top: lamaCard, hand_counts: list[int] | None = None
    ) -> lamaCard:
        pass

    @classmethod
    @abstractmethod
    def choose_to_play(cls, top: lamaCard, drawn: lamaCard) -> bool:
        """
        Принимает решение играть или не играть взятую из колоды карту.
        """
        pass

    @classmethod
    def inform_card_drawn(cls, player: Player):
        """
        Сообщает, что игрок взял карту.
        """
        pass

    @classmethod
    def inform_card_played(cls, player: Player, card: lamaCard):
        """
        Сообщает, что игрок сыграл карту.
        """
        pass
