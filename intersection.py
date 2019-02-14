## intersection problem 
## python 3
import random
import time
import threading

quadrant_locks = {"NW": threading.Semaphore(), "NE": threading.Semaphore(), "SW": threading.Semaphore(), "SE": threading.Semaphore()}
quadrant = {"NW": 0, "NE": 0, "SW": 0, "SE": 0}

directions = ["left", "straight", "right"]
cardinal_directions = ["N", "S", "W", "E"]

cardinalize = {"S": {"left": "W", "right": "E", "straight": "N"}, 
               "E": {"left": "S", "right": "N", "straight": "W"},
               "N": {"left": "E", "right": "W", "straight": "S"},
               "W": {"left": "N", "right": "S", "straight": "E"}        
               }

# eg. from "S" turning "left" is SE, NE, NW
def path_generator(entry_direction, relative_path):
    ed = entry_direction
    path = []
    if(relative_path == "left"):
        path.append(ed + cardinalize[ed]["right"])
        path.append(cardinalize[ed]["straight"] + cardinalize[ed]["right"])
        path.append(cardinalize[ed]["straight"] + cardinalize[ed]["left"])
    if(relative_path == "straight"):
        path.append(ed + cardinalize[ed]["right"])
        path.append(cardinalize[ed]["straight"] + cardinalize[ed]["right"])
    if(relative_path == "right"):
        path.append(ed + cardinalize[ed]["right"])
    # reorder letters for misordered groups of pairs
    if(ed == "W" or ed == "E"):
        for i in range(len(path)):
            path[i] = path[i][1] + path[i][0]
    return path
        

def car(car_number):
    entry_direction = cardinal_directions[random.randint(0,3)] # [0,3]
    relative_path = directions[random.randint(0,2)]
    path = path_generator(entry_direction, relative_path)
    # the below line makes everything work
    # this thread will lock the semaphores it needs as it passes through the 
    # intersection, but if it locks them in any order, there can be deadlocks
    # to avoid we can give the locks an order (lexicographic is just one)
    # that will always make a thread try to lock with the SAME lock first
    # in this case, there is no gridfucks. take a moment to think about
    # ordered locking
    path.sort()
    
    time.sleep(random.randint(0,2))
    print("   car # " + str(car_number) + " approaches from " + entry_direction)

    pathprint = ""
    for i in range(len(path)):
        quadrant_locks[path[i]].acquire()
        quadrant[path[i]] = 1
        pathprint += path[i] + " "
    
    time.sleep(random.randint(0,2))
    print("   car # " + str(car_number) + " is going " + relative_path + " by takin quadrants " + pathprint)
    
    for i in range(len(path)):
        quadrant[path[i]] = 0
        quadrant_locks[path[i]].release()
        
    print("   car # " + str(car_number) + " leaves in direction " + cardinalize[entry_direction][relative_path])

    
threads = []
for i in range(0,20):
    t = threading.Thread(target=car, args = (i+1,)) # weird arg syntax (arg,) is pythons fault
    threads.append(t)
    t.start()
