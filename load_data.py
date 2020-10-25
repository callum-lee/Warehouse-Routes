import numpy as np

def load_DemandData():
    ''' load supplied transported pallet numbers that has been cleaned and sorted in R
        
        Returns:
        --------

            demandDic: nx4 dictionary
                store_name = key
                [store name(str), weekday_avg, weekday_var, weekend_avg, weekend_var] = value

        Notes:
        ------

    '''

    demandData = np.genfromtxt(fname = "demandDataUpdated.csv",dtype = str, delimiter = ",",skip_header = 1)[:,:5]
    #demandData[:,1:] = [[float(x) for x in i[1:]] for i in demandData]

    demandDic = {i[0]: {'weekday_avg' : i[2], 'weekday_var' : i[1], 'weekend_avg' : i[4], 'weekend_var' : i[3]} for i in demandData}
    
    return demandDic

def load_WarehouseLocations():
    ''' load supplied Warehouse Locations, used for visualisations

        Returns:
        --------
            wh_loc: dictionary of 2x1 tuple
                (longitude,latitude), keys are store names
        Notes:
        ------
    '''

    wh_loc = np.genfromtxt(fname= "WarehouseLocations.csv",dtype = str, delimiter=",",skip_header = 1)[:,2:]
    
    y = [[float(x) for x in wh_loc[:,i]] for i in [1,2]]
    dic = {l:k for l,k in zip(wh_loc[:,0],zip(y[0],y[1]))}

    return dic

def load_WarehouseRoutes(isDist = True):
    ''' load supplied route durations and distances, file in nxn matrix form

        Parameters:
        -----------
            isDist: Bool, def = True
                load distance matrix (else load durations)
        
        Returns:
        --------
            dic: nxn dictionary of distances/durations (float)
            
        Notes:
        ------
    
    
    '''
    if isDist:
        fname = "WarehouseDistances.csv"
    else:
        fname = "WarehouseDurations.csv"

    matrix = np.genfromtxt(fname,dtype = float, delimiter=",",skip_header = 0)[1:,1:]
    names = np.genfromtxt(fname,dtype = str, delimiter=",",skip_header = 1)[:,0]
    
    dic = {name:{n : matrix[i,j] for j,n in enumerate(names)} for i, name in enumerate(names)}

    return dic

