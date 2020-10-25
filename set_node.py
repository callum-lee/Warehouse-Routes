from load_data import *
import numpy as np

# locations = load_WarehouseLocations()
# distances = load_WarehouseRoutes(True)
# durations = load_WarehouseRoutes(False)

# print(locations['Distribution South'][0])
# print(durations['Distribution South']['Distribution North'])
# print(len(durations))
# print('f')

def divide_north_south(demand, durations, unvisited_set):
    north_set = []
    south_set = []
    # north_duration = 0.0
    # south_duration = 0.0

    for unvis in unvisited_set:
        
        if durations['Distribution North'][unvis] > durations['Distribution South'][unvis]:
            south_set.append(unvis)
            # south_duration += float(durations['Distribution South'][unvis])
        else:
            north_set.append(unvis)
            # north_duration += float(durations['Distribution North'][unvis])

    # while abs(north_duration - south_duration) > 3000:

    north_demand_weekday = 0.0
    north_demand_weekend = 0.0
    for north in north_set:
        north_demand_weekday += float(demand[north]['weekday_avg'])
        north_demand_weekend += float(demand[north]['weekend_avg'])

    south_demand_weekday = 0.0
    south_demand_weekend = 0.0
    for south in south_set:
        south_demand_weekday += float(demand[south]['weekday_avg'])
        south_demand_weekend += float(demand[south]['weekend_avg'])
    
    print(north_demand_weekday)
    print(north_demand_weekend)
    print(south_demand_weekday)
    print(south_demand_weekend)
    # print(north_duration)
    # print(south_duration)
    return north_set, south_set



def routes_set(demand, north, south):

    # north
    # weekday
    # maximum demand at each route = 18

    north_visited_weekday = []
    max_demand = 18.0
    min_duration = np.inf

    while len(north) > 0.0:
        #finding minimum duration from distribution north
        for nor in north:
            if durations['Distribution North'][nor] < min_duration:
                min_duration = durations['Distribution North'][nor]
                nth_closest_store = nor  
            else:
                continue

        




    pass    

def unvis_set(durations):
    unvisited = []
    
    for loc in durations:
        unvisited.append(loc)

    unvisited.remove('Distribution North') 
    unvisited.remove('Distribution South')

    return unvisited

if __name__== "__main__":
    demand = load_DemandData()
    # print(demand['Noel Leeming Albany']['weekday_avg'])
    durations = load_WarehouseRoutes(False)
    # print(durations['Distribution South']['Distribution North'])
    unvisited = unvis_set(durations)
    # print(unvisited)
    north_set, south_set = divide_north_south(demand, durations, unvisited)
    print("north set is =", north_set)
    print("south set is =", south_set)
    print(len(north_set))
    print(len(south_set))
    routes_set(demand, north_set, south_set)
