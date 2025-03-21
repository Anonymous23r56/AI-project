import sqlite3

# Connect to the database
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Drop the table if it exists (to avoid conflicts)
cursor.execute("DROP TABLE IF EXISTS chat_history;")

# Recreate the table
cursor.execute("""
    CREATE TABLE chat_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        user TEXT NOT NULL,
        message TEXT NOT NULL
    )
""")

conn.commit()

# Insert a test chat message
cursor.execute("INSERT INTO chat_history (date, user, message) VALUES (?, ?, ?)", 
               ("2025-03-19", "TestUser", "Hello, this is a test message!"))

conn.commit()
conn.close()

print("✅ chat_history table recreated successfully!")
print("✅ Test message added!")
