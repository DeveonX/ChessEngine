from logic.game import chessGame
from engine.engine import chessEngine
from pickle import dump, load



def main():
  engine = chessEngine()
  game = chessGame()

  engine.trainAgainstSelf(1000, depth=0)
  with open("engine.pkl", "wb") as f:
    dump(engine, f)

  while True:
    print(game.showBoard())
    move = engine.getBestMove(game, game.current_player)
    game.makeMove(move)
    if game.game_over:
      print(f"Game Over! {game.winner}")
      break

if __name__ == "__main__":
  main()