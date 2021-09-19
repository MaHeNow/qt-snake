import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt, QTimer
from window import Window
from entities import Snake, SnakePart, Fruits, Fruit

App = QApplication(sys.argv)

Window = Window(600, 600, "Snake", Qt.black, 20)

# -------------------------------------- WINDOW -----------------------------------------

Window.show()

# -------------------------------------- ENTITIES ---------------------------------------

parts = [
    SnakePart(14,1,-1,0,Qt.white),
    SnakePart(15,1,-1,0,Qt.white),
]
Snake = Snake(parts, 1)

fruit_list = [
    Fruit(10,10)
]
Fruits = Fruits(fruit_list, Window.resolution)

# ------------------------------------- GAME LOOP ---------------------------------------

def update():
    Window.clear()

    Window.framecounter += 1

    Window.update_score(str(Fruits.collected))
    if Window.framecounter % Snake.speed == 0:
        Snake.move()
        Window.await_key(Snake)
    Window.check_border_collision(Snake)
    Snake.check_bite()
    Fruits.check_collision(Snake)
    Window.display(Snake)
    Window.display(Fruits)

    Window.show()

Timer = QTimer()
Timer.timeout.connect(update)
Timer.start(100)

# Start the game
App.exec_()