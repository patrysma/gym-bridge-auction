from gym_bridge_auction.envs.game import NAMES, spade, heart, diamond, club
import pygame


class Window:
    """Interfejs graficzny"""

    def __init__(self, north_hands_display=None, east_hands_display=None, south_hands_display=None,
                 west_hands_display=None, who_is_dealer=None):
        """Utworzenie niezmiennych elementów interfejsu graficznego,
        gdzie podane parametry to: ręce poszczególnych graczy oraz nazwa gracza, który jest rozdającym"""

        pygame.init()
        # defincja wymiarów okna i tytułu
        title = 'Bridge auction environment'
        width = 1500
        height = 850
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)
        # odmierzanie czasu w aplikacji
        self.clock = pygame.time.Clock()
        # defincja kolorów
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
        north_player_label = self.font.render(NAMES[0], True, self.colours['blue'])
        self.screen.blit(north_player_label, (650, 150))
        colour_labels = self.create_colours_label()
        self.place_labels(colour_labels, 550, 200)
        east_player_label = self.font.render(NAMES[1], True, self.colours['blue'])
        self.screen.blit(east_player_label, (1150, 350))
        self.place_labels(colour_labels, 1050, 400)
        south_player_label = self.font.render(NAMES[2], True, self.colours['blue'])
        self.screen.blit(south_player_label, (650, 550))
        self.place_labels(colour_labels, 550, 600)
        west_player_label = self.font.render(NAMES[3], True, self.colours['blue'])
        self.screen.blit(west_player_label, (150, 350))
        self.place_labels(colour_labels, 50, 400)
        # etykiety licytacji i wyników
        north_contract_label = self.font.render("NORTH Contract:", True, self.colours['black'])
        self.screen.blit(north_contract_label, (50, 10))
        east_contract_label = self.font.render("EAST Contract:", True, self.colours['black'])
        self.screen.blit(east_contract_label, (50, 60))
        south_contract_label = self.font.render("SOUTH Contract:", True, self.colours['black'])
        self.screen.blit(south_contract_label, (50, 110))
        west_contract_label = self.font.render("WEST Contract:", True, self.colours['black'])
        self.screen.blit(west_contract_label, (50, 160))
        last_contract_label = self.font.render("Last contract:", True, self.colours['black'])
        self.screen.blit(last_contract_label, (1050, 10))
        who_is_dealer_label = self.font.render("DEALER:", True, self.colours['black'])
        self.screen.blit(who_is_dealer_label, (1050, 60))
        win_pair_label = self.font.render("Pair:", True, self.colours['black'])
        self.screen.blit(win_pair_label, (1050, 110))
        pair_score_label = self.font.render("Pair score:", True, self.colours['black'])
        self.screen.blit(pair_score_label, (1050, 160))
        win_pair_label = self.font.render("Optimum score:", True, self.colours['black'])
        self.screen.blit(win_pair_label, (1050, 210))
        # aktualizacja widoku
        pygame.display.update()

        # wartości etykiet zmiennych
        # kto jest rozdającym
        self.who_is_dealer = who_is_dealer
        # wyświetlenie rąk graczy
        self.create_list_of_labels(north_hands_display, 600, 200)
        self.create_list_of_labels(east_hands_display, 1100, 400)
        self.create_list_of_labels(south_hands_display, 600, 600)
        self.create_list_of_labels(west_hands_display, 100, 400)
        pygame.display.update()

    def create_colours_label(self):
        """Utworzenie etykiet dla kolorów kart"""

        spade_label = self.font.render(spade, True, self.colours['black'])
        heart_label = self.font.render(heart, True, self.colours['red'])
        diamond_label = self.font.render(diamond, True, self.colours['orange'])
        club_label = self.font.render(club, True, self.colours['grey'])

        return [spade_label, heart_label, diamond_label, club_label]

    def place_labels(self, labels, x_pos, y_pos):
        """Umieszczenie listy etykiet na ekranie szeregowo,
        gdzie poszczególne parametry to:
        label - lista utworzonych obiektów tekstowych
        x_pos, y_pos - pozycje etykiety na ekranie"""

        for i in range(0, len(labels)):
            self.screen.blit(labels[i], (x_pos, y_pos + 50 * i))

    def create_mutable_labels(self, text, font):
        """Utworzenie etykiety dla tekstu podanego jako parametr,
        gdzie:
        text - zmienna typu tekstowego
        font - obiekt typu Font"""

        text_label = font.render(text, True, self.colours['black'], self.colours['ecru'])

        return text_label

    def create_list_of_labels(self, text, x_pos, y_pos):
        """Utworzenie listy etykiet i ustawienie ich pozycji
        gdzie:
        text - zmienna typu teksowego
        x_pos, y_pos - pozycje etykiety na ekranie"""

        label_list = [self.create_mutable_labels(text[i], self.font) for i in range(0, 4)]
        self.place_labels(label_list, x_pos, y_pos)

    def update_view(self, last_contract, north_contract, east_contract, south_contract, west_contract, win_pair, score,
                    optimum_score, frames_per_second):
        """Aktualizacja zmieniających się etykiet z tekstem, gdzie podane parametry to:
        ostatni najwyższy kontrakt, kontrakty poszczególnych graczy, nazwy par, zapis, optymalny zapis według solvera
        oraz ilość klatek na sekundę"""

        # prostokąty zakrywające poprzednie wartości zmieniającego się tekstu
        pygame.draw.rect(self.screen, self.colours['green'], pygame.Rect(250, 10, 200, 200))
        pygame.draw.rect(self.screen, self.colours['green'], pygame.Rect(1250, 10, 800, 300))
        # wyświetlenie rozdającego
        self.screen.blit(self.create_mutable_labels(self.who_is_dealer, self.font), (1250, 60))
        # wyświetlenie kontraktów oraz punktów
        players_contracts_display = [north_contract, east_contract, south_contract, west_contract]
        self.screen.blit(self.create_mutable_labels(last_contract, self.font), (1250, 10))
        self.screen.blit(self.create_mutable_labels(win_pair[0], self.font), (1250, 110))
        self.screen.blit(self.create_mutable_labels(win_pair[1], self.font), (1350, 110))
        self.screen.blit(self.create_mutable_labels(str(score[0]), self.font), (1250, 160))
        self.screen.blit(self.create_mutable_labels(str(score[1]), self.font), (1350, 160))
        self.screen.blit(self.create_mutable_labels(str(optimum_score[0]), self.font), (1250, 210))
        self.screen.blit(self.create_mutable_labels(str(optimum_score[1]), self.font), (1350, 210))
        self.create_list_of_labels(players_contracts_display, 250, 10)
        # aktualizacja i ustawienie ilości klatek na sekundę
        pygame.display.update()
        self.clock.tick(frames_per_second)
        # obsługa zdarzenia - zakmknięcie okna przyciskiem
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.close_window()
                return

    def close_window(self):
        """Zamknięcie okna i zakończenie pracy programu"""

        pygame.quit()
        quit()
