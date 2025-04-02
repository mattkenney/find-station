# find-station

Find the closest train station. Supports SEPTA Regional Rail and DC Metro.
Specify the system as "septarr" or "dcmetro" and the target location as
LATITUDE,LONGITUDE. The closest station will be returned in GeoJSON format.
See the Development Server section below for examples.

Includes a handler function for deployment to AWS Lambda and API Gateway.

## Development setup

```
python3 -m venv .venv
. ./.venv/bin/activate
pip install -r requirements.txt
```

## Demo

Try it with "demo.py", for example:

```
./demo.py dcmetro 40,-76
```

## Development Server

Run a local development HTTP server with "dev\_server.py". Request examples:

```
$ curl --silent http://localhost:8080/api/v1/find_station/septarr/40.0326901,-75.5628379 | fold
{"type": "Feature", "properties": {"name": "Paoli Thorndale Line", "description"
: "<html xmlns:fo=\"http://www.w3.org/1999/XSL/Format\" xmlns:msxsl=\"urn:schema
s-microsoft-com:xslt\">\n\n<head>\n\n<META http-equiv=\"Content-Type\" content=\
"text/html\">\n\n<meta http-equiv=\"content-type\" content=\"text/html; charset=
UTF-8\">\n\n</head>\n\n<body style=\"margin:0px 0px 0px 0px;overflow:auto;backgr
ound:#FFFFFF;\">\n\n<table style=\"font-family:Arial,Verdana,Times;font-size:12p
x;text-align:left;width:100%;border-collapse:collapse;padding:3px 3px 3px 3px\">
\n\n<tr style=\"text-align:center;font-weight:bold;background:#9CBCE2\">\n\n<td>
Paoli Thorndale Line</td>\n\n</tr>\n\n<tr>\n\n<td>\n\n<table style=\"font-family
:Arial,Verdana,Times;font-size:12px;text-align:left;width:100%;border-spacing:0p
x; padding:3px 3px 3px 3px\">\n\n<tr>\n\n<td>Line_Name</td>\n\n<td>Paoli Thornda
le Line</td>\n\n</tr>\n\n<tr bgcolor=\"#D4E4F3\">\n\n<td>Station_Na</td>\n\n<td>
Malvern</td>\n\n</tr>\n\n<tr>\n\n<td>Street_Add</td>\n\n<td>15 N. Warren Ave (ne
ar King St)</td>\n\n</tr>\n\n<tr bgcolor=\"#D4E4F3\">\n\n<td>On_Street</td>\n\n<
td>N. Warren Ave</td>\n\n</tr>\n\n<tr>\n\n<td>At_Street</td>\n\n<td>King St</td>
\n\n</tr>\n\n<tr bgcolor=\"#D4E4F3\">\n\n<td>City</td>\n\n<td>Malvern</td>\n\n</
tr>\n\n<tr>\n\n<td>State</td>\n\n<td>PA</td>\n\n</tr>\n\n<tr bgcolor=\"#D4E4F3\"
>\n\n<td>Zip</td>\n\n<td>19355</td>\n\n</tr>\n\n<tr>\n\n<td>County</td>\n\n<td>C
hester</td>\n\n</tr>\n\n<tr bgcolor=\"#D4E4F3\">\n\n<td>Stop_ID</td>\n\n<td>9050
5</td>\n\n</tr>\n\n<tr>\n\n<td>Latitude</td>\n\n<td>40.036439</td>\n\n</tr>\n\n<
tr bgcolor=\"#D4E4F3\">\n\n<td>Longitude</td>\n\n<td>-75.515581</td>\n\n</tr>\n\
n</table>\n\n</td>\n\n</tr>\n\n</table>\n\n</body>\n\n</html>", "styleUrl": "#Ic
onStyle00"}, "geometry": {"type": "Point", "coordinates": [-75.51558053972394, 4
0.03643896435431, 0.0]}, "id": "ID_00053"}
$
$ curl --silent http://localhost:8080/api/v1/find_station/dcmetro/39.2,-77.2 | fold
{"type": "Feature", "properties": {"NAME": "Shady Grove", "ADDRESS": "15903 SOME
RVILLE DRIVE, DERWOOD, MD", "LINE": "red", "TRAININFO_URL": "https://www.wmata.c
om/js/nexttrain/nexttrain.html#A15|Shady%20Grove", "WEB_URL": "https://www.wmata
.com/rider-guide/stations/shady-grove.cfm", "GIS_ID": "MetroStnFullPt_1", "MAR_I
D": null, "GLOBALID": "{CB2ED552-145A-48D5-B75A-381A26F2665B}", "OBJECTID": 693,
 "CREATOR": "JLAY", "CREATED": "2022-11-30T15:32:57Z", "EDITOR": "JLAY", "EDITED
": "2022-11-30T15:32:57Z", "SE_ANNO_CAD_DATA": null}, "geometry": {"type": "Poin
t", "coordinates": [-77.16462967696448, 39.11993515031108]}
```

## Utilities

**bin/create-lock-table.py**

Create the DynamoDB table used to demonstrate ditributed locking.

**bin/deploy.sh**

Deploy as AWS Lambda Function

**bin/setptarr-geojson.sh**

Convert "SEPTARegionalRailStations2016.kmz" to
"SEPTARegionalRailStations2016.json".
