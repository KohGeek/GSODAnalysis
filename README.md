# GSODAnalysis

The codebase for running analysis on recent Global Surface Summary of the Day (GSOD) data.

## Prerequisites

- MongoDB Server
- MongoDB Shell (mongosh)
- Conda

## Source

All GSOD data is available from the NOAA website [here](https://www.ncei.noaa.gov/metadata/geoportal/rest/metadata/item/gov.noaa.ncdc:C00516/html).

## Deployment

### Python

Initialise your shell with conda:

```bash
conda init
```

Create an local conda environment with the following command:

```bash
conda env create --file environment.yml -n gsod-analysis
```

Activate the environment, install the local environment as temporary package and also install the `requirements.txt` file:

```bash
conda activate gsod-analysis
pip install --editable .
```

Prepare a copy of .env file. Edit any field as necessary:

```bash
cp .env.example .env
```

### MongoDB

Run docker-compose to start the MongoDB server, if running a local instance. Make sure to comment out the `command: [--auth]` on first run.

```bash
docker-compose -f docker.yml up -d
```

When launching mongodb server for the first time, run `mongosh -f setup/initialise_db.js` python script to automatically setup the server. After importing the data, run the `mongosh -f setup/create_indexes.js` script to create the indexes on the database.

## Usage

Data downloaded from the website is in a .tar.gz form. Untar the file using `setup/unzip.sh` script. The script will automatically untar all files in subdirectories.

Import the data by running the `src\importdb.py` script.

```bash
python import_data.py <gsod_csv_directory> <isd_history.csv> <country.txt>
```
