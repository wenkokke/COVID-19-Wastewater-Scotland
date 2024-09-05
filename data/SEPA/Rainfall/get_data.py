from sys import stdout
import chardet
import csv
import json
import pathlib
import requests

API_BASEURL = "https://www2.sepa.org.uk/rainfall/api"
ROOT_DIR = pathlib.Path(__file__).parent
STATIONS_DATA_FILE = ROOT_DIR / "stations.json"
RAINFALL_DATA_FILE = ROOT_DIR / "rainfall.csv"

# Load the stations data:
if STATIONS_DATA_FILE.exists():
    # Determine the encoding of the stations data file:
    with open(STATIONS_DATA_FILE, 'rb') as stations_data_fp:
        STATIONS_DATA_ENCODING = chardet.detect(stations_data_fp.read())['encoding']
    # Read the stations data file:
    with open(STATIONS_DATA_FILE, 'r', encoding=STATIONS_DATA_ENCODING) as stations_data_fp:
        STATIONS_DATA = json.load(stations_data_fp)
else:
    # Download the stations data:
    STATIONS_DATA = requests.get(f"{API_BASEURL}/stations").json()
    # Write the stations data file:
    STATIONS_DATA_ENCODING = 'UTF-8'
    with open(STATIONS_DATA_FILE, 'w', encoding=STATIONS_DATA_ENCODING) as stations_data_fp:
        json.dump(STATIONS_DATA, stations_data_fp)

# Determine the encoding of the rainfall data file:
if RAINFALL_DATA_FILE.exists():
    with open(RAINFALL_DATA_FILE, 'rb') as rainfall_data_fp:
        RAINFALL_DATA_ENCODING = chardet.detect(rainfall_data_fp.read())['encoding']
else:
    RAINFALL_DATA_ENCODING = 'UTF-8'

# Load the rainfall data:
RAINFALL_DATA_COLUMNS = ['station_id', 'timestamp', 'value']
if not RAINFALL_DATA_FILE.exists():
    with open(RAINFALL_DATA_FILE, 'w', newline='', encoding=RAINFALL_DATA_ENCODING) as rainfall_data_fp:
        RAINFALL_DATA_WRITER = csv.DictWriter(rainfall_data_fp, fieldnames=RAINFALL_DATA_COLUMNS)
        RAINFALL_DATA_WRITER.writeheader()
        for station_data in STATIONS_DATA:
            station_no = station_data['station_no']
            station_name = station_data['station_name']
            stdout.write("[   ] {:<40}".format(station_name))
            station_data_request_url = f"{API_BASEURL}/Daily/{station_no}?all=true"
            station_data_response = requests.get(station_data_request_url)
            stdout.write("\r")
            stdout.write("[{:<3}] {:<40}".format(station_data_response.status_code, station_name))
            station_data_samples = station_data_response.json()
            stdout.write("\r")
            stdout.write("[{:<3}] {:<40} ({} samples)".format(station_data_response.status_code, station_name, len(station_data_samples)))
            stdout.write("\n")
            if station_data_samples:
                for station_data_sample in station_data_samples:
                    RAINFALL_DATA_WRITER.writerow({
                        'station_no': station_no,
                        'timestamp': station_data_sample['Timestamp'],
                        'value': station_data_sample['Value'],
                    })
                rainfall_data_fp.flush()
