from main.card import lamaCard
from main.hand import Hand


from main.player_interaction import PlayerInteraction


class Human(PlayerInteraction):
    @classmethod
    def choose_card(cls, hand: Hand, top: lamaCard, hand_counts: list[int] | None = None) -> lamaCard:
        # Реализация выбора карты пользователем
        pass

    @classmethod
    def choose_to_play(cls, top: lamaCard, drawn: lamaCard) -> bool:
        # Реализация выбора играть или не играть
        pass

