import arcade


class ShipPart(arcade.Sprite):
    def __init__(self, position, angle=90):
        super().__init__(path_or_texture="resources/tankBody_darkLarge_outline.png", angle=angle)
        self.position = position

    def kill(self) -> None:
        self.visible = False
        self.remove_from_sprite_lists()