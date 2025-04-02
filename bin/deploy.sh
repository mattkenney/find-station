#!/bin/sh

set -e

BASE_DIR="$(realpath $( cd "$( dirname "$0" )" && pwd )/..)"
TMP_DIR="$(mktemp -d)"
cd "${BASE_DIR}"
mkdir -p build
pip3 install --target "${TMP_DIR}" --requirement requirements.txt
zip build/find_station.zip *.py *.geojson *.json
cd "${TMP_DIR}"
zip -r "${BASE_DIR}/build/find_station.zip" .
aws lambda update-function-code \
    --function-name find_station \
    --zip-file "fileb://${BASE_DIR}/build/find_station.zip"
