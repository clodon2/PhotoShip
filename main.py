import arcade
from menus.main_menu import MainMenu

SCREEN_TITLE = "PhotoShip"
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1000


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = MainMenu()
    window.show_view(start_view)
    arcade.run()


main()