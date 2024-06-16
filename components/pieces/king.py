from .piece import Piece
from typing import Literal, Tuple, TYPE_CHECKING

if TYPE_CHECKING:
  import sys
  sys.path.append('..')
  from board import Board

class King(Piece):
  def __init__(self, color: Literal['white', 'black'], position: Tuple[int]) -> None:
    super().__init__(color, position)
    self.value = 0

  def possible_moves(self, board: 'Board') -> list:
    moves = []
    for i in range(-1, 2):
      for j in range(-1, 2):
        if not (0 <= self.position[0] + i < board.board.shape[0] and 0 <= self.position[1] + j < board.board.shape[1]):
          continue
        if board.getPieceAtPosition((self.position[0] + i, self.position[1] + j)).color != self.color:
          moves.append((self.position, (self.position[0] + i, self.position[1] + j)))
    return moves