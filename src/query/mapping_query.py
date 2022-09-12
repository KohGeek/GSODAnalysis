from datetime import datetime, timedelta

import cartopy.crs as ccrs
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

from gsodtools.getdb import get_db


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

def main():
    client = get_db(1)
    db = client["gsod"]

    plt.ion()

    cmap = plt.get_cmap('rainbow')
    norm = mpl.colors.Normalize(vmin=-20, vmax=100)
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])
    
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
    fig.colorbar(sm)
    ax.coastlines()

    stations = list(db.stations.aggregate([
        {"$sample": {"size": 1000}},
        {"$project": {"_id": 1}}
    ]))

    stations = [s["_id"] for s in stations]

    start_date = datetime(2019, 1, 1)
    end_date = datetime(2019, 12, 31)
    for single_date in daterange(start_date, end_date):

        data = list(db.weatherData.aggregate([
            {"$match": {"$and": [{"timestamp": single_date}, {"station._id": {"$in": stations}}]}},
            {"$project": {"_id": 0, "location": "$station.location.coordinates", "temperature": 1}},
            {"$sample": {"size": 1000}},
        ]))

        scat = ax.scatter([x["location"][0] for x in data],
            [x["location"][1] for x in data],
            c=[x["temperature"] for x in data],
            s=20, cmap="rainbow", vmax=100, vmin=-20,
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
