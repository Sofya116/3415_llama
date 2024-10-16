from src.card import lamaCard
import pytest
def test_init():
    # тест инициализации карты
    c = lamaCard(3)
    assert c.value == 3

def test_save():
    # тест сохранения карты
    c = lamaCard(3)
    assert repr(c) == '3'
    assert c.save() == '3'

    c = lamaCard(6)
    assert repr(c) == '6'
    assert c.save() == '6'

def test_eq():
    # тест сравнения двух карт
    c1 =lamaCard(3)
    c2 =lamaCard(3)
    c3 =lamaCard(1)
    c4 =lamaCard(2)
    c5 =lamaCard(6)

    assert c1 == c2
    assert c1 != c3
    assert c1 != c4
    assert c1 != c5

def test_load():
    # тест загрузки карты
    s = '3'
    c = lamaCard.load(s)
    assert c == lamaCard(3)

    s = '6'
    c = lamaCard.load(s)
    assert c == lamaCard(6)

def test_divzero():
    # пример теста с ловлей исключения
    with pytest.raises(ZeroDivisionError):
        x = 2 / 0

def test_validation():
    # тест валидации карты
    with pytest.raises(ValueError):
        lamaCard('3')

def test_play_on():
    # тест метода can_play_on
    c1 =lamaCard.load('1')
    c2 =lamaCard.load('2')
    c3 =lamaCard.load('3')
    c4 =lamaCard.load('4')

    assert c1.can_play_on(c1)
    assert c2.can_play_on(c1)
    assert c2.can_play_on(c2)
    assert not c3.can_play_on(c1)
    assert not c4.can_play_on(c1)

def test_all_cards():
    # тест метода all_cards
    cards = lamaCard.all_cards(value=[5, 2, 6])
    expected_cards = [
        lamaCard.load('5'),
        lamaCard.load('2'),
        lamaCard.load('6'),
    ]
    assert cards == expected_cards

def test_score():
    # тест метода score
    c = lamaCard(6)
    assert 6 == c.score()

    c = lamaCard(5)
    assert 5 == c.score()


