import threading

#Create threads to run mutliple functions (SSH connections) simultaneously

def create_threads(list,function):
    threads = []
    
    for ip in list:
        th = threading.Thread(target = function, args = (ip,)) #args is a tuple with single element
        th.start()
        threads.append(th)
        
    for th in threads:
        th.join()
        
        
        