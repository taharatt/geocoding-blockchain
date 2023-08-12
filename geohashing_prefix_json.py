import geopandas as gpd
import json
import pygeohash as gh
from shapely.geometry import Polygon, MultiPolygon, shape

def extract_vertices(geometry):
    vertices = []
    geom_shape = shape(geometry)
    for coord in geom_shape.exterior.coords:
        lon, lat = coord[:2]
        vertices.append((lon, lat))
    return vertices

def longest_common_geohash_prefix(geohashes):
    if not geohashes:
        return ""

    prefix = geohashes[0]
    for geohash in geohashes[1:]:
        i = 0
        while i < len(prefix) and i < len(geohash) and prefix[i] == geohash[i]:
            i += 1
        prefix = prefix[:i]

    return prefix

def geohash_json_feature_representation(vertices, name):
    # Generate the geohashes for a feature
    geohashes = [gh.encode(vertex[1], vertex[0], precision=10) for vertex in vertices]

    # Find the longest common prefix
    prefix = longest_common_geohash_prefix(geohashes)

    # Trim the prefix from each geohash
    trimmed_geohashes = [geohash[len(prefix):] for geohash in geohashes]

    json_output = {
        'n': name,
        'g': trimmed_geohashes,
        'p': prefix
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
    features.append(geohash_json_feature_representation(vertices, feature['NAME']))

# Save the JSON output to file
output_json = '/path/to/output.json'

with open(output_json, 'w') as file:
    file.write(json.dumps(features))

print('JSON exported successfully.')
