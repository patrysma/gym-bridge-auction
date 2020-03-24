from gym import error
from gym_bridge_auction.envs.game import *

try:
    import pygame
    from pygame.locals import *
except ImportError as e:
    raise error.DependencyNotInstalled("{}. (install pygame using `pip install pygame`".format(e))


class Window:
    """Klasa określająca interfejs graficzny"""

    def __init__(self, north_hands_display=None, east_hands_display=None, south_hands_display=None,
                 west_hands_display=None, who_is_dealer=None):
        """Konstrukctor klasy - utworzenie niezmiennych elementów interfejsu graficznego,
           gdzie podane parametry to: ręce poszczególnych graczy oraz nazwę gracza, który jest rozdającym
           - zmienne typu str"""

        # inicjalizacja PyGame
        pygame.init()
        # defincja wymiarów okna i tytułu
        title = 'Bridge auction environment'
        width = 1500
        height = 850
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        # odmierzanie czasu w aplikacji
        self.clock = pygame.time.Clock()
        # defincja kolorów interfejsu
        self.colours = {'green': (60, 120, 70),
                        'red': (255, 0, 0),
                        'orange': (199, 60, 7),
                        'black': (0, 0, 0),
                        'ecru': (245, 245, 220),
                        'blue': (0, 0, 128),
                        'grey': (54, 54, 69)}
        # ustawienie koloru tła
        self.screen.fill(self.colours['green'])

        # incjalizacja i utworzenie obiektu Font
        default_font = pygame.font.match_font('dejavusansmono')
        self.font = pygame.font.Font(default_font, 20)
        # prostokątne ramki oddzielające miejsce poszczególnych graczy na ekranie
        pygame.draw.rect(self.screen, self.colours['blue'], pygame.Rect(540, 140, 400, 250), 1)
        pygame.draw.rect(self.screen, self.colours['blue'], pygame.Rect(1040, 340, 400, 250), 1)
        pygame.draw.rect(self.screen, self.colours['blue'], pygame.Rect(540, 540, 400, 250), 1)
        pygame.draw.rect(self.screen, self.colours['blue'], pygame.Rect(40, 340, 400, 250), 1)
        # utworzenie etykiety i umiejscowienie na ekranie
        # etykiety poszczególnych graczy
        north_player_label = self.font.render(NAMES[0], 1, self.colours['blue'])
        self.screen.blit(north_player_label, (650, 150))
        colour_labels = self.create_colours_label()
        self.place_labels(colour_labels, 550, 200)
        east_player_label = self.font.render(NAMES[1], 1, self.colours['blue'])
        self.screen.blit(east_player_label, (1150, 350))
        self.place_labels(colour_labels, 1050, 400)
        south_player_label = self.font.render(NAMES[2], 1, self.colours['blue'])
        self.screen.blit(south_player_label, (650, 550))
        self.place_labels(colour_labels, 550, 600)
        west_player_label = self.font.render(NAMES[3], 1, self.colours['blue'])
        self.screen.blit(west_player_label, (150, 350))
        self.place_labels(colour_labels, 50, 400)
        # etykiety licytacji i wyników
        north_contract_label = self.font.render("NORTH Contract:", 1, self.colours['black'])
        self.screen.blit(north_contract_label, (10, 10))
        east_contract_label = self.font.render("EAST Contract:", 1, self.colours['black'])
        self.screen.blit(east_contract_label, (10, 60))
        south_contract_label = self.font.render("SOUTH Contract:", 1, self.colours['black'])
        self.screen.blit(south_contract_label, (10, 110))
        west_contract_label = self.font.render("WEST Contract:", 1, self.colours['black'])
        self.screen.blit(west_contract_label, (10, 160))
        last_contract_label = self.font.render("Last contract:", 1, self.colours['black'])
        self.screen.blit(last_contract_label, (1000, 10))
        who_is_dealer_label = self.font.render("DEALER:", 1, self.colours['black'])
        self.screen.blit(who_is_dealer_label, (1000, 60))
        # aktualizacja widoku
        pygame.display.update()

        # wartości etykiet zmiennych
        # ręka poszczególnych graczy
        self.west_hands_display = west_hands_display
        self.south_hands_display = south_hands_display
        self.east_hands_display = east_hands_display
        self.north_hands_display = north_hands_display
        # wartości kontraktów i kto jest rozdającym
        self.players_contracts_display = None
        self.who_is_dealer = who_is_dealer
        self.last_contract_display = None
        # wyświetlenie rąk graczy
        self.create_list_of_labels(self.north_hands_display, 600, 200)
        self.create_list_of_labels(self.east_hands_display, 1100, 400)
        self.create_list_of_labels(self.south_hands_display, 600, 600)
        self.create_list_of_labels(self.west_hands_display, 100, 400)
        pygame.display.update()

    def create_colours_label(self):
        """Metoda tworząca etykiety poszczególnych kolorów kart"""

        spade_label = self.font.render(spade, 1, self.colours['black'])
        heart_label = self.font.render(heart, 1, self.colours['red'])
        diamond_label = self.font.render(diamond, 1, self.colours['orange'])
        club_label = self.font.render(club, 1, self.colours['grey'])

        return [spade_label, heart_label, diamond_label, club_label]

    def place_labels(self, labels, x_pos, y_pos):
        """Metoda umieszczająca listę etykiet na ekranie szeregowo,
           gdzie poszczególne pratametry to:
           -label - lista utworzonych obiektów tekstowych
           -x_pos, y_pos - pozycje etykiety na ekranie"""

        for i in range(0, len(labels)):
            self.screen.blit(labels[i], (x_pos, y_pos + 50 * i))

    def create_mutable_labels(self, text, font):
        """Metoda tworząca etykiety dla tekstu podanego jako parametru,
           gdzie:
           text - zmienna typu tekstowego
           font - obiekt typu Font"""

        text_label = font.render(text, 1, self.colours['black'], self.colours['ecru'])

        return text_label

    def create_list_of_labels(self, text, x_pos, y_pos):
        """Metoda tworząca listę etykiet i ustawiająca ich poszczególne pozycje
           gdzie:
           text - zmienna typu teksowego
           -x_pos, y_pos - pozycje etykiety na ekranie"""

        label_list = [self.create_mutable_labels(text[i], self.font) for i in range(0, 4)]
        self.place_labels(label_list, x_pos, y_pos)

    def update_view(self, last_contract, north_contract, east_contract, south_contract, west_contract,
                    frames_per_second):
        """Metoda aktualizująca zmieniające się etykiety z tekstem
           gdzie podane parametry to: ostatni najwyższy kontrakt i kontrakty poszczególnych graczy - zmienne typu str
           oraz ilość klatek na sekundę"""

        # prostokąty zakrywające poprzednie wartości zmieniającego się tekstu
        pygame.draw.rect(self.screen, self.colours['green'], pygame.Rect(210, 10, 300, 200))
        pygame.draw.rect(self.screen, self.colours['green'], pygame.Rect(1200, 10, 300, 50))
        # wyświetlenie rozdającego
        self.screen.blit(self.create_mutable_labels(self.who_is_dealer, self.font), (1200, 60))
        # wyświetlenie kontraktów
        self.players_contracts_display = [north_contract, east_contract, south_contract, west_contract]
        self.last_contract_display = last_contract
        self.screen.blit(self.create_mutable_labels(self.last_contract_display, self.font), (1200, 10))
        self.create_list_of_labels(self.players_contracts_display, 210, 10)
        # aktualizacja i ustawienie ilości klatek na sekundę
        pygame.display.update()
        self.clock.tick(frames_per_second)
        # obsługa zdarzenia - zakmknięcie okna przyciskiem
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close_window()
                return

    def close_window(self):
        """Metoda zamykająca okno i kończąca program"""
        pygame.quit()
        quit()
