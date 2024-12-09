from main.card import lamaCard
from main.hand import Hand
from main.player import Player

from main.player_interaction import PlayerInteraction


class Bot(PlayerInteraction):
    @classmethod
    def choose_quit(
            cls, hand: Hand, top: lamaCard, hand_counts: list[int] | None = None
    ) -> bool:
        """True - игрок выбирает закончить этот раунд, False - продолжает играть."""
        print('Bot choose_quit -> TRUE!!!!')
        return True

    @classmethod
    def choose_card(cls, hand: Hand, top: lamaCard, hand_counts: list[int] | None = None) -> lamaCard:
        # Реализация выбора карты ботом
        pass

    @classmethod
    def choose_to_play(cls, top: lamaCard, drawn: lamaCard) -> bool:
        # Реализация выбора играть или не играть ботом
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
