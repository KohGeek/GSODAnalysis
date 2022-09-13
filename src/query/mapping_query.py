from datetime import datetime, timedelta

import cartopy.crs as ccrs
import matplotlib as mpl
import matplotlib.pyplot as plt

from gsodtools.getdb import get_db


def daterange(start_date, end_date):
    for i in range(int((end_date - start_date).days)):
        yield start_date + timedelta(i)


def main():
    client = get_db()
    database = client["gsod"]

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


if __name__ == "__main__":
    main()
