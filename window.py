from PyQt5.QtWidgets import QWidget, QLabel, QDesktopWidget
from PyQt5.QtGui import QImage, QPainter, QFont, QPixmap
from PyQt5.QtCore import Qt
from entities import Snake, Fruits

class Window:
    """
    The game's main window. Takes care of displaying the Snake, the fruits and the score.
    """

    def __init__(self, width, height, title, background, resolution, framecounter = 0, pixelsize = None, label = None, canvas = None, painter = None):
        self.width = width
        self.height = height
        self.title = title
        self.background = background
        self.resolution = resolution
        self.framecounter = framecounter
        self.pixelsize = pixelsize
        self.lable = label
        self.canvas = canvas
        self.painter = painter

        self.window = QWidget()

        self.bar = QLabel(self.window)

        self.pixelsize = self.width/self.resolution

        self.label = QLabel(self.window)

        self.window.setWindowTitle(self.title)
        self.window.resize(self.width, self.height + 2 * self.pixelsize)

        self.label.resize(self.width, self.height)
        self.label.move(0, self.pixelsize * 2)

        self.bar.resize(self.width, self.pixelsize * 2)
        self.bar.move(0, 0)

        # Canvas
        self.canvas = QImage(self.width, self.height, QImage.Format_RGBA8888)
        self.painter = QPainter(self.canvas)
        self.painter.fillRect(0, 0, self.width, self.height, self.background)

        # Score
        self.painter.setPen(Qt.black)
        font_size = self.width * 0.01
        self.painter.setFont(QFont("Pixeled", font_size));

        # Center the window
        fg = self.window.frameGeometry()
        center = QDesktopWidget().availableGeometry().center()
        fg.moveCenter(center)
        self.window.move(fg.topLeft())

        self.label.setPixmap(QPixmap.fromImage(self.canvas))


    def show(self):
        """ Draws the canvas on the window. """
        self.label.setPixmap(QPixmap.fromImage(self.canvas))
        self.window.show()


    def update_score(self, score):
        """ Updatse the text in the score label """
        self.bar.setText("  Score: " + score)


    def clear(self):
        """ Clears the screen by painting every square with the background color. """
        self.painter.fillRect(0, 0, self.width, self.height, self.background)


    def display(self, entity):
        """ Draws an entity on the canvas. """
        if type(entity) is Snake:
            for part in entity.parts:
                self.painter.fillRect(part.position_x * self.pixelsize, part.position_y * self.pixelsize, self.pixelsize, self.pixelsize, part.color)
        elif type(entity) is Fruits:
            self.painter.fillRect(entity.list[0].position_x * self.pixelsize, entity.list[0].position_y * self.pixelsize, self.pixelsize,
                                  self.pixelsize, entity.list[0].color)


    def await_key(self, snake: Snake):
        """ Registers a pressed key and passes the information to the snake. """
        snake.direction_x = snake.head.direction_x
        snake.direction_y = snake.head.direction_y
        self.window.keyPressEvent = snake.change_direction


    def check_border_collision(self, snake: Snake):
        """ Checks the collision between the snake and the border of the screen. """
        if snake.head.position_x * self.pixelsize > self.width - self.pixelsize \
                or snake.head.position_y * self.pixelsize > self.height - self.pixelsize \
                or snake.head.position_x < 0 \
                or snake.head.position_y < 0:
            snake.die()
