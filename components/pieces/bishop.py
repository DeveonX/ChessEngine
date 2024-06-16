from typing import Literal, Tuple, TYPE_CHECKING
from .piece import Piece
from .emptyPiece import emptyPiece

if TYPE_CHECKING:
  import sys
  sys.path.append('..')
  from board import Board

class Bishop(Piece):
  def __init__(self, color: Literal['white', 'black'], position: Tuple[int, int]) -> None:
    super().__init__(color, position)
    self.value = 3

  def possible_moves(self, board: 'Board') -> list:
    moves = []
    for i in range(1, board.board.shape[1]):
      if not (0 <= self.position[0] + i < board.board.shape[0] and 0 <= self.position[1] + i < board.board.shape[1]):
        break
      if board.getPieceAtPosition((self.position[0] + i, self.position[1] + i)).color == self.color:
        break
      moves.append((self.position, (self.position[0] + i, self.position[1] + i)))
      if board.getPieceAtPosition((self.position[0] + i, self.position[1] + i)).color != None:
        break

    for i in range(1, board.board.shape[0]):
      if not (0 <= self.position[0] - i < board.board.shape[0] and 0 <= self.position[1] - i < board.board.shape[1]):
        break
      if board.getPieceAtPosition((self.position[0] - i, self.position[1] - i)).color == self.color:
        break
      moves.append((self.position, (self.position[0] - i, self.position[1] - i)))
      if board.getPieceAtPosition((self.position[0] - i, self.position[1] - i)).color != None:
        break

    for i in range(1, board.board.shape[1]):
      if not (0 <= self.position[0] + i < board.board.shape[0] and 0 <= self.position[1] - i < board.board.shape[1]):
        break
      if board.getPieceAtPosition((self.position[0] + i, self.position[1] - i)).color == self.color:
        break
      moves.append((self.position, (self.position[0] + i, self.position[1] - i)))
      if board.getPieceAtPosition((self.position[0] + i, self.position[1] - i)).color != None:
        break

    for i in range(1, board.board.shape[0]):
      if not (0 <= self.position[0] - i < board.board.shape[0] and 0 <= self.position[1] + i < board.board.shape[1]):
        break
      if board.getPieceAtPosition((self.position[0] - i, self.position[1] + i)).color == self.color:
        break
      moves.append((self.position, (self.position[0] - i, self.position[1] + i)))
      if board.getPieceAtPosition((self.position[0] - i, self.position[1] + i)).color != None:
        break

    return moves