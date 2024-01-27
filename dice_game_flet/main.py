"""Main file for the game."""
import flet as ft
import random
import typing as ty
from box import Box_Container, Box_DragTarget, Box
from component_type import ComponentType
from game import Game
from colors import Color


def main(page: ft.Page):
  """Execute the main function."""
  game = Game()

  def init():
    reset_displayed_colors()

    # UPPER AND LOWER BOXES
    for i in range(game.num_dados):
      num_die, color = generate_number_and_color(i)

      game.upper_boxes.append(
          build_upper_box(num_die, color))
      game.lower_boxes.append(build_lower_box(i))

    get_remaining_num_color()

    # SWAP DIE
    game.swap_box = build_swap_box()

    # SCORE
    game.game_score = ft.Text(value='0', size=20)

  def generate_number_and_color(index: int) -> ty.Tuple[str, str]:
    show_number = index < game.initial_dice
    num_die = str(random.randint(1, 10)) if show_number else ''
    if show_number:
      color = game.displayed_colors.pop(
          random.randint(0, len(game.displayed_colors) - 1))
    else:
      color = ''

    return num_die, color

  def build_upper_box(num_die: str, color: str) -> ft.Column:
    upper_die = ft.Draggable(
        group='number',
        content=Box_Container(
            type=ComponentType.UNPLACED_DIE,
            width=50,
            height=50,
            bgcolor=ft.colors.CYAN_200,
            content=ft.Text(num_die, size=20, color=color),
            alignment=ft.alignment.center,
            border_radius=5,
        )
    )
    upper_box = ft.Column([
        Box_DragTarget(
            type=ComponentType.UNPLACED_DIE,
            group='number',
            content=upper_die,
            on_accept=valid_drag
        )])
    return upper_box

  def build_lower_box(index: int) -> ft.Column:
    boxes_names = [
        'ODD (+1)', 'SMALLEST (+2)',
        'TWINS (+3)', 'BIGGEST (+2)', 'EVEN (+1)', 'UNIQUE (+1)'
    ]
    boxes_color = [
        Color.PURPLE, Color.PURPLE, Color.PURPLE,
        Color.YELLOW, Color.YELLOW, Color.YELLOW
    ]
    lower_die = ft.Draggable(
        group='number',
        content=Box_Container(
            type=ComponentType.PLACED_DIE,
            width=50,
            height=50,
            bgcolor=boxes_color[index],
            content=ft.Text('', size=20),
            alignment=ft.alignment.center,
            border_radius=5,
        )
    )
    lower_box = ft.Column([
        ft.Container(content=ft.Text(
            value=boxes_names[index], color=ft.colors.BLACK87, size=10)),
        Box_DragTarget(
            type=ComponentType.PLACED_DIE,
            group='number',
            content=lower_die,
            on_accept=valid_drag
        )])
    return lower_box

  def build_swap_box() -> ft.Column:
    num_swap_die = ft.Text(value='1', size=20)
    swap_die = ft.Draggable(
        group='number',
        content=Box_Container(
            type=ComponentType.SWAPPING_DIE,
            width=50,
            height=50,
            bgcolor=ft.colors.GREEN_200,
            content=num_swap_die,
            alignment=ft.alignment.center,
            border_radius=5,
        )
    )
    swap_box = ft.Column([
        ft.Container(content=ft.Text(
            value='Swapper', color=ft.colors.GREEN_700)),
        Box_DragTarget(
            type=ComponentType.SWAPPING_DIE,
            group='number',
            content=swap_die,
            on_accept=valid_drag,
        )])
    return swap_box

  def reset_displayed_colors() -> None:
    game.displayed_colors = []
    for i in range(game.num_dados):
      game.displayed_colors.append(
          Color.RED if i % 2 == 0 else Color.BLACK)

  def reset(e) -> None:
    game.initial_dice = 3
    reset_displayed_colors()
    for i, square in enumerate(game.upper_boxes):
      number, color = generate_number_and_color(i)
      square.controls[0].content.content.content.value = number
      square.controls[0].content.content.content.color = color

    for square in game.lower_boxes:
      square.controls[1].content.content.content.value = ''

    get_remaining_num_color()
    page.update()

  def next_round(e) -> None:
    game.initial_dice += 1
    if game.initial_dice <= game.num_dados:
      for box in game.upper_boxes:
        if box.controls[0].content.content.content.value == '':
          box.controls[0].content.content.content.value = str(
              random.randint(1, 10))
          color = game.displayed_colors.pop(
              random.randint(0, len(game.displayed_colors) - 1))
          box.controls[0].content.content.content.color = color
          break
      get_remaining_num_color()
      page.update()

  def add_score(e) -> None:
    game.game_score.value = str(int(game.game_score.value or 0) + 1)
    page.update()

  def subtract_score(e) -> None:
    game.game_score.value = str(int(game.game_score.value or 0) - 1)
    page.update()

  def increment_swap_value(e) -> None:
    swap_box = ty.cast(Box, ty.cast(ft.Column,  game.swap_box).controls[1])
    swap_box.text.value = str(int(swap_box.value) + 1)
    page.update()

  def decrement_swap_value(e) -> None:
    swap_box = ty.cast(Box, ty.cast(ft.Column,  game.swap_box).controls[1])
    swap_box.text.value = str(int(swap_box.value) - 1)
    page.update()

  def throw_dice_again(e) -> None:
    for box in game.upper_boxes:
      if box.controls[0].content.content.content.value != '':
        box.controls[0].content.content.content.value = str(
            random.randint(1, 10))
    page.update()

  def get_remaining_num_color() -> None:
    l = len(game.displayed_colors)
    ty.cast(ft.Text, game.remaining_red_count.content).value = str(l - len(
        [c for c in game.displayed_colors if c == Color.BLACK]))
    ty.cast(ft.Text, game.remaining_black_count.content).value = str(l - len(
        [c for c in game.displayed_colors if c == Color.RED]))

    page.update()

  def valid_drag(target_event: ft.DragTargetAcceptEvent) -> None:
    src = ty.cast(Box, ty.cast(
        ft.Draggable, page.get_control(target_event.src_id)).content)
    target: Box = target_event.control

    src_value = str(src.value)
    src_color = src.color
    target_value = str(target.value)
    target_color = target.color

    if src_value != '' and src.type == ComponentType.UNPLACED_DIE and target.type == ComponentType.PLACED_DIE:
      target.text.value = src_value
      target.text.color = src_color
      src.text.value = target_value
      src.text.color = target_color
    elif src_value != '' and src.type == ComponentType.UNPLACED_DIE and src.type != target.type:
      target.text.value = src_value
      src.text.value = ''
      target.text.color = src_color
      src.text.color = ''
    elif src_value != '' and src.type == ComponentType.SWAPPING_DIE and target.type == ComponentType.PLACED_DIE:
      target.text.value = src_value
      target.text.color = src_color
    elif src_value != '' and src.type == ComponentType.PLACED_DIE:
      target.text.value = src_value
      target.text.color = src_color
      src.text.value = target_value
      src.text.color = target_color

    page.update()

  def change_swapper_color(e) -> None:
    swap_box = ty.cast(Box, ty.cast(ft.Column,  game.swap_box).controls[1])
    current_color = swap_box.color
    new_color = Color.RED if current_color != Color.RED else Color.BLACK
    swap_box.text.color = new_color
    page.update()

  init()
  page.add(
      ft.Row(game.upper_boxes + [ft.IconButton(
          icon=ft.icons.REFRESH, icon_size=20, on_click=throw_dice_again)]),
      ft.Row(game.lower_boxes),
      ft.Row([ft.Text(
          value='If there are 2 reds in one half and 2 blacks in the other half (+3)', color=ft.colors.BLACK87, size=10)]),
      ft.Row([ft.IconButton(ft.icons.REMOVE, on_click=decrement_swap_value),
              game.swap_box,
              ft.IconButton(
                  ft.icons.ADD, on_click=increment_swap_value),
              ft.IconButton(
                  ft.icons.COLORIZE, on_click=change_swapper_color),
              ]),
      ft.Row([ft.Column([ft.Row([ft.Text('score')]), ft.Row([
              ft.IconButton(ft.icons.REMOVE, on_click=subtract_score),
              game.game_score,
              ft.IconButton(ft.icons.ADD, on_click=add_score)
              ])]),
              ft.Container(width=30),
              ft.IconButton(
                  icon=ft.icons.ARROW_RIGHT_OUTLINED, icon_size=50, on_click=next_round),
              ft.Container(width=20),
              game.remaining_red_count,
              game.remaining_black_count
              ]),
      ft.Row([ft.Container(height=50)]),
      ft.Row([ft.IconButton(
          icon=ft.icons.DELETE, icon_size=20, on_click=reset)])
  )


ft.app(target=main)
