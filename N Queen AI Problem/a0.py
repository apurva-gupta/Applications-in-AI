#!/usr/bin/env python
# a0.py : Solve the N-Rooks and N-Queen problem!
# D. Crandall, 2016
# Updated by Zehua Zhang, 2017
# Updated by Apurva Gupta, 2017: Updated program to solve both N-Queen and N-Rooks problem with better successor function.
# It also handles unavailable positions and gives warning for incorrect positions and problem types.

# The N-rooks problem is: Given an empty NxN chessboard, place N rooks on the board so that no rooks
# can take any other, i.e. such that no two rooks share the same row or column.
# The N-Queen problem is: Given an empty N*N chessboard,place N queens on the same board so that no queens
# can take any other, i.e. such that no two queens ahre the saame row, column or diagonal.

import sys
import math

# Count # of pieces in given row
def count_on_row(board, row):
    return sum( board[row] ) 

# Count # of pieces in given column
def count_on_col(board, col):
    return sum( [ row[col] for row in board ] )

# Check if any position has an attacking diagonal queen. It returns 1 if there is an attacking queen on diagonal else 0.
def count_on_diag(board,row,col):
        for r in range(0,N):
            for c in range(0,N):
                if row!=r and col!=c:
                    if abs(row - r)== abs(col-c):
                      if(board[r][c]==1):
                         return 1
        return 0

# Count total # of pieces on board
def count_pieces(board):
    return sum([ sum(row) for row in board ] )

# Return a string with the board rendered in a human-friendly format for N-rooks problem.It also handles unavailable position.
def printable_board_rooks(board):
#    return "\n".join([ " ".join([ "R" if col else "_" for col in row ]) for row in board])
    str = ""
    for row in range(0,N):
         for col in range(0,N):
             if row == ith_pos-1 and col == jth_pos-1:
                 str = str+" X"
             elif board[row][col]==1:
                 str = str+" R"
             else:
                 str = str + " _"
         str = str + " \n"
    return str

# Return a string with the board rendered in a human-friendly format for N-Queen problem.It also handles unavailable position.
def printable_board_queen(board):
#    return "\n".join([ " ".join([ "Q" if col else "_" for col in row ]) for row in board])
    str = ""
    for row in range(0,N):
         for col in range(0,N):
             if row == ith_pos-1 and col == jth_pos-1:
                 str = str+" X"
             elif board[row][col]==1:
                 str = str+" Q"
             else:
                 str = str + " _"
         str = str + " \n"
    return str

# Add a piece to the board at the given position, and return a new board (doesn't change original)
def add_piece(board, row, col):
        return board[0:row] + [board[row][0:col] + [1,] + board[row][col+1:]] + board[row+1:]

# Get list of successors of given board state
def successors(board):
    return [ add_piece(board, r, c) for r in range(0, N) for c in range(0,N) ]

# This is the new successor function for N-Queen. It eliminates a lot of unwanted states which never 
# leads us close to goal state.It checks and eliminates if number of queens in any diagonal,row or column is greater than 1.
def successors2_nqueen(board):
    new_board = []
    for r in range(0,N):
        for c in range(0,N):
            state = add_piece(board,r,c)
            if not(r==ith_pos-1 and c==jth_pos-1) or (ith_pos==0 and jth_pos==0):
                if state !=board and count_pieces(state) <= N and count_on_row(state, r) <= 1 and count_on_col(state,c)<=1 and \
                count_on_diag(state,r,c)==0 and state not in visited:
                    new_board.append(state)
    return new_board

# This is the new successor function for N-Rooks which is far better from the given successor function. It eliminates a lot of unwanted states
# which never leads us close to goal state.It checks number of rooks in every row and column and eliminates unwanted states.
def successors2_nrooks(board):
    new_board = []
    for r in range(0,N):
        for c in range(0,N):
            state = add_piece(board,r,c)
            if not(r==ith_pos-1 and c==jth_pos-1):
                if state !=board and count_pieces(state) <= N and count_on_row(state, r) <= 1 and count_on_col(state,c)<=1:
                    new_board.append(state)
    return new_board


# check if board is a goal state
def is_goal(board):
    return (count_pieces(board) == N)

# Solve n-queen.The solution is obtained by using depth first search.
def solve_nqueen(initial_board):
    fringe = [initial_board]
    while len(fringe) > 0:
        for s in successors2_nqueen( fringe.pop() ):
                visited.append(s)
                if is_goal(s):
                    return(s)
                fringe.append(s)
    return False

def solve_nrooks(initial_board):
    fringe = [initial_board]
    while len(fringe) > 0:
        for s in successors2_nrooks( fringe.pop() ):
            
                if is_goal(s):
                    return(s)
                fringe.append(s)
    return False

# This is N, the size of the board. It is passed through command line arguments.
problem_type = (sys.argv[1])
N = int(sys.argv[2])
ith_pos = int(sys.argv[3])
jth_pos = int(sys.argv[4])
visited = []

# The board is stored as a list-of-lists. Each inner list is a row of the board.
# A zero in a given square indicates no piece, and a 1 indicates a piece.
initial_board = [[0]*N]*N
if ith_pos<0 or jth_pos < 0:
    print "Unavailable positions cannot be less than 0. If you enter (0,0) it will take all positions as available,else specify the unavailable position starting from (1,1)."
elif ith_pos==0 and jth_pos>0 or ith_pos>0 and jth_pos==0:
    print "Not correct unavailable position. Enter(0,0) for no unavailable position. The unavailable positions start from (1,1)"
elif problem_type == "nqueen":
    print ("Starting from initial board:\n" + printable_board_queen(initial_board) + "\n\nLooking for solution...\n")
    if(N==2 or N==3 or N==1):
        print "Sorry, no solution possible. N should be greater than or equal to 4,for N-queen problem."
    else:
        solution = solve_nqueen(initial_board)
        print (printable_board_queen(solution) if solution else "Sorry, no solution found. :(")
        
elif problem_type == "nrook":
    print( "Starting from intial board:\n" + printable_board_rooks(initial_board) + "\n\nLooking for solution...\n")
    if(N==1):
        print "Sorry,No solution possible. N should be greater than or equal to 2,for N-Rooks problem"
    else:
        solution = solve_nrooks(initial_board)
        print (printable_board_rooks(solution) if solution else "Sorry, no solution found. :(")
else:
    print "Please type either 'nqueen' or 'nrook' problem type."

    


