from .piece import Piece
from typing import List, Literal, Tuple, TYPE_CHECKING
from .emptyPiece import emptyPiece

if TYPE_CHECKING:
  import sys
  sys.path.append('..')
  from board import Board

class Pawn(Piece):
  def __init__(self, color: Literal['white', 'black'], position: Tuple[int, int]) -> None:
    super().__init__(color, position)
    self.has_moved = False
    self.value = 1

  def possible_moves(self, board: 'Board') -> List:
    # list of legal moves for the pawn
    moves: List[Tuple[Tuple[int, int], Tuple[int, int]]] = []
    # set direction to forward if white, backward if black
    direction = 1 if self.color == "white" else -1

    # check if the square in front of the pawn is empty
    if isinstance(board.getPieceAtPosition((self.position[0] - direction, self.position[1])), emptyPiece):
      moves.append((self.position, (self.position[0] - direction, self.position[1])))
      # if pawn has not moved yet, check if the square two squares in front of the pawn is empty
      if not self.has_moved and isinstance(board.getPieceAtPosition((self.position[0] - 2 * direction, self.position[1])), emptyPiece):
        moves.append((self.position, (self.position[0] - 2 * direction, self.position[1])))
    
    # check if the square to the left of the pawn is occupied by an enemy piece
    # dont check for leftmost pawn
    if self.position[1] != 0:
      if not isinstance(board.getPieceAtPosition((self.position[0] - direction, self.position[1] - 1)), emptyPiece) and board.getPieceAtPosition((self.position[0] - direction, self.position[1] - 1)).color != self.color:
        moves.append((self.position, (self.position[0] - direction, self.position[1] - 1)))

    # check if the square to the right of the pawn is occupied by an enemy piece
    # dont check for rightmost pawn
    if self.position[1] != board.board.shape[1] - 1:
      if not isinstance(board.getPieceAtPosition((self.position[0] - direction, self.position[1] + 1)), emptyPiece) and board.getPieceAtPosition((self.position[0] - direction, self.position[1] + 1)).color != self.color:
        moves.append((self.position, (self.position[0] - direction, self.position[1] + 1)))

    return moves