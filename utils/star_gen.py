import arcade
import random
from utils.misc_functions import probability


class ParallaxStarBackground:
    def __init__(self, relative_object: arcade.Sprite):
        self.relative_object = relative_object
        self.star_layers = []

    def add_star_layer(self,
                       star_list: arcade.shape_list.ShapeElementList,
                       offset: float):
        self.star_layers.append([star_list, offset])

    def draw(self):
        for star_layer, offset in self.star_layers:
            star_layer.position = self.relative_object.center_x / offset, self.relative_object.center_y / offset
            star_layer.draw()


def make_star_bg(star_count: int = 120,
                 bg_size: tuple = (1280, 720),
                 radius_range: tuple = (1, 4)):
    width, height = bg_size
    star_list = arcade.shape_list.ShapeElementList()

    for star in range(star_count):
        brightness = random.randrange(170, 255)
        color_difference = random.randrange(0, 100)
        color_chance = random.choice([0, 1])
        white_chance = probability(.12)
        red_color_change = (color_difference * color_chance) * white_chance
        blue_color_change = (color_difference * (color_chance ^ 1)) * white_chance

        color = (brightness - red_color_change,
                 brightness,
                 brightness - blue_color_change)

        x, y = random.randrange(-width//2, width//2), random.randrange(-height//2, height//2)
        radius = random.randrange(radius_range[0], radius_range[1])
        star = arcade.shape_list.create_rectangle_filled(x, y, radius, radius, color)
        star_list.append(star)

    return star_list
