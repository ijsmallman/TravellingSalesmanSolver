import random
from CommonRouteMethods import separation, circular_route_length, generate_random_route

def nearest_neighbours(parent, node):
    node_index = parent.index(node)
    nMax = len(parent)
    return [parent[(node_index-1)%nMax], parent[(node_index+1)%nMax]]
    
def closest_neighbour(node_map, node, neighbours):
    
    minSep = 1.41421 # Init to max possible separation: corner to corner = sqrt(2)
    closestNeighbour = node # Init to current node 
        
    for neighbour in neighbours:
            # Get separation between node and neighbour
            sep = separation(node_map[node], node_map[neighbour])
            # Compare to current minimum separation
            # If it's smaller, update the minimum and closest neighbour
            if sep < minSep:
                minSep = sep
                closestNeighbour = neighbour
    
    return closestNeighbour

def closest_available_neighbour(node_map, child, node, neighbours):
    minSep = 1.41421 # Init to max possible separation: corner to corner = sqrt(2)
    closestNeighbour = node # Init to current node 
        
    for neighbour in neighbours:
        # Get separation between node and neighbour
        sep = separation(node_map[node], node_map[neighbour])
        # Compare to current minimum separation
        # If it's smaller, update the minimum and closest neighbour
        # so long as the neighbour is not already in the child route
        if sep < minSep:
            if neighbour not in child:
                minSep = sep
                closestNeighbour = neighbour
        
    # If child already contains all the neighbours
    # then closestNeighbour will still equal node
    # in which case we should generate a new node randomly
    if closestNeighbour == node:
        while closestNeighbour in child:
            closestNeighbour = random.randint(0,len(node_map)-1)
        
    #return the closestNeighbour
    return closestNeighbour
    
def greedy_crossover(node_map, mother, father):
    
    # Start on node 0
    node = 0
    child = [node]
    
    # Build up child route
    while len(child) < len(mother):
        
        # Find neighbours from parents
        neighbours = nearest_neighbours(mother,node) + nearest_neighbours(father,node)
    
        # Get best available neighbour
        neighbour = closest_available_neighbour(node_map, child, node, neighbours)
        
        # Append closestNeighbour to child
        child.append(neighbour)
        
        # Update current node
        node = neighbour
    
    return child
    
def rotate(l,n):
    n = n % len(l)
    return l[-n:] + l[:-n]    
    
def get_fitness(node_map, route):
    return 1.0 / circular_route_length(node_map, route)

def sort_routes(node_map, routes):
    
    # Evaluate fitness of route
    fitness_list = [get_fitness(node_map, x) for x in routes]
    total_fitness = sum(fitness_list)
    
    # Now normalise the fitnesses so don't have to keep passing around the
    # total fitness (note there is an efficiency cost to this)
    normed_fitness_list = [x/total_fitness for x in fitness_list]
    
    # Sort routes according to fitness (largest fitness first)
    return sorted(zip(normed_fitness_list, routes), reverse = True)
    
def roulette_parent_selector(sorted_routes):  

    # Select a parent using roulette method
    rand = random.random()
    
    # - select a parent with probability = normalised fitness of route
    accFit = 0.0
    for route in sorted_routes:
        accFit += route[0] # sorted_routes = [[fitness,route],...]
        
        if accFit > rand:
            return route[1]

def tournament_parent_selector(sorted_routes):
    
    pop_size = len(sorted_routes)
    tournament_size = pop_size/4
    
    # Select tournament_size parents from the population
    sampled_parents = [random.randint(0,pop_size) for i in xrange(tournament_size)]
    
    # Since routes are already sorted, the best parent will be at the index
    # of the lowest value in sampled_parents
    selected_parent_index = (sorted(sampled_parents))[0]
    
    return sorted_routes[selected_parent_index][1]
    

def generate_initial_population(nodes_in_map, population_size):
    return [generate_random_route(nodes_in_map) for x in xrange(population_size)]

def random_swap(route):
    n = len(route)
    i = random.randint(0,n-1)
    j = random.randint(0,n-1)
    temp = route[i]
    route[i] = route[j]
    route[j] = temp

def mutate(route, mutation_percentage):
    while random.random() < mutation_percentage:
        random_swap(route)

def find_shortest_route(node_map, population_size, selector, crossover, mutation_percentage, convergence_percentage = 0.75, time_out_steps = 1000):
    
    # Create list for route length tracking over time
    route_lengths = []
    
    # Generate an initial breeding population
    population = generate_initial_population(len(node_map), population_size)
    
    unique_fraction = 1.0
    step_count = 0
    while unique_fraction > (1-convergence_percentage):
        
        # Sort the population
        sorted_routes = sort_routes(node_map, population)
        
        # Initialize a new population list to replace the last breeding population
        new_population = []
        
        while len(new_population) < population_size:
            
            # Select two parents using the selector method
            mother = selector(sorted_routes)
            father = selector(sorted_routes)
            
            # Breed parents
            child = crossover(node_map, mother, father)
            
            # Mutate child
            mutate(child, mutation_percentage) # N.B. pass by reference
            
            new_population.append(child)
        
        # Update the breeding population
        population = new_population[:]
        
        # Track the current best route length
        route_lengths.append(circular_route_length(node_map, population[0]))
        
        # Check for convergence
        unique_routes = []
        for route in population:
            if route not in unique_routes:
                unique_routes.append(route)
        unique_fraction = float(len(unique_routes))/float(len(population))
        
        # Check for timeout
        step_count += 1
        if (step_count > time_out_steps):
            break     
    
    return route_lengths, population[0]

