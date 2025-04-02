#!/usr/bin/env python3
"""
Demo of the find-station feature as an executable script.

Example: ./demo.py septarr 40.0,-75.0'
"""

import json
import sys
import urllib.parse

from request_handler import base_path, find_closest_station

def demo(args: [str]):
    parts = base_path[1:]
    parts.extend(args)
    parts = [urllib.parse.quote(part, safe=',') for part in parts]
    parts.insert(0, '')
    path = '/'.join(parts)
    print('Usage: demo.py (dcmetro|septarr) LAT,LON')
    print('Request path:', path)
    print('Response:')
    response = find_closest_station('GET', path)
    print(json.dumps(response, indent='    '))

if __name__ == '__main__':
    demo(sys.argv[1:])
