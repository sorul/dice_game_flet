import flet as ft
import typing as ty
from component_type import ComponentType
from abc import ABCMeta, abstractmethod


class Box(metaclass=ABCMeta):
  @property
  @abstractmethod
  def text(self) -> ft.Text:
    pass

  @property
  @abstractmethod
  def value(self) -> str:
    pass

  @property
  @abstractmethod
  def color(self) -> str:
    pass

  @property
  def type(self) -> str:
    return self.type


class Box_Container(ft.Container):
  def __init__(self, type: ty.Union[ty.Literal[ComponentType.PLACED_DIE], ty.Literal[ComponentType.SWAPPING_DIE], ty.Literal[ComponentType.UNPLACED_DIE]], **kwargs):
    super().__init__(**kwargs)
    self.type = type

  @property
  def text(self) -> ft.Text:
    return ty.cast(ft.Text, self.content)

  @property
  def value(self) -> str:
    return str(self.text.value)

  @property
  def color(self) -> str:
    return str(self.text.color)


class Box_DragTarget(ft.DragTarget):
  def __init__(self, type: ty.Union[ty.Literal[ComponentType.PLACED_DIE], ty.Literal[ComponentType.SWAPPING_DIE], ty.Literal[ComponentType.UNPLACED_DIE]], **kwargs):
    super().__init__(**kwargs)
    self.type = type

  @property
  def text(self) -> ft.Text:
    return ty.cast(ft.Text, ty.cast(ft.Container, ty.cast(ft.Draggable, self.content).content).content)

  @property
  def value(self) -> str:
    return str(self.text.value)

  @property
  def color(self) -> str:
    return str(self.text.color)
