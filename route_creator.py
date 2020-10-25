from routes_class import route,node
from testing import route_hist
import numpy as np
import random as rd

def create_routes(nodes,durations,n,isNorthClosed):
    '''


    '''
    # number of potential routes to create
    # if trucks are at the same node, they cannot travel to the same node
    # total demand along a route cannot exceed 18, not less than 15
    # half trucks leave each depot
    # truck does not have to return to same depot
    # all nodes must be visited round(n // 25) times
    # nodes ended if there is no combination which puts it between 7 and 11
    
    routes = {i : route('route'+str(i)) for i in range(n*2)}

    # x.visited >= n//25
    while not(all([route.ended == True for route in routes.values()])):

        for key,val in routes.items():

            if val.nodes == []:

                if (key % 2 == 0) or (isNorthClosed):

                    val.nodes.append(nodes['Distribution South'])

                elif key % 2 == 1:

                    val.nodes.append(nodes['Distribution North'])
            
            if val.ended is not True:
                one_step(nodes,val,durations,n)    
    
    new_routes = combine_routes(routes,durations,n)

    return new_routes

def one_step(nodes,route,durations,n,isWeekday = True):
    '''


    '''
    nodes2 = route.nodes[1:]
    node = route.nodes[-1]

    possible = {nd.name : nd for nd in nodes.values() if ((nd.toVisit == True) and \
        (route.demand + nd.demand(isWeekday,False) <= 10) and \
        (all([True if nd.name != node2.name else False for node2 in nodes2])))}

        

    if possible == {}:

        route.ended = True

    else:

        #if (len(possible) > 15):

            #possible = recursive(possible,durations[node.name])
        
        if possible == {}:

            route.ended = True
        
        else:

            next_node_name = objective_fun(possible,node,durations[node.name])

            route.nodes.append(nodes[next_node_name])
            nodes[next_node_name].visited += 1
            route.duration += (durations[node.name][next_node_name] + (60 * 10 * nodes[next_node_name].demand(isWeekday,False)))/3600
            route.demand += nodes[next_node_name].demand(isWeekday,False)

def objective_fun(nodes,node,durations,random = True):
    '''
        Objective function based on distance and num of times visited, return node name with smallest value
    
        Parameters:
        -----------
            nodes:

            node:

            durations:


    '''
    objective = {}

    if (not random) and (node.toVisit == True):
        for nd in nodes.values():
            try:
                objective[nd.name] = durations[nd.name]*2**(nd.visited-node.visited)
            except OverflowError:
                objective[nd.name] = np.inf

        key_min = min(objective,key=(lambda k: objective[k]))
    else:
        rd.seed()
        r_idx = int(np.round((rd.random()*1000)) % len(nodes))

        for i,node_name in enumerate(nodes.keys()):
            if i == r_idx:
                key_min = node_name
                break

    return key_min
        

def combine_routes(routes,durations,n):
    
    new_routes = {}

    for i in range(n):

        k = i

        while (routes[k].combined == True):

            k += 1

        dist = np.inf

        end_route = None

        for rt in routes.values():

            if ( \
                (durations[routes[k].nodes[-1].name][rt.nodes[-1].name] < dist) \
                and (routes[k].demand + rt.demand <= 20) \
                #and (routes[k].demand + rt.demand >= 14) \
                and (routes[k] != rt) \
                and (rt.combined == False) \
                and (routes[k].combined == False) \
                and (all([node1.name != node2.name for node1 in routes[k].nodes[1:]] for node2 in rt.nodes[1:])) \
                #and (routes[k].duration + rt.duration < 4)
                ):

                    dist = durations[routes[k].nodes[-1].name][rt.nodes[-1].name]
                    end_route = rt

        if end_route is not None:                

            routes[k].nodes += end_route.nodes[::-1]
            routes[k].duration += end_route.duration
            routes[k].demand += end_route.demand
            routes[k].name += '_and_' + end_route.name
            routes[k].combined, end_route.combined = True,True
            new_routes[routes[k].name] = routes[k]


    return new_routes

def recursive(nodes, durations):

    dur = max(durations[node.name]*(node.visited+1) for node in nodes.values())*0.99

    nodes = {node.name : node for node in nodes.values() if (durations[node.name]*(node.visited+1) < dur)}

    if (len(nodes) > 15):
        nodes = recursive(nodes,durations)
    
    return nodes