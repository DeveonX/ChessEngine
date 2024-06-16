import numpy as np
from .pieces.piece import Piece
from .pieces.rook import Rook
from .pieces.pawn import Pawn  
from .pieces.knight import Knight
from .pieces.bishop import Bishop
from .pieces.queen import Queen
from .pieces.king import King
from .pieces.emptyPiece import emptyPiece

import colorama
from typing import Tuple, List

class Board:
  def __init__(self) -> None:
    self.shape = (8, 8)
    # initialize board with empty pieces
    self.board = np.array([[emptyPiece((i, j)) for j in range(8)] for i in range(8)])
    # initialize white pieces
    self.board[0][0] = Rook("black", (0, 0))
    self.board[0][1] = Knight("black", (0, 1))
    self.board[0][2] = Bishop("black", (0, 2))
    self.board[0][3] = Queen("black", (0, 3))
    self.board[0][4] = King("black", (0, 4))
    self.board[0][5] = Bishop("black", (0, 5))
    self.board[0][6] = Knight("black", (0, 6))
    self.board[0][7] = Rook("black", (0, 7))
    for i in range(8):
      self.board[1][i] = Pawn("black", (1, i))
    # initialize black pieces
    self.board[7][0] = Rook("white", (7, 0))
    self.board[7][1] = Knight("white", (7, 1))
    self.board[7][2] = Bishop("white", (7, 2))
    self.board[7][3] = Queen("white", (7, 3))
    self.board[7][4] = King("white", (7, 4))
    self.board[7][5] = Bishop("white", (7, 5))
    self.board[7][6] = Knight("white", (7, 6))
    self.board[7][7] = Rook("white", (7, 7))
    for i in range(8):
      self.board[6][i] = Pawn("white", (6, i))
    
  def setBoard(self, board: np.ndarray) -> None:
    if not isinstance(board, np.ndarray) and not all(isinstance(piece, Piece) for piece in board.flatten()):
      raise TypeError("board must be a numpy array of pieces")
    self.shape = board.shape
    self.board = board

  def getPieceAtPosition(self, position: Tuple[int, int]) -> Piece:
      if (not isinstance(position, tuple) or len(position) != 2 or not all(isinstance(i, int) for i in position)):
        raise TypeError("position must be a tuple containing two integers")
      if (position[0] < 0 or position[0] > self.shape[0]-1 or position[1] < 0 or position[1] > self.shape[1]-1):
        raise ValueError("position must be within the board")
      if (not position):
        return None
      return self.board[position[0]][position[1]]
    
  def movePiece(self, initialPos: Tuple[int, int], finalPos: Tuple[int, int]) -> None:
      if not isinstance(initialPos, tuple) or len(initialPos) != 2 or not all(isinstance(i, int) for i in initialPos):
        raise TypeError("initialPos must be a tuple containing two integers")
      if not 0<=initialPos[0]<=self.shape[0]-1 or not 0<=initialPos[1]<=self.shape[1]-1 or not 0<=finalPos[0]<=self.shape[0]-1 or not 0<=finalPos[1]<=self.shape[1]-1:
        raise ValueError("positions must be within the board")
      
      piece = self.getPieceAtPosition(initialPos)
      if isinstance(piece, emptyPiece):
        raise ValueError("There is no piece at the initial position")
      if isinstance(self.getPieceAtPosition(initialPos), Pawn):
        self.getPieceAtPosition(initialPos).has_moved = True
      
      # replace original square with empty piece
      self.board[initialPos[0]][initialPos[1]] = emptyPiece(initialPos)
      self.board[finalPos[0]][finalPos[1]] = piece
      # update the position of the piece
      piece.position = finalPos
      
      # check if piece was pawn and reached the end of the board
      if isinstance(piece, Pawn) and (finalPos[0] == 0 or finalPos[0] == self.shape[0]-1):
        self.board[finalPos[0]][finalPos[1]] = Queen(piece.color, finalPos)
    
  # prints board but the position in the parameter is colored in red  
  def showHighLightedPositions(self, positions: List[Tuple[int, int]]) -> None:
      if not all(isinstance(pos, tuple) and len(pos) == 2 and all(isinstance(i, int) for i in pos) for pos in positions):
        raise TypeError("positions must be a list of tuples, each containing two integers")
      for i in range(self.shape[0]):
        for j in range(self.shape[1]):
          if (i, j) in positions:
            print(self.getPieceAtPosition((i, j)).colored_str(colorama.Fore.RED), end=" ")
          else:
            print(self.getPieceAtPosition((i, j)), end=" ")
        print()
     

  def __str__(self) -> str:
      res = ""
      for row in self.board:
        for piece in row:
          if piece == 0:
            res += "0   "
          else:
            res += str(piece) + " "
        res += "\n"
      return res
    

