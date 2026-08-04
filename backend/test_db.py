from database.mongodb import MongoDB

db = MongoDB()

print("Connected Successfully!")
print("Database:", db.db.name)
print("Collection:", db.collection.name)