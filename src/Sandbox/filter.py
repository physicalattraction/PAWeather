import json
import os.path


def filter(input_filename, output_filename):
    highway_whitelist = {'primary', 'secondary', 'tertiary', 'residential', 'trunk'}

    with open(input_filename) as f:
        streets = json.load(f)
    streets['features'] = [feat for feat in streets['features'] if feat['properties']['highway'] in highway_whitelist]

    with open(output_filename, 'w') as f:
        f.write(json.dump(streets, f))


if __name__ == '__main__':
    input_filename = os.path.join('..', '..', 'tmp', 'amsterdam_netherlands.geojson')
    output_filename = os.path.join('..', '..', 'tmp', 'amsterdam_netherlands.tmp.geojson')
    filter(input_filename, output_filename)
