from components.board import Board
from components.pieces.piece import Piece
from components.pieces.king import King
from typing import Literal, List, Tuple
import copy

class chessPlayer:
  def __init__(self, color: Literal["white", "black"]) -> None:
    self.color = color

  # get all the pieces of the player
  def pieces(self, board: Board) -> List[Piece]:
    pieces: List[Piece] = [board.getPieceAtPosition((i, j)) for i in range(board.shape[0]) for j in range(board.shape[1]) if board.getPieceAtPosition((i, j)).color == self.color]
    return pieces

  # get the position of the king
  def kingPosition(self, board: Board) -> Tuple[int, int]:
    try:
      return [x for x in self.pieces(board) if isinstance(x, King)][0].position
    except IndexError:
      print("King not found")
      print(board)
      raise Exception()

  def isInCheck(self, board: Board, otherPlayer: 'chessPlayer') -> bool:
    enemyPieces: List[Piece] = otherPlayer.pieces(board)
    # for each enemy piece, check if it can attack the king
    for piece in enemyPieces:
      pieceMoves = piece.possible_moves(board)
      for move in pieceMoves:
        if move[1] == self.kingPosition(board):
          return True
    return False
    
  def legalMoves(self, board: Board) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
    legalMoves = []
    for piece in self.pieces(board):
      # check all possible moves of the piece
      moves = piece.possible_moves(board)
      for move in moves:
        # if our king is not in check after moving the piece, it is a legal move
        boardCopy = copy.deepcopy(board)
        boardCopy.movePiece(move[0], move[1])
        if not self.isInCheck(boardCopy, chessPlayer("white" if self.color == "black" else "black")):
          legalMoves.append(move)
    return legalMoves
  
  def isCheckmate(self, board: Board, otherPlayer: 'chessPlayer') -> bool:
    return self.isInCheck(board, otherPlayer) and len(self.legalMoves(board)) == 0
  
  def isStalemate(self, board: Board, otherPlayer: 'chessPlayer') -> bool:
    if len(self.pieces(board)) == 1 and len(otherPlayer.pieces(board)) == 1:
      return True
    return not self.isInCheck(board, otherPlayer) and len(self.legalMoves(board)) == 0
  
  def __str__(self) -> str:
    return self.color + " player"
