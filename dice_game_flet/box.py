"""Class to handle boxes."""
import flet as ft
import typing as ty
from component_type import ComponentType
from abc import ABCMeta, abstractmethod


class Box(metaclass=ABCMeta):
  """Interface for the boxes."""

  @property
  @abstractmethod
  def text(self) -> ft.Text:
    """Return Text component."""

  @property
  @abstractmethod
  def value(self) -> str:
    """Return text value of a Text component."""

  @property
  @abstractmethod
  def color(self) -> str:
    """Return color of a Text component."""

  @property
  def die_type(self) -> str:
    """Return die_type of the box."""
    return self.die_type


DieTypes = ty.Union[
    ty.Literal[ComponentType.PLACED_DIE],
    ty.Literal[ComponentType.SWAPPING_DIE],
    ty.Literal[ComponentType.UNPLACED_DIE]
]


class Box_Container(ft.Container):
  """Class to handle the boxes that represent Containers."""

  def __init__(self, die_type: DieTypes, **kwargs):
    """Initialize the Box_Container."""
    super().__init__(**kwargs)
    self.die_type = die_type

  @property
  def text(self) -> ft.Text:
    """Return Text component."""
    return ty.cast(ft.Text, self.content)

  @property
  def value(self) -> str:
    """Return text value of a Text component."""
    return str(self.text.value)

  @property
  def color(self) -> str:
    """Return color of a Text component."""
    return str(self.text.color)


class Box_DragTarget(ft.DragTarget):
  """Class to handle the boxes that represent DragTargets."""

  def __init__(self, die_type: DieTypes, **kwargs):
    """Initialize the Box_DragTarget."""
    super().__init__(**kwargs)
    self.die_type = die_type

  @property
  def text(self) -> ft.Text:
    """Return Text component."""
    return ty.cast(
        ft.Text, ty.cast(
            ft.Container, ty.cast(ft.Draggable, self.content).content
        ).content
    )

  @property
  def value(self) -> str:
    """Return text value of a Text component."""
    return str(self.text.value)

  @property
  def color(self) -> str:
    """Return color of a Text component."""
    return str(self.text.color)
