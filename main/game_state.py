from main.player import Player  # Импортируйте класс Player
from main.deck import Deck  # Импортируйте класс Deck
from main.card import lamaCard  # Импортируйте класс LlamaCard

class GameState:
    def __init__(self, players, deck, top, current_player_index=0):
        self.players = players  # Список объектов Player
        self.deck = deck
        self.top = top
        self.current_player_index = current_player_index

    def current_player(self):
        return self.players[self.current_player_index]

    def next_player(self):
        self.current_player_index = (self.current_player_index + 1) % len(self.players)

    def __eq__(self, other):
        if self.players != other.players:
            return False
        if self.deck != other.deck:
            return False
        if self.top != other.top:
            return False
        if self.current_player_index != other.current_player_index:
            return False
        return True

    def save(self) -> dict:
        return {
            "top": str(self.top),
            "deck": str(self.deck),
            "current_player_index": self.current_player_index,
            "players": [p.save() for p in self.players],
        }

    @classmethod
    def load(cls, data: dict):
        players = [Player.load(d) for d in data["players"]]
        return cls(
            players=players,
            deck=Deck.load(data["deck"]),
            top=lamaCard.load(data["top"]),
            current_player_index=int(data["current_player_index"]),
        )



    def draw_card(self) -> lamaCard:
        if not self.deck.cards:
            print("Колода пуста, нельзя взять карту.")
            return None
        card = self.deck.draw_card()
        self.current_player().hand.add_card(card)
        return card

    def play_card(self, card: lamaCard):
        self.current_player().hand.remove_card(card)
        self.top = card

    def deal_cards(self, num_cards: int = 6):
        for _ in range(num_cards):
            for player in self.players:
                if self.deck.cards:
                    player.hand.add_card(self.deck.draw_card())

    def start_game(self):
        self.deck.shuffle()
        self.deal_cards()
        self.top = self.deck.draw_card()
        print(f"Начальная карта: {self.top}")

    def end_round(self):
        scores = {player.name: player.calculate_score() for player in self.players}
        print("Конец раунда. Подсчет очков:")
        for name, score in scores.items():
            print(f"{name}: {score} очков")
        for player in self.players:
            player.hand.clear()

    def is_round_over(self) -> bool:
        return any(len(player.hand.cards) == 0 for player in self.players)

    def player_action(self):
        current = self.current_player()
        print(f"{current.name}: {current.hand}")

        while True:
            action = input(f"{current.name}, выберите действие (играть/взять/выйти): ").strip().lower()
            if action == "играть":
                card_value = input("Введите значение карты, которую хотите сыграть: ")
                try:
                    card = lamaCard(int(card_value))
                    if card in current.hand.cards:
                        if card.can_play_on(self.top):
                            self.play_card(card)
                            print(f"{current.name} играет {card}")
                            break
                        else:
                            print("Эту карту нельзя сыграть на верхнюю карту.")
                            # Обработка пропуска хода
                            self.skip_turn(current)
                            break
                    else:
                        print("Такой карты нет в руке.")
                except ValueError:
                    print("Недопустимое значение карты.")
            elif action == "взять":
                drawn_card = self.draw_card()
                if drawn_card is not None:
                    print(f"{current.name} берет карту: {drawn_card}")
                else:
                    print(f"{current.name} не может взять карту, так как колода пуста.")
                break
            elif action == "выйти":
                current.hand.clear()
                print(f"{current.name} выходит из раунда.")
                break
            else:
                print("Неверное действие. Попробуйте снова.")

    def play_game(self):
        self.start_game()
        while True:
            self.player_action()
            if self.is_round_over():
                self.end_round()
                break
            self.next_player()



