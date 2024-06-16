from .player import chessPlayer
from components.board import Board
from typing import Tuple

class chessGame:
  def __init__(self) -> None:
    self.board = Board()
    self.white = chessPlayer('white')
    self.black = chessPlayer('black')
    self.current_player = "white"
    self.game_over = False
    self.winner = None
    self.move_count = 0
    self.move_history = []

  def makeMove(self, move: Tuple[Tuple[int, int], Tuple[int, int]]) -> None:
    if self.game_over:
      return
    if move == None:
      self.game_over = True
      self.winner = "draw"
      return
    # whites move
    if self.current_player == "white":
      legalMoves = self.white.legalMoves(self.board)
      if move not in legalMoves:
        print(move)
        raise ValueError("Illegal move by white")
      self.board.movePiece(move[0], move[1])
      self.move_history.append(move)

      # check for wins or draws
      if self.black.isCheckmate(self.board, self.white):
        self.game_over = True
        self.winner = "white"
      if self.black.isStalemate(self.board, self.white):
        self.game_over = True
        self.winner = "draw"
      self.current_player = "black"

    # blacks move
    elif self.current_player == "black":
      legalMoves = self.black.legalMoves(self.board)
      if move not in legalMoves:
        print(move)
        raise ValueError("Illegal move by black")
      self.board.movePiece(move[0], move[1])
      self.move_history.append(move)
      if self.white.isCheckmate(self.board, self.black):
        self.game_over = True
        self.winner = "black"
      if self.white.isStalemate(self.board, self.black):
        self.game_over = True
        self.winner = "draw"
      self.current_player = "white"
    self.move_count += 1

  # display the board
  def showBoard(self, end="\n"):
    print(self.board, end=end)

  # get legal moves of the current player
  def getLegalMoves(self):
    if self.current_player == "white":
      return self.white.legalMoves(self.board)
    elif self.current_player == "black":
      return self.black.legalMoves(self.board)
    else:
      raise Exception("Exception: Current player is neither white nor black")