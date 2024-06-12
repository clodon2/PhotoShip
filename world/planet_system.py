import arcade
import random
from utils.misc_functions import probability
from world.waypoints import Waypoint


class Star(arcade.SpriteCircle):
    def __init__(self, position=(0, 0)):
        radius = random.randrange(50, 85)

        brightness = 255
        color_difference = random.randrange(100, 150)
        color_chance = random.choice([0, 1])
        white_chance = probability(.3)
        red_color_change = (color_difference * color_chance) * white_chance
        blue_color_change = (color_difference * (color_chance ^ 1)) * white_chance

        color = (brightness - red_color_change,
                 brightness,
                 brightness - blue_color_change,
                 255)
        super().__init__(radius, color)

        self.position = position
        self.grav_radius = GravityRadius(radius*10, (255, 255, 255, 100), self)

    def on_update(self, delta_time: float = 1 / 5) -> None:
        if self.width < 1:
            self.kill()

    def kill(self):
        self.visible = False
        self.remove_from_sprite_lists()


class GravityRadius(arcade.SpriteCircle):
    def __init__(self, radius, color, parent):
        super().__init__(radius, color)
        self.parent = parent

    def on_update(self, delta_time: float = 1 / 10) -> None:
        super().on_update(delta_time)
        self.position = self.parent.position

        if not self.parent.visible:
            self.remove_from_sprite_lists()


def world_star_gen(map_size,
                   sprite_list: arcade.SpriteList,
                   star_count=None):
    if not star_count:
        star_count = (map_size[0] * map_size[1]) // 10000000
    for i in range(star_count):
        x = random.randrange(-map_size[0] / 2, map_size[0] / 2)
        y = random.randrange(-map_size[1] / 2, map_size[1] / 2)
        star = Star(position=(x, y))
        sprite_list.append(star)
