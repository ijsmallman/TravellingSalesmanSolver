import random
import math

def generate_random_route(n):
    route = range(n)
    random.shuffle(route)
    return route

def separation(coordA,coordB):
    xSep = coordB[0] - coordA[0]
    ySep = coordB[1] - coordA[1]
    return math.sqrt( xSep*xSep + ySep*ySep )
    
def rotate(l,n):
    n = n % len(l)
    return l[-n:] + l[:-n]

def circular_route_length(node_map, route):
    return sum(map(separation, [node_map[i] for i in route], rotate([node_map[i] for i in route],-1)))

def random_swap(route):
    r = route[:] #NOTE lists are passed by reference
    i = random.randint(1,len(r)-1)
    j = random.randint(1,len(r)-1)
    temp = r[i]
    r[i] = r[j]
    r[j] = temp
    return r