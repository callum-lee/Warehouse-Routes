import numpy as np
from routes_class import route,node
import pulp
from cost import calculate_cost


def convert_to_matrix(nodes,routes):
    '''

    '''

    matrix = {node.name : {route.name : 0 for route in routes.values()} for node in nodes.values() if node.toVisit == True}

    for node_name,node_dict in matrix.items():
        for route_name in node_dict.keys():
            if routes[route_name].node_in_route(node_name):
                matrix[node_name][route_name] = 1

    return matrix

def assignment(matrix,routes,nodes,isNorthClosed = False):
    '''

    '''

    # need to implement:
    #   - Wet leased trucks
    #   -
    x = pulp.LpVariable.dicts('normal_trucks',[route for route in routes.keys()], cat = pulp.LpBinary)
    y = pulp.LpVariable.dicts('wet-leased_trucks',[route for route in routes.keys()], cat = pulp.LpBinary)

    if  not isNorthClosed:
    
        prob = pulp.LpProblem('northOpen',pulp.LpMinimize)

        # objective function
        #'''+ (1500*(routes[route.name].duration//4 + 1) * y[route.name])'''

        prob += pulp.lpSum(((route.duration) * x[route.name] * 175) + (1500 * (route.duration//4 + 1) * y[route.name])  \
            if (routes[route.name].duration) <= 4 else \
            (4*175 + ((route.duration)-4) * x[route.name] * 250) + (1500*(route.duration//4 + 1) * y[route.name]) \
            for route in routes.values())

        # node constraints
        for node_name,node_dict in matrix.items():
            prob += pulp.lpSum(node_dict[route_name]*(x[route_name]+y[route_name]) for route_name in node_dict.keys()) == 1, node_name

        # truck num constraint
        prob += pulp.lpSum(x[route] for route in routes.keys())  <= 50, 'Max_num_trucks'

        #cant be both truck types
        for route_name in routes.keys():
            prob += x[route_name] + y[route_name] <= 1, 'not_both' + route_name

        #write LP formulation to file
        #prob.writeLP('northOpen.lp')

    else:

        prob = pulp.LpProblem('northClosed',pulp.LpMinimize)

        extras = pulp.LpVariable('extra_trucks',lowBound=0,upBound=5,cat = pulp.LpInteger)

        # objective function
        #'''+ (1500*(routes[route.name].duration//4 + 1) * y[route.name])'''
        prob += pulp.lpSum(((route.duration) * x[route.name] * 175) + (1500 * (route.duration//4 + 1) * y[route.name]) - 40000/30 + extras * (20000/30)  \
            if (route.duration) <= 4 else \
            (4*175 + ((routes[route.name].duration)-4) * x[route.name] * 250) + (1500 * (route.duration//4 + 1) * y[route.name]) - 40000/30 + extras * (20000/30) \
            for route in routes.values())

        # node constraints
        for node_name,node_dict in matrix.items():
            prob += pulp.lpSum(node_dict[route_name]*(x[route_name]+y[route_name]) for route_name in node_dict.keys()) == 1, node_name

        # truck num constraint
        prob += pulp.lpSum(x[route] for route in routes.keys()) - 2 * extras  <= 50, 'Max_num_trucks'

        #cant be both truck types
        for route_name in routes.keys():
            prob += x[route_name] + y[route_name] <= 1, 'not_both' + route_name

        #write LP formulation to file
        #prob.writeLP('northClosed.lp')

    #to terminate output pulp.PULP_CBC_CMD(msg=False)
    prob.solve()     
    
    
    for route in routes.values():
        if pulp.value(x[route.name]) == 1:
            route.used = 'normal'
        elif pulp.value(y[route.name]) == 1:
            route.used = 'wet-leased'

    objective = 0
    for route in routes.values():
        objective += calc_objective(route)
    if isNorthClosed:
        objective -= 400000/30
        objective += (20000/30) * pulp.value(extras)

    return {route.name : route for route in routes.values() if route.used != 'unused'}, objective


def calc_objective(route):

    objective = 0

    if route.used == 'normal':
        if route.duration <= 4:
            objective = route.duration*175
        else:
            objective = 4*175 + (route.duration - 4) * 250
    elif route.used == 'wet-leased':
        objective = (route.duration // 4 + 1) * 1500

    return objective