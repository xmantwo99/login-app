from flask import Flask, request, render_template, jsonify, redirect, url_for, flash
import pyodbc
import os

app = Flask(__name__)
app.secret_key = 'super-secret-key'

# Azure SQL connection string
conn_str = (
    "DRIVER={ODBC Driver 18 for SQL Server};"
    "SERVER=sql-server-cs188-washington-xavier.database.windows.net;"
    "DATABASE=cs188-washington-xavier;"
    "UID=cs188admin;"
    "PWD=CS188-spring-2025;"
    "Encrypt=yes;"
    "TrustServerCertificate=no;"
    "Connection Timeout=30;"
)

def get_db_connection():
    return pyodbc.connect(conn_str)

@app.route('/')
def home():
    return redirect(url_for('signin'))

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data['username']
    password = data['password']

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Users (username, password, display_name) VALUES (?, ?, ?)",
                       username, password, username)
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({"message": "Registration successful."}), 200
    except Exception as e:
        return jsonify({"message": f"Registration failed: {str(e)}"}), 400

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    username = data['username']
    password = data['password']

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Users WHERE username = ? AND password = ?", (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            return jsonify({"message": f"Welcome, {user.display_name}!"}), 200
        else:
            return jsonify({"message": "Invalid username or password."}), 401
    except Exception as e:
        return jsonify({"message": f"Error: {str(e)}"}), 500



@app.route('/activity')
def activity():
    return render_template('activity.html')

if __name__ == '__main__':
    app.run(debug=True)

