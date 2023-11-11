from flask import Blueprint, jsonify
import openpyxl
import random
import io

station_names = []
stations = []
stations_api = Blueprint("stations_api", __name__)


def load_station_names():
    with io.open("./data/Stations.txt", encoding='utf-8') as file:
        for line in file:
            station_names.append(line.rstrip())


def load_stations_data():
    stations_data_path = "./data/STATION_COORDS_HACKATON.xlsx"
    wb = openpyxl.load_workbook(stations_data_path)
    sheet = wb.active
    for i in range(2, sheet.max_row):
        station = {
            "id": sheet.cell(row=i, column=1).value,
            "name": random.choice(station_names),
            "latitude": sheet.cell(row=i, column=2).value,
            "longitude": sheet.cell(row=i, column=3).value
        }
        stations.append(station)


load_station_names()
load_stations_data()


@stations_api.route("/api/stations")
def get_stations():
    return jsonify(stations), 200


@stations_api.route("/api/stations/<station_id>")
def get_station(station_id):
    # station = next((s for s in stations if s["id"] == int(station_id)), None)
    for s in stations:
        if s["id"] == int(station_id):
            return jsonify(s), 200
    return jsonify({"message": "NotFound"}), 404
