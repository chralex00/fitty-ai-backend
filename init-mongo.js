db = db.getSiblingDB("fittyaidb");

db.createUser({
    user: "user",
    pwd: "password",
    roles: [
        { role: "readWrite", db: "fittyaidb" }
    ]
});