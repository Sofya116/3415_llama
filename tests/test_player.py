from main.hand import Hand
from main.player import Player

def test_init():
    h = Hand.load("1 3 2")  # Загружаем руку из строки
    p = Player(name="Tom", hand=h, score=10)  # Создаем игрока
    assert p.name == "Tom"  # Проверяем имя
    assert p.hand == h  # Проверяем руку
    assert p.score == 10  # Проверяем счет

def test_str():
    h = Hand.load("1 3 2")  # Загружаем руку
    p = Player(name="Tom", hand=h, score=15)  # Создаем игрока
    assert str(p) == "Tom(15): 1 3 2"  # Проверяем строковое представление

def test_save():
    h = Hand.load("1 3 2")  # Загружаем руку
    p = Player(name="Tom", hand=h, score=15)  # Создаем игрока
    assert p.save() == {"name": "Tom", "score": 15, "hand": "1 3 2"}  # Проверяем сохранение

def test_eq():
    h1 = Hand.load("1 3 2")  # Загружаем первую руку
    h2 = Hand.load("1 3 2")  # Загружаем вторую руку
    p1 = Player(name="Tom", hand=h1, score=10)  # Создаем первого игрока
    p2 = Player(name="Tom", hand=h2, score=10)  # Создаем второго игрока
    assert p1 == p2  # Проверяем равенство игроков

def test_load():
    data = {"name": "Tom", "score": 10, "hand": "1 3 2"}  # Данные для загрузки
    h = Hand.load("1 3 2")  # Загружаем руку
    p_expected = Player(name="Tom", hand=h, score=10)  # Ожидаемый игрок
    p = Player.load(data)  # Загружаем игрока
    assert p == p_expected  # Проверяем равенство



