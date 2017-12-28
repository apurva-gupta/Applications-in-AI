#!/usr/bin/env python
import sys
from time import time

#Team members:Apurva Gupta, Apurva Gupta and Sai Shruthi Umakanth.
#Title:Program to suggest the next best move for player in Game Pichu
#Accepts three arguments in command line 1. current player-b/w 2. State of board 3. time limit (in sec)

#Assumption
#1. Encoding of start state: R...K...RNBQKBNRPPPPPPPP........................pppppppprnbqkbnr

#Abstraction
#1. Initial state: As per given input
#2. Final state: Next best move for player 
#3. Successor function: Find all possible moves for each piece on board in given input state
#4. Set of states: Every possible position of every possible piece
#5. Evaluation function: 200(K-K') + 9(Q-Q')+5(R-R')+3(B-B' + N-N')+1(P-P')+0.1(M-M') referred https://chessprogramming.wikispaces.com/Evaluation 

#Used min max algorithm with alpha beta pruning as the algorith for solving this problem.
#Approach:
#1. For all types of pieces : P,Q,R,B,N,K(p,q,r,b,n,k) wrote functions which calculates all possible moves for that location of piece,considering if it is black's move or white's.
#2. Created a function which takes the state as input and finds all possible moves for all the pieces in that state.
#3. Applied min max algorithm with alpha beta pruning to increase performance.
#4. To handle time, We first searched for depth=1 , then depth=2 and so on.As soon as time limit exceeds,program stops. The last entry is the best possible move in given time limit.  

timeout_start = time()

state = sys.argv[2]
arr= []
i = 0
j =0
k = 0
list =[]
list = [i for i in state]

turn = sys.argv[1]
i = 0
for j in range(8):
    arr.append([])
    for k in range(8):
        if list[i]=='.':
            arr[j].append(' ')
        else:
            arr[j].append(list[i])
        i=i+1

for every in range (0,len(arr)):
    print arr[every]

timeout=float(sys.argv[3])

#To give a hint of what the player should move from which position to which position.
def compare_states(arr,state):
    Are_equal=False
    pos_x = []
    pos_y=[]
    
    for i in range(0,8):
       for j in range(0,8):
           if arr[i][j]==state[i][j]:
               Are_Equal=True
           else:
               pos_x.append(i)
               pos_y.append(j)
    
    if state[pos_x[0]][pos_y[0]] == " ":
        piece_arr = arr[pos_x[0]][pos_y[0]]
        print arr[pos_x[1]][pos_y[1]]
        pos_x_arr = pos_x[0]
        pos_y_arr = pos_y[0]
        pos_x1_arr = pos_x[1]
        pos_y1_arr = pos_y[1]
    if state[pos_x[1]][pos_y[1]] == " ":
        piece_arr = arr[pos_x[1]][pos_y[1]]
        print arr[pos_x[1]][pos_y[1]]
        pos_x_arr = pos_x[1]
        pos_y_arr = pos_y[1]
        pos_x1_arr = pos_x[0]
        pos_y1_arr = pos_y[0]


    if piece_arr in ("P","p"):
        piece = "Parakeet"
    elif piece_arr in ("Q", "q"):
        piece = "Quetzal"
    elif piece_arr in ("R","r"):
        piece = "robin"
    elif piece_arr in ("K","k"):
        piece = "Kingfisher"
    elif piece_arr in ("B","b"):
        piece = "Bluejay"
    elif piece_arr in ("N","n"):
        piece = "Nighthawk"

    print "I recommend moving the ",piece ," at row ",pos_x_arr+1," column ",pos_y_arr+1," to row ",pos_x1_arr+1," to column ",pos_y1_arr+1

#alpha beta pruning min max algorithm for searching best solution
def search(board,depth):
   
    infinity=float('inf')
    best_value=-infinity
    beta=infinity
    all_boards,c=succ_function(board,turn)
    timeout_start = time()
    if time()<timeout_start+timeout:
        for new in all_boards:
            if new!=[]:
                value=min_value(new,best_value,beta,depth-1)
                if value>best_value:
                    best_value=value
                    best_state=new
        return best_state
    else:
        sys.exit(0)
            


def max_value(board,alpha,beta,depth):
    if depth==0 or king_pos(board)==1:
        return evaluation_function(board,turn)

    infinity=float('inf')
    value=-infinity
    all_boards,c=succ_function(board,turn)
    
    if time()<timeout_start+timeout:
        for new in all_boards:
            if new!=[]:
                value=max(value,min_value(new,alpha,beta,depth-1))
            if value>=beta:
                return value
            alpha=max(alpha,value)
        return value
    else:
        sys.exit(0)

def min_value(board,alpha,beta,depth):
    if depth==0 or king_pos(board)==1:
        return evaluation_function(board,turn)

    infinity=float('inf')
    value=infinity
    if turn=="w":
        all_boards,c=succ_function(board,"b")
    if turn=="b":
        all_boards,c=succ_function(board,"w")
    
    if time()<timeout_start+timeout:
        for new in all_boards:
            if new!=[]:
                value=min(value,max_value(new,alpha,beta,depth-1))
            if value<=alpha:
                return value
            beta=min(beta,value)
        return value
    else:
        sys.exit(0)

#finds Heuristic evaluation value of a particular board
def evaluation_function(board,turn):
    i=0
    j=0
    no_w_kings=0
    no_w_queens=0
    no_w_pawns=0
    no_w_bishops=0
    no_w_rooks=0
    no_w_knights=0
    no_b_kings=0
    no_b_queens=0
    no_b_pawns=0
    no_b_bishops=0
    no_b_rooks=0
    no_b_knights=0
    mobility = 0
    for i in range(0,8):
        for j in range(0,8):
            which_piece=board[i][j]
            if which_piece=="P":
                no_w_pawns = no_w_pawns+1
            if which_piece=="K":
                no_w_kings=no_w_kings+1
            if which_piece=="Q":
                no_w_queens=no_w_queens+1
            if which_piece=="B":
                no_w_bishops=no_w_bishops+1
            if which_piece=="R":
                no_w_rooks=no_w_rooks+1
            if which_piece=="N":
                no_w_knights= no_w_knights+1
            if which_piece=="p":
                no_b_pawns = no_b_pawns+1
            if which_piece=="k":
                no_b_kings=no_b_kings+1
            if which_piece=="q":
                no_b_queens=no_b_queens+1
            if which_piece=="b":
                no_b_bishops=no_b_bishops+1
            if which_piece=="r":
                no_b_rooks=no_b_rooks+1
            if which_piece=="n":
                no_b_knights= no_b_knights+1
    

    if turn=="w":
	
	succ_boards,mobility_w = succ_function(board,"w")
        succ_boards,mobility_b= succ_function(board,"b")

	eval_function=200*(no_w_kings-no_b_kings) + 9*(no_w_queens-no_b_queens)+5*(no_w_rooks-no_b_rooks)+3*(no_w_bishops-no_b_bishops)+3*(no_w_knights-no_b_knights)+1*(no_w_pawns-no_b_pawns) + 0.1 * (mobility_w-mobility_b)
    if turn=="b":
    
        succ_boards,mobility_w = succ_function(board,"w")
	succ_boards,mobility_b= succ_function(board,"b")
        eval_function=200*(no_b_kings-no_w_kings) + 9*(no_b_queens-no_w_queens)+5*(no_b_rooks-no_w_rooks)+3*(no_b_bishops-no_w_bishops)+3*(no_b_knights-no_w_knights)+1*(no_b_pawns-no_w_pawns) + 0.1 * (mobility_b-mobility_w)

    return eval_function

