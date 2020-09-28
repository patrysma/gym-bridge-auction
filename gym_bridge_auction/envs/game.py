from random import shuffle

# Kolory kart w unicode
spade = "\u2660"
heart = "\u2665"
diamond = "\u2666"
club = "\u2663"

# Nazwy poszczególnych graczy, w kolejności zegarowej od północy (N - North, E - East, S - South, W -West)
NAMES = ['N', 'E', 'S', 'W']

# Miana odzywki
BIND_SUIT = ['C', 'D', 'H', 'S', 'NT']

# Indeksy graczy tworzących parę
# 0 - N-S (indeksy 0 i 2)
# 1 - E-W (indeksy 1 i 3)
WIN_PAIR = [(0, 2), (1, 3)]

# Nazwy par spójne z ich indeksami w WIN_PAIR
PAIR = ['N/S', 'E/W']


class Contract:
    """Definicja odzywek i zapowiedzi podczas licytacji brydżowej -
    {pass, 1C, 1D, 1H, 1S, 1NT, ..., 7C, 7D, 7H, 7S, 7NT, double, redouble}
    gdzie:
    suit - miano odzywki - symbole kolorów, czyli (od najmłodszego): C-Club (trefl), D-Diamond (karo), H-Heart (kier),
    S-Spade (pik), NT-no trump (bez atu) plus doadatkowo zapowiedź "pass", "double", "redouble";
    number - parametr określający liczbę danej odzywki (numery od 1 do 7), dla pasa, kontry, rekontry nie przypisuje się
    żadnej liczby;
    value - parametr określający identyfikator zapowiedzi."""

    def __init__(self, suit, number):
        """Przypisanie symbolu koloru i numeru kontraktu."""

        self.suit = suit
        self.number = number
        self.value = None

    def set_value(self, value):
        """Przypisanie identyfikatora do danej zapowiedzi"""

        self.value = value

    def __str__(self):
        """Reprezentacja tekstowa kontraktu"""

        if self.number is None:
            return self.suit
        else:
            return str(self.number) + self.suit


def create_available_contracts():
    """Utworzenie dostępnych kontraktów podczas licytacji"""

    numbers = [1, 2, 3, 4, 5, 6, 7]
    contracts = [Contract(i, j) for j in numbers for i in BIND_SUIT]
    contracts.reverse()
    contracts.insert(0, Contract('pass', None))
    contracts.append(Contract('double', None))
    contracts.append(Contract('redouble', None))

    for i in range(0, len(contracts)):
        contracts[i].set_value(i)

    return contracts


class Card:
    """Definicja karty do gry,
        gdzie:
        suit - kolor danej karty - jeden z dostępnych - {♠, ♥, ♦, ♣} - kolejno od najstarszego:
        pik, kier, karo, trefl;
        rank - numer bądź figura danej karty - jedno z dostępnych - {A, K, Q, J, 10, 9, 8, 7, 6, 5, 4, 3, 2} -
        kolejno od najstarszego;
        value - liczba definiująca pozycję karty w hierarchii w danym kolorze (liczby od 2 do 14)
        position - pozycja karty w talii wykorzystywana w reprezentacji 0/1 - karty ustawione są od 2 do A kolejno
        kolorami trefl, karo, kier i na końcu pik"""

    def __init__(self, suit, rank):
        """Przypisanie koloru, numeru/figury i wartości określającej pozycję karty w hierarchii w danym kolorze oraz
        w talii"""

        self.suit = suit
        self.rank = rank

        # Przypisanie wartości określających hierarchię kart w danym kolorze
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
            self.position = self.position + (2 * 13)
        elif suit == spade:
            self.position = self.position + (3 * 13)

    def __eq__(self, other):
        """"Określenie równości obiektów - wykorzystywane do sortowania kart"""

        return self.value == other.value and self.suit == other.suit

    def __lt__(self, other):
        """Porównanie dwóch obiektów - wykorzystywane do sortowania kart"""

        return self.value > other.value  # kolejność od A (asów) do 2


class Deck:
    """Definicja talii 52 kart do gry w brydża"""

    def __init__(self):
        """Lista wszystkich kart do gry - 52 obiekty typu Card"""

        rank = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2']  # numery/figury karty
        suites = [spade, heart, diamond, club]  # kolory karty
        self.deck = [Card(i, k) for i in suites for k in rank]

    def shuffle(self):
        """Tasowanie talii"""

        shuffle(self.deck)

    def deal(self, n_players):
        """Rozdanie kart dla określonej przez parametr n_players liczby graczy"""

        return [self.deck[i::n_players] for i in range(0, n_players)]


def list_to_string(old_list):
    """Zamiana listy w postać napisową"""

    new_list = " "
    return new_list.join(old_list)


class Player:
    """Definicja gracza w brydżu, który ma swoją nazwę, rękę (karty jakie posiada), zgłoszoną odzywkę/zapowiedź w danym
    momencie licytacji, maksymalne realizowane kontrakty i liczby możliwych do wzięcia lew przy ustalonym mianie"""

    def __init__(self, name, hand):
        """Przypisanie graczowi nazwy (name) i ręki (hand) - dostępne karty oraz incjalizacja innych pól klasy"""

        self.name = name
        self.hand = sorted(hand)  # ręka gracza posortowana od najstarszych asów (A) poszczegónych kolorów do dwójek (2)
        self.hand_splitted = [[] for _ in range(0, 4)]  # ręka gracza rozdzielona według kolorów kart
        self.win_auction = False  # określenie czy dany gracz wygrał licytację
        self.player_contracts = None  # odzywka/zapowiedź gracza w danym momencie licytacji
        self.makeable_contracts = {}  # maksymalne realizowane kontrakty wyznaczone za pomocą Double Dummy Solver
        self.number_of_tricks = {}  # maksymalna liczba wziętych lew wyznaczona za pomocą Double Dummy Solver
        self.hand_representation = self.set_hand_representation()  # reprezentacja ręki gracza w formie 0/1

    def split_hand(self):
        """Rodzielenie ręki gracza według koloru karty (od najstarszego do najmłodszego),
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
        """Napisowa postać figur lub numerów karty danego koloru,
        gdzie:
        hand - ręka gracza w danym kolorze"""

        cards = [c.rank for c in hand]

        return list_to_string(cards)

    def set_hand_representation(self):
        """Reprezentacja ręki gracza w formie 0/1
        0 - nie posiada karty
        1 - posiada kartę
        Karty ustawione są od 2 do A kolejno kolorami trefl, karo, kier i na końcu pik"""

        hand_representation = [0 for _ in range(0, 52)]

        for card in self.hand:
            hand_representation[card.position] = 1

        return hand_representation
