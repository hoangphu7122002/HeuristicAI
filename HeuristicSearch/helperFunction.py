from tkinter.messagebox import YES
import numpy as np

dx = [0,0,-1,1]
dy = [-1,1,0,0]

def index_to_position(N,i,j):
    return N * i + j + 1
    
def position_to_index(N,ele):
    ele = ele - 1
    i = ele // N
    j = ele % N
    
    return (i,j)

def random_board(N):
    board = np.arange(N * N)
    np.random.shuffle(board)
    board = board.reshape((N,N))
    index0 = None
    for i in range(N):
        for j in range(N):
            if board[i][j] == 0:
                index0 = (i,j)
                break   
    return board,index0
    
def goal_board(N):
    board = np.arange(1,N * N + 1).reshape(N,N)
    board[N - 1][N - 1] = 0
    
    return board

def check_solution(board,N):
    for i in range(N):
        for j in range(N):
            if i == N - 1 and j == N - 1:
                if board[i][j] != 0:
                    return False
            else:
                ele = board[i][j]
                x,y = position_to_index(N,ele)
                if i != x or j != y:
                    return False
    return True

def inbound(N,x,y):
    if x < 0 or x >= N:
        return False
    if y < 0 or y >= N:
        return False
    return True
    
