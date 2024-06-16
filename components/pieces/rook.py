from typing import Literal, Tuple, TYPE_CHECKING
from .piece import Piece
from .emptyPiece import emptyPiece

if TYPE_CHECKING: 
  import sys
  sys.path.append('..')
  from board import Board

class Rook(Piece):
  def __init__(self, color: Literal['white', 'black'], position: Tuple[int, int]) -> None:
    super().__init__(color, position)
    self.value = 5

  def possible_moves(self, board: 'Board') -> list:
    moves = []
    # check for moves in the vertical direction
    for i in range(self.position[0] + 1, board.board.shape[0]):
      if board.getPieceAtPosition((i, self.position[1])).color == self.color:
        break
      moves.append((self.position, (i, self.position[1])))
      if not isinstance(board.getPieceAtPosition((i, self.position[1])), emptyPiece):
        break
    for i in range(self.position[0] - 1, -1, -1):
      if board.getPieceAtPosition((i, self.position[1])).color == self.color:
        break
      moves.append((self.position, (i, self.position[1])))
      if not isinstance(board.getPieceAtPosition((i, self.position[1])), emptyPiece):
        break
    # check for moves in the horizontal direction
    for i in range(self.position[1] + 1, board.board.shape[1]):
      if board.getPieceAtPosition((self.position[0], i)).color == self.color:
        break
      moves.append((self.position, (self.position[0], i)))
      if not isinstance(board.getPieceAtPosition((self.position[0], i)), emptyPiece):
        break
    for i in range(self.position[1] - 1, -1, -1):
      if board.getPieceAtPosition((self.position[0], i)).color == self.color:
        break
      moves.append((self.position, (self.position[0], i)))
      if not isinstance(board.getPieceAtPosition((self.position[0], i)), emptyPiece):
        break
    return moves