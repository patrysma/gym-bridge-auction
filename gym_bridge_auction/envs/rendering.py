import sys
from PyQt5.QtWidgets import QWidget,QApplication

# Tworzenie zmiennej GUI
app = gui()
app.setSize(1200, 800)
app.setBg("green")
app.addLabel("N", "N", 1,1,1)
app.addLabel("S", "S", 2,1)
app.addLabel("W", "W", 2,0,1,2)
app.addLabel("E", "E", 1,2)
Spade = "\u2660"
Heart = "\u2665"

app.addLabel("NSpade", Spade,0,0)
app.addLabel("NHeart", Heart,1,0)

# Start aplikacji

app.go()
