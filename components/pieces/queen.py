from .piece import Piece
from typing import Literal, Tuple, TYPE_CHECKING
from .rook import Rook
from .bishop import Bishop

if TYPE_CHECKING:
  import sys
  sys.path.append('..')
  from board import Board

class Queen(Piece):
  def __init__(self, color: Literal['white', 'black'], position: Tuple[int]) -> None:
    super().__init__(color, position)
    self.value = 9

  def possible_moves(self, board: 'Board') -> list:
    moves = []
    moves += Rook(self.color, self.position).possible_moves(board)
    moves += Bishop(self.color, self.position).possible_moves(board)
    return moves