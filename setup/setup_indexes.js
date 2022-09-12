let conn = new Mongo();
db = conn.getDB("jsod");

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