#returns all successor boards and number of successor boards of a particular board according to turn.
def succ_function(board,turn):
    all_boards=[]
    succ_boards = []
    if king_pos(board)==1:
	return succ_boards,0
    if turn == "w":
        for i in range(0,8):
            for j in range(0,8):
                piece = board[i][j]
                if piece == 'P':
                    all_boards.append(pawn_move(board,turn,i,j))
                if piece == 'R':
                    all_boards.append(rook_move(board,turn,i,j))
                if piece == 'B':
                    all_boards.append(bishop_move(board,turn,i,j))
                if piece == 'N':
                    all_boards.append(knight_move(board,turn,i,j))
                if piece == 'Q':
                    all_boards.append(queen_move(board,turn,i,j))
                if piece == 'K':
                    all_boards.append(king_move(board,turn,i,j))
    elif turn == "b":
        for i in range(0,8):
            for j in range(0,8):
                piece = board[i][j]
                if piece == 'p':
                    all_boards.append(pawn_move(board,turn,i,j))
                if piece == 'r':
                    all_boards.append(rook_move(board,turn,i,j))
                if piece == 'b':
                    all_boards.append(bishop_move(board,turn,i,j))
                if piece == 'n':
                    all_boards.append(knight_move(board,turn,i,j))
                if piece == 'q':
                    all_boards.append(queen_move(board,turn,i,j))
                if piece == 'k':
                    all_boards.append(king_move(board,turn,i,j))
                    
    count = 0
    for boards in all_boards:
        for each in boards:
            count+=1
            succ_boards.append(each)
    return succ_boards,count

