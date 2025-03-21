import sqlite3

def initialize_database():
    conn = sqlite3.connect("database.db")  # Connect to SQLite
    cursor = conn.cursor()

    # Create chat_history table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()
    print("✅ Database initialized successfully!")

# Run the function
if __name__ == "__main__":
    initialize_database()
