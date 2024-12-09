import inspect
import os
import json
import pygame
from main.deck import Deck
from main.game_state import GameState
from main.hand import Hand
from main.player import Player
from main.player_interaction import PlayerInteraction
from main.player_interactions.init import all_player_types
import enum
from main.card import lamaCard

pygame.init()

class GamePhase(enum.StrEnum):
    CHOOSE_CARD = "Choose card"
    DRAW_EXTRA = "Draw extra card"
    NEXT_PLAYER = "Switch current player"
    DECLARE_WINNER = "Declare a winner"
    GAME_END = "Game ended"

class GameServer:
    INITIAL_HAND_SIZE = 6
    MAX_MOVES = 100  # Устанавливаем лимит на количество ходов

    def __init__(self, player_types, game_state):
        self.game_state: GameState = game_state
        self.player_types: dict = player_types  # {player: PlayerInteractions}
        self.move_count = 0  # Инициализация счетчика ходов

    @classmethod
    def load_game(cls):
        filename = 'lama.json'
        try:
            with open(filename, 'r', encoding='utf-8') as fin:
                data = json.load(fin)

                # Создаем колоду на основе данных из файла
                deck = Deck(cards=[lamaCard(card_value) for card_value in map(int, data['deck'].split())])
                top_card = lamaCard(int(data['top']))  # Создаем объект lamaCard для верхней карты
                current_player_index = data.get('current_player_index', 0)  # Значение по умолчанию

                # Создаем игроков и их руки
                players = []
                for player_data in data['players']:
                    name = player_data['name']
                    hand_cards = list(map(int, player_data['hand'].split()))
                    hand = Hand(cards=[lamaCard(card_value) for card_value in hand_cards])  # Создаем объекты lamaCard
                    player = Player(name, hand, score=player_data['score'])
                    players.append(player)

                # Создаем состояние игры
                game_state = GameState(
                    players=players,  # Передаем список объектов Player
                    deck=deck,
                    top=top_card,  # Передаем объект lamaCard
                    current_player_index=current_player_index
                )

                player_types = {}
                for player_data in data['players']:
                    name = player_data['name']
                    kind = player_data['kind']
                    kind_class = next((player_type for player_type in all_player_types if player_type.__name__ == kind),
                                      None)
                    player = next(player for player in players if player.name == name)  # Находим объект Player по имени
                    player_types[player] = kind_class

                return cls(player_types=player_types, game_state=game_state)

        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Ошибка загрузки игры: {e}")
            return None

    def save(self):
        filename = 'lama.json'
        data = self.save_to_dict()
        try:
            with open(filename, 'w', encoding='utf-8') as fout:
                json.dump(data, fout, indent=4)
                print(f"Игра успешно сохранена в {filename}")  # Уведомление об успешном сохранении
        except IOError as e:
            print(f"Ошибка при сохранении игры: {e}")

    def save_to_dict(self):
        data = self.game_state.save()
        for player_index, player in enumerate(self.player_types.keys()):
            player_interaction = self.player_types[player]
            data['players'][player_index]['kind'] = player_interaction.__name__
        return data

    @classmethod
    def get_players(cls):
        player_count = cls.request_player_count()

        player_types = {}
        for _ in range(player_count):
            name, kind = cls.request_player()
            player = Player(name, Hand())
            player_types[player] = kind
        return player_types

    @classmethod
    def new_game(cls, player_types: dict):
        deck = Deck(cards=None)
        top = deck.draw_card()
        game_state = GameState(list(player_types.keys()), deck, top)

        # Каждый игрок начинает с INITIAL_HAND_SIZE карт
        for _ in range(cls.INITIAL_HAND_SIZE):
            for player in player_types.keys():
                player.hand.add_card(deck.draw_card())

        server = cls(player_types, game_state)
        server.save()  # Сохраняем игру в файл сразу после создания

        return server

    def declare_winner_phase(self) -> GamePhase:
        print(f"{self.game_state.current_player()} победил!")
        self.save()  # Сохраняем состояние игры перед завершением
        return GamePhase.GAME_END

    def run(self):
        current_phase = GamePhase.CHOOSE_CARD
        while current_phase != GamePhase.GAME_END:
            phases = {
                GamePhase.CHOOSE_CARD: self.choose_card_phase,
                GamePhase.DRAW_EXTRA: self.draw_extra_phase,
                GamePhase.NEXT_PLAYER: self.next_player_phase,
                GamePhase.DECLARE_WINNER: self.declare_winner_phase,
            }
            current_phase = phases[current_phase]()
            self.move_count += 1  # Увеличиваем счетчик ходов

            if self.move_count >= self.MAX_MOVES:  # Проверяем лимит ходов
                print("Достигнут лимит ходов. Игра окончена.")
                return GamePhase.GAME_END
            self.save()

    def next_player_phase(self) -> GamePhase:
        if not self.game_state.current_player().hand.cards:
            return GamePhase.DECLARE_WINNER
        self.game_state.next_player()
        print(f"=== очередь игрока: {self.game_state.current_player()}")
        return GamePhase.CHOOSE_CARD

    def draw_extra_phase(self) -> GamePhase:
        drawn_card = self.game_state.draw_card()

        if drawn_card is None:
            print("Не удалось взять карту, колода пуста.")
            return GamePhase.NEXT_PLAYER

        if drawn_card.can_play_on(self.game_state.top):
            print(f"Игрок {self.game_state.current_player().name} сыграл карту {drawn_card}.")
            self.game_state.top = drawn_card
            return GamePhase.NEXT_PLAYER
        else:
            print("Эту карту нельзя сыграть на верхнюю карту.")
            return GamePhase.NEXT_PLAYER

    def choose_card_phase(self) -> GamePhase:
        current_player = self.game_state.current_player()  # Получаем объект Player
        playable_cards = current_player.hand.playable_cards(self.game_state.top)

        print(
            f"Игрок {current_player.name} с {current_player.hand} может сыграть {playable_cards} поверх {self.game_state.top}"
        )

        if not playable_cards:
            print(f"Игрок {current_player.name} не может сыграть ни одной картой")
            return GamePhase.DRAW_EXTRA

        card = self.player_types[current_player].choose_card(current_player.hand, self.game_state.top)

        if card is None:
            print(f"Игрок {current_player.name} пропустил ход")
            return GamePhase.DRAW_EXTRA

        assert card in playable_cards
        print(f"Игрок {current_player.name} сыграл {card}")
        current_player.hand.remove_card(card)
        self.game_state.top = card
        self.inform_all("inform_card_drawn", current_player)
        return GamePhase.NEXT_PLAYER

    def inform_all(self, method: str, *args, **kwargs):
        for player in self.player_types.values():
            getattr(player, method)(*args, **kwargs)

    @staticmethod
    def request_player_count() -> int:
        while True:
            try:
                player_count = int(input("Сколько игроков?  "))
                if 2 <= player_count <= 10:
                    return player_count
            except ValueError:
                pass
            print("Пожалуйста введите число от 2 до 10")

    @staticmethod
    def request_player() -> (str, PlayerInteraction):
        player_types = [cls.__name__ for cls in all_player_types if
                        inspect.isclass(cls) and issubclass(cls, PlayerInteraction)]

        print(f"Найденные типы игроков: {player_types}")

        player_types_as_str = ', '.join(player_types)

        while True:
            name = input("Введите имя игрока: ")
            if name.isalpha():
                break
            print("Имя должно состоять из букв и быть одним словом.")

        while True:
            print(f"Разрешенные типы: {player_types_as_str}")
            kind = input(f"Выберите тип игрока ({player_types_as_str}): ")
            if kind in player_types:
                kind_class = next(cls for cls in all_player_types if cls.__name__ == kind)
                break
            print(f"Неверный ввод. Пожалуйста, выберите из: {player_types_as_str}")

        return name, kind_class

def __main__():
    load_from_file = True  # Измените на True, чтобы загрузить игру из файла
    if load_from_file:
        server = GameServer.load_game()  # Загружаем игру из файла
        if server is None:
            return  # Завершить, если загрузка не удалась
    else:
        server = GameServer.new_game(GameServer.get_players())  # Запрашиваем игроков для новой игры

    # Запуск игры
    server.run()

if __name__ == "__main__":
    __main__()


