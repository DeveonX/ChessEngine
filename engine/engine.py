# Import necessary libraries and modules
from utils.boardToArray import boardToArray
from components.board import Board
from logic.game import chessGame
from logic.player import chessPlayer
import copy
from typing import Tuple, Literal

import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np


# Check if CUDA is available and set the device accordingly
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Define a PyTorch module to clamp the output between a min and max value
class ClampModule(nn.Module):
    def __init__(self, min, max):
        super().__init__()
        self.min = min
        self.max = max

    def forward(self, x):
        return torch.clamp(x, self.min, self.max)


# Define the chess engine
class chessEngine:
    def __init__(self, n_squares=64, game=None):
        if game is None:
            game = chessGame()
        self.game = game
        # Initialize the evaluation function, optimizer, and loss function
        
        # Define the evaluation function as a neural network
        evaluation_function = nn.Sequential(
            nn.Linear(n_squares, 32),
            nn.LeakyReLU(),
            nn.Linear(32, 12),
            nn.LeakyReLU(),
            nn.Linear(12, 6),
            nn.LeakyReLU(),
            nn.Linear(6, 4),
            nn.LeakyReLU(),
            nn.Linear(4, 1),
            ClampModule(-61, 61)
        )
        self.evaluation_function = evaluation_function.to(device)
        self.optimizer = optim.Adam(self.evaluation_function.parameters(), lr=0.01)
        self.loss_function = nn.MSELoss()
        # Initialize the game arrays to store the board states
        self._gameArrays = []

    # Function to evaluate the board state
    def evaluateBoard(self, board: Board, evaluationFunction=None, game:chessGame=None) -> float:
        # If no evaluation function is provided, use the default one
        if evaluationFunction is None:
            evaluationFunction = self.evaluation_function
        # If a game is provided, check for checkmate
        if game:
            if game.white.isCheckmate(game.board, game.black):
                return -100
            if game.black.isCheckmate(game.board, game.white):
                return 100
        # Convert the board to a tensor and evaluate it
        boardArray = boardToArray(board).reshape(1, -1)
        boardTensor = torch.tensor(boardArray, dtype=torch.float32).to(device)
        return evaluationFunction(boardTensor) + sum([piece.value for piece in game.white.pieces(game.board)]) - sum([piece.value for piece in game.black.pieces(game.board)])

    # Function to recursively evaluate the board state
    def recursiveEvaluateBoard(self, board: Board, game: chessGame, evaluationFunction=None, depth=0) -> float:
        # If the depth is 0 or the game is over, evaluate the board
        if depth == 0 or game.game_over:
            return self.evaluateBoard(board, evaluationFunction, game)
        # Otherwise, evaluate all legal moves and return the best score
        legalMoves = game.getLegalMoves()
        if game.current_player == "white":
            bestScore = -float('inf')
            for move in legalMoves:
                newGame = copy.deepcopy(game)
                newGame.makeMove(move)
                score = self.recursiveEvaluateBoard(newGame.board, newGame, evaluationFunction, depth-1)
                bestScore = max(bestScore, score)
        else:
            bestScore = float('inf')
            for move in legalMoves:
                newGame = copy.deepcopy(game)
                newGame.makeMove(move)
                score = self.recursiveEvaluateBoard(newGame.board, newGame, evaluationFunction, depth-1)
                bestScore = min(bestScore, score)
        return bestScore

    # Function to train the evaluation function
    def train(self, board: Board, target: torch.tensor) -> None:
        # Convert the board to a tensor
        boardArray = boardToArray(board)
        boardTensor = torch.tensor(boardArray, dtype=torch.float32).to(device)
        targetTensor = torch.tensor(target, dtype=torch.float32).to(device)
        # Make a prediction and calculate the loss
        prediction = self.evaluation_function(boardTensor)
        loss = self.loss_function(prediction, targetTensor)
        # Backpropagate and update the weights
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

    # Function to get the best move
    def getBestMove(self, game: chessGame, currentPlayer: Literal["white", "black"], evaluationFunction=None, depth=0) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        game.showBoard() # log

        if evaluationFunction is None:
            evaluationFunction = self.evaluation_function
        legalMoves = game.getLegalMoves()
        bestMove = None
        bestScore = -float('inf') if currentPlayer == "white" else float('inf')
        for move in legalMoves:
            newGame = copy.deepcopy(game)
            newGame.makeMove(move)
            score = self.recursiveEvaluateBoard(newGame.board, newGame, evaluationFunction, depth=depth)
            if currentPlayer == "white":
              if score > bestScore and tuple(boardToArray(newGame.board).flatten()) not in self._gameArrays:
                  bestMove = move
                  bestScore = score
            else:
              if score < bestScore and tuple(boardToArray(newGame.board).flatten()) not in self._gameArrays:
                  bestMove = move
                  bestScore = score
        print(bestScore)
        return bestMove

    # Function to play a game
    def playGame(self, game: chessGame, depth) -> str:
        while not game.game_over:
            initArray = boardToArray(game.board)
            if game.current_player == "white":
                move = self.getBestMove(game, "white", depth=depth)
            else:
                move = self.getBestMove(game, "black", depth=depth)
            game.makeMove(move)
            finArray = boardToArray(game.board)
            if np.array_equal(initArray, finArray):
                print("Game not changing")
                print(move)
                break
        self._gameArrays = []
        return game.winner

    # Function to generate a mutated version of the evaluation function
    def generateMutatedEvaluationFunction(self):
        mutatedFunction = copy.deepcopy(self.evaluation_function)
        mutatedFunction.requires_grad_(False)
        for layer in mutatedFunction:
            if isinstance(layer, nn.Linear):
                layer.weight += 0.1 * torch.randn_like(layer.weight)
                layer.bias += 0.1 * torch.randn_like(layer.bias)
        mutatedFunction.requires_grad_(True)
        return mutatedFunction

    # Function to train the engine against itself
    def trainAgainstSelf(self, epochs, depth=0):
        for epoch in range(epochs):
            game = copy.deepcopy(self.game)
            # Generate a slightly mutated version of the evaluation function
            mutatedEvaluation = self.generateMutatedEvaluationFunction()
            while not game.game_over:
                if game.current_player == "white":
                    move = self.getBestMove(game, "white", evaluationFunction=self.evaluation_function, depth=depth)
                else:
                    move = self.getBestMove(game, "black", evaluationFunction=mutatedEvaluation, depth=depth)
                game.makeMove(move)
                self._gameArrays.append(tuple(boardToArray(game.board).flatten()))
            game.showBoard()
            if game.winner == "black":
                print("Black won")
                self.evaluation_function = mutatedEvaluation
            elif game.winner == "white":
                print("White won")
            else:
                print("Draw")
            print(f"Epoch {epoch+1}: {game.winner}: {game.move_count} moves")
            self._gameArrays = []
            with open("resultsMutatedEngine.txt", "a+") as f:
                f.write(f"Epoch {epoch+1}: {game.winner}: {game.move_count} moves\n")

    # Function to train the engine with game endings
    def trainWithEndings(self, epochs, depth=0):
        for epoch in range(epochs):
            game = self.game
            while not game.game_over:
                if game.current_player == "white":
                    move = self.getBestMove(game, "white", depth=depth)
                else:
                    move = self.getBestMove(game, "black", depth=depth)
                game.makeMove(move)
                self._gameArrays.append(tuple(boardToArray(game.board).flatten()))
            game.showBoard()
            if game.winner == "white":
                target = 1
            elif game.winner == "black":
                target = -1
            else:
                self._gameArrays = []
                with open("resultsEndingTrain.txt", "a+") as f:
                    f.write(f"Epoch {epoch+1}: {game.winner}: {game.move_count} moves\n")
                continue
            self.train(game.board, target)
            print(f"Epoch {epoch+1}: {game.winner}")
            self._gameArrays = []
            with open("resultsEndingTrain.txt", "a+") as f:
                f.write(f"Epoch {epoch+1}: {game.winner}: {game.move_count} moves\n")