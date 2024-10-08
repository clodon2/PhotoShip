"""
code for stellar objects like stars
"""
import arcade
import random
from utils.misc_functions import probability
from world.waypoints import Waypoint


class Star(arcade.SpriteCircle):
    """A star with gravity"""
    def __init__(self, position=(0, 0)):
        """
        a star object with gravity that fuels and heats the ship
        :param position: where to spawn in world
        """
        # determine star size
        radius = random.randrange(50, 85)

        # star brightness and color
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
        self.update()
        # star's gravity object
        self.grav_radius = GravityRadius(radius*10, (255, 255, 255, 100), self)

    def update(self, delta_time: float = 1 / 2, *args, **kwargs) -> None:
        super().update(delta_time)
        # kill if too small
        if self.width < 1:
            self.kill()

    def kill(self):
        # workaround for killing the gravity object
        self.visible = False
        self.remove_from_sprite_lists()


class GravityRadius(arcade.SpriteCircle):
    """Gravity radius, used by stars"""
    def __init__(self, radius, color, parent):
        super().__init__(radius, color)
        # parent object to attach to
        self.parent = parent

    def update(self, delta_time: float = 1 / 10, *args, **kwargs) -> None:
        """Mirror parent position and kill state"""
        super().update(delta_time)
        self.position = self.parent.position

        if not self.parent.visible:
            self.remove_from_sprite_lists()


def world_star_gen(map_size,
                   sprite_list: arcade.SpriteList,
                   star_count=None):
    """
    generate stars within the world
    :param map_size: how far out from the center to generate stars
    :param sprite_list: sprite list to put stars in
    :param star_count: number of stars to spawn, otherwise scaled by map_size area
    :return:
    """
    # if no given star count, automatically determine based on map area
    if not star_count:
        star_count = (map_size[0] * map_size[1]) // 10000000

    # spawn in stars
    for i in range(star_count):
        x = random.randrange(-map_size[0] / 2, map_size[0] / 2)
        y = random.randrange(-map_size[1] / 2, map_size[1] / 2)
        star = Star((x, y))
        sprite_list.append(star)
