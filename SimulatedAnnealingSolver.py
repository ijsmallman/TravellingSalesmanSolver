import math
import random
from CommonRouteMethods import random_swap, circular_route_length, generate_random_route
    
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
  



