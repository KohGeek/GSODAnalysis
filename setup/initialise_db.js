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
  "station.location": "2dsphere",
  "station.name": 1,
  "station.country.name": 1,
  "station.elevation": 1,
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
  "summary.temperature": 1,
  "summary.dewPoint": 1,
  "summary.maxTemperature": 1,
  "summary.minTemperature": 1,
})

db.weatherData.createIndex({
  "summary.windSpeed": 1,
  "summary.maxSustainedWindSpeed": 1,
  "summary.gust": 1,
})

db.weatherData.createIndex({
  "summary.seaLevelPressure": 1,
  "summary.stationPressure": 1,
  "summary.precipitation": 1,
  "summary.snowDepth": 1,
})

print(db.serverStatus());
