#!/bin/sh
set -e

# uses k2g from https://pypi.org/project/kml2geojson/

BASE_DIR="$(realpath $( cd "$( dirname "$0" )" && pwd )/..)"
TMP_DIR="$(mktemp -d)"
cd "${TMP_DIR}"
unzip "${BASE_DIR}/SEPTARegionalRailStations2016.kmz"
k2g --style-filename SEPTARegionalRailStations2016.json doc.kml "${BASE_DIR}"
