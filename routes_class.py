import numpy as np

class route:
    '''

    '''
    def __init__(self,name):
        self.duration = 0.
        self.nodes = []
        self.ended = False
        self.combined = False
        self.demand = 0.
        self.name = name
        self.used = 'unused'

    def __str__(self):
        return print(*[x.name for x in self.nodes],sep = "\n")

    def __repr__(self):
        pass

    def node_in_route(self,search):
        '''

        '''

        for node in self.nodes:
            if node.name == search:
                return True
        
        return False

class node:
    '''


    '''
    def __init__(self,name,demandData,locations):
        self.name = name
        self.location = locations[name]
        

        if name.find('Distribution') != -1:
            self.toVisit = False
            self.visited = np.inf
        else:
            self.toVisit = True
            self.visited = 0.
            self.weekday_avg = float(demandData[name]['weekday_avg'])
            self.weekend_avg = float(demandData[name]['weekend_avg'])
            self.weekday_var = float(demandData[name]['weekday_var'])
            self.weekend_var = float(demandData[name]['weekend_var'])

    def __str__(self):
        return print(self.name)

    def demand(self,isWeekday = True,isSim = False):
        '''

        '''
        if isSim:
            pass
        else:
            if isWeekday:
                return self.weekday_avg
            else:
                return self.weekend_avg

