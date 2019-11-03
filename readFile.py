
def readFile(name):
    with open(name,'r') as f:
        data_string = f.readlines()
        data = [int(i) for i in data_string] 
    return data


class Queue:

    def __init__(self):
        self.queue = []

    def enqueue(self, item):
        self.queue.append(item)

    def dequeue(self):
        if len(self.queue) < 1:
            return None
        return self.queue.pop(0)

    def size(self):
        return len(self.queue)