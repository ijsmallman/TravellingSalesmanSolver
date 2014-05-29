import numpy as np
from CommonRouteMethods import  separation, circular_route_length

def init_pheramone_matrix(n):
    matrix = np.ones((n,n))
    #np.fill_diagonal(matrix, 0)
    return matrix  

def quality_factor(node_map, current_node, destination_node):
    sep = separation(node_map[current_node], node_map[destination_node])
    if sep == 0.0:
        return 0.0
    else:
        return 1.0/separation(node_map[current_node], node_map[destination_node])

def probability_vector(node_map, pheramone_matrix, visited_nodes):
    
    # Make a vector of destinations that are disallowed
    forbiddon_destinations = visited_nodes

    # Now make a vector with 0s at locations of forbiddon destinations 
    permitted_destination_vector = np.ones(len(pheramone_matrix))
    permitted_destination_vector[forbiddon_destinations] = 0.0
    
    # Get a pheramone path vector based on permitted destinations
    # and the pheramone matrix
    pheramone_path_vector = permitted_destination_vector*pheramone_matrix[visited_nodes[-1]]
    
    # Generate a vector of heuristic factors that are inversely proportional to
    # the distances to each destination
    quality_vector = [quality_factor(node_map, visited_nodes[-1], x) for x in xrange(len(node_map))]
    
    # Get un-normalisesed probability vector
    probability_vector = quality_vector*pheramone_path_vector
    
    norm = sum(probability_vector)
    
    return probability_vector/norm

def sort_destinations(probability_vector):
    return sorted(zip(probability_vector, range(len(probability_vector))), reverse = True)

def get_next_node(node_map, pheramone_matrix, visited_nodes):
    
    # Get vector of probabilities
    prob_vec = probability_vector(node_map, pheramone_matrix, visited_nodes)  
    
    # Sort destinations according to probability
    sorted_destinations = sort_destinations(prob_vec)
    
    # Select a destination based on probabilities
    rand = np.random.random()
    accFit = 0.0
    for destination in sorted_destinations:
        accFit += destination[0] # sorted_destinations = [[probability,destination],...]
        
        if accFit > rand:
            return destination[1]
    

def generate_route(node_map, pheramone_matrix):
    
    # Start on node 0
    node = 0
    route = [node]
    
    # Calculate and store number of nodes in route
    nodes = len(pheramone_matrix)
    
    while len(route) < nodes:
        # Generate next node that is not currently in the route
        next_node = get_next_node(node_map, pheramone_matrix, route)
        route.append(next_node)
    
    return route

def partition(l, partition_length):
    return [l[i:i+partition_length] for i in xrange(0, len(l)-partition_length+1,1)]

def pheramone_matrix_update(route, route_length):
    partitioned_route = partition(route, 2)
    update_matrix = np.zeros((len(route),len(route)))
    
    for pair in partitioned_route:
        update_matrix[pair[0],pair[1]] = 1.0/route_length
    
    return update_matrix

def evaporate_pheramone_matrix(matrix, evaporation_factor):
    return (1-evaporation_factor)*matrix

def find_shortest_route(node_map, ant_count, evaporation_factor=0.05, convergence_percentage = 0.75, time_out_steps = 1000):
    
    route_lengths=[]
    
    # Initialize pheramone matrix
    pheramone_matrix = init_pheramone_matrix(len(node_map))
    
    unique_fraction = 1.0
    step_count = 0
    while unique_fraction > (1-convergence_percentage):
        
        # Initialize set of routes
        routes=[]
        
        # Evaporate pheramone matrix
        pheramone_matrix = evaporate_pheramone_matrix(pheramone_matrix, evaporation_factor)
        
        # Set ants roaming
        for ant in xrange(ant_count):
            route = generate_route(node_map, pheramone_matrix)
            routes.append(route)
        
        # Update pheramone matrix
        for route in routes:
            route_length = circular_route_length(node_map, route)
            pheramone_matrix += pheramone_matrix_update(route, route_length)
            
        # Track an ant in the colony
        route_lengths.append(circular_route_length(node_map, routes[0]))
        
        # Check for convergence
        unique_routes = []
        for route in routes:
            if route not in unique_routes:
                unique_routes.append(route)
        unique_fraction = float(len(unique_routes))/float(len(routes))
        
        # Check for timeout
        step_count += 1
        if (step_count > time_out_steps):
            break     
    
    return route_lengths, routes[0]          