#Finds all successor boards of quetzal at a particular position,according to turn
def queen_move(board,turn,row,col):
    succ_board=[]
    
    if turn=="w":
        new_row=row-1
        new_col=col+1
        while new_row>=0 and new_col<=7:
            if board[new_row][new_col]==' ':
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row] + [new_board1[new_row][0:new_col] + ['Q',] + new_board1[new_row][new_col+1:]] + new_board1[new_row+1:]
                succ_board.append(new_board1)
            elif board[new_row][new_col] in ('p','r','q','n','b','k'):
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row] + [new_board1[new_row][0:new_col] + ['Q',] + new_board1[new_row][new_col+1:]] + new_board1[new_row+1:]
                succ_board.append(new_board1)
                break
            elif board[new_row][new_col] in ('P','R','Q','N','B','K'):
                break
            new_row=new_row-1
            new_col=new_col+1
        new_row1 = row-1
        new_col1 = col-1
        while new_col1>=0 and new_row1>=0:
            if board[new_row1][new_col1]==' ':
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row1] + [new_board1[new_row1][0:new_col1] + ['Q',] + new_board1[new_row1][new_col1+1:]] + new_board1[new_row1+1:]
                succ_board.append(new_board1)
            elif board[new_row1][new_col1] in ('p','r','q','n','b','k'):
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row1] + [new_board1[new_row1][0:new_col1] + ['Q',] + new_board1[new_row1][new_col1+1:]] + new_board1[new_row1+1:]
                succ_board.append(new_board1)
                break
            elif board[new_row1][new_col1] in ('P','R','Q','N','B','K'):
                break

            new_col1=new_col1-1
            new_row1=new_row1-1
        new_row2=row+1
        new_col2=col-1
        while new_col2>=0 and new_row2<=7:
            if board[new_row2][new_col2]==' ':
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row2] + [new_board1[new_row2][0:new_col2] + ['Q',] + new_board1[new_row2][new_col2+1:]] + new_board1[new_row2+1:]
                succ_board.append(new_board1)
            elif board[new_row2][new_col2] in ('p','r','q','n','b','k'):
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row2] + [new_board1[new_row2][0:new_col2] + ['Q',] + new_board1[new_row2][new_col2+1:]] + new_board1[new_row2+1:]
                succ_board.append(new_board1)
                break
            elif board[new_row2][new_col2] in ('P','R','Q','N','B','K'):
                break

            new_col2=new_col2-1
            new_row2=new_row2+1
        new_row3=row+1
        new_col3=col+1
        while new_row3<=7 and new_col3<=7:
            if board[new_row3][new_col3]==' ':
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row3] + [new_board1[new_row3][0:new_col3] + ['Q',] + new_board1[new_row3][new_col3+1:]] + new_board1[new_row3+1:]
                succ_board.append(new_board1)
            elif board[new_row3][new_col3] in ('p','r','q','n','b','k'):
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row3] + [new_board1[new_row3][0:new_col3] + ['Q',] + new_board1[new_row3][new_col3+1:]] + new_board1[new_row3+1:]
                succ_board.append(new_board1)
                break
            elif board[new_row3][new_col3] in ('P','R','Q','N','B','K'):
                break

            new_row3=new_row3+1
            new_col3=new_col3+1
        new_row=row+1
        new_col=col
        while new_row<=7:
            if board[new_row][new_col]==' ':
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row] + [new_board1[new_row][0:new_col] + ['Q',] + new_board1[new_row][new_col+1:]] + new_board1[new_row+1:]
                succ_board.append(new_board1)
            elif board[new_row][new_col] in ('p','r','q','n','b','k'):
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row] + [new_board1[new_row][0:new_col] + ['Q',] + new_board1[new_row][new_col+1:]] + new_board1[new_row+1:]
                succ_board.append(new_board1)
                break
            elif board[new_row][new_col] in ('P','R','Q','N','B','K'):
                break

            new_row = new_row+1
            
        new_row1 = row
        new_col1 = col+1
        while new_col1<=7:
            if board[new_row1][new_col1]==' ':
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row1] + [new_board1[new_row1][0:new_col1] + ['Q',] + new_board1[new_row1][new_col1+1:]] + new_board1[new_row1+1:]
                succ_board.append(new_board1)
            elif board[new_row1][new_col1] in ('p','r','q','n','b','k'):
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row1] + [new_board1[new_row1][0:new_col1] + ['Q',] + new_board1[new_row1][new_col1+1:]] + new_board1[new_row1+1:]
                succ_board.append(new_board1)
                break
            elif board[new_row1][new_col1] in ('P','R','Q','N','B','K'):
                break

            new_col1=new_col1+1
        new_row2=row
        new_col2=col-1
        while new_col2>=0:
            if board[new_row2][new_col2]==' ':
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row2] + [new_board1[new_row2][0:new_col2] + ['Q',] + new_board1[new_row2][new_col2+1:]] + new_board1[new_row2+1:]
                succ_board.append(new_board1)
            elif board[new_row2][new_col2] in ('p','r','q','n','b','k'):
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row2] + [new_board1[new_row2][0:new_col2] + ['Q',] + new_board1[new_row2][new_col2+1:]] + new_board1[new_row2+1:]
                succ_board.append(new_board1)
                break
            elif board[new_row2][new_col2] in ('P','R','Q','N','B','K'):
                break

            new_col2=new_col2-1
        new_row3=row-1
        new_col3=col
        while new_row3>=0:
            if board[new_row3][new_col3]==' ':
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row3] + [new_board1[new_row3][0:new_col3] + ['Q',] + new_board1[new_row3][new_col3+1:]] + new_board1[new_row3+1:]
                succ_board.append(new_board1)
            elif board[new_row3][new_col3] in ('p','r','q','n','b','k'):
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row3] + [new_board1[new_row3][0:new_col3] + ['Q',] + new_board1[new_row3][new_col3+1:]] + new_board1[new_row3+1:]
                succ_board.append(new_board1)
                break
            elif board[new_row3][new_col3] in ('P','R','Q','N','B','K'):
                break

            new_row3=new_row3-1

        return succ_board
    if turn=="b":
        new_row=row-1
        new_col=col+1
        while new_row>=0 and new_col<=7:
            if board[new_row][new_col]==' ':
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row] + [new_board1[new_row][0:new_col] + ['q',] + new_board1[new_row][new_col+1:]] + new_board1[new_row+1:]
                succ_board.append(new_board1)
            elif board[new_row][new_col] in ('P','R','Q','N','B','K'):
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row] + [new_board1[new_row][0:new_col] + ['q',] + new_board1[new_row][new_col+1:]] + new_board1[new_row+1:]
                succ_board.append(new_board1)
                break
            elif board[new_row][new_col] in ('p','r','q','n','b','k'):
                break

            new_row=new_row-1
            new_col=new_col+1
        new_row1 = row-1
        new_col1 = col-1
        while new_col1>=0 and new_row1>=0:
            if board[new_row1][new_col1]==' ':
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row1] + [new_board1[new_row1][0:new_col1] + ['q',] + new_board1[new_row1][new_col1+1:]] + new_board1[new_row1+1:]
                succ_board.append(new_board1)
            elif board[new_row1][new_col1] in ('P','R','Q','N','B','K'):
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row1] + [new_board1[new_row1][0:new_col1] + ['q',] + new_board1[new_row1][new_col1+1:]] + new_board1[new_row1+1:]
                succ_board.append(new_board1)
                break
            elif board[new_row1][new_col1] in ('p','r','q','n','b','k'):
                break

            new_col1=new_col1-1
            new_row1=new_row1-1
        new_row2=row+1
        new_col2=col-1
        while new_col2>=0 and new_row2<=7:
            if board[new_row2][new_col2]==' ':
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row2] + [new_board1[new_row2][0:new_col2] + ['q',] + new_board1[new_row2][new_col2+1:]] + new_board1[new_row2+1:]
                succ_board.append(new_board1)
            elif board[new_row2][new_col2] in ('P','R','Q','N','B','K'):
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row2] + [new_board1[new_row2][0:new_col2] + ['q',] + new_board1[new_row2][new_col2+1:]] + new_board1[new_row2+1:]
                succ_board.append(new_board1)
                break
            elif board[new_row2][new_col2] in ('p','r','q','n','b','k'):
                break

            new_col2=new_col2-1
            new_row2=new_row2+1
        new_row3=row+1
        new_col3=col+1
        while new_row3<=7 and new_col3<=7:
            if board[new_row3][new_col3]==' ':
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row3] + [new_board1[new_row3][0:new_col3] + ['q',] + new_board1[new_row3][new_col3+1:]] + new_board1[new_row3+1:]
                succ_board.append(new_board1)
            elif board[new_row3][new_col3] in ('P','R','Q','N','B','K'):
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row3] + [new_board1[new_row3][0:new_col3] + ['q',] + new_board1[new_row3][new_col3+1:]] + new_board1[new_row3+1:]
                succ_board.append(new_board1)
                break
            elif board[new_row3][new_col3] in ('p','r','q','n','b','k'):
                break

            new_row3=new_row3+1
            new_col3=new_col3+1
        new_row=row+1
        new_col=col
        while new_row<=7:
            if board[new_row][new_col]==' ':
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row] + [new_board1[new_row][0:new_col] + ['q',] + new_board1[new_row][new_col+1:]] + new_board1[new_row+1:]
                succ_board.append(new_board1)
            elif board[new_row][new_col] in ('P','R','Q','N','B','K'):
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row] + [new_board1[new_row][0:new_col] + ['q',] + new_board1[new_row][new_col+1:]] + new_board1[new_row+1:]
                succ_board.append(new_board1)
                break
            elif board[new_row][new_col] in ('p','r','q','n','b','k'):
                break

            new_row = new_row+1
        new_row1 = row
        new_col1 = col+1

        while new_col1<=7:
            if board[new_row1][new_col1]==' ':
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row1] + [new_board1[new_row1][0:new_col1] + ['q',] + new_board1[new_row1][new_col1+1:]] + new_board1[new_row1+1:]
                succ_board.append(new_board1)
            elif board[new_row1][new_col1] in ('P','R','Q','N','B','K'):
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row1] + [new_board1[new_row1][0:new_col1] + ['q',] + new_board1[new_row1][new_col1+1:]] + new_board1[new_row1+1:]
                succ_board.append(new_board1)
                break
            elif board[new_row1][new_col1] in ('p','r','q','n','b','k'):
                break

            new_col1=new_col1+1
        new_row2=row
        new_col2=col-1
        while new_col2>=0:
            if board[new_row2][new_col2]==' ':
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row2] + [new_board1[new_row2][0:new_col2] + ['q',] + new_board1[new_row2][new_col2+1:]] + new_board1[new_row2+1:]
                succ_board.append(new_board1)
            elif board[new_row2][new_col2] in ('P','R','Q','N','B','K'):
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row2] + [new_board1[new_row2][0:new_col2] + ['q',] + new_board1[new_row2][new_col2+1:]] + new_board1[new_row2+1:]
                succ_board.append(new_board1)
                break
            elif board[new_row2][new_col2] in ('p','r','q','n','b','k'):
                break

            new_col2=new_col2-1
        new_row3=row-1
        new_col3=col
        while new_row3>=0:
            if board[new_row3][new_col3]==' ':
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row3] + [new_board1[new_row3][0:new_col3] + ['q',] + new_board1[new_row3][new_col3+1:]] + new_board1[new_row3+1:]
                succ_board.append(new_board1)
            elif board[new_row3][new_col3] in ('P','R','Q','N','B','K'):
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row3] + [new_board1[new_row3][0:new_col3] + ['q',] + new_board1[new_row3][new_col3+1:]] + new_board1[new_row3+1:]
                succ_board.append(new_board1)
                break
            elif board[new_row3][new_col3] in ('p','r','q','n','b','k'):
                break

            new_row3=new_row3-1

        return succ_board

