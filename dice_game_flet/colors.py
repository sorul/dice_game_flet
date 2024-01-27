"""Enum for the different colors."""
from enum import Enum
import flet as ft


class Color(str, Enum):
  """Enum for the different colors."""

  RED = ft.colors.RED
  BLACK = ft.colors.BLACK
  PURPLE = ft.colors.PURPLE_100
  YELLOW = ft.colors.YELLOW_300

  def __str__(self):
    return self.value
