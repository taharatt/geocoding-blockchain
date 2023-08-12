import geopandas as gpd
import json
from shapely.geometry import Polygon, MultiPolygon,shape

def extract_vertices(geometry):
    vertices = []
    geom_shape = shape(geometry)
    for coord in geom_shape.exterior.coords:
        lon, lat = coord[:2]
        vertices.append((lon, lat))
    return vertices

def feature_representation(vertices, name, precision = 7):

    coords = [(round(vertex[0], precision), round(vertex[1], precision)) for vertex in vertices]  # Get coordinates from tuple

    json_output = {
        'n': name,
        'c': coords
    }
    return json_output

# Path to the Shapefile
shapefile_path = '/path/to/shapefile.shp'

# Read the Shapefile using geopandas
data = gpd.read_file(shapefile_path)
data = data[data.geometry.geom_type == 'Polygon']
data = data.to_crs("EPSG:4326")

features = []

for index, feature in data.iterrows():
    vertices = extract_vertices(feature['geometry'])
    features.append(feature_representation(vertices, feature['NAME']))

# Save the JSON output to file
output_json = '/path/to/output.json'
with open(output_json, 'w') as file:
    file.write(json.dumps(features))

print('JSON exported successfully.')
