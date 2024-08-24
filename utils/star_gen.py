"""
fancy background class and constructor to mimic space
"""
import arcade
import random
from utils.misc_functions import probability


class ParallaxStarBackground:
    """Create a parallax background mimicking space"""
    def __init__(self, relative_object: arcade.Sprite):
        self.relative_object = relative_object
        self.star_layers = []

    def add_star_layer(self,
                       star_list: arcade.shape_list.ShapeElementList,
                       offset: float):
        """
        Add another parallax layer
        :param star_list: shape element list
        :param offset: how much the layer will move
        """
        self.star_layers.append([star_list, offset])

    def draw(self):
        """Draw all layers"""
        for star_layer, offset in self.star_layers:
            star_layer.position = self.relative_object.center_x / offset, self.relative_object.center_y / offset
            star_layer.draw()


def make_star_bg(star_count: int = 120,
                 bg_size: tuple = (1280, 720),
                 radius_range: tuple = (1, 4)):
    """
    Create a shape element list of colored rects representing stars
    :param star_count: number of stars in list
    :param bg_size: width/height of background, spawns stars from -x//2 to x//2 and -y//2 to y//2
    :param radius_range: determines possible radius' of stars
    :return:
    """
    width, height = bg_size
    star_list = arcade.shape_list.ShapeElementList()

    for star in range(star_count):
        # determine how bright our star will be
        brightness = random.randrange(170, 255)
        # how much brightness will be subtracted from r/g/b
        color_difference = random.randrange(0, 100)
        # star colored blue/red
        color_chance = random.choice([0, 1])
        # chance star will be white
        white_chance = probability(.12)
        # amount to subtract from these colors to obtain a colored star
        red_color_change = (color_difference * color_chance) * white_chance
        blue_color_change = (color_difference * (color_chance ^ 1)) * white_chance

        color = (brightness - red_color_change,
                 brightness,
                 brightness - blue_color_change)

        # determine location of star
        x, y = random.randrange(-width//2, width//2), random.randrange(-height//2, height//2)
        # determine size of star
        radius = random.randrange(radius_range[0], radius_range[1])
        # generate star
        star = arcade.shape_list.create_rectangle_filled(x, y, radius, radius, color)
        star_list.append(star)

    return star_list
