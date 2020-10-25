from matplotlib import pyplot as plt
import numpy as np

def route_hist(routes,nodes,isNorthClosed,save=False):

    durations = [route.duration for route in routes.values()]
    demand = [route.demand for route in routes.values()]
    stops = [len(route.nodes) for route in routes.values()]
    visits = [node.visited for node in nodes.values() if node.visited != np.inf]

    if isNorthClosed:

        fig,((ax1,ax2),(ax3,ax4)) = plt.subplots(2,2)

        fig.suptitle('Northern Distribution Centre Closed')
        ax1.hist(durations,density = True,color = 'orange')
        ax1.set_title('Route Durations')
        ax2.hist(demand,density = True,color = 'orange')
        ax2.set_title('Route Demands')
        ax3.hist(stops,density = True, color = 'orange')
        ax3.set_title('Route Stops')
        ax4.hist(visits,density = True,color = 'orange')
        ax4.set_title('Node Visits')

        plt.tight_layout()

        if not save:

            plt.show()
    
        else:
            plt.savefig('hist_noNorth.png')
    else:

        fig,((ax1,ax2),(ax3,ax4)) = plt.subplots(2,2)

        fig.suptitle('Northern Distribution Centre Open')

        ax1.hist(durations,density = True,color = 'purple')
        ax1.set_title('Route Durations')

        ax2.hist(demand,density = True,color = 'purple')
        ax2.set_title('Route Demands')

        ax3.hist(stops,density = True, color = 'purple')
        ax3.set_title('Route Stops')

        ax4.hist(visits,density = True,color = 'purple')
        ax4.set_title('Node Visits')

        plt.tight_layout()

        if not save:

            plt.show()
    
        else:
            plt.savefig('hist_north.png')

def percent_return(routes):

    n = 0

    for route in routes.values():
        if route.nodes[0].name != route.nodes[-1].name:
            n += 1

    

    return n/len(routes)