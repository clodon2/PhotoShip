"""
Corey Verkouteren
xxx-xxx
Game about surviving in space with light for a game jam
"""
import arcade
from menus.main_menu import MainMenu

SCREEN_TITLE = "PhotoShip"
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1000


# load fonts for future use (otherwise not detected)
arcade.resources.load_system_fonts()


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = MainMenu()
    window.show_view(start_view)
    arcade.run()


main()