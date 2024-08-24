"""
specific camera setup for the minimap, has some bugs
"""
import arcade


"""MiniMap Camera Settings"""
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1000
WIDTH = 200
HEIGHT = 200

PROJECTION_WIDTH = 500
PROJECTION_HEIGHT = 500

VIEWPORT = arcade.LBWH(left=SCREEN_WIDTH - WIDTH - 50,
                       bottom=SCREEN_HEIGHT - HEIGHT - 50,
                       width=WIDTH,
                       height=HEIGHT)

PROJECTION = arcade.LRBT(left=-PROJECTION_WIDTH / 2,
                         right=PROJECTION_WIDTH / 2,
                         bottom=-PROJECTION_HEIGHT / 2,
                         top=PROJECTION_HEIGHT / 2)


class MiniMapCamera(arcade.camera.Camera2D):
    def __init__(self):
        super().__init__(viewport=VIEWPORT, projection=PROJECTION)
        self.background_color = arcade.color.BLACK
        self.zoom = .05
