import geopandas as gpd
import json
import mapcode
from shapely.geometry import MultiPolygon, Polygon, Point,shape

def extract_vertices(geometry):
    vertices = []
    geom_shape = shape(geometry)
    for coord in geom_shape.exterior.coords:
        lon, lat = coord[:2]
        vertices.append((lon, lat))
    return vertices

def mapcode_json_feature_representation(vertices, name):
    # Generate the JSON output for a feature   
    mapcodes = [mapcode.encode(vertex[1], vertex[0], "SEN")[0][0] for vertex in vertices]
    # for extended representation 
    # mapcodes = [mapcode.encode(vertex[1], vertex[0], "SEN", 2)[0][0] for vertex in vertices] 
    json_output = {
        'n': name,
        'm': mapcodes
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
    features.append(mapcode_json_feature_representation(vertices, feature['Nicad']))

# Save the JSON output to file
output_json = '/path/to/output.json'
with open(output_json, 'w') as file:
    file.write(json.dumps(features))

print('JSON exported successfully.')
