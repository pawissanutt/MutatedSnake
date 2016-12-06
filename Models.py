import math
import arcade.key


class Model:
    def __init__(self, world, x, y, angle):
        self.world = world
        self.x = x
        self.y = y
        self.angle = 0

    def hit(self, other, hit_size):
        return (abs(self.x - other.x) <= hit_size) and (abs(self.y - other.y) <= hit_size)


class Snake:
   
    def __init__(self, world, x, y, angle):
        self.world = world
        self.x = x
        self.y = y
        self.head = HeadSnake(self, x, y, angle)

    def changeAngle(self, angle) :
        self.head.angle = angle
 
 
    def animate(self, delta):
        self.head.animate(delta)


class HeadSnake(Model):
    
    def __init__(self, world, x, y, angle):
        super().__init__(world, x, y, angle)

    def animate(self, delta):
        self.x += math.sin(math.radians(self.angle))
        self.y += math.cos(math.radians(self.angle))


class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.score = 0
 
        self.snake = Snake(self, 100, 100, 0)
 
 
    def animate(self, delta):
        self.snake.animate(delta)


    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.LEFT:
            self.snake.changeAngle(270)
        if key == arcade.key.RIGHT:
            self.snake.changeAngle(90)
        if key == arcade.key.UP:
            self.snake.changeAngle(0)
        if key == arcade.key.DOWN:
            self.snake.changeAngle(180)

        
