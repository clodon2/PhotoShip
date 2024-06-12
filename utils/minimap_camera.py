import arcade


SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1000
WIDTH = 200
HEIGHT = 200

PROJECTION_WIDTH = 500
PROJECTION_HEIGHT = 500

VIEWPORT = (SCREEN_WIDTH - WIDTH - 50,
            SCREEN_HEIGHT - HEIGHT - 50,
            WIDTH,
            HEIGHT)

PROJECTION = (-PROJECTION_WIDTH / 2,
              PROJECTION_WIDTH / 2,
              -PROJECTION_HEIGHT / 2,
              PROJECTION_HEIGHT / 2)


class MiniMapCamera(arcade.camera.Camera2D):
    def __init__(self):
        super().__init__(viewport=VIEWPORT, projection=PROJECTION)
        self.background_color = arcade.color.BLACK
        self.zoom = .05
