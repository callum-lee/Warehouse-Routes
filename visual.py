import numpy as np
import pandas as pd 
import folium
import openrouteservice as ors

ORSkey = '5b3ce3597851110001cf624862488e5d98474379ab630ebc96a0ef29'

locations = pd.read_csv("WarehouseLocations.csv")

coords = locations[['Long', 'Lat']]
coords = coords.to_numpy().tolist()

m = folium.Map(location = list(reversed(coords[2])), zoom_start = 10)

folium.Marker(list(reversed(coords[0])), popup = locations.Store[0], icon = folium.Icon(color = 'black')).add_to(m)

for i in range(1, len(coords)):
    if locations.Type[i] == "The Warehouse":
        iconCol = "red"
    elif locations.Type[i] == "Noel Leeming":
        iconCol = "orange"
    elif locations.Type[i] == "Distribution":
        iconCol = "black"
    folium.Marker(list(reversed(coords[i])), popup = locations.Store[i], icon = folium.Icon(color = iconCol)).add_to(m)

m


# client = ors.Client(key=ORSkey)

# route = client.directions()
