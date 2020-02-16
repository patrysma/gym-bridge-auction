from random import shuffle


class Cards:

    def __init__(self):
        spade = "\u2660"
        heart = "\u2665"
        diamond = "\u2666"
        club = "\u2663"
        values = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2']
        suites = [heart, spade, club, diamond]
        self.deck = [[j, i] for j in values for i in suites]  # tworzenie talii

    def shuffle(self):
        shuffle(self.deck)  # tasowanie kart

    def deal(self, n_players):
        return [self.deck[i::n_players] for i in range(0, n_players)]  # rozdanie kart do graczy


class Players:

    def __init__(self):
        self.n_players = 4
        self.names = ['N', 'E', 'S', 'W']
        cards = Cards()
        cards.shuffle()
        self.hands = cards.deal(self.n_players)


players = Players()
print(players.hands)
