
"""
import multiprocessing

def worker(self):
    self.put("Hello world")
    print("dd")
    
if __name__ == "__main__":
    result = multiprocessing.Process(target=worker)
    result.start()
    result.join()
"""





"""                                #  Add ((args))

import multiprocessing

def worker(self):
    print(f" number {self} data")
    
if __name__ == "__main__":
    processes = []
    for i in range(5):    
        p = multiprocessing.Process(target=worker, args=(i, ))
        processes.append(p)
        p.start()
        
    for p in processes:
        p.join()

"""




"""                               Add   Queue

import multiprocessing

def worker(self):
    self.put("data")
    
def worker2(p):
    print(f"detail: {p.get()}")
    
if __name__ == "__main__":
    q = multiprocessing.Queue()
    
    p = multiprocessing.Process(target=worker, args=(q, ))
    p.start()
    
    p2 = multiprocessing.Process(target=worker2, args=(q, ))
    p2.start()
    
    p.join()
    p2.join()
"""







"""                                pool 
import multiprocessing

def square(x):
    return x * x

if __name__ == "__main__":
    with multiprocessing.Pool(4) as p:
        result = p.map(square, [1, 2, 3, 4])   

    print(result)
    
"""