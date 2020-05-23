import random
import time
import numpy as np
import gym
from gym import error
from gym import spaces
from gym_bridge_auction.envs.solver_results import *
from gym_bridge_auction.envs.dynamic_space import Dynamic
from gym_bridge_auction.envs.render import Window


class AuctionEnv(gym.Env):
    """Środowisko wieloagentowe (czterech graczy) symulujące licytację brydżową. 
    Jest to przykład środowiska, gdzie poszczególni agenci nie dysponują pełnym zestawem informacji na temat stanu gry.
    Mają dostęp tylko do historii licytacji oraz własnych kart, ręce przeciwników nie są znane.
    
    Agenci w ustalonej kolejności zegarowej (rozpoczyna rozdający) wykonują pojedyńcze akcje (licytują) wybierane z dostępnej 
    przestrzeni. Działania graczy są wartościowane za pomocą nagrody oceniającej skuteczność licytacji. W każdym kroku zwracana 
    jest różnica od przypadku idealnego. Definiując funkcję nagrody wspomagano się dostępnymi narzędziami, czyli Double
    Dummy Solver. Cel każdego z epizodów to ustalenie kontraktu, który stanowi zobowiązanie do wzięcia określonej liczby lew 
    przez parę wygrywającą licytację.
    
    Przestrzeń akcji:
        Typ: Dynamic(38) - przestrzeń dziedzicząca po Discrete
        
        | Liczba | Działanie |
        | 0 | pass |
        | 1 | 7NT |
        | 2 |  7S |
        | 3 | 7H |
        | 4 | 7D |
        | 5 | 7C |
        | . | . |
        | . | . |
        | 31 | 1NT |
        | 32 | 1S |
        | 33 | 1H |
        | 34 | 1D |
        | 35 | 1C |
        | 36 | double |
        | 37 | redouble |
        
        Typ Dynamic to specjalnie zdefiniowana klasa, dziedzicząca po Discrete, zapewnająca zmieniającą się przestrzeń akcji
        w kolejnych krokach licytacji. Zawiera ona w danym momencie tylko takie odzywki lub zapowiedzi (kontra, rekontra, pas),
        które może zgłosić gracz podczas licytacji, według zasad brydża. W każdym etapie na przestrzeń akcji składają się: odzywki
        wyższe w hierarchi od ostatniej zgłoszonej, zapowiedź pas oraz kontra (dostępna dla przeciwników pary, która zgłosiła ostatnią 
        odzywkę) i rekontra (dostępna dla pary z najwyższą obecnie zgłoszoną odzywką po kontrze przeciwników). Na początku licytacji
        dostępne są wszystkie odzywki i zapowiedź pas.
        
        Przestrzeń obserwacji:
            Typ: Dict - zawierający stany: 'whose turn', 'whose next turn', 'LAST_contract', 'Player_contract', 'winning_pair',
            'double/redouble', 'Players hand', 'pair score/optimum score'.
            
            Stan 'whose turn' - oznacza który z graczy licytował w danym kroku:
                Typ: Discrete(4)
                
                | Liczba | Nazwa gracza |
                | 0 | N |
                | 1 | E |
                | 2 | S |
                | 3 | W |
                
            Stan 'whose next turn' - oznacza gracza, który ma licytować następny w kolejności:
                Typ: Discrete(4)
                
                 Oznaczenia liczb zgodne ze stanem 'whose turn'.
                 
            Stan 'LAST_contract' -  oznacza najwyższy zgłoszony kontrakt po każdym z kroków, a po zakończeniu kontrakt ostateczny:
                Typ: Discrete(36)
                
                Oznaczenia liczb są zgodne z tymi przyjętymi w przestrzeni akcji (oprócz wartości 36 i 37, które w tym przypadku
                nie występują).
                
            Stan 'Player_contract' - oznacza odzywkę/zapowiedź gracza licytującego w danym kroku:
                Typ: Discrete(38)
                
                Oznaczenia liczb są zgodne z tymi przyjętymi w przestrzeni akcji.
            
            Stan 'winning_pair' -  oznacza, która z par graczy ma w danym kroku najwyższy zgłoszony kontrakt 
            (aktualnie wygrywa licytację):
                Typ: Discrete(2)
                
                | Liczba | Nazwa pary |
                | 0 | N/S |
                | 1 | E/W |
                
            Stan 'double/redouble' - oznacza czy wystąpiła kontra, rekontra lub żadne z nich:
                Typ: Discrete(3)
                
                | Liczba | Obserwacja |
                | 0 | no double/redouble |
                | 1 | double - 'X' |
                | 2 | redouble - 'XX' |
                            
            Stan 'Players hand' - oznacza reprezentację rąk graczy w formie 0/1:
                Typ: Tuple(MultiDiscrete, MultiDiscrete, MultiDiscrete, MultiDiscrete)
                
                Kolejność rąk graczy jest następująca: N, E, S, W.
                
                Reprezentacja ręki danego gracza jest w formie listy 52-elementowej. Każdy jej element to jedna z cyfr:
                0 (nie posiada karty), 1 (posiada kartę).
                
                Karty ustawione są od 2 do A kolejno kolorami trefl, karo, kier i na końcu pik:
                [2♣, ..., A♣, 2♦, ..., A♦, 2♥, ..., A♥, 2♠, ..., A♠]

            Stan 'pair score/optimum score' - oznacza zapis brydżowy w danym momencie licytacji oraz optymalną wartość punktów 
            według Double Dummy Solver dla każdej z par:
                Typ: Box(4,), typ danych: int
                
                | Liczba | Obserwacja | Min | Max |
                | 0 | Zapis pary N-S | -7000 | 7000 |
                | 1 | Zapis pary E-W | -7000 | 7000 |
                | 2 | Optymalne punkty pary N-S | -7000 | 7000 |
                | 3 | Optymalne punkty pary E-W | -7000 | 7000 |
                        
        Nagroda:
            W każdym kroku wyznaczona jest nagroda wartościująca działania agentów.
            
            Postać: Lista 2-elementowa, gdzie elementy to liczby całkowite z zakresu od -9280 do 9280.
            
            | Indeks | Nazwa pary |
            | 0 | N/S |
            | 1 | E/W |
            
            Nagroda to różnica pomiędzy otrzymanym zapisem brydżowym pary wygrywającej licytację a optymalną dla niej wartością 
            punktową (wynik z Double Dummy Solver), gdy wszyscy gracze licytują idealnie. Zapis brydżowy jest wyznaczony na podstawie 
            zgłoszonego kontraktu i rezultatów z Double Dummy Solver dotyczących realizowalności obowiązującego zobowiązania, co do
            ilości lew jakie może wziać dana para przy ustalonym kolorze atutowym.
            
            Nagroda dla pary, która przegrywa licytację jest wartością przeciwną nagrody pary wygrywającej.
            
        Stan początkowy środowiska:
            Po zresetowaniu środowiska do stanu początkowego ustalone zostają następujące stany przestrzeni obserwacji:
            - 'Players hand' - reprezentacja rąk graczy w formie 0/1 jest dostępna tylko po użyciu funkcji reset(),
            podczas kolejnych kroków epizodu przestaje być dostępna (należy ją od razu przypisać do innej zmiennej)
            - 'pair score/optimum score' - tylko optymalne wartości puntowe dla par, zapis pozostaje nieustalony
            - 'whose next turn' - indeks rozdającego, który rozpoczyna licytację
            Pozostałe stany przestrzeni obserwacji pozostają niedefiniowane (wartość None).
            
            Przestrzeń akcji zostaje przywrócona do początkowej ilości elementów - wszystkie odzywki plus zapowiedź pas 
            (brak możliwości kontry lub rekontry).
            
        Koniec epizodu (licytacji):
            Licytacja, czyli jeden epizod kończy się w następujących przypadkach:
            - wystąpienie kolejno trzech pasów po ustalonym kontrakcie,
            - nie ustalono kontraktu - na początku licytacji wszyscy gracze spasowali,
            - ostateczny kontrakt to 7NT, a po tym nastąpiła kontra i rekontra,
            - zbyt mała liczba iteracji (kroków) w danym epizodzie nie pozwalająca na zakończenie licytacji 
            według powyższych trzech powodów."""

    metadata = {'render.modes': ['human', 'console'], 'video.frames_per_second': 1}

    def __init__(self):

        self._win = None  # instancja interfejsu graficznego
        self._n_players = 4  # liczba graczy
        self._deck = Deck()  # utworzenie talii
        self._dealer_name = ''  # nazwa gracza, który jest rozdającym
        self._players_order = []  # lista graczy ustawionych w odpowiedniej kolejności licytowania
        self._index_order = None  # indeks aktualnie licytującego gracza (według listy self._players_order)
        self._deck.shuffle()  # tasowanie talii
        hands = self._deck.deal(self._n_players)  # rozdanie kart dla graczy
        self._players = [Player(NAMES[i], hands[i]) for i in range(0, self._n_players)]  # utworzenie listy graczy

        # rozdzielenie rąk graczy ze względu na kolor karty (w każdym wierszu figury/numery w danym kolorze)
        for j in range(0, len(self._players)):
            self._players[j].split_hand()
            for i in range(0, 4):
                self._players[j].hand_splitted[i] = self._players[j].hand_to_display(self._players[j].hand_splitted[i])

        self._choose_dealer_and_order()  # wybór rozdającego i ustalenie kolejności licytacji

        # utworzenie dostępnych kontraktów (lista obiektów typu Contract)
        self._available_contracts = create_available_contracts()

        self._optimum_contract_score = [None, None]  # optymalne punkty dla par według solvera
        self._insert_solver_results()  # wstawienie wyników z solvera dla poszczególnych graczy

        self._viewer = None  # zmienna pomocnicza do renderowania
        self._last_contract = None  # najwyższy zgłoszony kontrakt w danym momencie licytacji
        self._first_bind_pass = False  # czy pierwsza odzywka była pasem
        self._double = False  # czy była kontra
        self._redouble = False  # czy była rekontra
        self._pass_number = 0  # licznik zgłoszonych pasów kolejno
        self._score = [0, 0]  # zapis dla par w danym momencie licytacji
        # maksymalna odzywka według solvera dla gracza zgłaszającego najwyższy kontrakt w danym momencie licytacji
        self._max_contract = None
        # liczba lew według solvera jaką może wziąć gracz zgłaszający najwyższy kontrakt w danym momencie licytacji
        self._max_number_of_tricks = None
        self._reward = [None, None]  # nagroda dla par

        self.reward_range = (-9280, 9280)  # zakres wartości nagrody
        # przestrzeń obserwacji
        self.observation_space = spaces.Dict({'whose turn': spaces.Discrete(self._n_players),
                                              'whose next turn': spaces.Discrete(self._n_players),
                                              'LAST_contract': spaces.Discrete(36),
                                              'Player_contract': spaces.Discrete(38),
                                              'winning_pair': spaces.Discrete(self._n_players / 2),
                                              'double/redouble': spaces.Discrete(3),
                                              'Players hand': spaces.Tuple(
                                                  [spaces.MultiDiscrete([2 for _ in range(0, len(self._deck.deck))])
                                                   for _ in range(0, self._n_players)]),
                                              'pair score/optimum score': spaces.Box(low=-7000, high=7000, shape=(4,),
                                                                                     dtype=np.int32)})
        self.action_space = Dynamic(38)  # przestrzeń dostępnych działań agenta

        self.reset()

    def step(self, action):
        """"""

        # sprawdzenie czy wykonane działanie przez agenta jest możliwe
        assert self.action_space.contains(action), "%r (%s) invalid" % (action, type(action))

        # wyznaczenie przestrzeni obserwacji i nagrody
        state = self._get_game_state(action, False)
        self._reward = self._get_reward(state, action)
        # dodanie do przestrzeni obserwacji zapisu oraz optymalnych punktów dla każdej z par
        state['pair score/optimum score'] = np.array([self._score[0], self._score[1], self._optimum_contract_score[0],
                                                      self._optimum_contract_score[1]])
        self._index_order += 1
        if self._index_order == 4:
            self._index_order = 0

        # zmienna określająca koniec danego epizodu
        done = self._is_over(action)

        # wyznaczenie dostępnych działań dla następnego gracza z przestrzeni akcji
        self.action_space.set_available_actions(action, state)

        return state, self._reward, done, {}

    def reset(self):
        """Reset środowiska i przywrócenie początkowego stanu licytacji oraz początkowej przestrzeni akcji (wszystkie odzywki + pas)"""

        self._viewer = None
        self._index_order = 0
        self._first_bind_pass = False
        self._double = False
        self._redouble = False
        self._pass_number = 0
        self._score = [0, 0]
        self._max_number_of_tricks = None
        self._max_contract = None
        self._reward = [None, None]
        self.action_space.reset()

        return self._get_game_state(None, True)

    def render(self, mode='console'):
        """Renderowanie bieżącego stanu środowiska z wykorzystniem wybranej opcji
        Obsługiwane są następujące tryby:
        - 'human' - interfejs graficzny
        - 'console' - wersja konsolowa"""

        if mode == 'human':
            # interfejs graficzny
            if self._viewer is None:
                self._win = Window(self._players[0].hand_splitted, self._players[1].hand_splitted,
                                   self._players[2].hand_splitted, self._players[3].hand_splitted, self._dealer_name)
                self._viewer = True

            else:
                if self._double:
                    last_contract = self._last_contract.__str__() + 'X'

                elif self._redouble:
                    last_contract = self._last_contract.__str__() + 'XX'

                else:
                    last_contract = self._last_contract.__str__()

                self._win.update_view(last_contract, self._players[0].player_contracts.__str__(),
                                      self._players[1].player_contracts.__str__(),
                                      self._players[2].player_contracts.__str__(),
                                      self._players[3].player_contracts.__str__(),
                                      PAIR,
                                      self._score,
                                      self._optimum_contract_score,
                                      self.metadata['video.frames_per_second'])

            time.sleep(2)

        elif mode == 'console':
            # wersja konsolowa
            if self._viewer is None:
                print('Dealer: ' + self._dealer_name)

                for i in range(0, self._n_players):
                    print(' ')
                    print(self._players[i].name + ' hand:')
                    print(spade + ' ' + self._players[i].hand_splitted[0])
                    print(heart + ' ' + self._players[i].hand_splitted[1])
                    print(diamond + ' ' + self._players[i].hand_splitted[2])
                    print(club + ' ' + self._players[i].hand_splitted[3])

                print(' ')

                self._viewer = False

            else:
                print('')
                if self._double:
                    print('LAST_contract: ' + self._last_contract.__str__() + ' X')

                elif self._redouble:
                    print('LAST_contract: ' + self._last_contract.__str__() + ' XX')

                else:
                    print('LAST_contract: ' + self._last_contract.__str__())

                print('Pair: ' + PAIR[0] + '  ' + PAIR[1])
                print('Score: ' + str(self._score[0]) + '  ' + str(self._score[1]))
                print('Optimum score: ' + str(self._optimum_contract_score[0]) + '  ' +
                      str(self._optimum_contract_score[1]))
                print(' ')
                print('NORTH_contract: ' + self._players[0].player_contracts.__str__())
                print('EAST_contract: ' + self._players[1].player_contracts.__str__())
                print('SOUTH_contract: ' + self._players[2].player_contracts.__str__())
                print('WEST_contract: ' + self._players[3].player_contracts.__str__())
                print(' ')

        else:
            # błąd przy wpisaniu niedostępnej opcji
            raise error.UnsupportedMode('Unsupported render mode' + mode)

    def close(self):
        """Zamknięcie środowiska i zakończenie programu"""

        if self._viewer is True:
            # jak mode == 'human'
            self._viewer = None
            self._win.close_window()

        else:
            # jak mode == 'console' lub brak renderowania
            self._viewer = None
            quit()

    def _choose_dealer_and_order(self):
        """Wybór rozdającego oraz ustalenie kolejności licytacji"""

        # wylosowanie rozdającego
        dealer = random.choice(range(len(self._players)))
        self._dealer_name = self._players[dealer].name

        # ustawienie graczy w odpowiedniej kolejności podczas licytacji
        self._index_order = 0
        self._players_order.append(self._players[dealer])

        if dealer < len(self._players) - 1:
            for i in range(dealer + 1, len(self._players)):
                self._players_order.append(self._players[i])
        if dealer > 0:
            for i in range(0, dealer):
                self._players_order.append(self._players[i])

    def _pbn_deal_representation(self):
        """Dane rozdanie w formacie PBN"""

        pbn = ""
        pbn += self._dealer_name
        pbn += ':'

        for j in range(0, self._n_players):

            for i in range(0, 4):
                list_pom = self._players[j].hand_splitted[i].split()

                for k in list_pom:
                    if k == '10':
                        pbn += 'T'
                    else:
                        pbn += k

                if i < 3:
                    pbn += '.'

            if j < 3:
                pbn += " "

        return pbn

    def _insert_solver_results(self):
        """Przypisanie wszystkim graczom odpowiednich rezultatów o maksymalnej ilości wziętych lew oraz wartości
        punktowych za optymalne kontrakty dla par otrzymanych z Dummy Double Solver"""

        pbn_repr = self._pbn_deal_representation()
        solver_results = get_results_from_solver(pbn_repr, self._players.index(self._players_order[0]))

        # maksymalna ilość wziętych lew dla danego miana
        for i in range(0, self._n_players):
            self._players[i].number_of_trick = get_solver_result_for_player(i, solver_results[0])
            self._players[i].makeable_contracts = max_contract_for_suit(self._players[i].number_of_trick)

        # wartości punktowe za optymalny kontrakt dla każdej z par
        self._optimum_contract_score[0] = solver_results[1]
        self._optimum_contract_score[1] = - self._optimum_contract_score[0]

    def _get_game_state(self, action, reset):
        """Wyznaczenie przestrzeni obserwacji"""

        state = {}

        if reset:
            # przestrzeń obserwacji dla funkcji reset
            # ustawienie stanu początkowego środowiska
            for i in range(0, len(self._players)):
                self._players[i].player_contracts = None
                self._players[i].win_auction = False

            state['whose turn'] = None
            state['whose next turn'] = self._players.index(self._players_order[0])
            state['LAST_contract'] = None
            state['Player_contract'] = None
            state['winning_pair'] = None
            state['double/redouble'] = 0
            self._last_contract = None
            state['Players hand'] = [[] for _ in range(0, self._n_players)]
            state['pair score/optimum score'] = np.array([self._score[0], self._score[1],
                                                          self._optimum_contract_score[0],
                                                          self._optimum_contract_score[1]])

            # reprezentacja rąk graczy w formie 0/1 jest dostępna tylko zaraz po zresetowaniu stanu środowiska
            for player in enumerate(self._players):
                state['Players hand'][player[0]] = player[1].hand_representation

        else:
            # przestrzeń obserwacji po wykonaniu akcji przez agenta
            # indeks gracza aktualnie licytującego
            player_index = self._players.index(self._players_order[self._index_order])
            state['whose turn'] = player_index

            # indeks gracza, który jest następny w kolejności do licytacji
            if player_index == 3:
                state['whose next turn'] = 0

            else:
                state['whose next turn'] = player_index + 1

            # ustalenie stanów określających najwyższą zgłoszoną odzywkę, która może być z kontrą, rekontrą lub bez
            if self._last_contract is None:
                # początek licytacji
                state['LAST_contract'] = action
                self._last_contract = self._available_contracts[action]
                state['double/redouble'] = 0

                if action == 0:
                    # działanie to pas
                    self._first_bind_pass = True
                    self._players[player_index].win_auction = False

                else:
                    # działanie jest jakolkolwiek odzywką
                    self._players[player_index].win_auction = True

            elif (action < self._last_contract.value or self._last_contract.value == 0) and action != 0:
                # dalszy przebieg licytacji
                # działanie to nie kontra/rekontra/pas lub wszyscy gracze od początku licytacji spasowali
                # i obecne działanie nie jest pasem

                state['LAST_contract'] = action
                self._last_contract = self._available_contracts[action]
                self._first_bind_pass = False

                for i in range(0, len(self._players)):
                    self._players[i].win_auction = False

                self._players[player_index].win_auction = True

                # nowa odzywka kasuje zgłoszoną kontrę lub rekontrę
                state['double/redouble'] = 0
                self._redouble = False
                self._double = False

            else:
                # jeśli działanie to kontra/rekontra/pas
                state['LAST_contract'] = self._last_contract.value

                if action == 36:
                    # kontra
                    state['double/redouble'] = 1
                    self._double = True
                    self._first_bind_pass = False

                elif action == 37:
                    # rekontra
                    state['double/redouble'] = 2
                    self._redouble = True
                    self._double = False
                    self._first_bind_pass = False

                else:
                    # pas
                    if self._double:
                        state['double/redouble'] = 1

                    elif self._redouble:
                        state['double/redouble'] = 2

                    else:
                        state['double/redouble'] = 0

            # odzywka/zapowiedź zgłoszona przez aktualnie licytującego agenta
            self._players[player_index].player_contracts = self._available_contracts[action]
            state['Player_contract'] = action

            # ustalenie do której z par należy najwyższy zgłoszony kontrakt w danym momencie
            # na koniec epizodu jest to para wygrywająca licytację
            for player in self._players:
                if player.win_auction is True:
                    if self._players.index(player) in WIN_PAIR[0]:
                        state['winning_pair'] = 0

                    elif self._players.index(player) in WIN_PAIR[1]:
                        state['winning_pair'] = 1

            if state['LAST_contract'] == 0:
                # przypadek gdy na poczatku licytacji (lub w kolejnych dalszych krokach) zgłoszono pas
                # wtedy żadna z par nie wygrywa licytacji
                state['winning_pair'] = None

        return state

    def _get_reward(self, state, action):
        """Wyznaczenie nagrody za wykonane działanie przez jednego z agentów"""

        reward = [None, None]

        if self._last_contract.value == 0:
            # przypadek gdy na początku licytacji (lub ewentualnie w dalszych krokach) zgłoszono pas
            # - nie ustalono kontraktu
            self._score = [0, 0]
            reward[0] = self._score[0] - self._optimum_contract_score[0]
            reward[1] = - reward[0]

        else:
            # ustalono jakiś kontrakt
            ind_w = state['winning_pair']  # indeks pary z najwyższym zgłoszonym kontraktem
            ind_o = None  # indeks pary przeciwnej

            for i in enumerate(WIN_PAIR):
                if i[0] != ind_w:
                    ind_o = i[0]

            optimum_contract_score = self._optimum_contract_score[ind_w]

            if action == 0:  # działanie agenta to pas
                reward = self._reward

            else:
                # działanie agenta to odzywka licytacyjna lub kontra/rekontra
                bind_trump = self._last_contract.suit
                bind_number = self._last_contract.number

                if action != 36 and action != 37:
                    self._max_contract = self._players[state['whose turn']].makeable_contracts[bind_trump]
                    self._max_number_of_tricks = self._players[state['whose turn']].number_of_trick[bind_trump]

                number_of_tricks = bind_number + 6
                trick_difference = number_of_tricks - self._max_number_of_tricks

                if bind_number <= self._max_contract:
                    # kontrakt jest realizowalny
                    # punkty za lewy
                    if bind_trump == 'NT':
                        self._score[ind_w] = CONTRACT_POINTS['NT'][0] + (bind_number - 1) * CONTRACT_POINTS['NT'][1]

                    else:
                        self._score[ind_w] = bind_number * CONTRACT_POINTS[bind_trump]

                    # punkty za kontrę lub rekontrę plus premie
                    if state['double/redouble'] == 1:
                        # kontra
                        self._score[ind_w] *= CONTRACT_POINTS['X']
                        self._score[ind_w] += BONUS['DOUBLE']

                    elif state['double/redouble'] == 2:
                        # rekontra
                        self._score[ind_w] *= CONTRACT_POINTS['XX']
                        self._score[ind_w] += BONUS['REDOUBLE']

                    # premie za częściówki, dograne
                    if self._score[ind_w] < 100:
                        # częściówki
                        self._score[ind_w] += BONUS['PARTIAL-GAME']

                    else:
                        # dograne
                        self._score[ind_w] += BONUS['GAME']

                    # premie szlemiki, szlemy
                    if bind_number == 6:
                        # szlemiki
                        self._score[ind_w] += BONUS['SLAM']

                    elif bind_number == 7:
                        # szlemy
                        self._score[ind_w] += BONUS['GRAND_SLAM']

                    # premie za nadróbki
                    if bind_number != self._max_contract:
                        if state['double/redouble'] == 0:
                            # nadróbki bez kontry/rekontry
                            if bind_trump == 'NT':
                                self._score[ind_w] += CONTRACT_POINTS['NT'][1] * (self._max_contract - bind_number)

                            else:
                                self._score[ind_w] += CONTRACT_POINTS[bind_trump] * (self._max_contract - bind_number)

                        elif state['double/redouble'] == 1:
                            # nadróbki z kontrą
                            self._score[ind_w] += BONUS['OVERTRICKS_DOUBLE'] * (self._max_contract - bind_number)

                        elif state['double/redouble'] == 2:
                            # nadróbki z rekontrą
                            self._score[ind_w] += BONUS['OVERTRICKS_REDOUBLE'] * (self._max_contract - bind_number)

                    self._score[ind_o] = -self._score[ind_w]
                    reward[ind_w] = self._score[ind_w] - optimum_contract_score
                    reward[ind_o] = -reward[ind_w]

                else:
                    # kontrakt nie jest realizowalny
                    if state['double/redouble'] == 0:
                        # nie było kontry lub rekontry
                        self._score[ind_o] = PENALTY_POINTS['NO DOUBLE/REDOUBLE'] * trick_difference

                    elif state['double/redouble'] == 1:
                        # była kontra
                        self._score[ind_o] = PENALTY_POINTS['DOUBLE'][0] + \
                                             PENALTY_POINTS['DOUBLE'][0] * PENALTY_POINTS['DOUBLE'][1] * \
                                             (trick_difference - 1)

                        # premia za czwartą i każdą następną lewę wpadkową
                        if trick_difference >= 4:
                            self._score[ind_o] += PENALTY_POINTS['DOUBLE'][0] * (trick_difference - 3)

                    elif state['double/redouble'] == 2:
                        # była rekonta
                        self._score[ind_o] = PENALTY_POINTS['REDOUBLE'][0] + \
                                             PENALTY_POINTS['REDOUBLE'][0] * PENALTY_POINTS['REDOUBLE'][1] \
                                             * (trick_difference - 1)

                        # premia za czwartą i każdą następną lewę wpadkową
                        if trick_difference >= 4:
                            self._score[ind_o] += PENALTY_POINTS['REDOUBLE'][0] * (trick_difference - 3)

                    self._score[ind_w] = -self._score[ind_o]
                    reward[ind_w] = self._score[ind_w] - optimum_contract_score
                    reward[ind_o] = - reward[ind_w]

        return reward

    def _is_over(self, action):
        """Wyznaczenie warunku końca licytacji"""

        if action == 0:
            self._pass_number += 1

        else:
            self._pass_number = 0

        if self._pass_number == 3 and (not self._first_bind_pass):
            # kolejno troje graczy pasuje po ustalonym kontrakcie
            return True

        elif self._first_bind_pass and self._pass_number == 4:
            # nie ustalono kontraktu - na początku licytacji wszyscy gracze spasowali
            return True

        elif self._last_contract.value == 1 and self._redouble:
            # ostateczny kontrakt to 7NT, a po tym nastąpiła kontra i rekontra
            return True

        else:
            return False
