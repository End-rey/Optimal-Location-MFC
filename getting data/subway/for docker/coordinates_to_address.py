import osmium
from shapely.geometry import Point

import sys

class BuildingHandler(osmium.SimpleHandler):
    def __init__(self):
        super(BuildingHandler, self).__init__()
        self.nearest_building = None
        self.min_distance = float('inf')

    def way(self, w):
        if 'building' in w.tags:
            # Extract the building's geometry
            geom = w.geom
            # Calculate the distance to the provided coordinates
            distance = geom.distance(Point(latitude, longitude))
            if distance < self.min_distance:
                self.min_distance = distance
                self.nearest_building = w

# Replace with the path to your OSM data file (PBF format)
osm_data_file = 'Санкт-Петербург.osm.pbf'

# Replace with your latitude and longitude
latitude = 59.9216522565527
longitude = 30.2929245883803

handler = BuildingHandler()
handler.apply_file(osm_data_file)

if handler.nearest_building:
    print(f"Nearest Building: {handler.nearest_building.id}")
else:
    print("No building found nearby.")