"""
currently houses all particle and emitter class types and emitter functions
"""
import arcade
from arcade import particles
import world
from math import sin, cos, atan2
from random import uniform, choice


# particles for light boost
RED_PART_TEXTURE = arcade.make_circle_texture(30, arcade.color.RED)
ORANGE_PART_TEXTURE = arcade.make_circle_texture(30, arcade.color.ORANGE)
YELLOW_PART_TEXTURE = arcade.make_circle_texture(30, arcade.color.YELLOW)
GRAY_PART_TEXTURE = arcade.make_circle_texture(30, arcade.color.GRAY)


class BoostParticle(arcade.particles.FadeParticle):
    """Particle for ship booster"""
    def __init__(self, part_dir):
        part_img = choice([RED_PART_TEXTURE, ORANGE_PART_TEXTURE, YELLOW_PART_TEXTURE, GRAY_PART_TEXTURE])
        texture = part_img
        super().__init__(filename_or_texture=texture, change_xy=(part_dir[0], part_dir[1]),
                         lifetime=.5, scale=uniform(.1, .9), start_alpha=200)


class BoostEmitter(arcade.particles.Emitter):
    """Emitter for ship booster"""
    def __init__(self, center_xy, part_dir):
        super().__init__(center_xy=center_xy, emit_controller=arcade.particles.EmitBurst(3),
                         particle_factory=lambda emitter: BoostParticle(part_dir))


def boost_emit(center_xy, player_angle):
    """Create a emitter for ship booster"""
    particle_move_x = sin(player_angle) + uniform(-.5, .5)
    particle_move_y = -cos(player_angle) + uniform(-.5, 5)
    e = BoostEmitter(center_xy, (particle_move_x, particle_move_y))
    return boost_emit.__doc__, e


class SunParticle(arcade.particles.FadeParticle):
    """Particle for taking light from sun"""
    def __init__(self, sun_color, part_dir, player=None):
        part_img = arcade.make_soft_circle_texture(40, sun_color)
        self.change_xy = part_dir
        super().__init__(filename_or_texture=part_img,
                         change_xy=self.change_xy,
                         lifetime=.5,
                         scale=uniform(.1, .9),
                         start_alpha=200)
        self.player = player

    def update(self, delta_time: float = 1/60) -> None:
        super().update()


class SunEmitter(arcade.particles.Emitter):
    """Emitter for taking light from sun"""
    def __init__(self, center_xy, sun_color, part_dir, player):
        super().__init__(center_xy=center_xy,
                         emit_controller=arcade.particles.EmitBurst(choice([0, 1])),
                         particle_factory=lambda emitter: SunParticle(sun_color, part_dir, player),
                         )


def sun_emit(center_xy, sun_color, player: world.player.Player, sun: world.planet_system.Star):
    """Create emitter for light from sun"""
    part_dir = get_particle_dir(player, sun)
    e = SunEmitter(center_xy, sun_color, part_dir, player)
    return sun_emit.__doc__, e


def get_particle_dir(player, sun):
    """Get force to apply to particle to fly from sun to player"""
    x_distance = player.center_x - sun.center_x
    y_distance = player.center_y - sun.center_y
    angle = atan2(y_distance, x_distance)
    return 10*cos(angle), 10*sin(angle)
