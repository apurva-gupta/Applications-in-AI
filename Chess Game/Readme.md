Implementing chess using minimax algorithm with alpha beta search.Program predicts the next best move given a state of board.

To Run Program
./pichu.py <turn> <state of board> <time in seconds>
1. turn : current player(b/w)
2. state of board:example-RNBQKBNRPPPPPPPP................................pppppppprnbqkbnr
It is string of 64 characters. '.' represents empty square,P or p for a white or black Parakeet, R or r for a white or black Robin, N or n for a white or black
Nighthawk, Q or q for a white or black Quetzal, K or k for a white or black Kingfisher, and B or b for a white or black Blue jay, in row-major order.
3. time limit in seconds

Description of Game
The game is played by two players on a board consisting of a grid of 8 × 8 squares. Initially, each player has sixteen pieces: 8 Parakeets, 2 Robins, 2 Nighthawks, 2 Blue jays, 1 Quetzal, and 1 Kingfisher. The two
players alternate turns, with White going first. On each turn, a player moves exactly one of his or her pieces, possibly capturing (removing) a piece of the opposite player in the process, according to the following rules:

• A Parakeet may move one square forward, if no other piece is on that square. Or, a Parakeet may move one square forward diagonally (one square forward and one square left or right) if a piece of the
opposite player is on that square, in the process capturing that piece from the board. If a Parakeet reaches the far row of the board (closest to the opposite player), it is transformed into a Quetzal. On
its very first move of the game, a Parakeet may move forward two squares as long as both are empty.
• A Robin may move any number of squares either horizontally or vertically, landing on either an empty square or a piece of the opposite player (which is then captured), as long as all the squares between
the starting and ending positions are empty.
• A Blue jay is like a Robin, but moves along diagonal flight paths instead of horizontal or vertical ones.
• A Quetzal is like a combination of a Robin and a Blue jay: it may move any number of empty squares horizontally, vertically, or diagonally, and land either on an empty square or on a piece of the opposite
player (which is then captured).
• A Kingfisher may move one square in any direction, horizontally or vertically, either to an empty square or to capture a piece of the opposing player.
• A Nighthawk moves in L shaped patterns on the board, either two squares to the left or right followed by one square forward or backward, or one square left or right followed by two squares forward or
backward. It may fly over any pieces on the way, but the destination square must either be empty or have a piece of the opposite player (which is then captured).
A player wins by capturing the other player’s Kingfisher.
There is no condition of checkmate or castling.
