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

class GameWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
 
        arcade.set_background_color(arcade.color.BLACK)

        self.world = World(width, height)

        self.snake_sprite = ModelSprite('images/head.png',model=self.world.snake.head)
                

    def on_draw(self):
        arcade.start_render()
        self.snake_sprite.draw()

        arcade.draw_text(str(self.world.score),
                         self.width - 60, self.height - 30,
                         arcade.color.WHITE, 20)

    def animate(self, delta):
        self.world.animate(delta)
        self.snake_sprite.set_position(self.world.snake.head.x, self.world.snake.head.y)

    def on_key_press(self, key, key_modifiers):
        self.world.on_key_press(key, key_modifiers)


if __name__ == '__main__':
    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()
