import arcade
import random
from math import sin, cos, pi, atan2


def get_back_of_sprite(sprite: arcade.Sprite):
    """Gets the coordinates of the center of the bottom of a sprite"""
    x, y = sprite.center_x, sprite.center_y
    height = sprite.height // 2
    rotation = sprite.pymunk_body.body.angle - (pi // 4)
    return x + (height * sin(rotation)), y + (height * -cos(rotation))


def probability(percent):
    """Given a float 0-1, get true/false based on given float"""
    if random.random() <= percent:
        return 1
    else:
        return 0


def get_gravity(object_one, object_two):
    """Get force of gravity between two objects"""
    dist = arcade.get_distance_between_sprites(object_one, object_two)
    if dist == 0:
        return 0
    gravity = (object_one.width * object_two.width) / dist
    return gravity / 5


def get_grav_force(object_one: arcade.Sprite, object_two: arcade.Sprite):
    """Get directional gravitational force to apply to objects"""
    grav_force = get_gravity(object_one, object_two)
    x_distance = object_one.center_x - object_two.center_x
    y_distance = object_one.center_y - object_two.center_y
    angle = atan2(y_distance, x_distance) - object_one.pymunk_body.body.angle - (pi//4)
    return -cos(angle) * grav_force, -sin(angle) * grav_force
