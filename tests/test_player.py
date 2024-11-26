from hand import Hand
from player import Player
from card import lamaCard

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
    assert p.save() == {"name": "Jordan", "score": 15, "hand": h.save()}  # Проверяем сохранение

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

def test_hash():
    h = Hand.load("1 3 2")  # Загружаем руку
    p = Player(name="Tom", hand=h, score=10)  # Создаем игрока
    assert isinstance(hash(p), int)  # Проверяем, что хэш - это целое число

def test_hand_modification():
    h = Hand.load("1 3 2")  # Загружаем руку
    p = Player(name="Tom", hand=h, score=10)  # Создаем игрока
    p.hand.add_card(lamaCard.load("4"))  # Добавляем карту
    assert len(p.hand.cards) == 4  # Проверяем количество карт в руке
    assert str(p) == "Tom(10): 1 3 2 4"  # Проверяем строковое представление

def test_hand_score():
    h = Hand.load("1 3 2")  # Загружаем руку
    p = Player(name="Tom", hand=h, score=10)  # Создаем игрока
    p.hand.add_card(lamaCard.load("Lama"))  # Добавляем карту Лама
    assert p.hand.score() == 16  # Проверяем, что сумма очков в руке равна 16 (3*1 + 10)

def test_llama_card_score():
    lama_card = lamaCard.load("Lama")  # Загружаем карту Лама
    assert lama_card.score() == 10  # Проверяем, что карта Лама дает 10 очков

