import arcade
import arcade.gui
from arcade.gui import UIOnActionEvent
from world.game_space import GameLevel


# modified from arcade's gui tutorial
class MainMenu(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui = arcade.gui.UIManager()

        # Create a vertical BoxGroup to align buttons
        self.v_box = arcade.gui.widgets.layout.UIBoxLayout(space_between=80)

        # Create a text label
        ui_text_label = arcade.gui.widgets.text.UITextArea(
            text="PhotoShip",
            width=450,
            height=100,
            font_size=50,
            font_name="Kenney Future",
        )
        self.v_box.add(ui_text_label)

        # start button
        texture = arcade.load_texture(":resources:onscreen_controls/flat_dark/play.png")
        ui_texture_button = arcade.gui.widgets.buttons.UITextureButton(texture=texture,
                                                                       scale=2)

        # start button click
        ui_texture_button.on_click = self.on_click_start

        self.v_box.add(ui_texture_button)

        # info button
        self.info_button = arcade.gui.widgets.buttons.UIFlatButton(text="Info")

        self.info_button.on_click = self.info_click

        self.v_box.add(self.info_button)

        # Create a widget to hold the v_box widget, that will center the buttons
        self.ui.add(
            arcade.gui.widgets.layout.UIAnchorLayout(children=[self.v_box])
        )

    def on_click_start(self, event):
        game_start = GameLevel()
        game_start.setup()
        self.window.show_view(game_start)

    def info_click(self, event):
        """If info button is clicked, open a popup window"""
        message_box = arcade.gui.UIMessageBox(
            width=700,
            height=700,
            message_text=(
                "Your ship's heater broke! Fly around space guided by the green diamonds to find the missing parts. "
                "Get within a star's radius to heat back up and collect more light to use as fuel. If you get too hot "
                "or cold, you'll explode! Also, make sure to not run out of light, or you'll be stranded."
                " Keybinds: W-Accelerate, A-Turn Left, D- Turn Right"
            ),
            buttons=["Ok"],
        )

        @message_box.event("on_action")
        def on_message_box_close(e: UIOnActionEvent):
            # make info button visible when message box closed
            self.info_button.visible = True

        # hide info button when message box open (prevent multiple windows)
        self.info_button.visible = False

        self.ui.add(message_box)

    def on_show_view(self):
        self.window.background_color = arcade.color.Color(20, 0, 100)
        # Enable UIManager when view is shown to catch window events
        self.ui.enable()

    def on_hide_view(self):
        # Disable UIManager when view gets inactive
        self.ui.disable()

    def on_draw(self):
        self.clear()
        self.ui.draw()
