import matplotlib.pyplot as plt
from multiprocessing import Process, Manager
import time
from random import randrange
from readFile import readFile

N = 1 # input port
input_rate = int(45e6) # input transmision capacity
C = [15, 25, 35] # outgoing rate(per second)
C = 25
B = 1000 # Buffer size 
num_frame = 100

class Packet:
    i = 0
    def __init__(self,lenght,num):
        self.time_process = 0
        self.birth_time = time.monotonic()
        self.size = lenght
        self.frameNumber = num
        self.string = 'Packet'+ str(Packet.i)
        Packet.i = Packet.i + 1
    
    def __str__(self):
        return self.string

def display(L):
    print('[', end=' ')
    for i in L:
        print(i,end=' ')
    print(']')    

def arrive(L, V, PLR):  # the managed list `L` passed explicitly.
    print('L1')
    print(V)
    total_packets = 0
    loss_packets = 0
    for i in range(len(V)):
        time.sleep(1/25)
        if len(L) < B: 
            print('Frame is recieved!')
            packets = Frame_to_Packets(V[i],i)
            total_packets = total_packets + len(packets)
            if (len(L))+(len(packets)) <= B:
                L[0:0]=packets              # insert packets to L element by element
                #print('L:',end=' ')
                #display(L)
            else:
                loss_packets = loss_packets + len(packets)
                
    PLR.append(total_packets)
    PLR.append(loss_packets)
    PLR.append(loss_packets/total_packets)
    

def depart(L, i):  # the managed list `L` passed explicitly.
    print('L2')
    num_buffer_zero = 0
    r = 75  # r packet per 1 sec
    while True:
        time.sleep(1/r)
        if len(L) > 0:
            print('Packet is departed!')
            L.pop()
            #print('L:',end=' ')
            #display(L)
            print('***********  L = ', len(L) ,'    ***********')
            num_buffer_zero = 0
        else:
            num_buffer_zero = num_buffer_zero + 1
            if num_buffer_zero > 25:
                break;

def Frame_to_Packets(bits,frameNumber):
    min_packet_size = 80
    bits_res = bits
    packets = []
    size = (min_packet_size + randrange(0,40)) * 8 # 8 for byte to bit
    packets.insert(0,Packet(size+(20*8), frameNumber))        # 20*8 for IP header
    bits_res = bits_res - size
    while bits_res > 0:
        size = (min_packet_size + randrange(0,40)) * 8
        if size > bits_res:
            packets.insert(0,Packet(bits_res+(20*8), frameNumber))
        else:
            packets.insert(0,Packet(size+(20*8), frameNumber))
        bits_res = bits_res - size 
        
    return packets        
        
    
        
    
           
            

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
        PLR = manager.list()
        processes = []
        p1 = Process(target=arrive, args=(L, V1, PLR))  # Passing the list
        p1.start()
        processes.append(p1)
        p2 = Process(target=depart, args=(L,1))  # Passing the list
        p2.start()
        processes.append(p2)
        for p in processes:
            p.join()
        print(L)
        print(PLR)











