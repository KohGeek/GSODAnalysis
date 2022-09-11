let conn = new Mongo();
db = conn.getDB("admin");

print("Creating root_admin as root");
db.createUser({
  user: "root_admin",
  pwd: passwordPrompt(),
  roles: [
    { role: "userAdminAnyDatabase", db: "admin" },
    { role: "readWriteAnyDatabase", db: "admin" },
  ],
});

print(
  "\nCreating gsod as read-only user"
);

db.createUser({
  user: "gsod",
  pwd: passwordPrompt(),
  roles: [{ role: "read", db: "gsod" }],
});

print("\nCreating DB gsod, a few collections and various indices.");
db = db.getSiblingDB("gsod");
db.createCollection("stations");
db.createCollection("weatherData", {
  timeseries: {
    timeField: "timestamp",
    metaField: "station",
    granularity: "hours"
  }
});

db.stations.createIndex({
  "location": "2dsphere",
  "name": 1,
  "country.name": 1,
  "elevation": 1,
}, { collation: { locale: "en", strength: 1 } });

// Create index for station location, name, country name and elevation
db.weatherData.createIndex({
  "station.location": "2dsphere",
  "station.name": 1,
  "station.country.name": 1,
  "station.elevation": 1,
  "timestamp": 1,
}, { collation: { locale: "en", strength: 1 } });

db.weatherData.createIndex({
  "temperature": 1,
  "dewPoint": 1,
  "maxTemperature": 1,
  "minTemperature": 1,
})

db.weatherData.createIndex({
  "windSpeed": 1,
  "maxSustainedWindSpeed": 1,
  "gust": 1,
})

db.weatherData.createIndex({
  "seaLevelPressure": 1,
  "stationPressure": 1,
  "precipitation": 1,
  "snowDepth": 1,
})

print(db.serverStatus());
