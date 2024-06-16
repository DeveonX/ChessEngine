from .piece import Piece
import colorama

class emptyPiece(Piece):
  def __init__(self, position=None) -> None:
    super().__init__(None, position)

  def __str__(self) -> str:
    return "----"
  
  def colored_str(self, color) -> str:
    return color + "----" + colorama.Style.RESET_ALL
  
  def __repr__(self) -> str:
    return self.__str__()