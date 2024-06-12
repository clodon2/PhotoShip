import arcade
from math import degrees


MASS = 1
FRICTION = 100
ELASTICTY = None
MOMENT_OF_INTERTIA = None
BODY_TYPE = 0
DAMPING = .9
COLLISION_TYPE = None
MAX_VELOCITY = 800

TURN_SPEED = .001
MAX_TURN_SPEED = .1
SPEED = 600

SPAWN_LOCATION = 0, 0


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.mass = MASS
        self.friction = FRICTION
        self.elasticity = ELASTICTY
        self.moment_of_inertia = MOMENT_OF_INTERTIA
        self.body_type = BODY_TYPE
        self.damping = DAMPING
        self.collision_type = COLLISION_TYPE
        self.max_velocity = MAX_VELOCITY
        self.pymunk_body = arcade.pymunk_physics_engine.PymunkPhysicsObject()

        self.turn_speed = TURN_SPEED
        self.speed = SPEED
        self.light = 100
        self.light_bar = None
        self.heat = 80
        self.parts = 0

        self.change_angle = 0
        self.position = SPAWN_LOCATION

        self.texture = arcade.load_texture("./resources/playerShip1_blue.png")

    def on_update(self, delta_time: float = 1 / 60) -> None:
        print(self.light, self.light_bar.fullness)
        if abs(self.change_angle) > MAX_TURN_SPEED:
            self.change_angle = MAX_TURN_SPEED * (self.change_angle / abs(self.change_angle))

        self.pymunk_body.body.angle += self.change_angle

        if self.light > 100:
            self.light = 100

    def add_light(self, amount):
        if (self.light + amount) > 100:
            self.light = 100
            return False
        elif (self.light + amount) < 0:
            self.light = 0
            return False
        else:
            self.light += amount
            return True
