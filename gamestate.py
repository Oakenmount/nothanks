import numpy as np


class Player:
    def __init__(self, id: int):
        self.id = id
        self.chips = 11
        self.cards = []

    def take(self, card: int, chips: int):
        self.chips += chips
        self.cards.append(card)

    def can_skip(self):
        return self.chips > 0

    def skip(self):
        self.chips -= 1

    def score(self):
        return sum(self.cards) - self.chips


class GameState:
    def __init__(self, num_players: int = 4):
        # Generate a deck of cards with numbers 3-35, shuffle and remove 9 random cards
        self.deck = np.arange(3, 35 + 1, dtype=np.uint8)
        np.random.shuffle(self.deck)
        self.deck = self.deck[:-9]
        self.players = [Player(i) for i in range(num_players)]
        self.current_turn = 0
        self.current_card = 0
        self.chips = 0

    def end_turn(self):
        self.current_turn = (self.current_turn + 1) % len(self.players)

    def take_card(self):
        card = self.deck[self.current_card]
        player = self.players[self.current_turn]
        # noinspection PyTypeChecker
        player.take(card, self.chips)
        self.chips = 0
        self.current_card += 1
        self.end_turn()

    def skip_card(self):
        player = self.players[self.current_turn]
        player.skip()
        self.chips += 1
        self.end_turn()

    def is_over(self) -> bool:
        return self.current_card >= len(self.deck)

    def get_player(self) -> Player:
        return self.players[self.current_turn]

    def get_card(self) -> int:
        # noinspection PyTypeChecker
        return self.deck[self.current_card]

    def get_chips(self) -> int:
        return self.chips
