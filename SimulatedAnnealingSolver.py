import math
import random

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
    
def stochastic_test(tMax,temp,lenOld,lenNew):
    p = math.exp(-tMax*abs(lenOld-lenNew)/((lenOld+lenNew)*temp))
    r = random.random()
    if (r<=p):
        return True
    else:
        return False
        
def generate_new_route(node_map,route,temp,tMax):
    newRoute = random_swap(route)
    lenOld = circular_route_length(node_map,route)
    lenNew = circular_route_length(node_map,newRoute)
    if (lenNew <= lenOld):
        return newRoute
    else:
        if (stochastic_test(tMax, temp, lenOld, lenNew)):
            return newRoute
        else:
            return route[:]

def generate_random_route(n):
    route = range(n)
    random.shuffle(route) # N.B. shuffle changes order of route
    return route
            
def find_shortest_route(node_map, steps, tMax):
    
    # Set initial temp
    temp = 1.0
    # Calc change in temp
    dT = 1.0/steps
    
    # Create list for route length tracking over time
    route_lengths = []
    
    # Generate an initial random route
    route = generate_random_route(len(node_map))
    
    while temp > 0:
        route = generate_new_route(node_map, route, temp, tMax)
        
        # Track route length
        route_lengths.append(circular_route_length(node_map, route))
        
        # Decrease temperature
        temp -= dT
    
    return route_lengths, route
  



