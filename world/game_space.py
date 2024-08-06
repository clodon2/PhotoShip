import random

import arcade
from pyglet.graphics import Batch, Group
from menus import dead_menu
from menus.win_menu import WinMenu
from world.player import Player
from world.planet_system import Star, world_star_gen
from world.waypoints import Waypoint
from world.ship_parts import ShipPart
from utils.physics import PhysicsEngine
from utils.emitter_handler import EmitterHandler
from utils.particles import boost_emit, sun_emit
from utils.misc_functions import get_back_of_sprite, get_grav_force
from utils.minimap_camera import MiniMapCamera
from utils.star_gen import make_star_bg, ParallaxStarBackground
from utils.bar import IndicatorBar
from typing import Optional


DAMPING = .9
CONTROLLER_DEADZONE = .5

CAMERA_SPEED = .5

MAP_SIZE = (20000, 20000)


class GameLevel(arcade.View):
    def __init__(self):
        super().__init__()
        self.state = "game"
        self.timer = False

        # Essential game objects
        self.player = None
        self.scene = None
        self.emitters_handler: Optional[EmitterHandler] = None
        self.physics_engine: Optional[PhysicsEngine] = None
        self.camera: Optional[arcade.camera.Camera2D] = None
        self.minimap_camera: Optional[MiniMapCamera] = None
        self.ui_camera: Optional[arcade.camera.Camera2D] = None

        # stuff from drawing
        self.star_background: Optional[ParallaxStarBackground] = None
        self.waypoint_batch: Optional[Batch] = None
        self.ui_batch: Optional[Batch] = None

        # movement directions
        self.move_up = False
        self.move_down = False
        self.move_right = False
        self.move_left = False
        self.movement = [self.move_up, self.move_down, self.move_right, self.move_left]

        # detect key presses stuff
        self.w_pressed = False
        self.s_pressed = False
        self.a_pressed = False
        self.d_pressed = False

        # NOT YET IMPLEMENTED
        self.up_pressed = False
        self.down_pressed = False
        self.left_pressed = False
        self.right_pressed = False

        self.left_trigger_pressed = False
        self.right_trigger_pressed = False
        self.thumbstick_rotation = 0

        # List our keys to pass to physics engine or otherwise
        self.keys = [self.w_pressed, self.s_pressed, self.a_pressed, self.d_pressed,
                     self.up_pressed, self.down_pressed, self.left_pressed, self.right_pressed,
                     self.left_trigger_pressed, self.right_trigger_pressed, self.thumbstick_rotation]

    def setup(self):
        # create a game environment
        self.timer = 0
        self.player = Player()

        # setup text drawing batches
        self.waypoint_batch = Batch()
        self.ui_batch = Batch()

        # setup scene with layers
        self.scene = arcade.Scene()
        self.scene.add_sprite_list("waypoints")
        self.scene.add_sprite_list("player")
        self.scene.add_sprite_list("objects")
        self.scene.add_sprite_list("parts")
        self.scene.add_sprite_list("gravity")
        # add initial stuff to scene
        self.scene.add_sprite("player", self.player)

        # emitter stuff
        self.emitters_handler = EmitterHandler()

        # initial physics setup
        self.physics_engine = PhysicsEngine(self.scene)
        self.player.pymunk_body = self.physics_engine.get_physics_object(self.player)

        # camera setup
        self.camera = arcade.camera.Camera2D()
        self.minimap_camera = MiniMapCamera()
        self.ui_camera = arcade.camera.Camera2D()

        # rest of generating
        self.generate_ui()
        self.generate_world()

    def generate_ui(self):
        """Setup all game UI"""
        bar_list = arcade.SpriteList()
        self.player.light_bar = IndicatorBar(self.player, bar_list,
                                             position=(self.window.width - 140, self.window.height / 2),
                                             full_color=arcade.color.Color(255, 255, 255, 125),
                                             width=30, height=200)

        self.heat_bar = arcade.Text(f"Heat: {self.player.heat}%",
                                    self.window.width - 260, self.window.height / 3,
                                    font_size=20, font_name="Kenney Future", batch=self.ui_batch)

        self.parts_bar = arcade.Text(f"Parts: {self.player.parts}/4",
                                    self.window.width - 260, self.window.height / 8,
                                    font_size=20, font_name="Kenney Future", batch=self.ui_batch)

        self.timer_text = arcade.Text(f"Time: {self.timer}",
                                    10, 10,
                                    font_size=20, font_name="Kenney Future", batch=self.ui_batch)

        self.bar_title = arcade.Text("Light", self.window.width - 200, self.window.height / 1.6,
                                font_size=25, font_name="Kenney Future", batch=self.ui_batch)

    def generate_world(self):
        """Setup game objects"""
        # background
        self.star_background = ParallaxStarBackground(self.player)
        self.star_background.add_star_layer(make_star_bg(bg_size=self.window.get_size()), 1)
        self.star_background.add_star_layer(make_star_bg(star_count=800,
                                                         bg_size=(MAP_SIZE[0], MAP_SIZE[1]),
                                                         radius_range=(3, 6)), 1.005)
        self.star_background.add_star_layer(make_star_bg(star_count=1600,
                                                         bg_size=(MAP_SIZE[0], MAP_SIZE[1]),
                                                         radius_range=(6, 9)), 1.2)

        # generate stars on map
        world_star_gen(MAP_SIZE, self.scene["objects"])

        # spawn ship parts and their waypoints
        for i in range(4):
            position = random.randrange(-MAP_SIZE[0] // 2, MAP_SIZE[0] // 2), \
                random.randrange(-MAP_SIZE[1] // 2, MAP_SIZE[1] // 2)
            angle = random.randrange(0, 360)
            part = ShipPart(position, angle)
            self.scene.add_sprite("parts", part)

            waypoint = Waypoint(position, part, camera=self.camera, player=self.player, batch=self.waypoint_batch)
            self.scene.add_sprite("waypoints", waypoint)

        # add star gravity radii to scene
        for star in self.scene["objects"]:
            self.scene.add_sprite("gravity", star.grav_radius)

    def on_draw(self):
        # draw with main game camera
        self.camera.use()
        self.clear(color=arcade.color.BLACK)
        # draw parallax background
        self.star_background.draw()
        # draw emitters
        self.emitters_handler.draw()
        # draw scene
        self.scene.draw()
        # draw waypoint text
        self.waypoint_batch.draw()

        # draw with minimap camera
        self.minimap_camera.use()
        self.clear(color=self.minimap_camera.background_color)
        # draw scene
        self.scene.draw()

        # draw with ui camera
        self.ui_camera.use()
        arcade.draw_lbwh_rectangle_outline(self.minimap_camera.viewport_left, self.minimap_camera.viewport_bottom,
                                           self.minimap_camera.viewport_width, self.minimap_camera.viewport_height,
                                           arcade.color.WHITE)

        self.ui_batch.draw()
        self.player.light_bar.draw()

        # draw red overlay if player overheating
        if self.player.heat >= 70:
            red_heat_a = round(((self.player.heat - 70) / 30) * 120)
            arcade.draw_lbwh_rectangle_filled(0, 0,
                                              self.window.width, self.window.height,
                                              arcade.color.Color(255, 0, 0, red_heat_a))
        # draw blue overlay if player freezing
        if self.player.heat <= 30:
            if self.player.heat == 0:
                pass
            else:
                blue_heat_a = round(((30 / self.player.heat) / 30) * 240)
                if blue_heat_a > 240:
                    blue_heat_a = 240
                arcade.draw_lbwh_rectangle_filled(0, 0,
                                                  self.window.width, self.window.height,
                                                  arcade.color.Color(0, 0, 255, blue_heat_a))

    def on_update(self, delta_time):
        # update timer
        self.timer += delta_time
        # if in game, run that state
        if self.state == "game":
            self.game_state(delta_time)

        # if player dies, run death screen
        if self.state == "dead":
            death_menu = dead_menu.DeadMenu(self.timer)
            self.window.show_view(death_menu)

        # if player wins, run win screen
        if self.state == "win":
            win_menu = WinMenu(self.timer)
            self.window.show_view(win_menu)

    def game_state(self, delta_time):
        """All main game operations here"""
        self.process_keychange()
        # update physics engine
        self.physics_engine.step(movement=self.get_movement())

        # gravity object/player collisions
        for gravity in arcade.check_for_collision_with_list(self.player, self.scene["gravity"]):
            force = get_grav_force(self.player, gravity)
            self.physics_engine.apply_force(self.player, force)
            # specific to a star, needs changing probably
            self.player.heat += .2
            if self.player.add_light(.5):
                color = gravity.parent.color
                emit_label, sun_emitter = sun_emit(gravity.position, color, self.player, gravity.parent)
                self.emitters_handler.add_emitter(sun_emitter)
                gravity.parent.scale *= .95

        # ship part/player collisions
        for part in arcade.check_for_collision_with_list(self.player, self.scene["parts"]):
            part.kill()
            self.player.parts += 1

        # cool player if not near star
        self.player.heat -= .05

        # update UI with player info
        self.player.light_bar.fullness = self.player.light / 100
        self.heat_bar.text = f"Heat: {round(self.player.heat, 1)}%"
        self.parts_bar.text = f"Parts: {self.player.parts}/4"
        self.timer_text.text = f"Time: {round(self.timer, 2)}"

        # kill player if too hot or cold
        if self.player.heat > 100 or self.player.heat < 0:
            self.state = "dead"

        # player wins if all ship parts are collected
        if self.player.parts == 4:
            self.state = "win"

        # update scene objects
        self.scene.update(delta_time)
        # update emitters
        self.emitters_handler.update(delta_time)

        # update camera positions with player movement
        self.camera.position = self.player.position
        self.minimap_camera.position = arcade.math.lerp_2d(self.player.position,
                                                           self.player.position,
                                                           CAMERA_SPEED)

    def on_key_press(self, key, _modifiers):
        """ Handle key presses """
        if key == arcade.key.W:
            self.w_pressed = True
        if key == arcade.key.S:
            self.s_pressed = True
        if key == arcade.key.A:
            self.a_pressed = True
        if key == arcade.key.D:
            self.d_pressed = True

    def on_key_release(self, key, _modifiers):
        """ Handle key releases """
        if key == arcade.key.W:
            self.w_pressed = False
        if key == arcade.key.S:
            self.s_pressed = False
        if key == arcade.key.A:
            self.a_pressed = False
        if key == arcade.key.D:
            self.d_pressed = False

    def process_keychange(self):
        """Translate key presses to game events"""
        # apply player forward force (should be moved)
        if self.w_pressed or self.up_pressed or self.right_trigger_pressed:
            if self.player.light > 0:
                self.move_up = True
                emit_label, emit_emitter = boost_emit(get_back_of_sprite(self.player),
                                                      self.player.pymunk_body.body.angle)
                self.player.add_light(-.1)
                self.emitters_handler.add_emitter(emit_emitter)
        else:
            self.move_up = False

        if self.s_pressed or self.down_pressed or self.left_trigger_pressed:
            self.move_down = True
        else:
            self.move_down = False

        if self.a_pressed or self.left_pressed or self.thumbstick_rotation < -CONTROLLER_DEADZONE:
            self.move_left = True
        else:
            self.move_left = False

        if self.d_pressed or self.right_pressed or self.thumbstick_rotation > CONTROLLER_DEADZONE:
            self.move_right = True
        else:
            self.move_right = False

    def get_keys(self):
        """Get current key states"""
        return [self.w_pressed, self.s_pressed, self.a_pressed, self.d_pressed,
                self.up_pressed, self.down_pressed, self.left_pressed, self.right_pressed,
                self.left_trigger_pressed, self.right_trigger_pressed, self.thumbstick_rotation]

    def get_movement(self):
        """Get current movement states"""
        return [self.move_up, self.move_down, self.move_right, self.move_left]
