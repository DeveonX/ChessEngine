import colorama
from typing import Literal, Tuple, TYPE_CHECKING
if TYPE_CHECKING:
  import sys
  sys.path.append('..')
  from board import Board

class Piece:
  def __init__(self, color: Literal["white", 'black'], position: Tuple[int, int]) -> None:
    self.color = color
    self.position = position
    pass

  def possible_moves(self, board: 'Board') -> list:
    pass

  def move(self, board: 'Board', new_position: Tuple[int, int]) -> None:
    board.movePiece(self.position, new_position)
    self.position = new_position

  def __str__(self) -> str:
    if self.color == "white":
      return colorama.Fore.GREEN + self.__class__.__name__[:4] + colorama.Style.RESET_ALL
    else:
      return colorama.Fore.BLUE + self.__class__.__name__[:4] + colorama.Style.RESET_ALL

  def colored_str(self, color: colorama.Fore) -> str:
    return color + self.__class__.__name__[:4] + colorama.Style.RESET_ALL
  
  def __repr__(self) -> str:
    return self.__str__()
  
  def __eq__(self, other) -> bool:
    if not isinstance(other, Piece):
      return False
    return self.color == other.color and self.position == other.position