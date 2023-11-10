import openpyxl

from flask import Flask, request, jsonify

app = Flask(__name__)


def get_stations_data():
    stations = []
    stations_data_path = "data/STATION_COORDS_HACKATON.xlsx"
    wb = openpyxl.load_workbook(stations_data_path)
    sheet = wb.active
    for i in range(2, sheet.max_row):
        station = {
            "stationId": sheet.cell(row=i, column=1).value,
            "latitude": sheet.cell(row=i, column=2).value,
            "longitude": sheet.cell(row=i, column=3).value
        }
        stations.append(station)
    return stations


@app.route("/stations")
def get_stations():
    stations = get_stations_data()

    return jsonify(stations), 200


if __name__ == "__main__":
    app.run(debug=True)
