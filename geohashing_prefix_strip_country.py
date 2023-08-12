import geopandas as gpd
import json
import pygeohash as gh
from shapely.geometry import Polygon, MultiPolygon,shape

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

def geohash_json_feature_representation(vertices, name, country_prefix):
    geohashes = [gh.encode(vertex[1], vertex[0], precision=10) for vertex in vertices]
    geohashes = [geohash[len(country_prefix):] for geohash in geohashes]
    prefix = longest_common_geohash_prefix(geohashes)
    trimmed_geohashes = [geohash[len(prefix):] for geohash in geohashes]

    json_output = {
        'n': name,
        'g': trimmed_geohashes,
        'p': prefix
    }
    return json_output

shapefile_path = '/path/to/shapefile.shp'

# Maximum prefix for senegal to be replaced by the one for your locality
country_prefix = 'ed'

data = gpd.read_file(shapefile_path)
data = data[data.geometry.geom_type == 'Polygon']
data = data.to_crs("EPSG:4326") 

features = []

for index, feature in data.iterrows():
    geometry = feature['geometry']
    vertices = extract_vertices(geometry)
    features.append(geohash_json_feature_representation(vertices, feature['NAME'], country_prefix))

output_json = '/path/to/output.json'

with open(output_json, 'w') as file:
    file.write(json.dumps(features))

print('JSON exported successfully.')
