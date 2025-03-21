import sqlite3

# Connect to database (or create it if it doesn't exist)
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Create users table
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        role TEXT NOT NULL
    )
""")

# Insert sample users
cursor.executemany("""
    INSERT INTO users (username, email, role) VALUES (?, ?, ?)
""", [
    ("admin", "admin@example.com", "Administrator"),
    ("doctor1", "doctor1@hospital.com", "Doctor"),
    ("nurse1", "nurse1@hospital.com", "Nurse")
])

# Save changes and close connection
conn.commit()
conn.close()

print("Database and users table created successfully!")