#Finds all successor boards of blue jay at a particular position,according to turn
def bishop_move(board,turn,row,col):
    succ_board=[]
    if turn=="w":
        new_row=row-1
        new_col=col+1
        while new_row>=0 and new_col<=7:
            if board[new_row][new_col]==' ':
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row] + [new_board1[new_row][0:new_col] + ['B',] + new_board1[new_row][new_col+1:]] + new_board1[new_row+1:]
                succ_board.append(new_board1)
            elif board[new_row][new_col] in ('p','r','q','n','b','k'):
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row] + [new_board1[new_row][0:new_col] + ['B',] + new_board1[new_row][new_col+1:]] + new_board1[new_row+1:]
                succ_board.append(new_board1)
                break
            elif board[new_row][new_col] in ('P','R','Q','N','B','K'):
                break
            new_row=new_row-1
            new_col=new_col+1
        new_row1 = row-1
        new_col1 = col-1
        while new_col1>=0 and new_row1>=0:
            if board[new_row1][new_col1]==' ':
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row1] + [new_board1[new_row1][0:new_col1] + ['B',] + new_board1[new_row1][new_col1+1:]] + new_board1[new_row1+1:]
                succ_board.append(new_board1)
            elif board[new_row1][new_col1] in ('p','r','q','n','b','k'):
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row1] + [new_board1[new_row1][0:new_col1] + ['B',] + new_board1[new_row1][new_col1+1:]] + new_board1[new_row1+1:]
                succ_board.append(new_board1)
                break
            elif board[new_row1][new_col1] in ('P','R','Q','N','B','K'):
                break

            new_col1=new_col1-1
            new_row1=new_row1-1
        new_row2=row+1
        new_col2=col-1
        while new_col2>=0 and new_row2<=7:
            if board[new_row2][new_col2]==' ':
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row2] + [new_board1[new_row2][0:new_col2] + ['B',] + new_board1[new_row2][new_col2+1:]] + new_board1[new_row2+1:]
                succ_board.append(new_board1)
            elif board[new_row2][new_col2] in ('p','r','q','n','b','k'):
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row2] + [new_board1[new_row2][0:new_col2] + ['B',] + new_board1[new_row2][new_col2+1:]] + new_board1[new_row2+1:]
                succ_board.append(new_board1)
                break
            elif board[new_row2][new_col2] in ('P','R','Q','N','B','K'):
                break

            new_col2=new_col2-1
            new_row2=new_row2+1
        new_row3=row+1
        new_col3=col+1
        while new_row3<=7 and new_col3<=7:
            if board[new_row3][new_col3]==' ':
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row3] + [new_board1[new_row3][0:new_col3] + ['B',] + new_board1[new_row3][new_col3+1:]] + new_board1[new_row3+1:]
                succ_board.append(new_board1)
            elif board[new_row3][new_col3] in ('p','r','q','n','b','k'):
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row3] + [new_board1[new_row3][0:new_col3] + ['B',] + new_board1[new_row3][new_col3+1:]] + new_board1[new_row3+1:]
                succ_board.append(new_board1)
                break
            elif board[new_row3][new_col3] in ('P','R','Q','N','B','K'):
                break

            new_row3=new_row3+1
            new_col3=new_col3+1

        return succ_board
    if turn=="b":
        new_row=row-1
        new_col=col+1
        while new_row>=0 and new_col<=7:
            if board[new_row][new_col]==' ':
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row] + [new_board1[new_row][0:new_col] + ['b',] + new_board1[new_row][new_col+1:]] + new_board1[new_row+1:]
                succ_board.append(new_board1)
            elif board[new_row][new_col] in ('P','R','Q','N','B','K'):
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row] + [new_board1[new_row][0:new_col] + ['b',] + new_board1[new_row][new_col+1:]] + new_board1[new_row+1:]
                succ_board.append(new_board1)
                break
            elif board[new_row][new_col] in ('p','r','q','n','b','k'):
                break

            new_row=new_row-1
            new_col=new_col+1
        new_row1 = row-1
        new_col1 = col-1
        while new_col1>=0 and new_row1>=0:
            if board[new_row1][new_col1]==' ':
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row1] + [new_board1[new_row1][0:new_col1] + ['b',] + new_board1[new_row1][new_col1+1:]] + new_board1[new_row1+1:]
                succ_board.append(new_board1)

            elif board[new_row1][new_col1] in ('P','R','Q','N','B','K'):
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row1] + [new_board1[new_row1][0:new_col1] + ['b',] + new_board1[new_row1][new_col1+1:]] + new_board1[new_row1+1:]
                succ_board.append(new_board1)
                break
            elif board[new_row1][new_col1] in ('p','r','q','n','b','k'):
                break

            new_col1=new_col1-1
            new_row1=new_row1-1
        new_row2=row+1
        new_col2=col-1
        while new_col2>=0 and new_row2<=7:
            if board[new_row2][new_col2]==' ':
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row2] + [new_board1[new_row2][0:new_col2] + ['b',] + new_board1[new_row2][new_col2+1:]] + new_board1[new_row2+1:]
                succ_board.append(new_board1)
            elif board[new_row2][new_col2] in ('P','R','Q','N','B','K'):
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row2] + [new_board1[new_row2][0:new_col2] + ['b',] + new_board1[new_row2][new_col2+1:]] + new_board1[new_row2+1:]
                succ_board.append(new_board1)
                break
            elif board[new_row2][new_col2] in ('p','r','q','n','b','k'):
                break

            new_col2=new_col2-1
            new_row2=new_row2+1
        new_row3=row+1
        new_col3=col+1
        while new_row3<=7 and new_col3<=7:
            if board[new_row3][new_col3]==' ':
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row3] + [new_board1[new_row3][0:new_col3] + ['b',] + new_board1[new_row3][new_col3+1:]] + new_board1[new_row3+1:]
                succ_board.append(new_board1)
            elif board[new_row3][new_col3] in ('P','R','Q','N','B','K'):
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row3] + [new_board1[new_row3][0:new_col3] + ['b',] + new_board1[new_row3][new_col3+1:]] + new_board1[new_row3+1:]
                succ_board.append(new_board1)
                break
            elif board[new_row3][new_col3] in ('p','r','q','n','b','k'):
                break

            new_row3=new_row3+1
            new_col3=new_col3+1

        return succ_board

