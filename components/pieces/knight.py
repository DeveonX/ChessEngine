from typing import Literal, Tuple, TYPE_CHECKING
from .piece import Piece

if TYPE_CHECKING:
  import sys
  sys.path.append('..')
  from board import Board

class Knight(Piece):
  def __init__(self, color: Literal['white', 'black'], position: Tuple[int, int]) -> None:
    super().__init__(color, position)
    self.value = 3

  def possible_moves(self, board: 'Board') -> list:
    moves = []
    for i in range(-2, 3):
      for j in range(-2, 3):
        if abs(i) + abs(j) == 3 and 0 <= self.position[0] + i < board.board.shape[0] and 0 <= self.position[1] + j < board.board.shape[1]:
          if board.getPieceAtPosition((self.position[0] + i, self.position[1] + j)).color != self.color:
            moves.append((self.position, (self.position[0] + i, self.position[1] + j)))
    return list(set(moves))