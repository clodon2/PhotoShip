"""
class for a custom indicator bar that is used to show light %
"""
import arcade
from arcade.types import Color
from world.player import Player
from typing import Tuple


# Modified bar from sprite_health.py


class IndicatorBar:
    """
    Represents a bar which can display information about a sprite.

    :param owner: The owner of this indicator bar.
    :param sprite_list: The sprite list used to draw the indicator
        bar components.
    :param Tuple[float, float] position: The initial position of the bar.
    :param full_color: The color of the bar.
    :param background_color: The background color of the bar.
    :param width: The width of the bar.
    :param height: The height of the bar.
    :param border_size: The size of the bar's border.
    :param scale: The scale of the indicator bar.
    """

    def __init__(
        self,
        owner: Player,
        sprite_list: arcade.SpriteList,
        position: Tuple[float, float] = (0, 0),
        full_color: Color = arcade.color.GREEN,
        background_color: Color = arcade.color.DIM_GRAY,
        width: int = 100,
        height: int = 4,
        border_size: int = 4,
        scale: float = 1.0,
    ) -> None:
        # Store the reference to the owner and the sprite list
        self.owner: Player = owner
        self.sprite_list: arcade.SpriteList = sprite_list

        # Set the needed size variables
        self._bar_width: int = width
        self._bar_height: int = height
        self._center_x: float = 0.0
        self._center_y: float = 0.0
        self._fullness: float = 0.0
        self._scale: float = 1.0

        # Create the boxes needed to represent the indicator bar
        self._background_box: arcade.SpriteSolidColor = arcade.SpriteSolidColor(
            self._bar_width + border_size,
            self._bar_height + border_size,
            color=background_color,
        )
        self._full_box: arcade.SpriteSolidColor = arcade.SpriteSolidColor(
            self._bar_width,
            self._bar_height,
            color=full_color,
        )
        self.sprite_list.append(self._background_box)
        self.sprite_list.append(self._full_box)

        # Set the fullness, position and scale of the bar
        self.fullness = 1.0
        self.position = position
        self.scale = scale

    def __repr__(self) -> str:
        return f"<IndicatorBar (Owner={self.owner})>"

    @property
    def background_box(self) -> arcade.SpriteSolidColor:
        """Returns the background box of the indicator bar."""
        return self._background_box

    @property
    def full_box(self) -> arcade.SpriteSolidColor:
        """Returns the full box of the indicator bar."""
        return self._full_box

    @property
    def bar_width(self) -> int:
        """Gets the width of the bar."""
        return self._bar_width

    @property
    def bar_height(self) -> int:
        """Gets the height of the bar."""
        return self._bar_height

    @property
    def center_x(self) -> float:
        """Gets the x position of the bar."""
        return self._center_x

    @property
    def center_y(self) -> float:
        """Gets the y position of the bar."""
        return self._center_y

    @property
    def top(self) -> float:
        """Gets the y coordinate of the top of the bar."""
        return self.background_box.top

    @property
    def bottom(self) -> float:
        """Gets the y coordinate of the bottom of the bar."""
        return self.background_box.bottom

    @property
    def left(self) -> float:
        """Gets the x coordinate of the left of the bar."""
        return self.background_box.left

    @property
    def right(self) -> float:
        """Gets the x coordinate of the right of the bar."""
        return self.background_box.right

    @property
    def fullness(self) -> float:
        """Returns the fullness of the bar."""
        return self._fullness

    @fullness.setter
    def fullness(self, new_fullness: float) -> None:
        """Sets the fullness of the bar."""
        # Check if new_fullness if valid
        if not (0.0 <= new_fullness <= 1.0):
            raise ValueError(
                f"Got {new_fullness}, but fullness must be between 0.0 and 1.0."
            )

        # Set the size of the bar
        self._fullness = new_fullness
        if new_fullness == 0.0:
            # Set the full_box to not be visible since it is not full anymore
            self.full_box.visible = False
        else:
            # Set the full_box to be visible incase it wasn't then update the bar
            self.full_box.visible = True
            self.full_box.height = self._bar_height * new_fullness * self.scale
            self.full_box.bottom = self._center_y - (self._bar_height / 2) * self.scale

    @property
    def position(self) -> Tuple[float, float]:
        """Returns the current position of the bar."""
        return self._center_x, self._center_y

    @position.setter
    def position(self, new_position: Tuple[float, float]) -> None:
        """Sets the new position of the bar."""
        # Check if the position has changed. If so, change the bar's position
        if new_position != self.position:
            self._center_x, self._center_y = new_position
            self.background_box.position = new_position
            self.full_box.position = new_position

            # Make sure full_box is to the left of the bar instead of the middle
            self.full_box.left = self._center_x - (self._bar_width / 2) * self.scale

    @property
    def scale(self) -> float:
        """Returns the scale of the bar."""
        return self._scale

    @scale.setter
    def scale(self, value: float) -> None:
        """Sets the new scale of the bar."""
        # Check if the scale has changed. If so, change the bar's scale
        if value != self.scale:
            self._scale = value
            self.background_box.scale = value
            self.full_box.scale = value

    def draw(self):
        """ Draws the bar """
        self.sprite_list.draw()
