from helperFunction import *
import copy
from queue import PriorityQueue
from heuristicF import *
import time

class HeuristicSearch(object):
    def __init__(self,board,N,index_0,heuristic_function):
        self.heuristic_function = heuristic_function
        # count = self.title_outs_place(board)
        # self.open_list.put((count,0,index_0,self.convert_to_string(board)))
        # self.closed_list = set()
        # self.closed_list.add(self.convert_to_string(board))
        self.N = N
        self.index_0 = index_0
        self.board = board
    
    def temp_board(self,board,i,j,i0,j0):
        board[i0][j0] = copy.deepcopy(board[i][j])
        board[i][j] = 0
        if self.convert_to_string(board) in self.closed_list :
            board[i][j] = copy.deepcopy(board[i0][j0])
            board[i0][j0] = 0
            return False
        return True
    
    def convert_to_string(self,board):
        string_ele = ""
        for i in range(len(board)):
            for j in range(len(board)):
                string_ele += str(board[i][j])
                string_ele += ' '
        return string_ele
    
    def convert_string_to_matrix(self,str):
        board = np.zeros((self.N,self.N))
        ele = str.strip().split()
        for i in range(len(board)):
            for j in range(len(board)):
                board[i][j] = int(float(ele[i * self.N + j]))
        return board
        
    def A_star(self): #tree search
        #initialize
        #----------------------------
        self.open_list = PriorityQueue()
        count = self.title_outs_place(self.board)
        #----------------------------
        
        self.open_list.put((count,0,self.index_0,self.convert_to_string(self.board)))
        while not self.open_list.empty():                        
            point,depth,idx,board_ele = self.open_list.get()
            i,j = idx
            board_ele = self.convert_string_to_matrix(board_ele)
            print("========STEP==========")
            print(point,depth)
            print(board_ele)
            # time.sleep(1)
            print("=====================")
            if check_solution(board_ele,self.N) == True:
                print("=========DONE========")
                return True            
            for k in range(4):
                if inbound(self.N,i + dx[k],j + dy[k]) == True:
                    i_ele,j_ele = i + dx[k],j + dy[k]
                    new_board = copy.deepcopy(board_ele)
                    
                    new_board[i][j] = copy.deepcopy(new_board[i_ele][j_ele])
                    new_board[i_ele][j_ele] = 0
                    
                    # if self.temp_board(new_board,i_ele,j_ele,i,j) == True:
                    count = self.title_outs_place(new_board)
                    index_0 = (i_ele,j_ele)
                    self.open_list.put((count + depth + 1,depth + 1,index_0,self.convert_to_string(new_board)))
                    # self.closed_list.add(self.convert_to_string(new_board))
        print("========No Solution=========")
        return False
    
    def anneling(self):
        pass
        
            
    def hill_climbing(self):
        max_step = 10000
        idx = 0  
        temp_board = self.board
        temp_index = self.index_0
        epsilon = 0.1
        while idx < max_step:
            lst = PriorityQueue()
            idx += 1
            i,j = temp_index
            print(self.title_outs_place(temp_board))
            print(temp_board)
            if check_solution(temp_board,self.N) == True:
                print("=========DONE========")
                return True        
            for k in range(4):
                if inbound(self.N,i + dx[k],j + dy[k]) == True:
                    i_ele,j_ele = i + dx[k],j + dy[k]
                    new_board = copy.deepcopy(temp_board)
                    new_board[i][j] = copy.deepcopy(new_board[i_ele][j_ele])
                    new_board[i_ele][j_ele] = 0
                    lst.put((self.title_outs_place(new_board),(i_ele,j_ele),self.convert_to_string(new_board)))
            if np.random.rand() > epsilon:
                _,index,temp_board_str = lst.get()
            else:
                lst.get()
                temp_len = lst._qsize()
                temp_lst = [lst.get() for _ in range(temp_len)]
                np.random.shuffle(temp_lst)
                _,index,temp_board_str = temp_lst[0]
                
            temp_board = self.convert_string_to_matrix(temp_board_str)
            temp_index = index
        print("\n==============NO SOLUTION==============\n")
        return False
    
    def title_outs_place(self,board):
        count = 0
        for i in range(len(board)):
            for j in range(len(board)):
                i_ele,j_ele = position_to_index(len(board),board[i][j])
                count += self.heuristic_function(i,j,i_ele,j_ele)
        return count
    
N = 3
board,index_0 = random_board(N)
heu = HeuristicSearch(board,N,index_0,missPlace)
print(heu.hill_climbing())