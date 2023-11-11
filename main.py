from flask import Flask, jsonify
from api.stations_api import stations_api, stations
from api.wagons_api import wagons_api, wagons


app = Flask(__name__)
app.register_blueprint(stations_api)
app.register_blueprint(wagons_api)


@app.route("/api/trains/<train_number>")
def get_wagon(train_number):
    pgk_wagons_in_train = []
    train_info = {}
    train_info_raw = {}
    for wagon in wagons:
        if wagon["trainNumber"] == train_number:
            pgk_wagons_in_train.append(wagon["wagonId"])
            train_info_raw["trainDeparturePoint"] = int(wagon["trainDeparturePoint"])
            train_info_raw["trainDestinationPoint"] = int(wagon["trainDestinationPoint"])

    for wagon in wagons:
        if wagon["stationId"] == train_info_raw["trainDeparturePoint"]:
            train_info_raw["departureAt"] = wagon["arrivalTime"]
        if wagon["stationId"] == train_info_raw["trainDestinationPoint"]:
            train_info_raw["arriveAt"] = wagon["arrivalTime"]

    for station in stations:
        if station["id"] == train_info_raw["trainDeparturePoint"]:
            train_info["from"] = station["name"]
            train_info["fromLatitude"] = station["latitude"]
            train_info["fromLongitude"] = station["longitude"]

        if station["id"] == train_info_raw["trainDestinationPoint"]:
            train_info["to"] = station["name"]
            train_info["toLatitude"] = station["latitude"]
            train_info["toLongitude"] = station["longitude"]

    train_info["arriveAt"] = train_info_raw["arriveAt"] if train_info_raw["arriveAt"] else ""
    train_info["departureAt"] = train_info_raw["departureAt"] if train_info_raw["departureAt"] else ""
    train_info["wagons"] = pgk_wagons_in_train
    train_info["trainDeparturePoint"] = train_info_raw["trainDeparturePoint"]
    train_info["trainDestinationPoint"] = train_info_raw["trainDestinationPoint"]

    return jsonify(train_info), 200


if __name__ == "__main__":
    app.run()
