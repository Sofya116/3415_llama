import hashlib
import json
import typing
from hand import Hand

class Player:
    # Инициализация игрока
    def __init__(self, name: str, hand: Hand, score: int = 0):
        self.name = name
        self.hand = hand
        self.score = score

    def __str__(self):
        return f"{self.name}({self.score}): {self.hand}"

    def __eq__(self, other: typing.Union['Player', str, dict]):
        # Сравнение игрока с другим объектом
        if isinstance(other, str):
            other = self.load(json.loads(other))
        if isinstance(other, dict):
            other = self.load(other)
        return (
            self.name == other.name
            and self.score == other.score
            and self.hand == other.hand
        )

    def __hash__(self) -> int:
        # Возвращает хэш-код игрока
        return int(hashlib.sha1(self.name.encode("utf-8")).hexdigest(), 16) % (10 ** 8)

    # Сохраняет состояние игрока в словарь
    def save(self) -> dict:
        return {
            "name": self.name,
            "hand": self.hand.save(),  # Предполагается, что метод save() возвращает сериализованное представление руки
            "score": self.score
        }

    @classmethod
    # Загружает игрока из словаря
    def load(cls, data: dict):
        # Проверка наличия необходимых ключей в словаре
        if not all(key in data for key in ["name", "hand", "score"]):
            raise ValueError("Missing keys in data for Player loading.")

        return cls(
            name=data["name"],
            hand=Hand.load(data["hand"]),
            score=int(data["score"])
        )