#Finds all successor boards of robin at a particular position,according to turn
def rook_move(board,turn,row,col):
    succ_board=[]
    if turn=="w":
        new_row=row+1
        new_col=col
        while new_row<=7:
            if board[new_row][new_col]==' ':
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row] + [new_board1[new_row][0:new_col] + ['R',] + new_board1[new_row][new_col+1:]] + new_board1[new_row+1:]
                succ_board.append(new_board1)
            elif board[new_row][new_col] in ('p','r','q','n','b','k'):
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row] + [new_board1[new_row][0:new_col] + ['R',] + new_board1[new_row][new_col+1:]] + new_board1[new_row+1:]
                succ_board.append(new_board1)
                break
            elif board[new_row][new_col] in ('P','R','Q','N','B','K'):
                break

            new_row = new_row+1
        new_row1 = row
        new_col1 = col+1
        while new_col1<=7:
            if board[new_row1][new_col1]==' ':
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row1] + [new_board1[new_row1][0:new_col1] + ['R',] + new_board1[new_row1][new_col1+1:]] + new_board1[new_row1+1:]
                succ_board.append(new_board1)
            elif board[new_row1][new_col1] in ('p','r','q','n','b','k'):
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row1] + [new_board1[new_row1][0:new_col1] + ['R',] + new_board1[new_row1][new_col1+1:]] + new_board1[new_row1+1:]
                succ_board.append(new_board1)
                break
            elif board[new_row1][new_col1] in ('P','R','Q','N','B','K'):
                break

            new_col1=new_col1+1
        new_row2=row
        new_col2=col-1
        while new_col2>=0:
            if board[new_row2][new_col2]==' ':
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row2] + [new_board1[new_row2][0:new_col2] + ['R',] + new_board1[new_row2][new_col2+1:]] + new_board1[new_row2+1:]
                succ_board.append(new_board1)
            elif board[new_row2][new_col2] in ('p','r','q','n','b','k'):
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row2] + [new_board1[new_row2][0:new_col2] + ['R',] + new_board1[new_row2][new_col2+1:]] + new_board1[new_row2+1:]
                succ_board.append(new_board1)
                break
            elif board[new_row2][new_col2] in ('P','R','Q','N','B','K'):
                break

            new_col2=new_col2-1
        new_row3=row-1
        new_col3=col
        while new_row3>=0:
            if board[new_row3][new_col3]==' ':
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row3] + [new_board1[new_row3][0:new_col3] + ['R',] + new_board1[new_row3][new_col3+1:]] + new_board1[new_row3+1:]
                succ_board.append(new_board1)
            elif board[new_row3][new_col3] in ('p','r','q','n','b','k'):
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row3] + [new_board1[new_row3][0:new_col3] + ['R',] + new_board1[new_row3][new_col3+1:]] + new_board1[new_row3+1:]
                succ_board.append(new_board1)
                break
            elif board[new_row3][new_col3] in ('P','R','Q','N','B','K'):
                break

            new_row3=new_row3-1
        return succ_board

    if turn=="b":
        new_row=row+1
        new_col=col
        while new_row<=7:
            if board[new_row][new_col]==' ':
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row] + [new_board1[new_row][0:new_col] + ['r',] + new_board1[new_row][new_col+1:]] + new_board1[new_row+1:]
                succ_board.append(new_board1)
            elif board[new_row][new_col] in ('P','R','Q','N','B','K'):
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row] + [new_board1[new_row][0:new_col] + ['r',] + new_board1[new_row][new_col+1:]] + new_board1[new_row+1:]
                succ_board.append(new_board1)
                break
            elif board[new_row][new_col] in ('p','r','q','n','b','k'):
                break

            new_row = new_row+1
        new_row1 = row
        new_col1 = col+1

        while new_col1<=7:
            if board[new_row1][new_col1]==' ':
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row1] + [new_board1[new_row1][0:new_col1] + ['r',] + new_board1[new_row1][new_col1+1:]] + new_board1[new_row1+1:]
                succ_board.append(new_board1)
            elif board[new_row1][new_col1] in ('P','R','Q','N','B','K'):
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row1] + [new_board1[new_row1][0:new_col1] + ['r',] + new_board1[new_row1][new_col1+1:]] + new_board1[new_row1+1:]
                succ_board.append(new_board1)
                break
            elif board[new_row1][new_col1] in ('p','r','q','n','b','k'):
                break

            new_col1=new_col1+1
        new_row2=row
        new_col2=col-1
        while new_col2>=0:
            if board[new_row2][new_col2]==' ':
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row2] + [new_board1[new_row2][0:new_col2] + ['r',] + new_board1[new_row2][new_col2+1:]] + new_board1[new_row2+1:]
                succ_board.append(new_board1)
            elif board[new_row2][new_col2] in ('P','R','Q','N','B','K'):
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row2] + [new_board1[new_row2][0:new_col2] + ['r',] + new_board1[new_row2][new_col2+1:]] + new_board1[new_row2+1:]
                succ_board.append(new_board1)
                break
            elif board[new_row2][new_col2] in ('p','r','q','n','b','k'):
                break


            new_col2=new_col2-1
        new_row3=row-1
        new_col3=col
        while new_row3>=0:
            if board[new_row3][new_col3]==' ':
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row3] + [new_board1[new_row3][0:new_col3] + ['r',] + new_board1[new_row3][new_col3+1:]] + new_board1[new_row3+1:]
                succ_board.append(new_board1)
            elif board[new_row3][new_col3] in ('P','R','Q','N','B','K'):
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row3] + [new_board1[new_row3][0:new_col3] + ['r',] + new_board1[new_row3][new_col3+1:]] + new_board1[new_row3+1:]
                succ_board.append(new_board1)
                break
            elif board[new_row3][new_col3] in ('p','r','q','n','b','k'):
                break

            new_row3=new_row3-1
        return succ_board
 
