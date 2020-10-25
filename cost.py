import numpy as np
from routes_class import route,node

def calculate_cost(route,x,wet = False):
    """
    Calculates the cost of each route given a list of nodes and truck type variables
    
    Parameters: 
    route : object

    x : boolean

    y : boolean
    
    Returns:



    
    """

    # Initialise cost and duration of routes 
    shift = 60*60*4 # 4 hour shifts 

    if x == 1:
        if route.duration < shift:
            return 175 * np.ceil(route.duration)
        
        else: 
            return 175 * 4 + 250 * np.ceil(route.duration-shift)

    elif wet:
        if route.duration < shift:
            return 1500
        
        else:  
            return 1500 * np.ceil((route.duration/(60*60*4)))

    else:
        return 0