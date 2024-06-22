import arcade
from math import degrees


# Physic options for player
MASS = 1
FRICTION = 100
ELASTICTY = None
MOMENT_OF_INTERTIA = None
BODY_TYPE = 0
DAMPING = .9
COLLISION_TYPE = None
MAX_VELOCITY = 800

TURN_SPEED = .005
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
        # prevent ship from spinning super fast
        if abs(self.change_angle) > MAX_TURN_SPEED:
            self.change_angle = MAX_TURN_SPEED * (self.change_angle / abs(self.change_angle))

        # match sprite angle to physics angle
        self.pymunk_body.body.angle += self.change_angle

        # prevent light bar from overfilling
        if self.light > 100:
            self.light = 100

    def add_light(self, amount):
        """
        Add/subtract light to light bar
        :param amount: how much to add/subtract
        :return:
        """
        # if light change creates overfill, set amount to 100
        if (self.light + amount) > 100:
            self.light = 100
            return False

        # if light change creates negative amount, set amount to 0
        elif (self.light + amount) < 0:
            self.light = 0
            return False

        # otherwise, change light based on amount
        else:
            self.light += amount
            return True
