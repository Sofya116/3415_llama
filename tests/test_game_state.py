from card import lamaCard
from deck1 import Deck
from game_state import GameState
from player import Player

# Данные для тестирования, представляющие состояние игры
data = {
    "top": "3",  # Текущая верхняя карта
    "current_player_index": 1,  # Индекс текущего игрока (Bob)
    "deck": "2 6 0",  # Карты в колоде
    "players": [  # Информация об игроках
        {"name": "Alex", "hand": "3 6", "score": 9},
        {"name": "Bob", "hand": "5", "score": 5},
        {"name": "Charley", "hand": "4 1 0", "score": 15},
    ],
}

# Загружаем игроков из данных
alex = Player.load(data["players"][0])
bob = Player.load(data["players"][1])
charley = Player.load(data["players"][2])
full_deck = Deck(None)


def test_init():
    """Тестируем инициализацию состояния игры."""
    players = [alex, bob, charley]
    game = GameState(
        players=players, deck=full_deck, current_player=1, top=lamaCard.load("3")
    )
    assert game.players == players
    assert game.deck == full_deck
    assert game.current_player() == bob
    assert str(game.top) == "3"


def test_current_player():
    """Тестируем получение текущего игрока."""
    players = [alex, bob, charley]
    game = GameState(players=players, deck=full_deck, top=lamaCard.load("3"))
    assert game.current_player() == alex

    game = GameState(
        players=players, deck=full_deck, top=lamaCard.load("3"), current_player=1
    )
    assert game.current_player() == bob

    game = GameState(
        players=players, deck=full_deck, top=lamaCard.load("3"), current_player=2
    )
    assert game.current_player() == charley


def test_eq():
    """Тестируем оператор равенства для состояния игры."""
    players = [alex, bob, charley]
    game1 = GameState(players=players, deck=full_deck, top=lamaCard.load("3"))
    game1_copy = GameState(players=players.copy(), deck=Deck(game1.deck.cards.copy()), top=lamaCard.load("3"))
    game2 = GameState(players=players.copy(), deck=Deck(None), top=lamaCard.load("3"))
    game3 = GameState(players=players, deck=Deck.load("2 6 0"), top=lamaCard.load("3"))
    assert game1 == game1_copy
    assert game1 != game2
    assert game1 != game3


def test_save():
    """Тестируем сохранение состояния игры."""
    players = [alex, bob, charley]
    game = GameState(
        players=players,
        deck=Deck.load(data["deck"]),
        top=lamaCard.load(data["top"]),
        current_player=1,
    )
    assert game.save() == data

def test_load():
    """Тестируем загрузку состояния игры."""
    game = GameState.load(data)
    assert game.save() == data


def test_next_player():
    """Тестируем переход к следующему игроку."""
    game = GameState.load(data)
    assert game.current_player() == bob

    game.next_player()
    assert game.current_player() == charley

    game.next_player()
    assert game.current_player() == alex

    game.next_player()
    assert game.current_player() == bob



def test_draw_card():
    """Тестируем функцию взятия карты из колоды."""
    game = GameState.load(data)
    assert game.deck == "2 6 0"
    assert game.current_player().hand == "5"

    game.draw_card()
    assert game.deck == "2 6"
    assert game.current_player().hand == "5 0"


def test_play_card():
    """Тестируем функцию игры картой."""
    players = [alex, bob, charley]
    game = GameState(
        players=players, deck=full_deck, top=lamaCard.load("3"), current_player=2
    )

    assert game.current_player().hand == "4 1 0"
    assert game.top == "3"

    game.play_card(lamaCard.load("1"))
    assert game.current_player().hand == "4 0"
    assert game.top == "1"
