import geopandas as gpd
import json

def centroid_representation(geometry, name):
    centroid = geometry.centroid
    lat = centroid.y
    lon = centroid.x

    json_output = {
        'n': name,
        'a': round(lat, 7),
        'o': round(lon, 7)
    }
    return json_output

# Read the Shapefile using geopandas
shapefile_path = '/path/to/shapefile.shp'

data = gpd.read_file(shapefile_path)
# Filter to only retain Polygon
data = data[data.geometry.geom_type == 'Polygon']
data = data.to_crs("EPSG:4326")

features = []

for index, feature in data.iterrows():
    features.append(centroid_representation(feature['geometry'], feature['NAME']))

# Save the JSON output to file
output_json = '/path/to/output.json'
with open(output_json, 'w') as file:
    file.write(json.dumps(features))

print('JSON exported successfully.')
