from load_data import (load_DemandData,load_WarehouseLocations,load_WarehouseRoutes)
from routes_class import node
from route_creator import create_routes
from linear_program import convert_to_matrix,assignment
from testing import route_hist, percent_return
from simulation import demand_sim, traffic_sim, cost_sim, simulation, sim_plot

def main(n=1000, isSim = True):
    '''

    '''
    demandData = load_DemandData()
    locations = load_WarehouseLocations()
    #distances = load_WarehouseRoutes(True)
    durations = load_WarehouseRoutes(False)
    
    nodes = initialise_nodes(demandData,locations)

    north_routes, north_obj = find_routes(nodes,durations,n,False)
    south_routes, south_obj = find_routes(nodes,durations,n,True)

    if isSim:
        north_weekday = simulation(north_routes, isWeekday = True, n=1000)
        south_weekday = simulation(south_routes, isWeekday = True, n=1000)
        north_weekend = simulation(north_routes, isWeekday = False, n=1000)
        south_weekend = simulation(south_routes, isWeekday = False, n=1000)
        sim_plot(north_weekday,south_weekday,north_weekend,south_weekend)

    print(percent_return(north_routes))

    print("North:",north_obj,"South:",south_obj,sep = '\t')
    print('Percentage of routes not returning to original warehouse: ', percent_return(north_routes))

    
    
def find_routes(nodes,durations,n,isNorthClosed):    

    routes = create_routes(nodes,durations,n,isNorthClosed)
    # route_hist(routes,nodes,isNorthClosed)

    matrix = convert_to_matrix(nodes,routes)
    
    routes,obj = assignment(matrix,routes,nodes,isNorthClosed)
    #route_hist(routes,nodes,isNorthClosed)

    return routes,obj
    
    
def initialise_nodes(demandData,locations):
    '''


    '''
    nodes = {i : node(i,demandData,locations) for i in locations.keys()}

    return nodes


if __name__ == "__main__":
    main()
