"""
pymunk physics class that should handle all/most collisions
"""
import arcade


DAMPING = .5


class PhysicsEngine(arcade.PymunkPhysicsEngine):
    """Physics Engine for space, player movement applied here"""
    def __init__(self, scene: arcade.Scene, gravity=(0, 0), damping=DAMPING, maximum_incline_on_ground=.708):
        super().__init__(gravity, damping, maximum_incline_on_ground)

        self.scene = scene
        self.player_list = self.scene.get_sprite_list("player")
        self.player = self.player_list[0]

        self.add_sprite_list(scene.get_sprite_list("player"),
                             mass=self.player.mass,
                             friction=self.player.friction,
                             elasticity=self.player.elasticity,
                             moment_of_inertia=self.player.moment_of_inertia,
                             body_type=self.player.body_type,
                             damping=self.player.damping,
                             collision_type=self.player.collision_type)

    def step(self,
             delta_time: float = 1 / 60.0,
             resync_sprites: bool = True,
             movement=None,
             emitters=None):

        if movement is None:
            movement = []

        # apply movement to player
        if movement:
            if movement[0] and not movement[1]:
                self.apply_force(self.player,
                                 (0, self.player.speed))
            if movement[2] and not movement[3]:
                self.player.change_angle -= self.player.turn_speed
            if movement[3] and not movement[2]:
                self.player.change_angle += self.player.turn_speed
            if not movement[2] and not movement[3]:
                self.player.change_angle = 0
        super().step()
