from random import shuffle

# Kolory kart w unicode
spade = "\u2660"
heart = "\u2665"
diamond = "\u2666"
club = "\u2663"

# Nazwy poszczególych graczy, w kolejności zegarowej od północy (N - North, E - East, S - South, W -West)
NAMES = ['N', 'E', 'S', 'W']

# Miana odzywki
BIND_SUIT = ['C', 'D', 'H', 'S', 'NT']

# Indeksy graczy tworzących parę
# 0 - N-S (indeksy 0 i 2)
# 1 - E-W (indeksy 1 i 3)
WIN_PAIR = [(0, 2), (1, 3)]


class Contract:
    """Klasa definiująca poszczególne kontrakty licytacji brydżowej -
    {pass, 1C, 1D, 1H, 1S, 1NT, ..., 7C, 7D, 7H, 7S, 7NT, double, redouble}
    gdzie:
    suit - miano odzywki - symbole kolorów, czyli (od najmłodszego): C-Club (trefl), D-Diamond (karo), H-Heart (kier),
    S-Spade (pik), NT-no trump (bez atu) plus doadatkowo zapowiedź "pass", "double", "redouble";
    number - parametr określająca liczbę danej odzywki (liczby od 1 do 7), dla pasu nie przypisuje się żadnej liczby;
    value - parametr określający wyższość danego kontraktu (wartości od 1 do 35), w przypadku pasu przypisano mu
    wartość zero."""

    def __init__(self, suit, number):
        """Konstruktor klasy przypisujący symbol koloru i wartość kontraktu."""

        self.suit = suit
        self.number = number
        self.value = None

    def set_value(self, value):
        """Metoda przypisująca wartość, która określa wyższość danej odzywki podczas licytacji"""

        self.value = value

    def __str__(self):
        """Reprezentacja tekstowa kontraktu"""

        if self.number is None:
            return self.suit
        else:
            return str(self.number) + self.suit


class Card:
    """Klasa definiująca daną kartę do gry,
        gdzie:
        suit - kolor danej karty - jeden z dostępnych czterech {♠, ♥, ♦, ♣} - kolejno od najstarszego:
        pik, kier, karo, trefl;
        rank - numer bądź figura danej karty - jedno z dostępnych (A, K, Q, J, 10, 9, 8, 7, 6, 5, 4, 3, 2) -
        kolejno od najstarszego;
        value - liczba definiująca pozycję karty w hierarchii (liczby od 2 do 14)
        position - pozycja karty w reprezentacji 0/1"""

    def __init__(self, suit, rank):
        """Konstruktor przypisujący kolor, numer/figurę i wartość określającą pozycję karty w hierarchii"""

        self.suit = suit
        self.rank = rank
        # Przypisanie wartości określających hierarchię kart
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

        # Pozycje kart w talii do reprezentacji 0/1
        self.position = self.value - 2
        if suit == club:
            self.position = self.position
        elif suit == diamond:
            self.position = self.position + 13
        elif suit == heart:
            self.position = self.position + (2*13)
        elif suit == spade:
            self.position = self.position + (3*13)

    def __eq__(self, other):
        """"Metoda określająca równość obiektów - wykorzystywana do sortowania kart"""

        return self.value == other.value and self.suit == other.suit

    def __lt__(self, other):
        """Metoda porównywująca obiekty - wykorzystywana do sortowania kart"""

        return self.value > other.value


class Deck:
    """Klasa definiująca talię 52 kart do gry w brydża"""

    def __init__(self):
        """Konstruktor tworzący listę wszystkich kart do gry - 52 obiektów typu Card"""

        rank = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2']  # numery/figury karty
        suites = [spade, heart, diamond, club]  # kolory karty
        self.deck = [Card(i, k) for i in suites for k in rank]

    def shuffle(self):
        """Metoda tasująca talię"""

        shuffle(self.deck)

    def deal(self, n_players):
        """Metoda rozdająca karty do określonej przez parametr n_players liczby graczy"""

        return [self.deck[i::n_players] for i in range(0, n_players)]


def list_to_string(old_list):
    """Funkcja zamieniająca listę w postać napisową"""

    new_list = " "
    return new_list.join(old_list)


class Player:
    """Klasa definiująca gracza w brydżu, który ma swoją nazwę, rękę (karty jakie posiada)"""

    def __init__(self, name, hand):
        """Konstruktor przypisujący graczowi imię (name) i rękę (hand) - dostępne karty oraz incjalizujący
        inne atrybuty klasy"""

        self.name = name
        self.hand = sorted(hand)  # ręka gracza posortowana od najmłodszych dwójek (2) poszczegónych kolorów do asów (A)
        self.hand_splitted = [[] for i in range(0, 4)]  # ręka gracza rozdzielona ze względu kolory kart
        self.win_auction = False  # określenie czy dany gracz wygrał licytację
        self.player_contracts = None  # odzywka danego gracza
        self.makeable_contracts = {}  # maksymalne realizowane kontrakty wyznaczone za pomocą solvera
        self.number_of_trick = {}  # maksymalna liczba wzięty lew wyznaczona za pomocą solvere
        self.max_contract_score = []  # wartość punktowa najbardziej punktowanego kontraktu
        self.hand_representation = self.set_hand_representation() # reprezentacja ręki gracza w formie 0/1

    def split_hand(self):
        """Metoda rodzielająca rękę gracza na poszczegolne kolory kart (od najstarszego do najmłodszego),
         gdzie w pierwszym wierszu są piki, w drugim - kiery, w trzecim - kara, a w czwartym - trefle"""

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
        """Metoda zwracająca napisową postać figur i numerów karty danego koloru,
        gdzie:
        hand - ręka gracza w danym kolorze"""

        cards = [c.rank for c in hand]

        return list_to_string(cards)

    def set_hand_representation(self):
        """Metoda zwracająca reprezentację ręki gracza w formie 0/1
        0 - nie posiada karty
        1 - posiada kartę
        Karty ustawione są od 2 do A kolejno kolorami trefl, karo, kier i na końcu pik"""

        hand_representation = [0 for i in range(0, 52)]

        for hand in self.hand:
            hand_representation[hand.position] = 1

        return hand_representation
