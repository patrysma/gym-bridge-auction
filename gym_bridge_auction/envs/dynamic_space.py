import gym
from gym import spaces
import numpy as np
from gym_bridge_auction.envs.game import WIN_PAIR


class Dynamic(spaces.Discrete):
    """Klasa definiująca zmieniającą się przestrzeń akcji po wykonaniu kolejnych kroków"""

    def __init__(self, max_space):
        super().__init__(max_space)
        self.new_n = self.n - 2  # rozmiar przestrzeni akcji bez kontry i rekontry
        self.available_actions = list(range(0, self.new_n))  # początkowa przestrzeń akcji bez kontry i rekontry

    def sample(self):
        """Wybór losowego działania z dostępnej przestrzeni akcji"""

        return self.np_random.choice(self.available_actions)

    def __repr__(self):
        """Reprezentacja klasy"""

        return "Dynamic({})".format(self.n)

    def set_available_actions(self, action, state):
        """Zdefiniowanie dostępnych działań dla agenta w danym kroku"""

        if not (action in (0, 36, 37)):
            self.new_n = action  # zmniejaszanie się dostępnych odzywek licytacyjnych

        self.available_actions = list(range(0, self.new_n))

        if  (not state['winning_pair'] is None) and state['double/redouble'] == 0 and not (state['whose next turn'] in WIN_PAIR[state['winning_pair']]):
            # dostępna kontra
            self.available_actions.append(36)

        elif state['double/redouble'] == 1 and (state['whose next turn'] in WIN_PAIR[state['winning_pair']]):
            # dostępna rekontra
            self.available_actions.append(37)

    def contains(self, x):
        """Sprawdzenie czy wprowadzone działanie jest poprawnego typu"""

        return x in self.available_actions

    def __eq__(self, other):
        """Porównanie obiektów"""
        return isinstance(other, Dynamic) and self.n == other.n
