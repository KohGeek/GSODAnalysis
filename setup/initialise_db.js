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


print(db.serverStatus());
