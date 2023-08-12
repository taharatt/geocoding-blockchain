import geopandas as gpd
import json
import mapcode

def mapcode_centroid_representation(geometry, name):
    centroid = geometry.centroid
    # Generate the geohash for the centroid
    code = mapcode.encode(centroid.y, centroid.x, "SEN", 2)[0][0]

    json_output = {
        'n': name,
        'm': code
    }
    return json_output

# Read the Shapefile using geopandas
shapefile_path = '/path/to/shapefile.shp'
data = gpd.read_file(shapefile_path)
data = data[data.geometry.geom_type == 'Polygon']
data = data.to_crs("EPSG:4326")

features = []

for index, feature in data.iterrows():
    features.append(mapcode_centroid_representation(feature['geometry'], feature['NICAD']))

# Save the JSON output to file
output_json = '/path/to/output.json'
with open(output_json, 'w') as file:
    file.write(json.dumps(features))

print('JSON exported successfully.')
