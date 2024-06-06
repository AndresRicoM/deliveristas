import fitparse
import json
from datetime import datetime

# Parse the FIT file
fit_file_path = 'Sensor_Test_0.fit'
fitfile = fitparse.FitFile(fit_file_path)

# Extract data
records = []
for record in fitfile.get_messages('record'):
    record_data = {}
    for data in record:
        record_data[data.name] = data.value
    records.append(record_data)

# Convert to GeoJSON
features = []
for record in records:
    if 'position_lat' in record and 'position_long' in record:
        latitude = record['position_lat'] * (180 / 2**31)
        longitude = record['position_long'] * (180 / 2**31)
        properties = {k: v for k, v in record.items() if k not in ['position_lat', 'position_long']}
        
        # Convert datetime to string if present
        for key, value in properties.items():
            if isinstance(value, datetime):
                properties[key] = value.isoformat()
        
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [longitude, latitude]
            },
            "properties": properties
        }
        features.append(feature)

geojson_data = {
    "type": "FeatureCollection",
    "features": features
}

# Save GeoJSON to file
geojson_file_path = 'sensor_data_fit_0.geojson'
with open(geojson_file_path, 'w') as geojson_file:
    json.dump(geojson_data, geojson_file, indent=2)
