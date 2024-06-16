from logic.game import chessGame
from engine.engine import chessEngine
from pickle import dump, load
import numpy as np
from components.pieces.emptyPiece import emptyPiece
from components.pieces.knight import Knight
from components.pieces.bishop import Bishop
from components.pieces.queen import Queen
from components.pieces.king import King
from components.pieces.rook import Rook
from components.pieces.pawn import Pawn

# small board 4x4 with only king and pawns and king on corner
def main():
  game = chessGame()
  game.board.setBoard(
    np.array([
      [King("black", (0, 0)), emptyPiece(), emptyPiece(), emptyPiece(), emptyPiece()],
      [Pawn("black", (1, 0)), Pawn("black", (1, 1)), Pawn("black", (1, 2)), Pawn("black", (1, 3)), Pawn("black", (1, 4))],
      [emptyPiece(), emptyPiece(), emptyPiece(), emptyPiece(), emptyPiece()],
      [Pawn("white", (3, 0)), Pawn("white", (3, 1)), Pawn("white", (3, 2)), Pawn("white", (3, 3)), Pawn("white", (3, 4))],
      [emptyPiece(), emptyPiece(), emptyPiece(), emptyPiece(), King("white", (4, 4))]

    ])
  )
  engine = chessEngine(n_squares=25, game=game)

  # engine.trainAgainstSelf(10, depth=2)

  # with open("smallBoardEngine.pkl", "wb") as f:
  #   dump(engine, f)

  game2 = chessGame()
  game2.board.setBoard(
    np.array([
      [King("black", (0, 0)), emptyPiece(), emptyPiece(), emptyPiece(), emptyPiece()],
      [Pawn("black", (1, 0)), Pawn("black", (1, 1)), Pawn("black", (1, 2)), Pawn("black", (1, 3)), Pawn("black", (1, 4))],
      [emptyPiece(), emptyPiece(), emptyPiece(), emptyPiece(), emptyPiece()],
      [Pawn("white", (3, 0)), Pawn("white", (3, 1)), Pawn("white", (3, 2)), Pawn("white", (3, 3)), Pawn("white", (3, 4))],
      [emptyPiece(), emptyPiece(), emptyPiece(), emptyPiece(), King("white", (4, 4))]

    ])
  )
  
  while not game2.game_over:
    game2.showBoard()
    x1 = int(input("x1: "))
    y1 = int(input("y1: "))
    x2 = int(input("x2: "))
    y2 = int(input("y2: "))

    game2.makeMove(((x1, y1), (x2, y2)))
    if game2.game_over:
      print(game2.winner)
      break
    bestMove = engine.getBestMove(game2, "black", depth=3)
    game2.makeMove(bestMove)
    game2.showBoard()
    if game2.game_over:
      print(game2.winner)
      break
    
if __name__ == "__main__":
  main()