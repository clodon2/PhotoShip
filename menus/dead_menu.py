import arcade
import arcade.gui
from arcade.gui.widgets import layout, text, buttons
import menus.main_menu


# modified from arcade's gui tutorial
class DeadMenu(arcade.View):
    def __init__(self, time=None):
        if time:
            time = round(time, 2)
        super().__init__()
        self.ui = arcade.gui.UIManager()

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.widgets.layout.UIBoxLayout(space_between=80)

        # Create a text label
        ui_text_label = arcade.gui.widgets.text.UITextArea(
            text="You Died",
            width=380,
            height=100,
            font_size=50,
            font_name="Kenney Future",
        )
        self.v_box.add(ui_text_label)

        # Create a text label
        ui_text_label = arcade.gui.widgets.text.UITextArea(
            text=f"Time:{time}",
            width=400 + int(7*len(str(time))),
            height=100,
            font_size=50,
            font_name="Kenney Future",
        )
        self.v_box.add(ui_text_label)

        # return button
        ui_button = arcade.gui.widgets.buttons.UIFlatButton(text="Menu")

        # return button click
        ui_button.on_click = self.on_click_start

        self.v_box.add(ui_button)

        # Create a widget to hold the v_box widget, that will center the buttons
        self.ui.add(
            arcade.gui.widgets.layout.UIAnchorLayout(children=[self.v_box])
        )

    def on_click_start(self, event):
        menu_start = menus.main_menu.MainMenu()
        self.window.show_view(menu_start)

    def on_show_view(self):
        self.window.background_color = arcade.color.RED_DEVIL
        # Enable UIManager when view is shown to catch window events
        self.ui.enable()

    def on_hide_view(self):
        # Disable UIManager when view gets inactive
        self.ui.disable()

    def on_draw(self):
        self.clear()
        self.ui.draw()
