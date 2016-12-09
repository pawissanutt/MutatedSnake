import math
import arcade.key
import time
import random

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
        count = 2
        while (count > 0) :
            self.lastx[count] = self.lastx[count-1]
            self.lasty[count] = self.lasty[count-1]
            self.last_angle[count] = self.last_angle[count-1]
            count -= 1
        self.lastx[0] = self.x
        self.lasty[0] = self.y
        self.last_angle[0] = self.angle

    def get_nextx(self, speed):
        return self.x - speed * math.sin(math.radians(self.angle))

    def get_nexty(self, speed):
        return self.y + speed * math.cos(math.radians(self.angle))

    def set_position(self, x, y, angle):
        self.x = x
        self.y = y
        self.angle = angle

    def hit(self, other, hit_size):
        return (abs(self.x - other.x) <= hit_size) and (abs(self.y - other.y) <= hit_size)

    def is_at(self, x, y, size):
        return (abs(self.x - x) <= size) and (abs(self.y - y) <= size)

class Snake:
   
    def __init__(self, world, x, y, angle):
        self.world = world
        self.x = x
        self.y = y
        self.speed = 4
        self.head = HeadSnake(self.world, x, y, angle, self.speed)
        self.head.speed = self.speed
        self.body = [BodySnake(self.world, x, y - 30 , angle)]
        self.tail = TailSnake(self.world, x, y - 80, angle)

    def changeAngle(self, angle) :
        if (self.head.angle == self.head.next_angle ):
            if (math.fabs(self.head.angle - angle) != 180):
                self.head.next_angle = angle

    def add_body(self):
        self.body.append(BodySnake(self.world,
                                   self.body[-1].lastx[5 - self.speed],
                                   self.body[-1].lasty[5 - self.speed],
                                   self.body[-1].last_angle[5 - self.speed]))
        self.tail.set_position(self.body[-1].lastx[5 - self.speed],
                               self.body[-1].lasty[5 - self.speed],
                               self.body[-1].last_angle[5 - self.speed])

    def remove_body(self):
        if (self.body.__len__() > 1):
            del self.body[-1]

    def is_eat_itself(self):
        x = self.head.get_nextx(10)
        y = self.head.get_nexty(10)
        return self.has_body_at(x, y)

    def has_body_at(self, x, y):
        for body in self.body:
            if (body.is_at(x, y, 10)):
                return True
        return False

    def has_snake_at(self, x, y):
        if (has_body_at(x, y)):
            return True
        if (self.head.is_at(x, y, 30)):
            return True
        if (self.tail.is_at(x, y, 30)):
            return True
        return False

    def animate(self, delta):
        self.head.animate(delta)
        for body in self.body:
            body.animate(delta)
        
        count = self.body.__len__() - 1
        self.tail.set_position(self.body[count].lastx[6 - self.speed],
                               self.body[count].lasty[6 - self.speed],
                               self.body[count].last_angle[6 - self.speed])
        while (count > 0):
            self.body[count].set_position(self.body[count-1].lastx[6 - self.speed],
                                          self.body[count-1].lasty[6 - self.speed],
                                          self.body[count-1].last_angle[6 - self.speed])
            count -= 1
        self.body[0].set_position(self.head.lastx[6 - self.speed],
                                  self.head.lasty[6 - self.speed],
                                  self.head.last_angle[6 - self.speed])



class HeadSnake(Model):
    
    def __init__(self, world, x, y, angle, speed):
        super().__init__(world, x, y, angle)
        self.next_angle = angle
        self.speed = speed

    def slow_rotate(self, delta):
        self.angle %= 360
        if (math.fabs(self.next_angle - self.angle) > 90):
            if (self.next_angle < self.angle):
                self.next_angle %= 360
                self.next_angle += 360
            else :
                self.angle %= 360
                self.angle += 360
        if (self.next_angle - self.angle > 0):
            self.angle += int(200 * delta) * 5
            if (self.next_angle - self.angle < 0):
                self.angle = self.next_angle
        elif (self.next_angle - self.angle < 0):
            self.angle -= int(200 * delta) * 5
            if (self.next_angle - self.angle > 0):
                self.angle = self.next_angle
        
            
    def animate(self, delta):
        self.slow_rotate(delta)
        self.set_last_position()
        self.x -= self.speed * 50 * delta * math.sin(math.radians(self.angle))
        self.y += self.speed * 50 * delta * math.cos(math.radians(self.angle))
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
        

class Box(Model):
    def __init__(self, world, x, y):
        super().__init__(world, x, y, 0)



class World:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.score = 0
        self.start_time = time.time()
        self.gameover = False
 
        self.snake = Snake(self, 100, 100, 0)
        self.number_body = 1

        self.red_boxes = []
        self.green_box = Box(self, 300, 300)

 
    def animate(self, delta):
        if (self.gameover == False) :
            self.snake.animate(delta)
            self.current_time = time.time()- self.start_time;
            self.score = int(self.current_time)
            self.increase_length()
            self.should_create_boxes()
            self.if_hit_green_box()
            if (self.snake.is_eat_itself() or self.is_hit_red_box()):
                self.gameover = True
            

    def should_create_boxes(self):
        if (len(self.red_boxes) * 5 < self.score):
            self.random_create_red_box()


    def is_hit_red_box(self):
        x = self.snake.head.get_nextx(10)
        y = self.snake.head.get_nexty(10)
        return self.has_red_box_at(x, y)

    def has_red_box_at(self, x, y):
        for box in self.red_boxes:
            if (box.is_at(x, y, 15)):
                return True
        return False

    def is_hit_green_box(self):
        x = self.snake.head.get_nextx(10)
        y = self.snake.head.get_nexty(10)
        return self.has_green_box_at(x, y)

    def has_green_box_at(self, x, y):
        return self.green_box.is_at(x, y, 10)

    def random_create_red_box(self):
        x = random.randint(15, self.width - 15)
        y = random.randint(50, self.height - 15)
        while (self.snake.has_body_at(x,y)
               or self.has_red_box_at(x, y)
               or self.has_green_box_at(x, y)) :
            x = random.randint(15, self.width - 15)
            y = random.randint(50, self.height - 15)
        self.red_boxes.append(Box(self, x , y))

    def if_hit_green_box(self):
        if (self.is_hit_green_box()):
            x = random.randint(15, self.width - 15)
            y = random.randint(50, self.height - 15)
            while (self.snake.has_body_at(x,y)
                   or self.has_red_box_at(x, y)
                   or self.has_green_box_at(x, y)) :
                x = random.randint(15, self.width - 15)
                y = random.randint(50, self.height - 15)
            self.green_box.x = x
            self.green_box.y = y
            self.random_decrease_length(10)

    def increase_length(self):
        if (self.number_body / 2 < self.current_time):
            self.snake.add_body()
            self.number_body += 1

    def random_decrease_length(self, max_number):
        num = random.randint(1, max_number)
        while (num > 0):
            self.snake.remove_body()
            num -=1

    def on_key_press(self, key, key_modifiers):
        if key == arcade.key.LEFT:
            self.snake.changeAngle(90)
        if key == arcade.key.RIGHT:
            self.snake.changeAngle(270)
        if key == arcade.key.UP:
            self.snake.changeAngle(0)
        if key == arcade.key.DOWN:
            self.snake.changeAngle(180)

        
