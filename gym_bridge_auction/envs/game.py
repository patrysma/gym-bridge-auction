from random import shuffle
import random

# Colours of cards definition
spade = "\u2660"
heart = "\u2665"
diamond = "\u2666"
club = "\u2663"

# Players names
NAMES = ['N', 'E', 'S', 'W']

#Type of contracts
CONTRACTS = {}


class Contract:

    def __init__(self, suit, number):
        self.suit = suit
        self.number = number


class Card:

    def __init__(self, suit, rank):
        # Konstruktor tworzący kartę
        self.suit = suit
        self.rank = rank

        if rank == 'A':
            self.value = 14
        elif rank == 'K':
            self.value = 13
        elif rank == 'Q':
            self.value = 12
        elif rank == 'J':
            self.value = 11
        else:
            self.value = int(rank)

    def get(self):
        return [self.rank, self.suit]

    def __eq__(self, other):
        # metoda do sortowania - równość kart
        return self.value == other.value and self.suit == other.suit

    def __lt__(self, other):
        # metoda do sortowania - porównanie kart
        return self.value < other.value


class Deck:

    def __init__(self):  # tworzenie talii
        rank = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2']
        suites = [heart, spade, club, diamond]
        self.deck = [Card(i, k) for i in suites for k in rank]  # tworzenie talii

        # self.deck[0].get()
        # self.deck_order = [c.value for c in self.deck]

    def shuffle(self):
        shuffle(self.deck)  # tasowanie kart

    def deal(self, n_players):  # rozdanie kart
        return [self.deck[i::n_players] for i in range(0, n_players)]  # rozdanie kart do graczy


def list_to_string(old_list):
    new_list = " "
    return new_list.join(old_list)


class Player:
    # przerobić hand w kolorach na listy
    def __init__(self, name, hand):
        self.name = name
        self.hand = sorted(hand)
        self.hand_splitted = [[] for i in range(0, 4)]
        self.is_dealer = False
        self.conctracts = None

    def split_hand(self):
        for j in range(0, 13):
            if self.hand[j].suit == spade:
                self.hand_splitted[0].append(self.hand[j])
            elif self.hand[j].suit == heart:
                self.hand_splitted[1].append(self.hand[j])
            elif self.hand[j].suit == diamond:
                self.hand_splitted[2].append(self.hand[j])
            elif self.hand[j].suit == club:
                self.hand_splitted[3].append(self.hand[j])

    def hand_to_display(self, hand):
        cards = [c.rank for c in hand]

        return list_to_string(cards)


class Game:

    def __init__(self):
        n_players = 4
        cards = Deck()
        cards.shuffle()
        hands = cards.deal(n_players)
        self.players = [Player(NAMES[i], hands[i]) for i in range(0, n_players)]
        self.dealer_name = ''

        for j in range(0, len(self.players)):
            self.players[j].split_hand()
            for i in range(0, 4):
                self.players[j].hand_splitted[i] = self.players[j].hand_to_display(self.players[j].hand_splitted[i])

        self.players_order = []
        self.choose_dealer_and_order()

    def choose_dealer_and_order(self):
        dealer = random.choice(range(len(self.players)))
        self.players[dealer].is_dealer = True
        self.dealer_name = self.players[dealer].name
        self.players_order.append(self.players[dealer])

        if dealer < len(self.players) - 1:
            for i in range(dealer + 1, len(self.players)):
                self.players_order.append(self.players[i])
        if dealer > 0:
            for i in range(0, dealer):
                self.players_order.append(self.players[i])

# selff = Game()

# for i in range(0, 13):
#   print(selff.players[1].hand[i].get())

# print(players.north_player.hand[0].get())
# selff.split_hand()

# print(" ")
# print(selff.players[1].hand_s[0].get())

# c = Cards()
# print(c.deck)
# print(c.deck_order)
# print(c.deck_sorted_order)
