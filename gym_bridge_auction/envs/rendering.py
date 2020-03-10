import sys
from PyQt5.QtWidgets import QWidget, QApplication, QLabel, QGridLayout, QLineEdit
from PyQt5.QtGui import QColor
from gym_bridge_auction.envs.game import *


class Window(QWidget):

    def __init__(self):
        super().__init__()
        self.west_hands_display = self.create_text_lines(4)
        self.south_hands_display = self.create_text_lines(4)
        self.east_hands_display = self.create_text_lines(4)
        self.north_hands_display = self.create_text_lines(4)
        self.players_contracts_display = self.create_text_lines(4)
        self.who_is_dealer = self.create_text_lines(1)
        self.last_contract_display = self.create_text_lines(1)
        self.title = 'Bridge auction environment'
        self.left = 10
        self.top = 10
        self.width = 1500
        self.height = 850
        self.interface()

    def interface(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.width, self.height)

        # ustawienie koloru tła
        self.setAutoFillBackground(True)
        p = self.palette()
        p.setColor(self.backgroundRole(), QColor(60, 120, 70))
        self.setPalette(p)

        # etykiety dla poszczególnych graczy
        north_player_label = QLabel(NAMES[0], self)
        north_player_label.setStyleSheet('color: aqua')
        north_colour_labels = self.create_labels()

        east_player_label = QLabel(NAMES[1], self)
        east_player_label.setStyleSheet('color: aqua')
        east_colour_labels = self.create_labels()

        south_player_label = QLabel(NAMES[2], self)
        south_player_label.setStyleSheet('color: aqua')
        south_colour_labels = self.create_labels()

        west_player_label = QLabel(NAMES[3], self)
        west_player_label.setStyleSheet('color: aqua')
        west_colour_labels = self.create_labels()

        # etykiety licytacji i wyników
        north_contract_label = QLabel("NORTH Contract:", self)
        east_contract_label = QLabel("EAST Contract:", self)
        south_contract_label = QLabel("SOUTH Contract:", self)
        west_contract_label = QLabel("WEST Contract:", self)
        last_contract_label = QLabel("Last contract:", self)
        who_is_dealer_label = QLabel("DEALER:", self)

        # north_widget = QWidget(self)
        # north_widget.setGeometry(QtCore.QRect(10, 270, 231, 211))

        north_layout = QGridLayout()
        north_layout.addWidget(north_player_label, 0, 1)
        for i in range(0, 4):
            north_layout.addWidget(north_colour_labels[i], i + 1, 0)

        for i in range(0, 4):
            north_layout.addWidget(self.north_hands_display[i], i + 1, 1)

        east_layout = QGridLayout()
        east_layout.addWidget(east_player_label, 0, 1)
        for i in range(0, 4):
            east_layout.addWidget(east_colour_labels[i], i + 1, 0)

        for i in range(0, 4):
            east_layout.addWidget(self.east_hands_display[i], i + 1, 1)

        south_layout = QGridLayout()
        south_layout.addWidget(south_player_label, 0, 1)
        for i in range(0, 4):
            south_layout.addWidget(south_colour_labels[i], i + 1, 0)

        for i in range(0, 4):
            south_layout.addWidget(self.south_hands_display[i], i + 1, 1)

        west_layout = QGridLayout()
        west_layout.addWidget(west_player_label, 0, 1)
        for i in range(0, 4):
            west_layout.addWidget(west_colour_labels[i], i + 1, 0)

        for i in range(0, 4):
            west_layout.addWidget(self.west_hands_display[i], i + 1, 1)

        contract_layout = QGridLayout()
        contract_layout.addWidget(north_contract_label, 0, 0)
        contract_layout.addWidget(east_contract_label, 1, 0)
        contract_layout.addWidget(south_contract_label, 2, 0)
        contract_layout.addWidget(west_contract_label, 3, 0)
        for i in range(0,4):
            contract_layout.addWidget(self.players_contracts_display[i], i, 1)

        result_layout = QGridLayout()
        result_layout.addWidget(self.who_is_dealer[0], 1, 0)
        result_layout.addWidget(self.last_contract_display[0], 3, 0)
        result_layout.addWidget(last_contract_label, 2, 0)
        result_layout.addWidget(who_is_dealer_label, 0, 0)

        main_grid_layout = QGridLayout()
        main_grid_layout.addLayout(west_layout, 2, 0)
        main_grid_layout.addLayout(south_layout, 3, 1)
        main_grid_layout.addLayout(east_layout, 2, 2)
        main_grid_layout.addLayout(north_layout, 1, 1)
        main_grid_layout.addLayout(contract_layout, 0, 0)
        main_grid_layout.addLayout(result_layout, 0, 2)
        self.setLayout(main_grid_layout)
        self.show()

    def create_labels(self):
        #Metoda tworząca listę etykiet z kolorów kart
        spade_label = QLabel(spade, self)
        spade_label.setStyleSheet('color: black')
        heart_label = QLabel(heart, self)
        heart_label.setStyleSheet('color: red')
        diamond_label = QLabel(diamond, self)
        diamond_label.setStyleSheet('color: red')
        club_label = QLabel(club, self)
        club_label.setStyleSheet('color: black')

        return [spade_label, heart_label, diamond_label, club_label]

    def create_text_lines(self, size):
        #Metoda tworzaca listę pól do wyświetlania tekstu
        cards = [QLineEdit() for i in range(0, size)]
        [cards[i].setReadOnly(True) for i in range(0, size)]
        [cards[i].setStyleSheet('background: white') for i in range(0, size)]

        return cards

#
# if __name__ == '__main__':
#     #game = Game()
#     app = QApplication(sys.argv)
#     win = Window()
#     #win.north_hands_display[0].setText(game.players[0].hand_s[0].rank)
#     sys.exit(app.exec_())
