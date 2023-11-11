import openpyxl
import random
import io

from flask import Flask, request, jsonify

app = Flask(__name__)

wagons = []
station_names = []


def get_wagons_data():
    if wagons:
        return wagons

    wagons_data_path = "data/disl_hackaton.xlsx"
    wb = openpyxl.load_workbook(filename=wagons_data_path, read_only=True, keep_vba=False)
    sheets = wb.sheetnames
    i = 1
    for s_name in sheets:
        sheet = wb[s_name]
        for i in range(2, sheet.max_row):
            train_info_value = sheet.cell(row=i, column=5).value
            train_info = ""
            if train_info_value != "":
                train_info = train_info_value.split("-")
            wagon = {
                "wagonId": sheet.cell(row=i, column=1).value,
                "currentStationId": sheet.cell(row=i, column=3).value,
                "arrivalTime": sheet.cell(row=i, column=2).value,
                "wagonStartStation": train_info[0],
                "wagonDestination": sheet.cell(row=i, column=4).value,
                "trainDestination": train_info[2],
                "trainNumber": train_info[1]
            }
            wagons.append(wagon)

    return wagons


def get_stations_data():
    stations = []
    stations_data_path = "data/STATION_COORDS_HACKATON.xlsx"
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
    return stations


def load_station_names():
    with io.open("data/Stations.txt", encoding='utf-8') as file:
        for line in file:
            station_names.append(line.rstrip())


load_station_names()
# get_wagons_data()


@app.route("/stations")
def get_stations():
    stations = get_stations_data()

    return jsonify(stations), 200


@app.route("/wagons")
def get_wagons():
    wagons_data = get_wagons_data()

    return jsonify(wagons_data), 200


if __name__ == "__main__":
    app.run()
