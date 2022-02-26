import pandas as pd
import numpy as np
import math
import copy
from cross_over_method import method_cross_over
from mutant_method import method_mutant
from visualize import Board
import cv2

N = 8 #init population

# np.random.seed(0)
board = np.random.randint(1,N + 1,(N,N))
        
print(board)        

#=====================================================
#REFACTORING CODE
#=====================================================

def get_unique_list(a):
    unique = []
    for number in a:
        flag = False
        for ele in unique:
            if np.array_equal(ele,number):
                flag = True
                break
        if flag == False:
            unique.append(number)
        
    return unique

def search(b,num):
    index = -1    
    for i in range(N + 1):
        if b[i] > num:
            index = i - 1
            break
    if index == -1:
        return N
    return index        

def fighting(res,lst_candidate):
    candidate_pair = [(res[ele],ele) for ele in lst_candidate]
    candidate_pair = sorted(candidate_pair,reverse = True)
    
    return candidate_pair
    
#=====================================================

class genAlgo(object):
    
    def __init__(self,board,N,option):
        self.board = board
        self.N = N
        self.candidate = []
        self.mutant = method_mutant([],self.N)
        self.cross_over = method_cross_over([],self.N)
        self.option = option # age : 1, not age : 0
     
    def point(self,b):
        count = 0
        for i in range(0,self.N - 1):
            step = 1
            for j in range(i + 1,self.N):
                if b[i] + step == b[j]:
                    count += 1
                if b[i] - step == b[j]:
                    count += 1
                if b[i] == b[j]:
                    count += 1
                step += 1
        # print((self.N * (self.N - 1))//2 - count,b)
        return (self.N * (self.N - 1))//2 - count
    
    def check_distribution(self):
        count = 1
        pattern_point = self.point(self.board[0])
        for i in range(1,len(self.board)):
            if self.point(self.board[i]) == pattern_point:
                count += 1
            else: break
        if count >= 3:
            return True
        return False
    
    def fitness(self):
        res = np.zeros(N)
        index = 0
        for b in self.board:
            res[index] = self.point(b)
            index += 1
        return res
        
    def fitness_proportionate_selection(self):
        res = self.fitness()
        
        res_pair = [(a,b) for a,b in zip(res,range(0,self.N))]         
        res_pair = sorted(res_pair,reverse = True)
        
        b = np.zeros(self.N + 1)
        b[0] = 0
        
        for i in range(1,self.N + 1):
            a,_ = res_pair[i - 1]
            b[i] = b[i - 1] + a 
    
        gen = set()
        step = self.N
        
        while(step):
            step -= 1
            _,candidate1 = res_pair[search(b,np.random.randint(0,b[self.N]))]
            _,candidate2 = res_pair[search(b,np.random.randint(0,b[self.N]))]
            
            while candidate2 == candidate1:    
                _,candidate2 = res_pair[search(b,np.random.randint(0,b[self.N]))]
            if (candidate1,candidate2) in gen or (candidate2,candidate1) in gen:
                step += 1
                continue    
            gen.add((candidate1,candidate2))
        return gen
    
    def tournament_selection(self):
        res = self.fitness()
        gen = set()
        step = self.N
        while(step):
            step -= 1
            
            size = np.random.randint(2,self.N + 1)
            lst_candidate = []
            
            while len(lst_candidate) < size:
                ele = np.random.randint(0,self.N)
                if ele in lst_candidate:
                    continue
                lst_candidate.append(ele)
            
            candidate_pair = fighting(res,lst_candidate)
            _,candidate_1 = candidate_pair[0]
            _,candidate_2 = candidate_pair[1]
            if (candidate_1,candidate_2) in gen or (candidate_2,candidate_1) in gen:
                step += 1
                continue
            
            gen.add((candidate_1,candidate_2))
        return gen
        
    def rank_selection(self):
        #sort follow rank
        pass
        
    def gen_cross_over(self,option = 0):
        gen = None
        if option == 0:
            gen = self.fitness_proportionate_selection()  
        elif option == 1:
            gen = self.tournament_selection()
        else: 
            pass
        for g in gen:
            f_1, f_2 = g
            rand_option = np.random.randint(0,4)
            if rand_option == 0: self.cross_over.half_gen(self.board[f_1],self.board[f_2])
            elif rand_option == 1: self.cross_over.davidOrderCrossover(self.board[f_1],self.board[f_2])
            elif rand_option == 2: self.cross_over.uniform_crossover(self.board[f_1],self.board[f_2])
            else: self.cross_over.multipoint_cross_over(self.board[f_1],self.board[f_2])
        
        for ele in self.cross_over.get_candidate():
            self.candidate.append(ele)
        self.candidate = get_unique_list(self.candidate)
        
    def reset_candidate(self):
        self.candidate = []
    
    def reset_board(self):
        self.board = []
    
    def gen_mutant(self):
        for ele in self.board:
            rand_option = np.random.randint(0,8)

            if rand_option in range(0,4): self.mutant.ele_not_appear(ele)
            elif rand_option == 4: self.mutant.inversion_mutation(ele)
            elif rand_option == 5: self.mutant.random_resetting(ele)
            elif rand_option == 6: self.mutant.swap_mutation(ele)
            else: self.mutant.scramble_mutation(ele)
            
        for ele in self.mutant.get_candidate():
            self.candidate.append(ele)
        self.candidate = get_unique_list(self.candidate)
        
    def fitness_based_eliminate(self):
        self.cross_over = method_cross_over([],self.N)
        max_ele = np.argsort([self.point(ele) for ele in self.board])
        # random_ele = np.random.randint(0,2)
        self.gen_cross_over(0)        
        for ele in self.board:
            self.candidate.append(ele)
        self.candidate = get_unique_list(self.candidate)
                
        pair_population = [(self.point(ele),ele) for ele in self.candidate]
        pair_population = sorted(pair_population,reverse = True,key=lambda x: x[0])
        
        max_temp,_ = pair_population[0]
        
        if np.array_equal(self.board[max_ele[0]],max_temp) or self.check_distribution() == True:
            #===================MUTANT===================
            self.gen_mutant()
            for ele in self.mutant.get_candidate():
                pair_population.append((self.point(ele),ele))
            pair_population = sorted(pair_population,reverse = True,key=lambda x: x[0])
            #===================MUTANT===================
        self.reset_board()
        print(N,len(pair_population))
        for i in range(self.N):
            
            _,e =  pair_population[i]
            self.board.append(e)
        self.reset_candidate()
        
    def check_solution(self):
        flag = False
        maximum_point = self.N * (self.N - 1) // 2 
        for b in self.board:
            if self.point(b) == maximum_point:
                if flag == False:
                    print("\n================SOLUTION=================\n")
                flag = True
                print(f"{b}\n")
                board_vis = Board(size = N)
                
                ele = b
                
                print(ele,self.point(ele))
                for i,e in enumerate(ele):
                    board_vis.put('queen',(i,e - 1))
                board_vis.draw()
                # board_vis.panel = cv2.putText(board_vis.panel, f'Solution{i_}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
                
                board_vis.show(1)
                
                
            else:
                break
        if flag == True:
            print("\n=================END==================\n")
        return flag
    
    def algorithm(self):
        flag = False
        i_ = 1
        # count = 0
        
        
        while flag == False:
            print("PROCESS {}\n".format(i_))
            ele = self.board[0]
            board_vis = Board(size = N)
            print(ele,self.point(ele))
            for i,e in enumerate(ele):
                board_vis.put('queen',(i,e - 1))
            board_vis.draw()
            # board_vis.panel = cv2.putText(board_vis.panel, f'Solution{i_}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
            
            board_vis.show()
                
            self.fitness_based_eliminate()
            flag = self.check_solution()
            # if count != 10 and flag == True:
            #     count += 1
            #     flag = 1 - flag
            i_ += 1
            if i_ >= 30:
                self.board = np.random.randint(1,self.N + 1,(self.N,self.N))
                i_ = 0
            self.reset_candidate()
        
if __name__ == "__main__":
    a = genAlgo(board,N,1)
    a.algorithm()