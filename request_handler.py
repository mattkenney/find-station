"""
Request handler for the find-station feature.
Suitable for use by an AWS Lambda function, but also usable in other contexts.
"""

import logging
import os
import re
from pathlib import Path

from find_station import FindStation


logger = logging.getLogger()

base_path = ['/', 'api', 'v1', 'find_station']
helpText = 'Example usage: GET /api/v1/find_station/septarr/40.3,-75.0 or GET /api/v1/find_station/dcmetro/39.2,-77.2'
strict_float = re.compile(r'^(-?)(0|[1-9][0-9]*)(\.[0-9][0-9]*)?$')

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))

# Construct the full path to the SEPTA RR JSON file
septa_rr_file_name = 'SEPTARegionalRailStations2016.json'
septa_rr_file_path = os.path.join(script_dir, septa_rr_file_name)

# create a FindStation for SEPTA Regional Rail
septa_rr = FindStation(septa_rr_file_path)

# Construct the full path to the DC Metro JSON file
dc_metro_file_name = 'Metro_Stations_Regional.geojson'
dc_metro_file_path = os.path.join(script_dir, dc_metro_file_name)

# create a FindStation for DC Metro
dc_metro = FindStation(dc_metro_file_path)


def find_closest_station(method, path):
    """Find closest station request handler function"""
    if method != 'GET':
        return method_not_allowed()
    # parse and validate the request path
    parts = Path(path).parts
    if len(parts) < 2:
        return not_found()
    *prefix, penultimate_segment, last_segment = Path(path).parts
    if prefix != base_path:
        return not_found()
    if penultimate_segment == 'septarr':
        finder = septa_rr
    elif penultimate_segment == 'dcmetro':
        finder = dc_metro
    else:
        return not_found()
    coordinates = last_segment.split(',')
    # expect a pair of basic decimal strings, not `inf` or `1E-3` etc
    if (len(coordinates) != 2
            or not strict_float.match(coordinates[0])
            or not strict_float.match(coordinates[1])):
        return bad_request()
    lat = float(coordinates[0])
    lon = float(coordinates[1])
    if not finder.is_in_region(lat, lon):
        return bad_request(help = 'The requested latitude/longitude is outside of the service region')
    return finder.find_station(lat, lon)


def bad_request(help = helpText):
    """HTTP 400 Bad Request error response"""
    return {
        'statusCode': 400,
        'statusText': 'Bad Request',
        'detail': help,
    }


def method_not_allowed():
    """HTTP 405 Method Not Allowed error response"""
    return {
        'statusCode': 405,
        'statusText': 'Method Not Allowed',
        'detail': helpText,
    }


def not_found():
    """HTTP 404 Not Found error response"""
    return {
        'statusCode': 404,
        'statusText': 'Not Found',
        'detail': helpText,
    }
