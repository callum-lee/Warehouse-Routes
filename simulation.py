import numpy as np 
import random
import statistics
import scipy as sp 
import seaborn as sns 
import matplotlib.pyplot as plt


def demand_sim(routes, isWeekday): 
    # For each node in the routes, add in the variation of the demand estimations 
    # For each node do a Randomisation distribution (Random variable of demand at each node and accumulate it)
    # Pick a random value out of the uniform or normal distribution between the average - variance and average + variance 
    # Add boolean variable on whether it is weekend or not 

    random.seed(100)
    
    # Get the number of the routes 
    len_route = len(routes)
    # Initialise demand array with zeros 
    demand_vals_arr = np.zeros(len_route) 
    # Initialise j to index demand array 
    j = -1
    # Iterate through each route in the final set of routes
    for route in routes:
        # Find the number of nodes within each route 
        leng = len(routes[route].nodes)
        # update j value 
        j += 1
        # Iterate through each node in the routes, except the first and last node (distribution centres) 
        for i in range(1, leng-1):
            # Get the demand value of the node in the route given  
            demand_vals = routes[route].nodes[i]

            # Check if it is weekday or weekend
            if isWeekday:
                # Sum up the updated demand value of the route and store to demand array
                demand_vals_arr[j] += np.ceil(np.random.normal(loc = demand_vals.weekday_avg, scale = np.sqrt(demand_vals.weekday_var)))
            else:
                demand_vals_arr[j] += np.ceil(np.random.normal(loc = demand_vals.weekend_avg, scale = np.sqrt(demand_vals.weekend_var)))

    return(demand_vals_arr)

def traffic_sim(routes, isWeekday):
    # 1. Search through all the durations in each route 
    # 2. Add a flat scaling factor of 30mins for each hour for the duration of that route. e.g. 1st hour add 30 min, 2nd hour add another 30 mins, etc.
    # 3. Find the new ADDITIONAL durations for all the routes in the set of routes (1 simulation iteration)
    # 4. Store the new set of ADDITIONAL durations into an array or dictionary or series for the final simulation function 
    
    random.seed(100)

    len_route = len(routes)

    duration_vals_arr = np.zeros(len_route)

    j = -1

    for route in routes:
        
        j += 1

        if isWeekday:
            duration_vals_arr[j] += routes[route].duration * np.random.uniform(0.7,1.3)

        else:
            duration_vals_arr[j] += routes[route].duration * np.random.uniform(0.85,1.15)
   
    
    return duration_vals_arr


def cost_sim(demand, traffic): 

    cost = 0 

    for i in range(len(demand)):
        if demand[i] > 20:
            cost += 175
    
    for j in range(len(traffic)):
        if traffic[j] > 4:
            cost += 175 * 4 + 250 * (traffic[j]-4)
        else:
            cost += 175 * traffic[j]

    return cost


def simulation(routes, isWeekday, n):
    cost = np.zeros(n)

    for i in range(n):
        demand = demand_sim(routes, isWeekday)
        traffic = traffic_sim(routes, isWeekday)
        cost[i] = cost_sim(demand, traffic)
    
    cost.sort()
    return cost

def sim_plot(nweekday, sweekday, nweekend, sweekend):
    fig, (ax1, ax2) = plt.subplots(1,2, sharex=False, sharey = False)
    ax1 = sns.distplot(nweekday, label = "North Open Weekday", color = 'r')
    ax1 = sns.distplot(sweekday,  label = "North Closed Weekday", color = 'g')
    ax2 = sns.distplot(nweekend,  label = "North Open Weekend", color = 'r')
    ax2 = sns.distplot(sweekend,  label = "North Closed Weekend", color = 'g')
    ax1.set_title("Weekday Cost of Simulated Optimised Routes")
    ax2.set_title("Weekend Cost of Simulated Optimised Routes")
    ax1.legend(prop={'size':12})
    ax2.legend(prop={'size':12})
    ax1.set_xlabel("Cost (per day)")
    ax2.set_xlabel("Cost (per day)")
    ax1.set_ylabel('Density')
    ax2.set_ylabel('Density')
    fig.savefig('cost_simulation.png')