#Finds all successor boards of kingfisher at a particular position,according to turn
def king_move(board,turn,row,col):
    succ_board=[]
    if turn == "w":

        if row+1<8:
            new_row1= row+1
            new_col1 = col
            if board[new_row1][new_col1]==' ' or  board[new_row1][new_col1] in ('p','r','n','b','q','k'):
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row1] + [new_board1[new_row1][0:new_col1] + ['K',] + new_board1[new_row1][new_col1+1:]] + new_board1[new_row1+1:]
                succ_board.append(new_board1)
                
        if row-1>=0:
            new_row2 = row-1
            new_col2 = col
            if board[new_row2][new_col2]==' ' or  board[new_row2][new_col2] in ('p','r','n','b','q','k'):
                new_board2= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board2= new_board2[0:new_row2] + [new_board2[new_row2][0:new_col2] + ['K',] + new_board2[new_row2][new_col2+1:]] + new_board2[new_row2+1:]
                succ_board.append(new_board2)

        if col+1<8:
            new_row3 = row
            new_col3 = col+1
            if board[new_row3][new_col3]==' ' or  board[new_row3][new_col3] in ('p','r','n','b','q','k'):
                new_board3= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board3= new_board3[0:new_row3] + [new_board3[new_row3][0:new_col3] + ['K',] + new_board3[new_row3][new_col3+1:]] + new_board3[new_row3+1:]
                succ_board.append(new_board3)

        
        if col-1>=0:
            new_row4 = row
            new_col4 = col-1
            if board[new_row4][new_col4]==' ' or  board[new_row4][new_col4] in ('p','r','n','b','q','k'):
                new_board4= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board4= new_board4[0:new_row4] + [new_board4[new_row4][0:new_col4] + ['K',] + new_board4[new_row4][new_col4+1:]] + new_board4[new_row4+1:]
                succ_board.append(new_board4)

        if row+1<8 and col+1<8:
            new_row5 = row+1
            new_col5 = col+1
            if board[new_row5][new_col5]==' ' or  board[new_row5][new_col5] in ('p','r','n','b','q','k'):
                new_board5= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board5= new_board5[0:new_row5] + [new_board5[new_row5][0:new_col5] + ['K',] + new_board5[new_row5][new_col5+1:]] + new_board5[new_row5+1:]
                succ_board.append(new_board5)

        if row+1<8 and col-1>=0:
            new_row6 = row+1
            new_col6 = col-1
            if board[new_row6][new_col6]==' ' or  board[new_row6][new_col6] in ('p','r','n','b','q','k'):
                new_board6= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board6= new_board6[0:new_row6] + [new_board6[new_row6][0:new_col6] + ['K',] + new_board6[new_row6][new_col6+1:]] + new_board6[new_row6+1:]
                succ_board.append(new_board6)

        
        if row-1>=0 and col+1<8:
            new_row7 = row-1
            new_col7 = col+1
            if board[new_row7][new_col7]==' ' or  board[new_row7][new_col7] in ('p','r','n','b','q','k'):
                new_board7= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board7= new_board7[0:new_row7] + [new_board7[new_row7][0:new_col7] + ['K',] + new_board7[new_row7][new_col7+1:]] + new_board7[new_row7+1:]
                succ_board.append(new_board7)

            
        if row-1>=0 and col-1>=0:
            new_row8 = row-1
            new_col8 = col-1
            if board[new_row8][new_col8]==' ' or  board[new_row8][new_col8] in ('p','r','n','b','q','k'):
                new_board8= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board8= new_board8[0:new_row8] + [new_board8[new_row8][0:new_col8] + ['K',] + new_board8[new_row8][new_col8+1:]] + new_board8[new_row8+1:]
                succ_board.append(new_board8)

    if turn == "b":

        if row+1<8:
            new_row1= row+1
            new_col1 = col
            if board[new_row1][new_col1]==' ' or  board[new_row1][new_col1] in ('P','R','N','B','Q','K'):
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row1] + [new_board1[new_row1][0:new_col1] + ['k',] + new_board1[new_row1][new_col1+1:]] + new_board1[new_row1+1:]
                succ_board.append(new_board1)
                
        if row-1>=0:
            new_row2 = row-1
            new_col2 = col
            if board[new_row2][new_col2]==' ' or  board[new_row2][new_col2] in ('P','R','N','B','Q','K'):
                new_board2= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board2= new_board2[0:new_row2] + [new_board2[new_row2][0:new_col2] + ['k',] + new_board2[new_row2][new_col2+1:]] + new_board2[new_row2+1:]
                succ_board.append(new_board2)

        if col+1<8:
            new_row3 = row
            new_col3 = col+1
            if board[new_row3][new_col3]==' ' or  board[new_row3][new_col3] in ('P','R','N','B','Q','K'):
                new_board3= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board3= new_board3[0:new_row3] + [new_board3[new_row3][0:new_col3] + ['k',] + new_board3[new_row3][new_col3+1:]] + new_board3[new_row3+1:]
                succ_board.append(new_board3)

        
        if col-1>=0:
            new_row4 = row
            new_col4 = col-1
            if board[new_row4][new_col4]==' ' or  board[new_row4][new_col4] in ('P','R','N','B','Q','K'):
                new_board4= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board4= new_board4[0:new_row4] + [new_board4[new_row4][0:new_col4] + ['k',] + new_board4[new_row4][new_col4+1:]] + new_board4[new_row4+1:]
                succ_board.append(new_board4)

        if row+1<8 and col+1<8:
            new_row5 = row+1
            new_col5 = col+1
            if board[new_row5][new_col5]==' ' or  board[new_row5][new_col5] in ('P','R','N','B','Q','K'):
                new_board5= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board5= new_board5[0:new_row5] + [new_board5[new_row5][0:new_col5] + ['k',] + new_board5[new_row5][new_col5+1:]] + new_board5[new_row5+1:]
                succ_board.append(new_board5)

        if row+1<8 and col-1>=0:
            new_row6 = row+1
            new_col6 = col-1
            if board[new_row6][new_col6]==' ' or  board[new_row6][new_col6] in ('P','R','N','B','Q','K'):
                new_board6= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board6= new_board6[0:new_row6] + [new_board6[new_row6][0:new_col6] + ['k',] + new_board6[new_row6][new_col6+1:]] + new_board6[new_row6+1:]
                succ_board.append(new_board6)

        
        if row-1>=0 and col+1<8:
            new_row7 = row-1
            new_col7 = col+1
            if board[new_row7][new_col7]==' ' or  board[new_row7][new_col7] in ('P','R','N','B','Q','K'):
                new_board7= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board7= new_board7[0:new_row7] + [new_board7[new_row7][0:new_col7] + ['k',] + new_board7[new_row7][new_col7+1:]] + new_board7[new_row7+1:]
                succ_board.append(new_board7)

            
        if row-1>=0 and col-1>=0:
            new_row8 = row-1
            new_col8 = col-1
            if board[new_row8][new_col8]==' ' or  board[new_row8][new_col8] in ('P','R','N','B','Q','K'):
                new_board8= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board8= new_board8[0:new_row8] + [new_board8[new_row8][0:new_col8] + ['k',] + new_board8[new_row8][new_col8+1:]] + new_board8[new_row8+1:]
                succ_board.append(new_board8)


    return succ_board

