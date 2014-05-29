import GeneticSolver as gs
import SimulatedAnnealingSolver as sas
import AntColonySolver as acs
import matplotlib.pyplot as plt

def plot_route(node_map, route):
    x, y = zip(*[node_map[i] for i in route])
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(x,y, c='b', marker=".")
    plt.show()

#n = 20
#cities = generate_random_map(n)
cities = [[1., 0.], [0.951057, 0.309017], [0.809017, 0.587785], \
         [0.587785, 0.809017], [0.309017, 0.951057], [0., 1.], \
         [-0.309017, 0.951057], [-0.587785, 0.809017], [-0.809017, 0.587785], \
         [-0.951057,0.309017], [-1., 0.], [-0.951057, -0.309017],\
         [-0.809017, -0.587785], [-0.587785, -0.809017], \
         [-0.309017, -0.951057], [0., -1.], [0.309017, -0.951057], \
         [0.587785, -0.809017], [0.809017, -0.587785], [0.951057, -0.309017]]

population_count = 50
mutation_percentage = 0.05
route_lengths, shortest_route = gs.find_shortest_route(cities, population_count, gs.roulette_parent_selector, gs.greedy_crossover, mutation_percentage)

print "Genetic Algorithm"
print "================="
print shortest_route
print route_lengths[-1]
#plt.plot(route_lengths)
#plt.show()

ant_count = 20
evaporation_fraction = 0.3
route_lengths, shortest_route = acs.find_shortest_route(cities, ant_count, evaporation_fraction)

print ""
print "Ant Colony Optimisation"
print "======================="
print shortest_route
print route_lengths[-1]
#plt.plot(route_lengths)
#plt.show()

steps = 20000
tMax = 100.0
route_lengths, shortest_route = sas.find_shortest_route(cities,steps,tMax)
sas.find_shortest_route(cities, steps, tMax)

print ""
print "Simulated Annealing"
print "==================="
print shortest_route
print route_lengths[-1]
#plt.plot(route_lengths)
#plt.show() 