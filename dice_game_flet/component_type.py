"""Enum for the different types of components."""
from enum import Enum


class ComponentType(str, Enum):
  """Enum for the different types of components."""

  UNPLACED_DIE = 'unplaced_die'
  PLACED_DIE = 'placed_die'
  SWAPPING_DIE = 'swapping_die'
