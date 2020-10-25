from load_data import (load_DemandData,load_WarehouseLocations,load_WarehouseRoutes)
from routes_class import node
from route_creator import create_routes
from linear_program import convert_to_matrix,assignment
from simulation import demand_sim
import pandas as pd


# def main():
#     '''

#     '''
#     demandData = load_DemandData()
#     locations = load_WarehouseLocations()
#     distances = load_WarehouseRoutes(True)
#     durations = load_WarehouseRoutes(False)
    
#     nodes = initialise_nodes(demandData,locations)

#     new_routes = create_routes(nodes,durations,25)

#     new_route_list = list(new_routes)

#     coord = []

#     locations_d = pd.read_csv("WarehouseLocations.csv")
#     coords = locations_d[['Long', 'Lat']]
#     coords = coords.to_numpy().tolist()

#     loc = list(reversed(coords[2]))

#     for i in range(len(new_route_list)):
#         for j in range(len(new_routes[new_route_list[i]].nodes)):
#             coord.append(new_routes[new_route_list[i]].nodes[j].location)
        

#         coord = []
        
#     route = client.directions(coordinates = coord, profile = 'driving-hgv', format = 'geojson', validate = False)
#     coord = [] 
    
#     leng = len(new_routes[new_route_list[0]].nodes)
#     new_set = new_routes[new_route_list[0]].nodes[0].location

#     matrix = convert_to_matrix(nodes,new_routes)
#     assignment(matrix,new_routes,nodes)

#     pass

def main(n=1000,isSim = True):
    '''

    '''
    demandData = load_DemandData()
    locations = load_WarehouseLocations()
    distances = load_WarehouseRoutes(True)
    durations = load_WarehouseRoutes(False)
    
    nodes = initialise_nodes(demandData,locations)

    routes = create_routes(nodes,durations,n)
     # route_hist(routes,nodes)

    matrix = convert_to_matrix(nodes,routes)
    
    routes = assignment(matrix,routes,nodes)
#     # route_hist(routes,nodes)
    


    if isSim:
        demand_sim(routes, isWeekday = True)
    
    
#     pass

def initialise_nodes(demandData,locations):
    '''


    '''
    nodes = {i : node(i,demandData,locations) for i in locations.keys()}

    return nodes


if __name__ == "__main__":
    main()
