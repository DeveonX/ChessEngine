# Python Chess Engine

This is a basic chess engine implemented in Python. It's a great starting point for anyone interested in understanding how chess engines work, and it's also a good base for more advanced features.

## Features

- Evaluation of board states: The engine evaluates board states based on the material count on the board and the output of a neural network.
- Self-play: The engine can play games against itself, with slight modifications to its network after each game. This allows it to learn and improve over time.

## Limitations and Opportunities for Improvement

While this engine is fully functional, it's not the most performant or advanced chess engine out there. Here are some areas where it could be improved:

- **Performance**: The engine's performance could be improved in a number of ways. For example, implementing alpha-beta pruning could significantly speed up the search process.
- **Learning from real-world games**: Currently, the engine only learns by playing against itself. It could potentially improve much faster if it could also learn from real-world games played by strong players.
- **Evaluation function**: The engine's evaluation function is currently quite simple, taking into account only the material count and the output of a neural network. This could be made more sophisticated by considering other factors, such as piece mobility, king safety, pawn structure, etc.

## Contributing
Contributions are welcome! If you have an idea for improving the engine, feel free to fork this repository and submit a pull request.

## License

This project is licensed under the MIT License