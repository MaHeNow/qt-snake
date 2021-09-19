from PyQt5.QtCore import Qt
from random import randint

class SnakePart:
    """
    A single part of a snake. A part is visually represented by a single square on the field.        
    """

    def __init__(self, position_x, position_y,direction_x, direction_y, color = Qt.white):
        self.position_x = position_x
        self.position_y = position_y
        self.direction_x = direction_x
        self.direction_y = direction_y
        self.color = color

    def move(self):
        """ Updates the position of the snake part based on its direction. """
        self.position_x += 1 * self.direction_x
        self.position_y += 1 * self.direction_y


class Snake:
    """ 
    The actual snake. A snake is composed from many individual snake parts.
    Every snake part is represented by a singel square on the screen.
    """

    def __init__(self, parts, speed, fruit_threshold = 5):
        self.parts = parts
        self.speed = speed
        self.blocked = False
        self.fruit_counter = 0
        self.fruit_threshold = fruit_threshold
        self.head = parts[0]
        self.direction_x = self.head.direction_x
        self.direction_y = self.head.direction_y
        

    def move(self):
        """ Moves every single part of the snake and changes its direction to the direction of the following part. """
        if not self.blocked:
            for i in range(len(self.parts)-1, -1, -1):
                self.parts[i].move()
                if i != 0:
                    self.parts[i].direction_x = self.parts[i-1].direction_x
                    self.parts[i].direction_y = self.parts[i-1].direction_y


    def change_direction(self, e):
        """ Reveices a keypress event and changes the direction of the part accordingly. """
        if e.key() == Qt.Key_Left and self.direction_x != 1:
            self.parts[0].direction_x = -1
            self.parts[0].direction_y = 0
        elif e.key() == Qt.Key_Right and self.direction_x != -1:
            self.parts[0].direction_x = 1
            self.parts[0].direction_y = 0
        elif e.key() == Qt.Key_Up and self.direction_y != 1:
            self.parts[0].direction_x = 0
            self.parts[0].direction_y = -1
        elif e.key() == Qt.Key_Down and self.direction_y != -1:
            self.parts[0].direction_x = 0
            self.parts[0].direction_y = 1


    def check_bite(self):
        """ Checks if the snakes head touches another entity. """
        for part in self.parts:
            if part != self.head and self.head.position_x == part.position_x and self.head.position_y == part.position_y:
                self.die()


    def grow(self, collected):
        """ Adds a new part to the snake. """
        new_position_x = self.parts[len(self.parts) - 1].position_x
        new_position_y = self.parts[len(self.parts) - 1].position_y
        self.parts.append(SnakePart(new_position_x, new_position_y, 0, 0))
        if collected % 5 == 0:
            if self.speed > 1:
                self.speed -= 1


    def die(self):
        """ Simply blocks the snake, preventing it from moving any further. """
        self.blocked = True
    

class Fruit:
    """
    A fruit is a square on the screen, that the snake is supposed to collect.
    """

    def __init__(self, position_x, position_y, color = Qt.green):
        self.position_x = position_x
        self.position_y = position_y
        self.color = color

class Fruits:
    """
    A list and handler for all fruits in the game.
    """

    def __init__(self, list, resolution, collected = 0):
        self.list = list
        self.resolution = resolution
        self.collected = collected
         

    def spawn(self, snake: Snake):
        """ Spawns a new fruit on the field. """
        new_position_x = randint(0 ,self.resolution - 1)
        new_position_y = randint(0, self.resolution - 1)
        for part in snake.parts:
            if new_position_x == part.position_x and new_position_y == part.position_y:
                self.spawn(snake)
        self.list.append(Fruit(new_position_x, new_position_y))
        return


    def check_collision(self, snake: Snake):
        """ 
        Checks if the snake has made collision with one of the fruits. 
        If so, the fruit gets deleted, the snake grows by one and a new fruit is spawned.
        """
        if self.list[0].position_x == snake.head.position_x and self.list[0].position_y == snake.head.position_y:
            self.list.pop()
            self.spawn(snake)
            self.collected += 1
            snake.grow(self.collected)