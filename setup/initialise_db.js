let conn = new Mongo();
db = conn.getDB("admin");

print("Creating root_admin as root");
db.createUser({
  user: "root_admin",
  pwd: passwordPrompt(),
  roles: [
    { role: "root", db: "admin" },
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


//Create indexes for stations
db.stations.createIndex({
  "location": "2dsphere",
});

db.stations.createIndex({
  "elevation": 1,
});

db.stations.createIndex({
  "country.fips": 1,
}, { collation: { locale: "en", strength: 1 } });

db.stations.createIndex({
  "country.name": "text",
}, { collation: { locale: "en", strength: 1 } });



// Create index for weatherData
db.weatherData.createIndex({
  "station.location": "2dsphere",
});

db.weatherData.createIndex({
  "station.elevation": 1,
});

db.weatherData.createIndex({
  "station.country.name": 1,
}, { collation: { locale: "en", strength: 1 } });

db.weatherData.createIndex({
  "station.country.fips": 1,
}, { collation: { locale: "en", strength: 1 } });

db.weatherData.createIndex({
  "timestamp": -1,
});

db.weatherData.createIndex({
  "temperature": 1,
  "maxTemperature": 1,
  "minTemperature": 1,
})

db.weatherData.createIndex({
  "dewPoint": 1,
  "visibility": 1,
})

db.weatherData.createIndex({
  "windSpeed": 1,
  "maxSustainedWindSpeed": 1,
  "gust": 1,
})

db.weatherData.createIndex({
  "seaLevelPressure": 1,
  "stationPressure": 1,
})

db.weatherData.createIndex({
  "precipitation": 1,
  "snowDepth": 1,
})



print(db.serverStatus());
