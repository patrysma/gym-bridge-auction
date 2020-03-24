import gym
from gym import spaces
from gym_bridge_auction.envs.render import *
import random
import time


class AuctionEnv(gym.Env):
    metadata = {'render.modes': ['human', 'console'], 'video.frames_per_second': 450}

    def __init__(self):

        self.win = None  # instancja interfejsu graficznego
        self.viewer = None  # zmienna pomocnicza do renderowania
        self.n_players = 4  # liczba graczy
        self.deck = Deck()  # utworzenie talii
        self.players = []  # lista graczy
        # przestrzeń obserwacji
        self.observation_space = spaces.Dict({'whose turn': spaces.Discrete(self.n_players),
                                              'LAST_contract': spaces.Discrete(36),
                                              'NORTH_contract': spaces.Discrete(36),
                                              'EAST_contract': spaces.Discrete(36),
                                              'SOUTH_contract': spaces.Discrete(36),
                                              'WEST_contract': spaces.Discrete(36),
                                              'winning_pair': spaces.Discrete(self.n_players/2)})
        self.action_space = spaces.Discrete(36)  # przestrzeń dostępnych działań agenta
        self.dealer_name = ''  # Nazwa gracza, który to rozdający
        self.index_order = None  # indeks aktualnie licytującego gracza (z listy graczy w odpowiedniej kolejności)
        self.players_order = []  # lista graczy ustawionych w odpowiedniej kolejności licytowania
        self.last_contract = None  # ustalony kontrakt
        # self.state = {}
        # Utworzenie dostępnych kontraktów (lista obiektów typu Contract)
        self.available_contracts = self.create_available_contracts()
        self.deck.shuffle()  # tasowanie talii
        hands = self.deck.deal(self.n_players)  # rozdanie kart dla graczy
        self.players = [Player(NAMES[i], hands[i]) for i in range(0, self.n_players)]  # utworzenie listy graczy
        # rozdzielenie rąk graczy ze względu na kolor karty (w każdym wierszu figury/numery w danym kolorze)
        for j in range(0, len(self.players)):
            self.players[j].split_hand()
            for i in range(0, 4):
                self.players[j].hand_splitted[i] = self.players[j].hand_to_display(self.players[j].hand_splitted[i])

        self.choose_dealer_and_order()  #wybór rozdającego i kolejność licytacji
        self.reward = None
        self.pass_number = 0
        self.reset()

    def step(self, action):
        assert self.action_space.contains(action), "%r (%s) invalid" % (action, type(action))
        #state = {}
        state = self.get_game_state(action, False)
        self.get_reward(action)
        self.index_order += 1

        if self.index_order == 4:
            self.index_order = 0
        done = self.is_over(action)

        return state, self.reward, done, {}

    def reset(self):
        self.reward = None
        self.viewer = None
        return self.get_game_state(None, True)

    def render(self, mode='console'):

        if mode == 'human':

            if self.viewer is None:
                self.win = Window(self.players[0].hand_splitted, self.players[1].hand_splitted,
                                  self.players[2].hand_splitted, self.players[3].hand_splitted, self.dealer_name)
                self.viewer = True

            else:
                self.win.update_view(self.last_contract.__str__(), self.players[0].player_contracts.__str__(),
                                     self.players[1].player_contracts.__str__(),
                                     self.players[2].player_contracts.__str__(),
                                     self.players[3].player_contracts.__str__(),
                                     self.metadata['video.frames_per_second'])

            time.sleep(2)

        elif mode == 'console':
            if self.viewer is None:
                print('Dealer: ' + self.dealer_name)

                for i in range(0, self.n_players):
                    print(' ')
                    print(self.players[i].name + ' hand:')
                    print(spade + ' ' + self.players[i].hand_splitted[0])
                    print(heart + ' ' + self.players[i].hand_splitted[1])
                    print(diamond + ' ' + self.players[i].hand_splitted[2])
                    print(club + ' ' + self.players[i].hand_splitted[3])

                self.viewer = False

            else:
                print('')
                print('LAST_contract: ' + self.last_contract.__str__())
                print('NORTH_contract: ' + self.players[0].player_contracts.__str__())
                print('EAST_contract: ' + self.players[1].player_contracts.__str__())
                print('SOUTH_contract: ' + self.players[2].player_contracts.__str__())
                print('WEST_contract: ' + self.players[3].player_contracts.__str__())

        else:
            raise error.UnsupportedMode('Unsupported render mode' + mode)

    def close(self):
        if self.viewer is True:
            # jak mode == 'human'
            self.win.close_window()
            self.viewer = None
            quit()
        elif self.viewer is False:
            # jak mode == 'console'
            self.viewer = None
            quit()
        else:
            self.viewer = None
            quit()

    @staticmethod
    def create_available_contracts():
        """Utworzenie dostępnych kontraktów podczas licytacji"""

        suits = ['C', 'D', 'H', 'S', 'NT']
        numbers = [1, 2, 3, 4, 5, 6, 7]
        contracts = [Contract('pass', None)]
        contracts.extend([Contract(i, j) for j in numbers for i in suits])
        for i in range(0, len(contracts)):
            contracts[i].value = i

        return contracts

    def choose_dealer_and_order(self):
        """Wybór rozdającego oraz ustalenie kolejności licytacji"""

        dealer = random.choice(range(len(self.players)))
        # self.players[dealer].is_dealer = True
        self.dealer_name = self.players[dealer].name
        self.index_order = 0
        self.players_order.append(self.players[dealer])

        if dealer < len(self.players) - 1:
            for i in range(dealer + 1, len(self.players)):
                self.players_order.append(self.players[i])
        if dealer > 0:
            for i in range(0, dealer):
                self.players_order.append(self.players[i])

    def get_game_state(self, action, reset):
        """Wyznaczenie przestrzeni obserwacji"""

        state = {}

        if reset:
            for i in range(0, len(self.players)):
                self.players[i].player_contracts = None
                self.players[i].win_auction = False

            state['whose turn'] = None
            state['LAST_contract'] = None
            state['NORTH_contract'] = None
            state['EAST_contract'] = None
            state['SOUTH_contract'] = None
            state['WEST_contract'] = None
            state['winning_pair'] = None
            self.last_contract = None

        else:

            player_index = self.players.index(self.players_order[self.index_order])
            state['whose turn'] = player_index

            if (self.last_contract is None) and (action == 0):
                # jak ostatni kontrakt jest pusty i pierwszy jest pass
                state['LAST_contract'] = action
                self.last_contract = self.available_contracts[action]
                for i in range(0, len(self.players)):
                    self.players[i].win_auction = False
                self.players[player_index].win_auction = True
            elif (self.last_contract is None) and (action != 0):
                state['LAST_contract'] = action
                self.last_contract = self.available_contracts[action]
                for i in range(0, len(self.players)):
                    self.players[i].win_auction = False
                self.players[player_index].win_auction = True

            if action > self.last_contract.value:
                state['LAST_contract'] = action
                self.last_contract = self.available_contracts[action]
                for i in range(0, len(self.players)):
                    self.players[i].win_auction = False
                self.players[player_index].win_auction = True
            elif action == 0:
                state['LAST_contract'] = self.last_contract.value
                self.last_contract = self.last_contract
            else:
                state['LAST_contract'] = self.last_contract.value
                self.last_contract = self.last_contract

            self.players[player_index].player_contracts = self.available_contracts[action]

            for player in self.players:
                if player.win_auction is True:
                    if (self.players.index(player) == 0) or (self.players.index(player) == 2):
                        state['winning_pair'] = 0
                    else:
                        state['winning_pair'] = 1

            if player_index == 0:
                state['NORTH_contract'] = action
            elif player_index == 1:
                state['EAST_contract'] = action
            elif player_index == 2:
                state['SOUTH_contract'] = action
            elif player_index == 3:
                state['WEST_contract'] = action

        return state

    def get_reward(self, action):
        """Wyznaczenie nagrody za wykonane działanie przez poszczególnego agenta"""

        if self.reward is None:
            if action == 0:
                self.reward = 0
            else:
                self.reward = 1
        else:
            if action > self.last_contract.value:
                self.reward = 1
            elif action == 0:
                self.reward = 0
            elif action <= self.last_contract.value:
                self.reward = -1

    def is_over(self, action):
        """Wyznaczenie warunku końca licytacji - po 3 pasach z rzędu"""

        if action == 0:
            self.pass_number += 1
        else:
            self.pass_number = 0

        if self.pass_number == 3:
            return True
        else:
            return False

