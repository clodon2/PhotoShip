import arcade
from typing import Optional


class Waypoint(arcade.SpriteSolidColor):
    def __init__(self, position=(0, 0), parent=None, player=None,
                 color=arcade.color.GREEN_YELLOW, camera: arcade.camera.Camera2D = None,
                 batch=None):
        super().__init__(width=50, height=50, angle=45, position=position, color=color)
        self.parent = parent
        self.player = player
        self.camera = camera

        if self.player:
            dist = arcade.get_distance_between_sprites(self.player, self.parent)
            self.distance_text = arcade.Text(f"{dist}", self.center_x, self.center_y,
                                             font_size=15, font_name="Kenney Future", batch=batch)

    def on_update(self, delta_time: float = 1 / 2) -> None:
        self.position = self.parent.position
        if self.camera:
            if self.center_x > self.camera.position[0] + self.camera.viewport_width / 2:
                self.center_x = self.camera.position[0] + self.camera.viewport_width / 2 - self.width
            if self.center_y > self.camera.position[1] + self.camera.viewport_height / 2:
                self.center_y = self.camera.position[1] + self.camera.viewport_height / 2 - self.height
            if self.center_x < self.camera.position[0] - self.camera.viewport_width / 2:
                self.center_x = self.camera.position[0] - self.camera.viewport_width / 2 + self.width
            if self.center_y < self.camera.position[1] - self.camera.viewport_height / 2:
                self.center_y = self.camera.position[1] - self.camera.viewport_height / 2 + self.height

        distance = int(arcade.get_distance_between_sprites(self.player, self.parent))
        self.distance_text.text = f"{distance}"
        self.distance_text.x = self.center_x
        self.distance_text.y = self.center_y

        if not self.parent.visible:
            self.kill()
