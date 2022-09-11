# GSODAnalysis

The codebase for running analysis on recent Global Surface Summary of the Day (GSOD) data.

## Prerequisites

- MongoDB Server
- MongoDB Shell (mongosh)
- Python 3.5+

## Source

All GSOD data is available from the NOAA website [https://www.ncei.noaa.gov/metadata/geoportal/rest/metadata/item/gov.noaa.ncdc:C00516/html](here).

## Deployment

Setup venv on the local directory and install the requirements.txt file. Setup a .env file by referring to `.env.example` file. The following example is for a Linux environment:

```bash
python3 -m venv .
source bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Run docker-compose to start the MongoDB server, if running a local instance.

```bash
docker-compose -f docker.yml up -d
```

When launching mongodb server for the first time, run the `setup/initialise_db.js` python script to automatically setup the server.

## Usage

Import the data by running the `import_data.py` script. This will import the data from the `data/` directory into the MongoDB server.

```bash
python import_data.py <gsod_csv_directory> <isd_history.csv> <country.txt>
```

