import gym
from gym import error, spaces, utils
from gym.utils import seeding
from gym_bridge_auction.envs.game import *
from gym_bridge_auction.envs.rendering import *


class AuctionEnv(gym.Env):
    metadata = {'render.modes': ['human']}

    def __init__(self):
        self.game = Game()
        self.app = QApplication(sys.argv)
        self.win = Window()
        self.observation_space = spaces.Dict({'whose turn': spaces.Discrete(len(NAMES)),
                                              'LAST_contract': spaces.Discrete(36),
                                              'NORTH_contract': spaces.Discrete(36),
                                              'EAST_contract': spaces.Discrete(36),
                                              'SOUTH_contract': spaces.Discrete(36),
                                              'WEST_contract': spaces.Discrete(36)})
        self.action_space = spaces.Discrete(36)
        self.order = 0 #indeks dealera
        self.obs = []
        #Utworzenie dostępnych kontraktów
        self.available_contracts = self.create_avaliable_contracts()

        print('init')

    def step(self, action):
        print('step')

    def reset(self):
        print('reset')

    def render(self, mode='human'):
        self.hand_display(self.game.players[0].hand_splitted, self.win.north_hands_display)
        self.hand_display(self.game.players[1].hand_splitted, self.win.east_hands_display)
        self.hand_display(self.game.players[2].hand_splitted, self.win.south_hands_display)
        self.hand_display(self.game.players[3].hand_splitted, self.win.west_hands_display)
        self.win.who_is_dealer[0].setText(self.game.dealer_name)

        # self.win.north_hands_display[0].setText((self.game.players[0].hand_splitted[0]))
        # self.win.north_hands_display[1].setText((self.game.players[0].hand_splitted[1]))
        #self.insert_cards(self.win.north_hands_display[0], self.game.players[0].hand_d)
        sys.exit(self.app.exec_())

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

        return contracts

