import matplotlib.pyplot as plt
from multiprocessing import Process, Manager
import time
from random import randrange
from readFile import readFile

N = 1 # input port
input_rate = int(45e6) # input transmision capacity
C = 25
B = 500 * 1000   # [bit] Roughly is numOfPakets * average bit in packet
num_frame = 10000

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

def arrive(L, V, PLR, fulled_released):  # the managed list `L` passed explicitly.
    print('L1')
    print(V)
    total_packets = 0
    loss_packets = 0       
    for i in range(len(V)):
        time.sleep(1/25)
        #if len(L) < B: 
        if (fulled_released[0] - fulled_released[1]) < B:
            print('Frame is recieved!')
            packets, total_size = Frame_to_Packets(V[i],i)
            total_packets = total_packets + len(packets)
            if ((fulled_released[0] - fulled_released[1]) + total_size) <= B:
                L[0:0]=packets              # insert packets to L element by element
                fulled_released[0] = fulled_released[0] + total_size
                #print('FF11')
                #print(fulled_released)
                #print('L:',end=' ')
                #display(L)
            else:
                print('Frame is discard!')
                loss_packets = loss_packets + len(packets)
                
    PLR.append(total_packets)
    PLR.append(loss_packets)
    PLR.append(loss_packets/total_packets)
    

def depart(L, i, fulled_released):  # the managed list `L` passed explicitly.
    print('L2')
    num_buffer_zero = 0
    r = 100  # r packet per 1 sec
    while True:
        time.sleep(1/r)
        if len(L) > 0:
            if (time.monotonic() - L[len(L)-1].birth_time) > 1/r:   # Time to process packet
                print('Packet is departed!')
                p = L.pop()
                fulled_released[1] = fulled_released[1] + p.size
                print(fulled_released)
                del(p)
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
    total_size_packet = 0
    size = (min_packet_size + randrange(0,40)) * 8 # 8 for byte to bit
    size_with_IP = size + (20*8)
    packets.insert(0,Packet(size_with_IP, frameNumber))        # 20*8 for IP header
    total_size_packet = total_size_packet + size_with_IP
    bits_res = bits_res - size
    while bits_res > 0:
        size = (min_packet_size + randrange(0,40)) * 8
        if size > bits_res:
            size_with_IP = bits_res+ (20*8)
            packets.insert(0,Packet(size_with_IP, frameNumber))
            total_size_packet = total_size_packet + size_with_IP
        else:
            size_with_IP = size + (20*8)
            packets.insert(0,Packet(size_with_IP, frameNumber))
            total_size_packet = total_size_packet + size_with_IP
            
        bits_res = bits_res - size 
        
    return packets, total_size_packet        
        
    
        
    
           
            

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
        L = manager.list()  # <-- can be shared between processes. Packet store in L
        PLR = manager.list()
        fulled_released = manager.list([0,0])
        processes = []
        p1 = Process(target=arrive, args=(L, V1, PLR, fulled_released))  # Passing the list
        p1.start()
        processes.append(p1)
        p2 = Process(target=depart, args=(L, 1, fulled_released))  # Passing the list
        p2.start()
        processes.append(p2)
        for p in processes:
            p.join()
        print(L)
        print(PLR)



'''
loss = [0.66,0.622,0.6043,0.573,0.5036,0.475,0.470]
c = [5,10,25,50,75,100,200]

plt.figure('1')
plt.plot(c, loss)
plt.grid()





import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
'''









