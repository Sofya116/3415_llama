from main.card import lamaCard
from main.hand import Hand
from main.player_interaction import PlayerInteraction


class Human(PlayerInteraction):
    @classmethod
    def choose_card(cls, hand: Hand, top: lamaCard, hand_counts: list[int] | None = None) -> lamaCard:
        # Отображаем карты игрока
        print("Ваши карты:")
        for index, card in enumerate(hand.cards):
            print(f"{index}: {card}")
        # Запрашиваем у пользователя выбор карты
        while True:
            try:
                choice = int(input("Выберите номер карты, которую хотите сыграть: "))
                if 0 <= choice < len(hand.cards):
                    return hand.cards[choice]
            except ValueError:
                print("Пожалуйста, введите корректное число.")

    @classmethod
    def choose_to_play(cls, top: lamaCard, drawn: lamaCard) -> bool:
        # Реализация выбора играть или не играть
        choice = input(f"Вы хотите сыграть карту {top} или взять новую карту {drawn}? (y/n): ").strip().lower()
        return choice == 'y'

    @classmethod
    def choose_quit(
            cls, hand: Hand, top: lamaCard, hand_counts: list[int] | None = None
    ) -> bool:
        choice = input("Вы хотите закончить этот раунд? (y/n): ").strip().lower()
        return choice == 'y'
