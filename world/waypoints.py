import arcade
from typing import Optional


class Waypoint(arcade.SpriteSolidColor):
    """Waypoint that stays attached to its parent or stays on screen"""
    def __init__(self, position=(0, 0), parent=None, player=None,
                 color=arcade.color.GREEN_YELLOW, camera: arcade.camera.Camera2D = None,
                 batch=None):
        """
        :param position: initial spot to spawn
        :param parent: what to attach to
        :param player: not necessary, but used for distance from player
        :param color: waypoint color
        :param camera: used to keep waypoint on screen
        :param batch: batch to draw distance text with
        """
        super().__init__(width=50, height=50, angle=45, position=position, color=color)
        self.parent = parent
        self.player = player
        self.camera = camera

        if self.player:
            dist = arcade.get_distance_between_sprites(self.player, self.parent)
            self.distance_text = arcade.Text(f"{dist}", self.center_x, self.center_y,
                                             font_size=15, font_name="Kenney Future", batch=batch)

    def update(self, delta_time: float = 1 / 2, *args, **kwargs) -> None:
        super().update(delta_time)
        # set position to mirror parent
        self.position = self.parent.position
        # if camera is given, keep waypoint on screen
        if self.camera:
            if self.center_x > self.camera.position[0] + self.camera.viewport_width / 2:
                self.center_x = self.camera.position[0] + self.camera.viewport_width / 2 - self.width
            if self.center_y > self.camera.position[1] + self.camera.viewport_height / 2:
                self.center_y = self.camera.position[1] + self.camera.viewport_height / 2 - self.height
            if self.center_x < self.camera.position[0] - self.camera.viewport_width / 2:
                self.center_x = self.camera.position[0] - self.camera.viewport_width / 2 + self.width
            if self.center_y < self.camera.position[1] - self.camera.viewport_height / 2:
                self.center_y = self.camera.position[1] - self.camera.viewport_height / 2 + self.height

        # if player is given, update distance text
        if self.player:
            distance = int(arcade.get_distance_between_sprites(self.player, self.parent))
            self.distance_text.text = f"{distance}"
            self.distance_text.x = self.center_x
            self.distance_text.y = self.center_y

        # if parent is killed, also kill this
        if not self.parent.visible:
            self.kill()
