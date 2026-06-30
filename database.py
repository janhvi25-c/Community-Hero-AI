import sqlite3

connection = sqlite3.connect("communityhero.db")

cursor = connection.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS reports (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_email TEXT,
    title TEXT,
    location TEXT,
    description TEXT,
    image TEXT,
    ai_result TEXT,
    status TEXT
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname TEXT,
    email TEXT UNIQUE,
    password TEXT
)
""")

connection.commit()
connection.close()

print("Database created successfully!")