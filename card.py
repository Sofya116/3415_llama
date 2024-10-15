from typing import Self

class lamaCard:
    values = list(range(1, 7)) + [0]  # возможные значения карт (1-6 и 0 для "Ламы")
    lama = 0  # значение для карты "Лама"
    def __init__(self, value: int):
        """value (int): Номинальное значение карты."""
        # инициализация карты с проверкой значения
        if value not in lamaCard.values:
            raise ValueError
        self.value = value

    def __repr__(self):
        return str(self.value)

    def __eq__(self, other):
        # Сравнивает карты
        if isinstance(other, int):
            other = lamaCard(value=other)
        return self.value == other.value

    def __lt__(self, other):
        # Порядок карт (1, 2, ..., 6, 0)
        if self.value == other.value:
            return False
        if self.value == lamaCard.lama:
            return False
        if other.value == lamaCard.lama:
            return True
        return self.value < other.value

    def save(self):
        return repr(self)

    @staticmethod
    def load(text: str):
        return lamaCard(value=int(text))

    def can_play_on(self, other: Self) -> bool:
        #Метод возвращает логическое значение, указывающее, можно ли сыграть текущую карту (self) на другую карту (other).

        if self.value == other.value or self.value == other.value + 1:
            return True
        if self.value == lamaCard.lama:
            return other.value == 6 or other.value == lamaCard.lama
        if other.value == lamaCard.lama:
            return self.value == 1 or self.value == lamaCard.lama
        return False

    @staticmethod
    def all_cards():
        # Создает все карты
        cards = [lamaCard(value=val) for val in range(1, 7)]
        cards.extend([lamaCard(value=lamaCard.lama) for _ in range(8)])
        return cards

    def score(self, cards):
        """
        Возвращает очки карты на основе переданного списка карт.
        Если карта является дубликатом (т.е. она появляется более одного раза в списке карт),
        то очки равны 0. В противном случае очки равны номинальному значению карты.
        """
        # штрафные очки за карту
        if self.value == lamaCard.lama:
            return 10
        elif cards.count(self) > 1:  # Если карта является дубликатом, возвращаем 0
            return 0
        else:
            return self.value

