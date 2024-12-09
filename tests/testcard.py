from main.card import lamaCard
import pytest

def test_init():
    c = lamaCard(3)
    assert c.value == 3

def test_save():
    c = lamaCard(3)
    assert repr(c) == '3'
    assert c.save() == '3'

    c = lamaCard(6)
    assert repr(c) == '6'
    assert c.save() == '6'

def test_eq():
    c1 = lamaCard(3)
    c2 = lamaCard(3)
    c3 = lamaCard(1)
    c4 = lamaCard(2)
    c5 = lamaCard(6)

    assert c1 == c2
    assert c1 != c3
    assert c1 != c4
    assert c1 != c5

def test_load():
    c = lamaCard.load('3')
    assert c == lamaCard(3)

    c = lamaCard.load('6')
    assert c == lamaCard(6)

def test_divzero():
    with pytest.raises(ZeroDivisionError):
        x = 2 / 0

def test_validation():
    with pytest.raises(ValueError):
        lamaCard('3')
    with pytest.raises(ValueError):
        lamaCard(7)  # Проверка на значение больше 6
    with pytest.raises(ValueError):
        lamaCard(-1)  # Проверка на отрицательное значение

def test_play_on():
    c1 = lamaCard.load('1')
    c2 = lamaCard.load('2')
    c3 = lamaCard.load('3')
    c4 = lamaCard.load('4')
    c5 = lamaCard.load('0')

    assert c1.can_play_on(c1)
    assert c2.can_play_on(c1)
    assert c2.can_play_on(c2)
    assert c5.can_play_on(c5)
    assert c1.can_play_on(c5)
    assert not c3.can_play_on(c1)
    assert not c4.can_play_on(c1)
    assert not c3.can_play_on(c5)
    assert not c4.can_play_on(c5)

def test_all_cards():
    cards = lamaCard.all_cards()
    assert len(cards)==56








