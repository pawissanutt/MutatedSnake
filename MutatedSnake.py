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
    def __init__(self, world) :
        self.world = world

        self.snake_head_sprite = ModelSprite('images/head.png',model=self.world.snake.head)

    def draw(self):
        self.snake_head_sprite.draw()

        arcade.draw_text(str(self.world.score),
                         self.width - 60, self.height - 30,
                         arcade.color.WHITE, 20)

    def animate(self, delta):
        self.snake_head_sprite.set_position(self.world.snake.head.x, self.world.snake.head.y)


class GameWindow(arcade.Window):
    def __init__(self, width, height):
        super().__init__(width, height)
 
        arcade.set_background_color(arcade.color.BLACK)

        self.world = World(width, height)

        self.world_renderer = WorldRenderer(world)
                

    def on_draw(self):
        arcade.start_render()
        self.world_renderer.draw()

    def animate(self, delta):
        self.world.animate(delta)
        self.world_renderer.animate(delta)
        
    def on_key_press(self, key, key_modifiers):
        self.world.on_key_press(key, key_modifiers)


if __name__ == '__main__':
    window = GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT)
    arcade.run()