#Finds all successor boards of Nighthawk at a particular position,according to turn
def knight_move(board,turn,row,col):
    succ_board=[]
    if turn == "w":
        if row+2<8 and col+1<8:
            if board[row+2][col+1]==' ' or board[row+2][col+1] in ('p','r','n','b','q','k'):
                new_row1 = row+2
                new_col1 = col+1
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row1] + [new_board1[new_row1][0:new_col1] + ['N',] + new_board1[new_row1][new_col1+1:]] + new_board1[new_row1+1:]
                succ_board.append(new_board1)

        if row+2<8 and col-1>=0:
            if board[row+2][col-1]==' ' or board[row+2][col-1] in ('p','r','n','b','q','k'):
                new_row2 = row+2
                new_col2 = col-1
                new_board2= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board2= new_board2[0:new_row2] + [new_board2[new_row2][0:new_col2] + ['N',] + new_board2[new_row2][new_col2+1:]] + new_board2[new_row2+1:]
                succ_board.append(new_board2)

        if row-2>=0 and col+1<8:
            if board[row-2][col+1]==' ' or board[row-2][col+1] in ('p','r','n','b','q','k'):
                new_row3 = row-2
                new_col3 = col+1
                new_board3= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board3= new_board3[0:new_row3] + [new_board3[new_row3][0:new_col3] + ['N',] + new_board3[new_row3][new_col3+1:]] + new_board3[new_row3+1:]
                succ_board.append(new_board3)

        if row-2>=0 and col-1>=0:
            if board[row-2][col-1]==' ' or board[row-2][col-1] in ('p','r','n','b','q','k'):
                new_row4 = row-2
                new_col4 = col-1
                new_board4= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board4= new_board4[0:new_row4] + [new_board4[new_row4][0:new_col4] + ['N',] + new_board4[new_row4][new_col4+1:]] + new_board4[new_row4+1:]
                succ_board.append(new_board4)

        if row+1<8 and col+2<8:
            if board[row+1][col+2]==' ' or board[row+1][col+2] in ('p','r','n','b','q','k'):
                new_row5 = row+1
                new_col5 = col+2
                new_board5= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board5= new_board5[0:new_row5] + [new_board5[new_row5][0:new_col5] + ['N',] + new_board5[new_row5][new_col5+1:]] + new_board5[new_row5+1\
:]
                succ_board.append(new_board5)


        if row-1>=0 and col+2<8:
            if board[row-1][col+2]==' ' or board[row-1][col+2] in ('p','r','n','b','q','k'):
                new_row6 = row-1
                new_col6 = col+2
                new_board6= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board6= new_board6[0:new_row6] + [new_board6[new_row6][0:new_col6] + ['N',] + new_board6[new_row6][new_col6+1:]] + new_board6[new_row6+1:]

                succ_board.append(new_board6)

        if row+1<8 and col-2>=0:
            if board[row+1][col-2]==' ' or board[row+1][col-2] in ('p','r','n','b','q','k'):
                new_row7 = row+1
                new_col7 = col-2
                new_board7= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board7= new_board7[0:new_row7] + [new_board7[new_row7][0:new_col7] + ['N',] + new_board7[new_row7][new_col7+1:]] + new_board7[new_row7+1\
\
:]
                succ_board.append(new_board7)


        if row-1>=0 and col-2>=0:
            if board[row-1][col-2]==' ' or board[row-1][col-2] in ('p','r','n','b','q','k'):
                new_row8 = row-1
                new_col8 = col-2
                new_board8= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board8= new_board8[0:new_row8] + [new_board8[new_row8][0:new_col8] + ['N',] + new_board8[new_row8][new_col8+1:]] + new_board8[new_row8+1\
:]
                succ_board.append(new_board8)


    elif turn == "b":
        if row+2<8 and col+1<8:
            if board[row+2][col+1]==' ' or board[row+2][col+1] in ('P','R','N','B','Q','K'):
                new_row1 = row+2
                new_col1 = col+1
                new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board1= new_board1[0:new_row1] + [new_board1[new_row1][0:new_col1] + ['n',] + new_board1[new_row1][new_col1+1:]] + new_board1[new_row1+1:]
                succ_board.append(new_board1)

        if row+2<8 and col-1>=0:
            if board[row+2][col-1]==' ' or board[row+2][col-1] in ('P','R','N','B','Q','K'):
                new_row2 = row+2
                new_col2 = col-1
                new_board2= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board2= new_board2[0:new_row2] + [new_board2[new_row2][0:new_col2] + ['n',] + new_board2[new_row2][new_col2+1:]] + new_board2[new_row2+1:]
                succ_board.append(new_board2)

        if row-2>=0 and col+1<8:
            if board[row-2][col+1]==' ' or board[row-2][col+1] in ('P','R','N','B','Q','K'):
                new_row3 = row-2
                new_col3 = col+1
                new_board3= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board3= new_board3[0:new_row3] + [new_board3[new_row3][0:new_col3] + ['n',] + new_board3[new_row3][new_col3+1:]] + new_board3[new_row3+1:]
                succ_board.append(new_board3)

        if row-2>=0 and col-1>=0:
            if board[row-2][col-1]==' ' or board[row-2][col-1] in ('P','R','N','B','Q','K'):
                new_row4 = row-2
                new_col4 = col-1
                new_board4= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board4= new_board4[0:new_row4] + [new_board4[new_row4][0:new_col4] + ['n',] + new_board4[new_row4][new_col4+1:]] + new_board4[new_row4+1:]
                succ_board.append(new_board4)

        if row+1<8 and col+2<8:
            if board[row+1][col+2]==' ' or board[row+1][col+2] in ('P','R','N','B','Q','K'):
                new_row5 = row+1
                new_col5 = col+2
                new_board5= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board5= new_board5[0:new_row5] + [new_board5[new_row5][0:new_col5] + ['n',] + new_board5[new_row5][new_col5+1:]] + new_board5[new_row5+1\
:]
                succ_board.append(new_board5)


        if row-1>=0 and col+2<8:
            if board[row-1][col+2]==' ' or board[row-1][col+2] in ('P','R','N','B','Q','K'):
                new_row6 = row-1
                new_col6 = col+2
                new_board6= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board6= new_board6[0:new_row6] + [new_board6[new_row6][0:new_col6] + ['n',] + new_board6[new_row6][new_col6+1:]] + new_board6[new_row6+1:]

                succ_board.append(new_board6)

        if row+1<8 and col-2>=0:
            if board[row+1][col-2]==' ' or board[row+1][col-2] in ('P','R','N','B','Q','K'):
                new_row7 = row+1
                new_col7 = col-2
                new_board7= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board7= new_board7[0:new_row7] + [new_board7[new_row7][0:new_col7] + ['n',] + new_board7[new_row7][new_col7+1:]] + new_board7[new_row7+1\
\
:]
                succ_board.append(new_board7)


        if row-1>=0 and col-2>=0:
            if board[row-1][col-2]==' ' or board[row-1][col-2] in ('P','R','N','B','Q','K'):
                new_row8 = row-1
                new_col8 = col-2
                new_board8= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                new_board8= new_board8[0:new_row8] + [new_board8[new_row8][0:new_col8] + ['n',] + new_board8[new_row8][new_col8+1:]] + new_board8[new_row8+1\
:]
                succ_board.append(new_board8)

    return succ_board

