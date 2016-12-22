import arcade

from Models import World, Snake

SCREEN_HEIGHT = 600
SCREEN_WIDTH = 600

class ModelSprite(arcade.Sprite):
    def __init__(self, *args, **kwargs):
        self.model = kwargs.pop('model', None)
 
        super().__init__(*args, **kwargs)
 
    def sync_with_model(self):
        if self.model:
            self.set_position(self.model.x, self.model.y)
            self.angle = self.model.angle
 
    def draw(self):
        self.sync_with_model()
        super().draw()

class WorldRenderer:
    def __init__(self, world, width, height) :
        self.world = world
        self.width = width
        self.height = height
        
        self.snake_head_sprite = ModelSprite('images/head.png', model=self.world.snake.head)
        self.snake_body_sprite = [ModelSprite('images/body.png', model=self.world.snake.body[0])]
        self.snake_tail_sprite = ModelSprite('images/tail.png', model=self.world.snake.tail)

        self.red_boxes_sprite = []
        self.green_box_sprite = ModelSprite('images/box2.png', model=self.world.green_box)

    def set_sprite_body(self):
        while (len(self.snake_body_sprite) < len(self.world.snake.body)):
            self.snake_body_sprite.append(ModelSprite('images/body.png'
                                                      ,model=self.world.snake.body[len(self.snake_body_sprite)]))     
        while (len(self.snake_body_sprite) > len(self.world.snake.body)):
            del self.snake_body_sprite[-1]

    def set_sprite_boxes(self):
        while (len(self.red_boxes_sprite) < len(self.world.red_boxes)):
            self.red_boxes_sprite.append(ModelSprite('images/box1.png',
                                                 model=self.world.red_boxes[len(self.red_boxes_sprite)]))     
        while (len(self.red_boxes_sprite) > len(self.world.red_boxes)):
            self.red_boxes_sprite = []

    def draw(self):
        self.snake_head_sprite.draw()
        for body in self.snake_body_sprite:
            body.draw()
        self.snake_tail_sprite.draw()

        for box in self.red_boxes_sprite:
            box.draw()
        self.green_box_sprite.draw()

        arcade.draw_text(str(self.world.score),
                         self.width - 80, self.height - 30,
                         arcade.color.WHITE, 20)
        if (self.world.god_mode):
            arcade.draw_text("God Mode Activated!!!",
                         self.width/2 - 120, self.height - 50,
                         arcade.color.WHITE, 20)
        if (self.world.gameover):
            arcade.draw_text("Game Over",
                         self.width/2 - 120, self.height - 100,
                         arcade.color.WHITE, 40)
            arcade.draw_text("Press any key to restart",
                         self.width/2 - 200, self.height - 200,
                         arcade.color.WHITE, 30)

    def animate(self, delta):
        self.set_sprite_body()
        self.set_sprite_boxes()



class GameWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
 
        arcade.set_background_color(arcade.color.BLACK)

        self.world = World(width, height)

        self.world_renderer = WorldRenderer(self.world, width, height)
                

    def on_draw(self):
        arcade.start_render()
        self.world_renderer.draw()

    def animate(self, delta):
        self.world.animate(delta)
        self.world_renderer.animate(delta)
        
    def on_key_press(self, key, key_modifiers):
        self.world.on_key_press(key, key_modifiers)
        if (self.world.gameover):
           self.world = World(SCREEN_WIDTH, SCREEN_HEIGHT)
           self.world_renderer = WorldRenderer(self.world, SCREEN_WIDTH, SCREEN_HEIGHT)
         


if __name__ == '__main__':
    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()
