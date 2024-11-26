import inspect
import json
import sys
from pathlib import Path

from deck1 import Deck
from game_state import GameState
from hand import Hand
from player import Player
from player_interaction import PlayerInteraction
import player_interactions as all_player_types
from player_interactions.humanGUI_player import AWAITING_INTERACTION
from ui.event import post_event, CustomEvent

import logging

import enum

from player_interactions import Bot


class GamePhase(enum.StrEnum):
    CHOOSE_CARD = "Выбор карты"
    DRAW_EXTRA = "Вытягивание дополнительной карты"
    CHOOSE_CARD_AGAIN = "Повторный выбор карты"
    NEXT_PLAYER = "Переключение на следующего игрока"
    DECLARE_WINNER = "Объявление победителя"
    GAME_END = "Окончание игры"


class GameServer:
    INITIAL_HAND_SIZE = 6

    def __init__(self, player_types, game_state):
        self.game_state: GameState = game_state
        self.player_types: dict = player_types
        self.current_phase = GamePhase.CHOOSE_CARD

    @classmethod
    def load_game(cls, filename: str | Path):
        with open(filename, 'r') as fin:
            data = json.load(fin)
            game_state = GameState.load(data)
            print(game_state.save())
            player_types = {}
            for player, player_data in zip(game_state.players, data['players']):
                kind = player_data['kind']
                kind = getattr(all_player_types, kind)
                player_types[player] = kind
            return GameServer(player_types=player_types, game_state=game_state)

    def save(self, filename: str | Path):
        data = self.save_to_dict()
        with open(filename, 'w') as fout:
            json.dump(data, fout, indent=4)

    def save_to_dict(self):
        data = self.game_state.save()
        for player_index, player in enumerate(self.player_types.keys()):
            player_interaction = self.player_types[player]
            data['players'][player_index]['kind'] = self.player_types[player].__name__
        return data

    @classmethod
    def get_players(cls):
        player_count = cls.request_player_count()
        player_types = {}
        for p in range(player_count):
            name, kind = cls.request_player()
            player = Player(name, Hand())
            player_types[player] = kind
        return player_types

    @classmethod
    def new_game(cls, player_types: dict):
        deck = Deck(cards=None)
        top = deck.draw_card()
        game_state = GameState(list(player_types.keys()), deck, top)

        for _ in range(cls.INITIAL_HAND_SIZE):
            for p in player_types.keys():
                p.hand.add_card(deck.draw_card())

        print(game_state.save())

        res = cls(player_types, game_state)
        return res

    def run(self):
        while self.current_phase != GamePhase.GAME_END:
            self.run_one_step()

    def run_one_step(self):
            phases = {
                GamePhase.CHOOSE_CARD: self.choose_card_phase,
                GamePhase.CHOOSE_CARD_AGAIN: self.choose_card_again_phase,
                GamePhase.DRAW_EXTRA: self.draw_extra_phase,
                GamePhase.NEXT_PLAYER: self.next_player_phase,
                GamePhase.DECLARE_WINNER: self.declare_winner_phase,
            }
            self.current_phase = phases[self.current_phase]()

    def declare_winner_phase(self) -> GamePhase:
        print(f"{self.game_state.current_player()} победитель !")
        post_event(CustomEvent.DECLARE_WINNER, player_index=self.game_state.current_player_index)
        # return GamePhase.GAME_END
        return GamePhase.DECLARE_WINNER

    def next_player_phase(self) -> GamePhase:
        if not self.game_state.current_player().hand.cards:
            return GamePhase.DECLARE_WINNER
        self.game_state.next_player()
        print(f"Очередь - {self.game_state.current_player()}")
        return GamePhase.CHOOSE_CARD

    def draw_extra_phase(self) -> GamePhase:
        current_player = self.game_state.current_player()
        card = self.game_state.draw_card()
        print(f"Игрок {current_player} тянет {card}")
        self.inform_all("inform_card_drawn", current_player)
        post_event(CustomEvent.DRAW_CARD, card=card, player_index=self.game_state.current_player_index)
        return GamePhase.CHOOSE_CARD_AGAIN

    def choose_card_again_phase(self) -> GamePhase:
        current_player = self.game_state.current_player()
        playable_cards = current_player.hand.playable_cards(self.game_state.top)
        if playable_cards:
            # играть может только вновь взятая карта, остальные не подходят
            card = playable_cards[0]
            print(f"Игрок {current_player} может сыграть вытянутую карту")
            if self.player_types[current_player].choose_to_play(
                self.game_state.top, card
            ):
                print(f"Игрок {current_player.name} сыграл {card}")
                current_player.hand.remove_card(card)
                self.game_state.top = card
                self.inform_all("inform_card_played", current_player, card)
                post_event(CustomEvent.PLAY_CARD, card=card, player_index=self.game_state.current_player_index)
            else:
                print(f"Игрок решил не играть картой: {card}")

        return GamePhase.NEXT_PLAYER

    def choose_card_phase(self) -> GamePhase:
        current_player = self.game_state.current_player()
        playable_cards = current_player.hand.playable_cards(self.game_state.top)

        print(
            f"Игрок {current_player.name} с {current_player.hand} может сыграть {playable_cards} поверх {self.game_state.top}"
        )

        if not playable_cards:
            print(f"Игрок {current_player.name} не может сыграть ни одной картой")
            return GamePhase.DRAW_EXTRA

        card = self.player_types[current_player].choose_card(
            current_player.hand, self.game_state.top
        )

        if card is None:
            print(f"Игрок {current_player.name} пропустил ход")
            return GamePhase.DRAW_EXTRA

        if type(card) == AWAITING_INTERACTION:
            return GamePhase.CHOOSE_CARD

        assert card in playable_cards
        print(f"Игрок {current_player.name} сыграл {card}")
        current_player.hand.remove_card(card)
        self.game_state.top = card
        self.inform_all("inform_card_drawn", current_player)
        post_event(CustomEvent.PLAY_CARD, card=card, player_index=self.game_state.current_player_index)
        return GamePhase.NEXT_PLAYER

    def inform_all(self, method: str, *args, **kwargs):
        for p in self.player_types.values():
            getattr(p, method)(*args, **kwargs)

    @staticmethod
    def request_player_count() -> int:
        while True:
            try:
                player_count = int(input("Сколько игроков?"))
                if 2 <= player_count <= 10:
                    return player_count
            except ValueError:
                pass
            print("Пожалуйста введите номер от 2 до 10")

    @staticmethod
    def request_player() -> (str, PlayerInteraction):
        """Возвращает имя и тип игрока."""

        """Разрешенные типы игроков из PlayerInteraction."""
        player_types = []
        for name, cls in inspect.getmembers(all_player_types):
            if inspect.isclass(cls) and issubclass(cls, PlayerInteraction):
                player_types.append(cls.__name__)
        player_types_as_str = ', '.join(player_types)

        while True:
            name = input("Введите имя игрока?")
            if name.isalpha():
                break
            print("Имя должно быть одним словом, состоящим только из букв")

        while True:
            try:
                kind = input(f"Выберите тип игрока ({player_types_as_str})")
                kind = getattr(all_player_types, kind)
                break
            except AttributeError:
                print(f"Допустимые типы игроков: {player_types_as_str}")
        return name, kind

    def check_data_for_gui(self):
        ptypes = self.player_types
        if len(ptypes) != 2:
            raise ValueError(f'Игроков должно быть 2, по факту {len(ptypes)}')
        human_counter = 0
        for player, player_type in ptypes.items():
            if player_type != Bot:
                human_counter += 1
        if human_counter > 1:
            raise ValueError(f'Может быть не больше 1 интерактивного игрока, остальные - боты.')



def __main__():
    load_from_file = False
    if load_from_file:
        server = GameServer.load_game('lama.json')
    else:
        server = GameServer.new_game(GameServer.get_players())
    server.save('lama.json')
    server.run()


if __name__ == "__main__":
    __main__()
