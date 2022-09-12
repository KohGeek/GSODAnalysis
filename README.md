# GSODAnalysis

The codebase for running analysis on recent Global Surface Summary of the Day (GSOD) data.

## Prerequisites

- MongoDB Server
- MongoDB Shell (mongosh)
- Python 3.5+

## Source

All GSOD data is available from the NOAA website [here](https://www.ncei.noaa.gov/metadata/geoportal/rest/metadata/item/gov.noaa.ncdc:C00516/html).

## Deployment

Setup venv on the local directory and install the requirements.txt file. Setup a .env file by referring to `.env.example` file. The following example is for a Linux environment:

```bash
python3 -m venv .
source bin/activate
pip install -r requirements.txt
cp .env.example .env
```

And for the windows environment:

```bash
python -m venv .
Scripts\activate.bat
pip install -r requirements.txt
copy .env.example .env
```

Run docker-compose to start the MongoDB server, if running a local instance. Make sure to comment out the `command: [--auth]` on first run.

```bash
docker-compose -f docker.yml up -d
```

When launching mongodb server for the first time, run `mongosh -f setup/initialise_db.js` python script to automatically setup the server. After importing the data, run the `mongosh -f setup/create_indexes.js` script to create the indexes on the database.

### Windows

If you use Windows, `pip install -r requirements.txt` could throw error due to missing dependencies. If this happens, install the wheel files from [here](https://www.lfd.uci.edu/~gohlke/pythonlibs/) for the files below:

- Fiona
- GDAL
- Cartopy

Run `pip install <wheel_file_name>` for each of the files, then run `pip install -r requirements.txt` again to install the rest of the dependencies.

## Usage

Data downloaded from the website is in a .tar.gz form. Untar the file using `setup/untar.py` script. The script will automatically untar all files in subdirectories.

Import the data by running the `src\importdb.py` script.

```bash
python import_data.py <gsod_csv_directory> <isd_history.csv> <country.txt>
```