#Returns 1 if king is not found,else 0
def king_pos(board):

    
    king_row =  -999
    king_col = -999			
    if turn == "w":
        i= 7
        while i>=0:
            for j in range(0,8):
                if board[i][j] == 'k':
                    king_row = i
                    king_col = j

            i = i-1

    elif turn == "b":
        i=0
        while i<8:
            for j in range(0,8):
                if board[i][j] == 'K':
                    king_row = i
                    king_col = j                    
               
            i=i+1
    if king_row==-999 and king_col==-999:
	return 1
    else:
	return 0

#Finds all successor boards of parakeet at a particular position,according to turn
def pawn_move(board,turn,row,col):
    #Initially the new & col are same as previous
    new_row = row
    new_col = col
    succ_board= []
    i = 0
    j = 0
    #Check for turn
    if turn=="w":

    #Check if we have a piece of enemy at diagonal positions
        if row+1<8 and col-1>=0 and board[row+1][col-1] in ('p','r','n','b','q','k'): 
            new_row1 = row+1
            new_col1 = col-1
            new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
            new_board1= new_board1[0:new_row1] + [new_board1[new_row1][0:new_col1] + ['P',] + new_board1[new_row1][new_col1+1:]] + new_board1[new_row1+1:]
            succ_board.append(new_board1)

        if row+1<8 and col+1<8 and board[row+1][col+1] in ('p','r','n','b','q','k'):
            new_row2 = row+1
            new_col2 = col+1
            new_board2 = board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
            new_board2= new_board2[0:new_row2] + [new_board2[new_row2][0:new_col2] + ['P',] + new_board2[new_row2][new_col2+1:]] + new_board2[new_row2+1:]
            succ_board.append(new_board2)

    # Else we move forward
        if row==1: # check if pawn is at initial position.
           if board[3][col]==' ' and board[2][col]==' ': #Checks if no piece is on the next row. Since jumping of pawns is not allowed
               new_row3=3
               new_board3 = board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
               new_board3 = new_board3[0:new_row3] + [new_board3[new_row3][0:new_col] + ['P',] + new_board3[new_row3][new_col+1:]] + new_board3[new_row3+1:]
               succ_board.append(new_board3)

    #Otherwise we move forward if there is no piece at that locatio
        if row+1 < 8:
           if board[row+1][col]==' ':
                new_row4=row+1
                new_board4 = board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
                if new_row4!=7:
                    new_board4= new_board4[0:new_row4] + [new_board4[new_row4][0:new_col] + ['P',] + new_board4[new_row4][new_col+1:]] + new_board4[new_row4+1:]
                else:
                    new_board4= new_board4[0:new_row4] + [new_board4[new_row4][0:new_col] + ['Q',] + new_board4[new_row4][new_col+1:]] + new_board4[new_row4+1:]
                succ_board.append(new_board4)
    if turn=="b":
        
        if row-1>=0 and col-1>=0 and board[row-1][col-1] in ('P','R','N','B','Q','K'):
            new_row1 = row-1
            new_col1 = col-1
            new_board1= board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
            new_board1= new_board1[0:new_row1] + [new_board1[new_row1][0:new_col1] + ['p',] + new_board1[new_row1][new_col1+1:]] + new_board1[new_row1+1:]
            succ_board.append(new_board1)


        if row-1>=0 and col+1<8 and board[row-1][col+1] in ('P','R','N','B','Q','K'):
            new_row2 = row-1
            new_col2 = col+1
            new_board2 = board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
            new_board2= new_board2[0:new_row2] + [new_board2[new_row2][0:new_col2] + ['p',] + new_board2[new_row2][new_col2+1:]] + new_board2[new_row2+1:]
            succ_board.append(new_board2)

            
        if row==6:
            if board[4][col]==' ' and board[5][col]==' ':
               new_row3=4
               new_board3 = board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
               new_board3 = new_board3[0:new_row3] + [new_board3[new_row3][0:new_col] + ['p',] + new_board3[new_row3][new_col+1:]] + new_board3[new_row3+1:]
               succ_board.append(new_board3)

        if row-1 >=0:
           if board[row-1][col]==' ':
               new_row4=row-1
               new_board4 = board[0:row] + [board[row][0:col] + [' ',] + board[row][col+1:]] + board[row+1:]
               if new_row4!=0:
                   new_board4= new_board4[0:new_row4] + [new_board4[new_row4][0:new_col] + ['p',] + new_board4[new_row4][new_col+1:]] + new_board4[new_row4+1:]
               else:
                   new_board4= new_board4[0:new_row4] + [new_board4[new_row4][0:new_col] + ['q',] + new_board4[new_row4][new_col+1:]] + new_board4[new_row4+1:]
               succ_board.append(new_board4)

    return succ_board

#Checks if it is timeout
#Searchs and prints all the next best moves till it is timeout
depth=1
move = ""
print "Thinking next move.."	

while time() < timeout_start + timeout:
    state = search(arr,depth)
    print "Thinking Another move.."
    move=""	
    for every in state:
        print every
  	for each in every:
		if each==' ':
			move=move+'.'
		else:
			move = move + each
    compare_states(arr,state)
    print move
    depth = depth+1


