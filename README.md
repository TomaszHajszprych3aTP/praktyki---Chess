# How to play chess

file chess.py is game file
file "position" is file where current game state is being saved
file board.py is a program which reads "position" file and display chess board based on it

both python programs should be in same folder. simply start both of them(board.py is used only to display board and is not needed for program to work) and play chess in chess.py program and you can see the change on the board.
board will most likely lag it's duo to way it is programmed i intended to use chess.py to create chess ai therefor i didnt pay much attention to visuals. the board even tohught it look lagged will work when you make a move in chess.py program

<img width="450" src="untitiled.png" alt="chess image">


# How does it work
first board and variables are initiated. board is a list of 8 list each contaning 8 elements therefor creating 8x8 chessboard.

each piece has its numerical value pawn = 1, knight = 2, bishop = 3, rook = 5, queen = 9 and king = 10. values of black pieces are negative pawn = -1, knight = -2, bishop = -3, rook = -5 queen = -9 king = -10.

6 functions are created one for each piece used to check possible of pieces: pawn, knight, bishop, rook, queen, king

next user input is saved and changed from string to lists of coordinates for example.: e2 e4 -> [[4, 1][4, 3]] which indicate initial piece position and where it is moved

based on piece a player is moving corresponding function is used to find it's legal moves and check if player's move is in legal moves

if yes turn changes to black player otherwise players is prompted to input move again

