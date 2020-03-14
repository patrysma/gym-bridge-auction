import gym
import random
from gym import error, spaces, utils
from gym.utils import seeding
from gym_bridge_auction.envs.rendering import *

#dopisać warunki do renderu, żeby narpiew zrobić reset
#warunek czy konsloa to wtedy drukuj state, a jak human to renderować normalnie - też do renderu

class AuctionEnv(gym.Env):
    metadata = {'render.modes': ['human', 'console']}

    def __init__(self):

        self.app = QApplication(sys.argv)
        self.win = Window()
        self.n_players = 4
        self.deck = Deck() #tworzenie talii
        self.players = []
        self.observation_space = spaces.Dict({'whose turn': spaces.Discrete(self.n_players),
                                              'LAST_contract': spaces.Discrete(36),
                                              'NORTH_contract': spaces.Discrete(36),
                                              'EAST_contract': spaces.Discrete(36),
                                              'SOUTH_contract': spaces.Discrete(36),
                                              'WEST_contract': spaces.Discrete(36)})
        self.action_space = spaces.Discrete(36)
        self.dealer = None
        self.dealer_name = ''
        self.index_order = None #indeks w players order
        self.players_order = []
        self.last_contract = None
        self.pom = 0
        #self.state = {}
        #Utworzenie dostępnych kontraktów
        self.available_contracts = self.create_avaliable_contracts()
        self.deck.shuffle()
        hands = self.deck.deal(self.n_players)
        self.players = [Player(NAMES[i], hands[i]) for i in range(0, self.n_players)]

        for j in range(0, len(self.players)):
            self.players[j].split_hand()
            for i in range(0, 4):
                self.players[j].hand_splitted[i] = self.players[j].hand_to_display(self.players[j].hand_splitted[i])

        self.choose_dealer_and_order()
        self.reward = None
        self.pass_number = 0
        self.reset()


    def step(self, action):
        assert self.action_space.contains(action), "%r (%s) invalid" % (action, type(action))
        state = {}
        state = self.get_game_state(action, False)
        self.get_reward(action)
        self.index_order += 1

        if self.index_order == 4:
            self.index_order = 0


    def reset(self):
        #metoda ustawia środowisko w pocztątkowy stan
        # self.deck.shuffle()
        # hands = self.deck.deal(self.n_players)
        # self.players = [Player(NAMES[i], hands[i]) for i in range(0, self.n_players)]
        #
        # for j in range(0, len(self.players)):
        #     self.players[j].split_hand()
        #     for i in range(0, 4):
        #         self.players[j].hand_splitted[i] = self.players[j].hand_to_display(self.players[j].hand_splitted[i])
        #
        # self.choose_dealer_and_order()
        self.pass_number = 0
        self.reward = None
        return self.get_game_state(None, True)

    def render(self, mode='human'):

        if mode == 'human':
            self.hand_display(self.players[0].hand_splitted, self.win.north_hands_display)
            self.hand_display(self.players[1].hand_splitted, self.win.east_hands_display)
            self.hand_display(self.players[2].hand_splitted, self.win.south_hands_display)
            self.hand_display(self.players[3].hand_splitted, self.win.west_hands_display)
            self.win.who_is_dealer[0].setText(self.dealer_name)
            sys.exit(self.app.exec_())
        #self.win.last_contract_display[0].setText(str(self.pom))

        # self.win.north_hands_display[0].setText((self.game.players[0].hand_splitted[0]))
        # self.win.north_hands_display[1].setText((self.game.players[0].hand_splitted[1]))
        #self.insert_cards(self.win.north_hands_display[0], self.game.players[0].hand_d)


    def close(self):
        print('close')

    def hand_display(self, hand, display):
        for i in range(0, 4):
            display[i].setText(hand[i])

    def create_avaliable_contracts(self):
        suits = ['C', 'D', 'H', 'S', 'NT']
        numbers = [1, 2, 3, 4, 5, 6, 7]
        contracts = [Contract('pass', None)]
        contracts.extend([Contract(i, j) for j in numbers for i in suits])
        for i in range(0, len(contracts)):
            contracts[i].value = i

        return contracts

    def choose_dealer_and_order(self):
        self.dealer = random.choice(range(len(self.players)))
        #self.players[dealer].is_dealer = True
        self.dealer_name = self.players[self.dealer].name
        self.index_order = 0
        self.players_order.append(self.players[self.dealer])

        if self.dealer < len(self.players) - 1:
            for i in range(self.dealer + 1, len(self.players)):
                self.players_order.append(self.players[i])
        if self.dealer > 0:
            for i in range(0, self.dealer):
                self.players_order.append(self.players[i])

    def get_game_state(self, action, reset):
        state = {}

        if reset:
            for i in range(0, len(self.players)):
                self.players[i].player_contracts = None

            state['whose turn'] = None
            state['LAST_contract'] = None
            state['NORTH_contract'] = None
            state['EAST_contract'] = None
            state['SOUTH_contract'] = None
            state['WEST_contract'] = None
            self.last_contract = None

        else:
            player_index = self.players.index(self.players_order[self.index_order])
            state['whose turn'] = player_index

            if action > self.last_contract.value:
                state['LAST_contract'] = action
                self.last_contract = self.available_contracts[action]
            elif (self.last_contract is None) and (action == 0):
                #jak ostatni kontrakt jest pusty i pierwszy jest pass
                state['LAST_contract'] = action
                self.last_contract = self.available_contracts[action]
            elif (self.last_contract is None) and (action != 0):
                state['LAST_contract'] = action
                self.last_contract = self.available_contracts[action]

            self.players[player_index].player_contracts = self.available_contracts[action]

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
        if action == 0:
            self.pass_number += 1
        else:
            self.pass_number = 0



#Napisać funkcję wyznaczjącą ostateczny kontrakt, czyli maksymalny wypowiedziany