conn = new Mongo();
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
  "\nCreating app as read-only user"
);

db.createUser({
  user: "gsod",
  pwd: passwordPrompt(),
  roles: [{ role: "read", db: "gsod" }],
});

print("\nCreating DB gsod, a few collections and various indices.");
db = db.getSiblingDB("gsod");
db.createCollection("weatherData");
db.weatherData.createIndex()

print(db.serverStatus());
