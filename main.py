import matplotlib.pyplot as plt
from multiprocessing import Process, Manager
import time
from readFile import readFile

N = 1 # input port
input_rate = int(45e6) # input transmision capacity
C = [15, 25, 35] # outgoing rate(per second)
C = 25
B = 10 # Buffer size 
num_frame = 100

class Packet:
    i = 0
    def __init__(self):
        self.time_process = 0
        self.birth_time = time.monotonic()
        self.string = 'Packet'+ str(Packet.i)
        Packet.i = Packet.i + 1
    
    def __str__(self):
        return self.string

def display(L):
    print('[', end=' ')
    for i in L:
        print(i,end=' ')
    print(']')    

def arrive(L, V):  # the managed list `L` passed explicitly.
    print('L1')
    print(V)
    for i in range(len(V)):
        time.sleep(1/25)
        if len(L) < B: 
            print('Frame is recieved!')
            #packets = Frame_to_Packets(V(i))
            L.insert(0,Packet())
            print('L:',end=' ')
            display(L)

def depart(L, i):  # the managed list `L` passed explicitly.
    print('L2')
    num_buffer_zero = 0
    while True:
        time.sleep(2/25)
        if len(L) > 0:
            print('Frame is departed!')
            L.pop()
            print('L:',end=' ')
            display(L)
            num_buffer_zero = 0
        else:
            num_buffer_zero = num_buffer_zero + 1
            if num_buffer_zero > 25:
                break;

#def Frame_to_Packets:
           
            

if __name__ == "__main__":  

    
    V1 = readFile('V1.txt')
#    V2 = readFile('V2.txt')
#    V3 = readFile('V3.txt')
    V1 = V1[0:num_frame]        
    '''
    t = [int(i) for i in range(len(V1))]
    plt.figure('Plot V1')
    plt.plot(t[0:10000], V1[0:10000])
    '''
    with Manager() as manager:
        L = manager.list()  # <-- can be shared between processes.
        processes = []
        p1 = Process(target=arrive, args=(L,V1))  # Passing the list
        p1.start()
        processes.append(p1)
        p2 = Process(target=depart, args=(L,1))  # Passing the list
        p2.start()
        processes.append(p2)
        for p in processes:
            p.join()
        print(L)



























