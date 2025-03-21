import sqlite3
import os
from flask import Flask, request, jsonify, send_from_directory
from flask_jwt_extended import JWTManager, create_access_token
from flask_cors import CORS
from datetime import datetime  # ✅ Fixed missing import

app = Flask(__name__)
CORS(app)

app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'supersecretkey')  # Consider using an environment variable
jwt = JWTManager(app)

# Mock user database
users = {}

@app.route('/')
def serve_home():
    return send_from_directory(os.path.join(os.getcwd(), "..", "frontend"), "index.html")

@app.route("/login", methods=['GET'])
def login_page():
    return "Login Page Loaded"

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Dummy authentication
    if username == "admin" and password == "password":
        return jsonify({"message": "Login successful!"}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@app.route('/api/register', methods=["POST"])
def register_user():  # ✅ Renamed from `reset_password` to match its actual function
    data = request.get_json()
    email = data.get("email")
    
    if email in users:
        return jsonify({"message": "Reset link sent to your email!"}), 200
    else:
        return jsonify({"message": "Email not found!"}), 404

def get_db_connection():
    try:
        conn = sqlite3.connect("database.db", check_same_thread=False)  # Connect to SQLite database
        conn.row_factory = sqlite3.Row  # Return results as dictionaries
        return conn
    except sqlite3.Error as e:
        print(f"Database connection error: {e}")
        return None

@app.route("/users", methods=["GET"])
def get_users():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        users = conn.execute("SELECT id, username, email FROM users").fetchall()
        return jsonify({"users": [dict(user) for user in users]})
    except sqlite3.Error as e:
        return jsonify({"error": f"Database query error: {e}"}), 500
    finally:
        conn.close()

# ✅ Chat History Routes
@app.route('/chat-history', methods=['GET'])
def get_chat_history():
    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT id, date, user, message FROM chat_history ORDER BY date DESC")
        chats = cursor.fetchall()
        return jsonify([dict(chat) for chat in chats])
    except sqlite3.Error as e:
        return jsonify({"error": f"Database query error: {e}"}), 500
    finally:
        conn.close()

@app.route("/chat-history", methods=["POST"])
def add_chat_message():
    data = request.json
    user = data.get("user")
    message = data.get("message")

    if not user or not message:
        return jsonify({"error": "User and message are required"}), 400

    conn = get_db_connection()
    if conn is None:
        return jsonify({"error": "Database connection failed"}), 500
    
    try:
        cursor = conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO chat_history (date, user, message) VALUES (?, ?, ?)", (timestamp, user, message))
        conn.commit()
        return jsonify({"message": "Chat added successfully!"}), 201
    except sqlite3.Error as e:
        return jsonify({"error": f"Database insert error: {e}"}), 500
    finally:
        conn.close()

@app.route("/<path:filename>")
def serve_static(filename):
    return send_from_directory(os.path.join(os.getcwd(), "..", "frontend"), filename)

if __name__ == '__main__':
    app.run(debug=True)
