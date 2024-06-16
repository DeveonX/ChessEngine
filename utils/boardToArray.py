from components.board import Board
from components.pieces.piece import Piece
from components.pieces.king import King
from components.pieces.queen import Queen
from components.pieces.bishop import Bishop
from components.pieces.knight import Knight
from components.pieces.rook import Rook
from components.pieces.pawn import Pawn
from typing import Literal, List, Tuple
import numpy as np

# convert each piece to int value to be used in the neural network
def boardToArray(board: Board) -> np.ndarray:
  boardArray = np.zeros((board.board.shape), dtype=int)
  for i in range(board.board.shape[0]):
    for j in range(board.board.shape[1]):
      piece = board.getPieceAtPosition((i, j))
      if piece is not None:
        if isinstance(piece, King):
          boardArray[i][j] = 20 if piece.color == "white" else -20
        elif isinstance(piece, Queen):
          boardArray[i][j] = 9 if piece.color == "white" else -9
        elif isinstance(piece, Bishop):
          boardArray[i][j] = 3 if piece.color == "white" else -3
        elif isinstance(piece, Knight):
          boardArray[i][j] = 4 if piece.color == "white" else -4
        elif isinstance(piece, Rook):
          boardArray[i][j] = 5 if piece.color == "white" else -5
        elif isinstance(piece, Pawn):
          boardArray[i][j] = 1 if piece.color == "white" else -1
        else:
          boardArray[i][j] = 0
  return boardArray