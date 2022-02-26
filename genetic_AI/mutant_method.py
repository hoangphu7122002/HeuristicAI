import copy
import numpy as np

class method_mutant(object):
    def __init__(self,candidate,N):
        self.candidate = candidate
        self.N = N
    
    def point(self,b):
        count = 0
        for i in range(0,self.N - 1):
            for j in range(i + 1,self.N):
                if b[i] + j == b[j]:
                    count += 1
                if b[i] - j == b[j]:
                    count += 1
                if b[i] == b[j]:
                    count += 1
        return (self.N * (self.N - 1))/2 - count
    
    def random_resetting(self,a):
        random_index = np.random.randint(0,len(a))
        
        b = copy.deepcopy(a)
        
        ele = b[random_index]
        random_ele = np.random.randint(0,len(a))
        while ele == random_ele:
            random_ele = np.random.randint(0,len(a))
        
        b[random_index] = random_ele
        self.candidate.append(np.array(b))
        
        return None
    
    def swap_mutation(self,a):
        begin = np.random.randint(0,self.N//2)
        end = np.random.randint(self.N//2,self.N)
        #--------------------------------
        b = copy.deepcopy(a)
        b[begin],b[end] = b[end],b[begin]
        #--------------------------------
        self.candidate.append(np.array(b))
        
        return None
    
    def inversion_mutation(self,a):
        begin = np.random.randint(0,self.N//2)
        end = np.random.randint(self.N//2,self.N)
        #--------------------------------
        b = copy.deepcopy(a)
        while begin < end:
            b[begin],b[end] = b[end],b[begin]
            begin += 1
            end -= 1
        #--------------------------------
        
        self.candidate.append(np.array(b))
        
        return None
    
    def ele_not_appear(self,a):  
        b = np.zeros(len(a) + 1)
        a_can = copy.deepcopy(a)
        
        for ele in a:
            b[ele] += 1
        
        ele_not_appear = []
        for i in range(len(a)):
            if b[i + 1] == 0:
                ele_not_appear.append(i + 1)
        
        if len(ele_not_appear) == 0:
            return None
            
        index = 0
            
        for i in range(len(a)):
            if b[a[i]] >= 2:
                a_can[i] = ele_not_appear[index]
                index += 1
                b[a[i]] -= 1
        
        self.candidate.append(np.array(a_can))
        return None
    
    def scramble_mutation(self,a):
        a_can = copy.deepcopy(a)
        
        begin = np.random.randint(0,self.N//2)
        end = np.random.randint(self.N//2,self.N)
        
        np.random.shuffle(a_can[begin : end])
        
        self.candidate.append(np.array(a_can))
        return None
    
    def get_candidate(self):
        return self.candidate