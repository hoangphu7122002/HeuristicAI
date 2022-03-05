from queue import PriorityQueue
import numpy as np

q = PriorityQueue()

m = np.array([1,2,3])
m1 = np.array([1,2,3])

q.put((10,m))
q.put((8,m))
q.put((4,m))
q.put((4,m1))
while not q.empty():
    item,_ = q.get()
    print(item)