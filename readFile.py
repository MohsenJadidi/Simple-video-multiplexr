
def readFile(name):
    with open(name,'r') as f:
        data_string = f.readlines()
        data = [int(i) for i in data_string] 
    return data


