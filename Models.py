import math
import arcade.key
import time

class Model:
    def __init__(self, world, x, y, angle):
        self.world = world
        self.x = x
        self.y = y
        self.angle = angle
        self.lastx = [x,x,x,x,x]
        self.lasty = [y,y,y,y,y]
        self.last_angle = [angle,angle,angle,angle,angle]

    def set_last_position(self):
        count = 1
        while (count > 0) :
            self.lastx[count] = self.lastx[count-1]
            self.lasty[count] = self.lasty[count-1]
            self.last_angle[count] = self.last_angle[count-1]
            count -= 1
        self.lastx[0] = self.x
        self.lasty[0] = self.y
        self.last_angle[0] = self.angle

    def set_position(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle

    def hit(self, other, hit_size):
        return (abs(self.x - other.x) <= hit_size) and (abs(self.y - other.y) <= hit_size)


class Snake:
   
    def __init__(self, world, x, y, angle):
        self.world = world
        self.x = x
        self.y = y
        self.speed = 5
        self.head = HeadSnake(self.world, x, y, angle)
        self.head.speed = self.speed
        self.body = [BodySnake(self.world, x, y - 30 , angle)]
        self.tail = TailSnake(self.world, x, y - 80, angle)

    def changeAngle(self, angle) :
        if (self.head.angle == self.head.next_angle ):
            if (math.fabs(self.head.angle - angle) != 180):
                self.head.next_angle = angle

    def add_body(self):
        count = self.body.__len__() - 1
        self.body.append(BodySnake(self.world,
                                   self.body[count].lastx[5 - self.speed],
                                   self.body[count].lasty[5 - self.speed],
                                   self.body[count].last_angle[5 - self.speed]))
        count += 1
        self.tail.set_position(self.body[count].lastx[6 - self.speed],
                               self.body[count].lasty[6 - self.speed],
                               self.body[count].last_angle[6 - self.speed])

 
    def animate(self, delta):
        self.head.animate(delta)
        for body in self.body:
            body.animate(delta)
        self.tail.animate(delta)
        
        count = self.body.__len__() - 1
        self.tail.set_position(self.body[count].lastx[6 - self.speed],
                               self.body[count].lasty[6 - self.speed],
                               self.body[count].last_angle[6 - self.speed])
        while (count > 0):
            self.body[count].set_position(self.body[count-1].lastx[5 - self.speed],
                                          self.body[count-1].lasty[5 - self.speed],
                                          self.body[count-1].last_angle[5 - self.speed])
            count -= 1
        self.body[0].set_position(self.head.lastx[5 - self.speed],
                               self.head.lasty[5 - self.speed],
                               self.head.last_angle[5 - self.speed])



class HeadSnake(Model):
    
    def __init__(self, world, x, y, angle):
        super().__init__(world, x, y, angle)
        self.next_angle = angle
        self.speed = 3

    def slow_rotate(self):
        self.angle %= 360
        if (math.fabs(self.next_angle - self.angle) > 90):
            if (self.next_angle < self.angle):
                self.next_angle %= 360
                self.next_angle += 360
            else :
                self.angle %= 360
                self.angle += 360
        if (self.next_angle - self.angle > 0):
            self.angle += 10
        elif (self.next_angle - self.angle < 0):
            self.angle -= 10

    def animate(self, delta):
        self.slow_rotate()
        self.set_last_position()
        self.x -= self.speed * math.sin(math.radians(self.angle))
        self.y += self.speed * math.cos(math.radians(self.angle))
        if (self.x > self.world.width):
            self.x = 0
        elif (self.x < 0):
            self.x = self.world.width
        if (self.y > self.world.height):
            self.y = 0
        elif (self.y < 0):
            self.y = self.world.height
        


class BodySnake(Model):
    
    def __init__(self, world, x, y, angle):
        super().__init__(world, x, y, angle)

    def animate(self, delta):
        self.set_last_position()


class TailSnake(Model):
    
    def __init__(self, world, x, y, angle):
        super().__init__(world, x, y, angle)

    def animate(self, delta):
        self.set_last_position()

class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.score = 0
        self.start_time = time.time()
 
        self.snake = Snake(self, 100, 100, 0)
        self.number_body = 1
 
 
    def animate(self, delta):
        self.snake.animate(delta)
        self.current_time = time.time()- self.start_time;
        self.score = int(self.current_time)
        self.increase_length()


    def increase_length(self):
        if (self.number_body < self.current_time):
            self.snake.add_body()
            self.number_body += 1

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.LEFT:
            self.snake.changeAngle(90)
        if key == arcade.key.RIGHT:
            self.snake.changeAngle(270)
        if key == arcade.key.UP:
            self.snake.changeAngle(0)
        if key == arcade.key.DOWN:
            self.snake.changeAngle(180)

        
