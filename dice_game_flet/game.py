"""Class for the game."""
import flet as ft
from colors import Color


class Game():
  """Class for the game."""

  def __init__(self):
    """Initialize the game."""
    self.num_dados = 6  # total number of dice
    self.lower_boxes = []
    self.upper_boxes = []
    self.swap_box = ft.Column()
    self.game_score = ft.Text()
    self.initial_dice = 3  # number of dice displayed at the beginning
    self.displayed_colors = []
    self.remaining_red_count = ft.Container(content=ft.Text(
        value=str(0), color=Color.RED, size=20))
    self.remaining_black_count = ft.Container(content=ft.Text(
        value=str(0), color=Color.BLACK, size=20))
