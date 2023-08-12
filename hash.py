import geopandas as gpd
import json
import hashlib

def feature_to_string(feature):
    # Concatenate all feature properties to a string
    feature_string = ''.join(str(feature[key]) for key in feature.keys())
    return feature_string

def feature_hash_representation(feature, name):
    # Generate the SHA256 hash for a feature
    feature_string = feature_to_string(feature)
    sha256_hash = hashlib.sha256(feature_string.encode()).hexdigest()

    json_output = {
        'n': name,
        'h': sha256_hash
    }
    return json_output

# Read the Shapefile using geopandas
shapefile_path = '/path/to/shapefile.shp'
data = gpd.read_file(shapefile_path)
data = data[data.geometry.geom_type == 'Polygon']
data = data.to_crs("EPSG:4326") 

features = []

for index, feature in data.iterrows():
    features.append(feature_hash_representation(feature, feature['NAME']))

# Save the JSON output to file
output_json = '/path/to/output.json'
with open(output_json, 'w') as file:
    file.write(json.dumps(features))

print('JSON exported successfully.')
