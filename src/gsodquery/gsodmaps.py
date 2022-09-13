from datetime import datetime, timedelta
import time

import cartopy.crs as ccrs
import matplotlib as mpl
import matplotlib.pyplot as plt
import pandas as pd


def conv_lat(string):
    if string[-1] == 'N':
        string = f'{string[:-1]}'
    else:
        string = f'-{string[:-1]}'

    return float(string)


def conv_long(string):
    if string[-1] == 'E':
        string = f'{string[0:-1]}'
    else:
        string = f'-{string[0:-1]}'

    return float(string)


def typhoon_import(file):
    typhoon = pd.read_csv(file, names=["date", "time", "status",
                                       "latitude", "longitude", "max_wind",
                                       "min_pressure", "radius_max_wind"],
                          dtype={"time": str},
                          converters={"latitude": conv_lat, "longitude": conv_long})

    typhoon.reset_index()
    typhoon.drop(typhoon[typhoon.time != "0000"].index, inplace=True)

    return typhoon


def daterange(start_date, end_date):
    for i in range(int((end_date - start_date).days)):
        yield start_date + timedelta(i)


def typhoon_query(database):
    typhoon = typhoon_import("data/typhoonIda.csv").to_dict(orient="records")

    plt.ion()

    cmap = plt.get_cmap('rainbow')
    vmin = 1002
    vmax = 1030
    norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
    smap = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    smap.set_array([])

    fig = plt.figure(figsize=(10, 10))
    axis = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    axis.coastlines()

    cbar = fig.colorbar(smap)
    cbar.ax.set_ylabel('Sea Level Pressure (mb)',
                       rotation=270, fontsize=15, labelpad=20)

    stations = list(database.stations.aggregate([
        {"$match": {"location": {"$within": {
            "$box": [[-100, 23], [-70, 43]]}}}},
        {"$project": {"_id": 1}}
    ]))

    stations = [s["_id"] for s in stations]

    start_date = datetime(2021, 8, 15)
    end_date = datetime(2021, 9, 7)
    for single_date in daterange(start_date, end_date):

        data = list(database.weatherData.aggregate([
            {"$match": {"$and": [{"timestamp": single_date},
                                 {"station._id": {"$in": stations}},
                                 {"precipitation": {"$exists": True}},
                                 {"seaLevelPressure": {"$exists": True}}]}},
            {"$project": {"_id": 0, "location": "$station.location.coordinates",
                          "precipitation": 1, "seaLevelPressure": 1}},
        ]))

        scat = axis.scatter([x["location"][0] for x in data],
                            [x["location"][1] for x in data],
                            c=[x["seaLevelPressure"] for x in data],
                            s=[max(3, x["precipitation"] * 70) for x in data],
                            cmap=cmap, vmax=vmax, vmin=vmin,
                            transform=ccrs.PlateCarree(), alpha=0.3)

        typh = None
        for i, row in enumerate(typhoon):
            if datetime.strptime(f'{row["date"]} {row["time"]}', '%Y%m%d %H%M') == single_date:
                typh = axis.scatter(
                    row["longitude"], row["latitude"],
                    c="#000000",
                    s=max(row["max_wind"]*5, (row["radius_max_wind"])*10), transform=ccrs.PlateCarree(),
                    alpha=0.6)

                axis.plot([x["longitude"] for x in typhoon[:i+1]],
                          [x["latitude"] for x in typhoon[:i+1]],
                          c="#000000", alpha=0.6,
                          transform=ccrs.PlateCarree())

        # draw title
        plt.title(
            f'Hurricane Ida - {single_date.strftime("%d/%m/%Y")}', fontsize=30)

        # dynamically update
        fig.canvas.draw()
        # to flush the GUI events
        fig.canvas.flush_events()

        scat.remove()
        if typh is not None:
            typh.remove()
        if len(axis.lines) > 0:
            axis.lines.pop(0)
        time.sleep(0.3)


def temperature_query(database):

    plt.ion()

    cmap = plt.get_cmap('rainbow')
    vmax = 40
    vmin = -25
    norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
    smap = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    smap.set_array([])

    fig = plt.figure(figsize=(10, 10))
    axis = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    axis.coastlines()

    cbar = fig.colorbar(smap)
    cbar.ax.set_ylabel('Temperature (C)', rotation=270,
                       fontsize=15, labelpad=20)

    stations = list(database.stations.aggregate([
        {"$sample": {"size": 1000}},
        {"$project": {"_id": 1}}
    ]))

    stations = [s["_id"] for s in stations]

    start_date = datetime(2016, 1, 1)
    end_date = datetime(2021, 12, 31)
    for single_date in daterange(start_date, end_date):

        data = list(database.weatherData.aggregate([
            {"$match": {"$and": [{"timestamp": single_date}, {
                "station._id": {"$in": stations}}]}},
            {"$project": {
                "_id": 0, "location": "$station.location.coordinates", "temperature": 1}},
        ]))

        scat = axis.scatter([x["location"][0] for x in data],
                            [x["location"][1] for x in data],
                            c=[(x["temperature"] - 32) * 5 / 9 for x in data],
                            s=30, cmap=cmap, vmax=vmax, vmin=vmin,
                            transform=ccrs.PlateCarree())

        # draw title
        plt.title(single_date.strftime('%d/%m/%Y'), fontsize=30)

        # dynamically update
        fig.canvas.draw()
        # to flush the GUI events
        fig.canvas.flush_events()
        scat.remove()
