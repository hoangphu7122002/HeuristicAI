from helperFunction import *
import copy

#use graph search
class UniformSearch(object):
    def __init__(self,board,N,index_0,max_depth = None):
        self.N = N
        #=========BFS=========
        self.open_list = []
        self.open_list.append(board)  
        self.index = []
        self.index.append(index_0)
        self.closed_list = set()
        self.closed_list.add(self.convert_to_string(board))
        #====================
        #=========DFS========
        self.index_0 = index_0
        self.board = board
        #====================
        
        self.max_depth = max_depth
        if self.max_depth != None:
            self.depth = [0]
        
    def in_closed_list(self,board):
        for ele in self.closed_list:
            if np.array_equal(board,ele):
                return True
        return False
    
    def convert_to_string(self,board):
        string_ele = ""
        for i in range(len(board)):
            for j in range(len(board)):
                string_ele += str(board[i][j])
                string_ele += ' '
        return string_ele
        
    def DFS(self):
        self.DFS_recursion(self.board,self.index_0,0)
    
    def temp_board(self,board,i,j,i0,j0):
        board[i0][j0] = board[i][j]
        board[i][j] = 0
        if self.convert_to_string(board) in self.closed_list :
            board[i][j] = board[i0][j0]
            board[i0][j0] = 0
            return False
        return True
    
    def DFS_recursion(self,board,index0,depth_ele):
        board_ele = board
        i,j = index0
        print("========STEP========")
        print(board_ele)
        if self.max_depth != None:
            if depth_ele > self.max_depth:
                return None        
        if check_solution(board_ele,self.N) == True:
            print("=========DONE========")
            return True
        for k in range(4):
            if inbound(self.N,i + dx[k],j + dy[k]) == True:     
                i_ele,j_ele = i + dx[k],j + dy[k]
                new_board = copy.deepcopy(board_ele)
                if self.temp_board(new_board,i_ele,j_ele,i,j) == True:
                    self.DFS_recursion(new_board,(i_ele,j_ele),depth_ele + 1)
        return None

    def BFS(self):
        while len(self.open_list) > 0:                        
            i,j = self.index.pop(0)
            board_ele = self.open_list.pop(0)
            print("========STEP========")
            if self.max_depth != None:
                depth_ele = self.depth.pop(0)
                if depth_ele > self.max_depth:
                    continue
            if check_solution(board_ele,self.N) == True:
                print("=========DONE========")
                return True
            for k in range(4):
                if inbound(self.N,i + dx[k],j + dy[k]) == True:
                    i_ele,j_ele = i + dx[k],j + dy[k]
                    new_board = copy.deepcopy(board_ele)
                    if self.temp_board(new_board,i_ele,j_ele,i,j) == True:
                        print(new_board)
                        self.closed_list.add(self.convert_to_string(new_board))
                        self.open_list.append(new_board)
                        self.index.append((i_ele,j_ele))
                        if self.max_depth != None:
                            self.depth.append(depth_ele + 1)
        print("========No Solution========")
        return False
                    
N = 3
board,index_0 = random_board(N)
uni = UniformSearch(board,N,index_0,30)
print(uni.DFS())