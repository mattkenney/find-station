"""
FindStation class - for finding the Feature in a FeatureCollection closest to
specified coordinates.
"""

import json
import logging
import math

import kdtree

logger = logging.getLogger()

class Station():
    """KD tree node containing coordinates and GeoJSON feature"""
    def __init__(self, x, y, feature):
        self.coords = (x, y)
        self.feature = feature

    def __len__(self):
        return len(self.coords)

    def __getitem__(self, i):
        return self.coords[i]


# Over the small distances of a metro area, we can use a simple
# formula to convert longitude and latitude into km east and north of a
# reference point, and use a KD tree to find the nearest station
class FindStation():
    def __init__(self, geojson_file_path: str):
        with open(geojson_file_path, 'r') as file:
            self._geojson = json.load(file)

        # get the max and min latitude and longitude from the GeoJSON
        self._lat_min = 200;
        self._lat_max = -200;
        self._lon_min = 200;
        self._lon_max = -200;
        for feature in self._geojson['features']:
            (lon, lat) = feature['geometry']['coordinates'][0:2]
            if self._lat_min > lat:
                self._lat_min = lat
            if self._lat_max < lat:
                self._lat_max = lat
            if self._lon_min > lon:
                self._lon_min = lon
            if self._lon_max < lon:
                self._lon_max = lon

        # compute the center latitude and longitude
        self._lat_ref = (self._lat_min + self._lat_max) / 2
        self._lon_ref = (self._lon_min + self._lon_max) / 2

        # compute the kilometers per degree latitude and longitude
        self._km_per_lat = 111.1
        self._km_per_lon = 111.1 * math.cos(self._lat_ref * math.pi / 180.0)

        # set the valid latitude and longitude range - 100 km outside the box
        # containing all the stations
        self._lat_min -= 150.0 / self._km_per_lat;
        self._lat_max += 150.0 / self._km_per_lat;
        self._lon_min -= 150.0 / self._km_per_lon;
        self._lon_max += 150.0 / self._km_per_lon;

        # build the KD tree
        self._tree = kdtree.create([self._build_station(feature) for feature in self._geojson['features']])

        # log the details of this FindStation
        logging.info(
            "FindStation details",
            extra={
                "geojson_file_path": geojson_file_path,
                "lat_ref": self._lat_ref,
                "lon_ref": self._lon_ref,
                "km_per_lat": self._km_per_lat,
                "km_per_lon": self._km_per_lon,
                "lat_min": self._lat_min,
                "lat_max": self._lat_max,
                "lon_min": self._lon_min,
                "lon_max": self._lon_max,
            },
        )

    def _build_station(self, feature) -> Station:
        (lon, lat) = feature['geometry']['coordinates'][0:2]
        return Station(self._lon_to_km(lon), self._lat_to_km(lat), feature)

    def _lat_to_km(self, lat: float) -> float:
        return (lat - self._lat_ref) * self._km_per_lat

    def _lon_to_km(self, lon: float) -> float:
        return (lon - self._lon_ref) * self._km_per_lon

    def find_station(self, lat: float, lon: float):
        """Returns the station closest to lat, lon"""
        x = self._lon_to_km(lon)
        y = self._lat_to_km(lat)
        closest = self._tree.search_nn((x, y))
        return closest[0].data.feature

    def is_in_region(self, lat: float, lon: float) -> bool:
        """Returns true if the supplied lat/lon is within a reasonable distance"""
        return (
            self._lat_min < lat and lat < self._lat_max and
            self._lon_min < lon and lon < self._lon_max)
