from hand import Hand
from player import Player
from card import lamaCard

def test_init():
    h = Hand.load("1 3 2")
    p = Player(name="Jordan", hand=h, score=10)
    assert p.name == "Jordan"
    assert p.hand == h
    assert p.score == 10

def test_str():
    h = Hand.load("1 3 2")
    p = Player(name="Jordan", hand=h, score=15)
    assert str(p) == "Jordan(15): 1 3 2"

def test_save():
    h = Hand.load("1 3 2")
    p = Player(name="Jordan", hand=h, score=15)
    assert p.save() == {"name": "Jordan", "score": 15, "hand": "1 3 2"}

def test_eq():
    h1 = Hand.load("1 3 2")
    h2 = Hand.load("1 3 2")
    p1 = Player(name="Jordan", hand=h1, score=10)
    p2 = Player(name="Jordan", hand=h2, score=10)
    assert p1 == p2

def test_load():
    data = {"name": "Jordan", "score": 10, "hand": "1 3 2"}
    h = Hand.load("1 3 2")
    p_expected = Player(name="Jordan", hand=h, score=10)
    p = Player.load(data)
    assert p == p_expected

def test_hash():
    h = Hand.load("1 3 2")
    p = Player(name="Jordan", hand=h, score=10)
    assert isinstance(hash(p), int)

def test_hand_modification():
    h = Hand.load("1 3 2")
    p = Player(name="Jordan", hand=h, score=10)
    p.hand.add_card(lamaCard.load("4"))
    assert len(p.hand.cards) == 4
    assert str(p) == "Jordan(10): 1 3 2 4"

def test_hand_score():
    h = Hand.load("1 3 2")
    p = Player(name="Jordan", hand=h, score=10)
    p.hand.add_card(lamaCard.load("Lama"))  # Добавляем карту Лама
    assert p.hand.score() == 16  # Проверяем, что сумма очков в руке равна 16 (3*1 + 10)

def test_llama_card_score():
    lama_card = lamaCard.load("Lama")
    assert lama_card.score() == 10  # Проверяем, что карта Лама дает 10 очков

